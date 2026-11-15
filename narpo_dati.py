#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivio Live di Narpo_Juri: dati (IGDB + Twitch) e sito, in un solo script.

Come si usa (serve Python 3, nessuna libreria da installare). Tieni modello_sito.html
nella stessa cartella dello script.
    python narpo_dati.py            giochi + ospiti + nuove live + sito
    python narpo_dati.py giochi     solo i giochi (poi rigenera il sito)
    python narpo_dati.py ospiti     solo gli ospiti (poi rigenera il sito)
    python narpo_dati.py sito       rigenera solo il sito dal foglio, senza cercare giochi e ospiti
Chiede una volta sola Client ID e Client Secret della tua app Twitch Developer
(oppure li legge dalle variabili TWITCH_CLIENT_ID e TWITCH_CLIENT_SECRET). Non li salva.

GIOCHI - legge la scheda "Giochi" del Google Sheet (colonne Gioco, Riscontro IGDB, ID IGDB).
  1) se c'e' una riga in igdb_narpo/correzioni.csv ("nome gioco;id IGDB") usa quell'ID;
  2) se nel foglio c'e' gia' l'ID IGDB, NON fa nessuna ricerca: scarica solo i dati di quella scheda;
  3) altrimenti cerca per nome (i giochi "Scartato" senza ID non vengono ricercati).

OSPITI - legge la scheda "Ospiti" (Ospite, Twitch (login), Descrizione, Immagine (URL), Link).
  Cerca i login su Twitch e scarica descrizione e immagine profilo. Un URL nella colonna
  Immagine sostituisce l'immagine di Twitch. Descrizione e Link scritti nel foglio hanno la precedenza.

NUOVE LIVE - legge da Twitch le dirette recenti del canale (Twitch le conserva per qualche settimana)
  e segna quelle che non sono ancora nello Storico. Le mette subito nel sito (data, durata, titolo)
  e prepara nuove_live.csv con le righe da incollare nello Storico, dove aggiungi gioco, rubrica e ospiti.

SITO - legge le schede Storico live, Giochi e Ospiti e crea la cartella "sito" (index.html, covers/, ospiti/).
  E' un sito statico: carica tutta la cartella su un hosting (Netlify, GitHub Pages...).

Cosa produce, accanto allo script:
    sito/                           il sito da pubblicare
    nuove_live.csv                  live trovate su Twitch e non ancora nel foglio
    narpo_dati.zip                  i dati grezzi (non serve per il sito)
    igdb_narpo/corrispondenze.csv   gioco -> scheda IGDB, da controllare
    ospiti_twitch.csv               ospite -> esito su Twitch, da controllare
Se il foglio non e' leggibile, salva le schede come storico.csv / giochi.csv / ospiti.csv accanto allo script.
"""
import csv, difflib, io, json, os, re, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))

SHEET_ID = "1tGyyuClCO4zoi4CxPzfI9nEH6IjybM7usOTLNDZJWrs"   # il Google Sheet dell'archivio
SHEET_TAB = "Giochi"
SOGLIA = 0.62          # sotto questo punteggio il gioco resta senza scheda
PAUSA = 0.30           # IGDB accetta 4 richieste al secondo
BASE = os.path.join(HERE, "igdb_narpo")
COVERS = os.path.join(BASE, "covers")
FIELDS = ("fields name,alternative_names.name,first_release_date,cover.image_id,"
          "platforms.abbreviation,platforms.name,genres.name,"
          "involved_companies.developer,involved_companies.company.name;")


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = s.replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def query_of(name):
    q = re.sub(r"\s*\([^)]*\)", "", name)      # toglie (PS1), (saga), (demake)...
    return q.strip(" -:") or name


def http(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST" if data is not None else "GET")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < 3:
                time.sleep(2)
                continue
            raise


def token(cid, secret):
    body = urllib.parse.urlencode({"client_id": cid, "client_secret": secret, "grant_type": "client_credentials"}).encode()
    return json.loads(http("https://id.twitch.tv/oauth2/token", body))["access_token"]


def igdb(cid, tok, body):
    h = {"Client-ID": cid, "Authorization": "Bearer " + tok, "Accept": "application/json"}
    out = json.loads(http("https://api.igdb.com/v4/games", body.encode("utf-8"), h))
    time.sleep(PAUSA)
    return out


def score(q, g):
    names = [g.get("name", "")] + [a.get("name", "") for a in g.get("alternative_names", [])]
    nq = norm(q)
    return max(difflib.SequenceMatcher(None, nq, norm(n)).ratio() for n in names if n)


def pack(g, sc):
    devs = [c["company"]["name"] for c in g.get("involved_companies", []) if c.get("developer") and c.get("company")]
    year = time.gmtime(g["first_release_date"]).tm_year if g.get("first_release_date") is not None else None
    return {
        "id": g["id"], "name": g.get("name"), "year": year,
        "platforms": [p.get("abbreviation") or p.get("name") for p in g.get("platforms", [])],
        "genres": [x["name"] for x in g.get("genres", [])],
        "developers": devs,
        "image_id": (g.get("cover") or {}).get("image_id"),
        "score": round(sc, 2),
    }


def find(cid, tok, name):
    q = query_of(name).replace('"', "")
    res = igdb(cid, tok, 'search "%s"; %s limit 10;' % (q, FIELDS))
    if not res:
        return None
    best = max(res, key=lambda g: (round(score(q, g), 3), bool(g.get("cover")), -(g.get("first_release_date") or 9e12)))
    sc = score(q, best)
    return pack(best, sc) if sc >= SOGLIA else None


def by_id(cid, tok, gid):
    res = igdb(cid, tok, "where id = %d; %s limit 1;" % (gid, FIELDS))
    return pack(res[0], 1.0) if res else None


def read_sheet():
    """Legge la scheda Giochi: prima giochi.csv accanto allo script, se c'e', altrimenti il Google Sheet.
    Restituisce {nome gioco: (riscontro, id o None)} nell'ordine del foglio, oppure None."""
    here = os.path.dirname(os.path.abspath(__file__))
    local = os.path.join(here, "giochi.csv")
    text = None
    if os.path.exists(local):
        text = open(local, encoding="utf-8-sig").read()
        print("Leggo la scheda Giochi da giochi.csv")
    else:
        url = "https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=%s" % (SHEET_ID, urllib.parse.quote(SHEET_TAB))
        try:
            text = http(url).decode("utf-8-sig")
            if text.lstrip().startswith("<"):
                text = None
        except Exception:
            text = None
        if text is None:
            print("Non riesco a leggere il Google Sheet (forse non e' condiviso con 'chiunque abbia il link').")
            print("Puoi scaricare la scheda Giochi come CSV (File > Scarica > CSV) e salvarla come giochi.csv qui accanto.")
            return None
        print("Leggo la scheda Giochi dal Google Sheet")
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return None
    head = [h.strip().lower() for h in rows[0]]
    try:
        ig, ir, ii = head.index("gioco"), head.index("riscontro igdb"), head.index("id igdb")
    except ValueError:
        print("Nella scheda Giochi non trovo le colonne Gioco / Riscontro IGDB / ID IGDB: ignoro il foglio.\n")
        return None
    out = {}
    for r in rows[1:]:
        r = r + [""] * (max(ig, ir, ii) + 1 - len(r))
        name = r[ig].strip()
        if not name:
            continue
        idtxt = re.sub(r"[^0-9]", "", r[ii].split(".")[0])
        out[name] = (r[ir].strip(), int(idtxt) if idtxt else None)
    print("  %d giochi, %d con ID IGDB nel foglio\n" % (len(out), sum(1 for v in out.values() if v[1])))
    return out


# ---------------------------------------------------------------- GIOCHI
def run_giochi(cid, tok):
    os.makedirs(COVERS, exist_ok=True)
    jpath = os.path.join(BASE, "igdb.json")
    data = json.load(open(jpath, encoding="utf-8")) if os.path.exists(jpath) else {}
    fixes = {}
    fpath = os.path.join(BASE, "correzioni.csv")
    if os.path.exists(fpath):
        for row in csv.reader(open(fpath, encoding="utf-8-sig"), delimiter=";"):
            if len(row) >= 2 and row[1].strip().isdigit():
                fixes[row[0].strip()] = int(row[1])
    sheet = read_sheet()
    if not sheet:
        print("Giochi saltati: scheda Giochi non leggibile.")
        return None
    games, total = list(sheet), len(sheet)
    for i, name in enumerate(games, 1):
        status, sid = sheet[name]
        cur = data.get(name)
        want, fonte = fixes.get(name), "correzione"
        if want is None and sid:
            want, fonte = sid, "ID dal foglio"
        try:
            if want is not None:
                # ID gia' noto: nessuna ricerca, completo solo i dati della scheda
                if (cur or {}).get("id") != want:
                    data[name] = by_id(cid, tok, want)
                    if data[name]: data[name]["fonte"] = fonte
                    else: print("  ID %s non trovato su IGDB" % want)
            elif status.lower().startswith("scartat"):
                data[name] = None            # scheda scartata e nessun ID: resta vuoto
            elif cur is None:
                data[name] = find(cid, tok, name)
                if data[name]: data[name]["fonte"] = "ricerca"
        except Exception as e:
            print("  errore su %s: %s" % (name, e))
            data.setdefault(name, None)
        d = data.get(name)
        print("[%d/%d] %s -> %s" % (i, total, name, ("%s (%s) [%s]" % (d["name"], d["year"], d.get("fonte", ""))) if d else "non trovato"))
        if d and d.get("image_id"):
            dest = os.path.join(COVERS, "%d.jpg" % d["id"])
            if not os.path.exists(dest):
                try:
                    open(dest, "wb").write(http("https://images.igdb.com/igdb/image/upload/t_cover_big/%s.jpg" % d["image_id"]))
                except Exception as e:
                    print("  copertina non scaricata: %s" % e)
        if i % 25 == 0:
            json.dump(data, open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    data = {n: data.get(n) for n in games}       # solo i giochi ancora presenti nel foglio
    json.dump(data, open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(BASE, "corrispondenze.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Gioco nell'archivio", "Scheda IGDB", "Anno", "ID IGDB", "Punteggio", "Fonte", "Link"])
        for name in games:
            d = data.get(name)
            w.writerow([name] + ([d.get("name"), d.get("year"), d["id"], d.get("score", ""), d.get("fonte", "ricerca"),
                                  "https://www.igdb.com/search?q=" + urllib.parse.quote(d.get("name") or "")] if d else [""] * 6))
    ok = sum(1 for n in games if data.get(n))
    byid = sum(1 for n in games if (data.get(n) or {}).get("fonte") == "ID dal foglio")
    print("\nGiochi: %d su %d con scheda (%d completati dall'ID nel foglio).\n" % (ok, total, byid))
    return data


# ---------------------------------------------------------------- OSPITI
def read_ospiti():
    local = os.path.join(HERE, "ospiti.csv")
    if os.path.exists(local):
        text = open(local, encoding="utf-8-sig").read()
        print("Leggo la scheda Ospiti da ospiti.csv")
    else:
        try:
            text = http("https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=Ospiti" % SHEET_ID).decode("utf-8-sig")
        except Exception:
            text = "<"
        if text.lstrip().startswith("<"):
            print("Non riesco a leggere la scheda Ospiti: scaricala come CSV e salvala come ospiti.csv qui accanto.")
            return None
        print("Leggo la scheda Ospiti dal Google Sheet")
    rows = list(csv.reader(io.StringIO(text)))
    head = [h.strip().lower() for h in rows[0]]
    col = lambda name: next((i for i, h in enumerate(head) if h.startswith(name)), None)
    ia, ib, ic, idd, ie = col("ospite"), col("twitch"), col("descrizione"), col("immagine"), col("link")
    out = []
    for r in rows[1:]:
        g = lambda i: (r[i].strip() if i is not None and i < len(r) else "")
        if g(ia):
            out.append({"ospite": g(ia), "login": g(ib).lstrip("@").lower(), "desc": g(ic), "img": g(idd), "link": g(ie)})
    return out


def run_ospiti(cid, tok):
    rows = read_ospiti()
    if not rows:
        return None, {}
    h = {"Client-Id": cid, "Authorization": "Bearer " + tok}
    logins = sorted({r["login"] for r in rows if re.fullmatch(r"[a-z0-9_]{3,25}", r["login"])})
    found = {}
    for i in range(0, len(logins), 100):
        q = "&".join("login=" + l for l in logins[i:i + 100])
        for u in json.loads(http("https://api.twitch.tv/helix/users?" + q, headers=h)).get("data", []):
            found[u["login"].lower()] = u
    slug = lambda s: re.sub(r"[^a-z0-9]+", "-", norm(s)).strip("-") or "ospite"
    data, images, report = {}, {}, []
    ua = {"User-Agent": "Mozilla/5.0 (narpo_dati.py)"}
    for r in rows:
        u = found.get(r["login"]) if r["login"] else None
        e = {"login": u["login"] if u else "", "nome_twitch": u["display_name"] if u else "",
             "desc_twitch": (u or {}).get("description", ""), "desc": r["desc"], "link": r["link"], "img": ""}
        url = r["img"] or (u or {}).get("profile_image_url", "").replace("-300x300.", "-150x150.")
        if url:
            try:
                b = http(url, headers=ua)
                ext = ".png" if b[:4] == b"\x89PNG" else ".gif" if b[:3] == b"GIF" else ".webp" if b[8:12] == b"WEBP" else ".jpg"
                if len(b) > 400000:
                    print("  ! immagine grande (%d KB) per %s: meglio una piu' piccola" % (len(b) // 1024, r["ospite"]))
                e["img"] = "img/%s%s" % (slug(r["ospite"]), ext)
                images[e["img"]] = b
            except Exception as ex:
                print("  ! immagine non scaricata per %s: %s" % (r["ospite"], ex))
        data[r["ospite"]] = e
        report.append([r["ospite"], r["login"], "trovato" if u else ("login non trovato su Twitch" if r["login"] else "senza login"),
                       e["nome_twitch"], e["desc_twitch"], ("https://www.twitch.tv/" + u["login"]) if u else ""])
    with open(os.path.join(HERE, "ospiti_twitch.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Ospite", "Login cercato", "Esito", "Nome su Twitch", "Descrizione Twitch", "Link"])
        w.writerows(report)
    print("Ospiti: %d trovati su Twitch su %d con login (%d in tutto).\n"
          % (sum(1 for x in report if x[2] == "trovato"), sum(1 for r in rows if r["login"]), len(rows)))
    return data, images


# ---------------------------------------------------------------- SITO
GIDS = {"Storico live": 674884793, "Giochi": 1250420308, "Ospiti": 777003}
CANALE = "narpo_juri"
ALIAS = {"takeshi no chosenjo": "Takeshi no Chousenjou", "zelda:wand of gamelon": "Zelda: The Wand of Gamelon"}
GIORNI = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
# nome console IGDB -> (nome mostrato, primo anno, ultimo anno): serve a stimare la console se "Console giocata" e' vuota
PLAT = {
 'Arcade':('Arcade',1970,2030),'PC':('PC',1992,2030),'DOS':('PC',1981,2030),'Mac':('Mac',1984,2030),
 'Android':('Mobile',2008,2030),'iOS':('Mobile',2008,2030),'Mobile':('Mobile',2003,2030),
 'NES':('NES / Famicom',1983,1995),'famicom':('NES / Famicom',1983,1995),'fds':('NES / Famicom',1986,1995),
 'SNES':('SNES / Super Famicom',1990,2000),'SFAM':('SNES / Super Famicom',1990,2000),'Satellaview':('Satellaview',1995,2000),
 'N64':('Nintendo 64',1996,2002),'64DD':('Nintendo 64',1999,2002),'NGC':('GameCube',2001,2007),'Wii':('Wii',2006,2013),
 'WiiU':('Wii U',2012,2017),'Switch':('Switch',2017,2026),'Switch 2':('Switch 2',2025,2030),
 'Game Boy':('Game Boy',1989,2003),'GBC':('Game Boy Color',1998,2003),'GBA':('Game Boy Advance',2001,2008),
 'NDS':('Nintendo DS',2004,2013),'3DS':('3DS',2011,2020),'New 3DS':('3DS',2014,2020),
 'PS1':('PlayStation',1994,2006),'PS2':('PlayStation 2',2000,2013),'PS3':('PlayStation 3',2006,2017),'PS4':('PlayStation 4',2013,2024),
 'PS5':('PlayStation 5',2020,2030),'PSP':('PSP',2004,2014),'Vita':('PS Vita',2011,2019),
 'XBOX':('Xbox',2001,2008),'X360':('Xbox 360',2005,2016),'XONE':('Xbox One',2013,2022),'Series X|S':('Xbox Series',2020,2030),
 'SMS':('Master System',1985,1996),'Genesis/MegaDrive':('Mega Drive',1988,1998),'Sega CD':('Mega CD',1991,1996),
 'Saturn':('Saturn',1994,2000),'DC':('Dreamcast',1998,2002),'Game Gear':('Game Gear',1990,1997),
 'neogeoaes':('Neo Geo',1990,2004),'neogeomvs':('Neo Geo',1990,2004),'Neo Geo CD':('Neo Geo',1994,1997),
 'Neo Geo Pocket Color':('Neo Geo Pocket',1999,2001),'WonderSwan':('WonderSwan',1999,2003),
 'Turbografx-16/PC Engine CD':('PC Engine',1988,1999),'PC-FX':('PC-FX',1994,1998),'3DO':('3DO',1993,1996),
 'Philips CDI':('CD-i',1991,1998),'Atari-ST':('Atari ST',1985,1993),'Amiga':('Amiga',1985,1996),'C64':('Commodore 64',1982,1994),
 'ZXS':('ZX Spectrum',1982,1992),'ACPC':('Amstrad CPC',1984,1990),'MSX':('MSX',1983,1995),
 'PC-9800 Series':('PC-98',1982,2000),'PC-8800 Series':('PC-88',1981,1989),'FM Towns':('FM Towns',1989,1997),
 'Atari2600':('Atari 2600',1977,1992),'Jaguar':('Atari Jaguar',1993,1998),'Apple][':('Apple II',1977,1993),
}


def stima_console(d):
    if not d: return []
    y, ps = d.get("year"), [p for p in d.get("platforms", []) if p in PLAT]
    names = lambda L: list(dict.fromkeys(PLAT[p][0] for p in L))
    cand = [p for p in ps if y and PLAT[p][1] <= y + 1 and PLAT[p][2] >= y]
    out = names(cand) if cand else names(ps)
    if y and y < 2000 and any(o not in ("PC", "Mac", "Mobile") for o in out):
        if "DOS" not in d.get("platforms", []) and "PC" in out: out.remove("PC")
        if "Mac" in out: out.remove("Mac")
    if "PC" in out and "Mac" in out: out.remove("Mac")
    if len(out) > 1 and "Mobile" in out: out.remove("Mobile")
    return out


def tab_rows(tab, localname):
    """Righe di una scheda del foglio: prima il CSV locale, poi il Google Sheet."""
    local = os.path.join(HERE, localname)
    if os.path.exists(local):
        return list(csv.reader(io.StringIO(open(local, encoding="utf-8-sig").read())))
    for url in ("https://docs.google.com/spreadsheets/d/%s/export?format=csv&gid=%d" % (SHEET_ID, GIDS[tab]),
                "https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=%s" % (SHEET_ID, urllib.parse.quote(tab))):
        try:
            text = http(url).decode("utf-8-sig")
            if not text.lstrip().startswith("<"):
                return list(csv.reader(io.StringIO(text)))
        except Exception:
            pass
    print("Non riesco a leggere la scheda %s: scaricala come CSV e salvala come %s accanto allo script." % (tab, localname))
    return None


def ora_roma(iso):
    """'2026-11-12T20:05:11Z' -> data e ora italiane (senza librerie esterne)."""
    import datetime as dt
    t = dt.datetime.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S")
    def ultima_dom(y, m):
        d = dt.datetime(y, m, 31, 1)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    estate = ultima_dom(t.year, 3) <= t < ultima_dom(t.year, 10)
    return t + dt.timedelta(hours=2 if estate else 1)


def nuove_live(cid, tok, date_note):
    """Dirette recenti del canale che non sono ancora nello Storico."""
    h = {"Client-Id": cid, "Authorization": "Bearer " + tok}
    try:
        u = json.loads(http("https://api.twitch.tv/helix/users?login=" + CANALE, headers=h))["data"][0]
        vids = json.loads(http("https://api.twitch.tv/helix/videos?user_id=%s&type=archive&first=100" % u["id"], headers=h)).get("data", [])
    except Exception as e:
        print("Non riesco a leggere le dirette recenti da Twitch: %s" % e)
        return []
    out = []
    for v in vids:
        t = ora_roma(v["created_at"])
        m = re.match(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", v.get("duration", ""))
        minuti = int(m.group(1) or 0) * 60 + int(m.group(2) or 0)
        data = t.strftime("%d/%m/%Y")
        ieri = (t - __import__("datetime").timedelta(days=1)).strftime("%d/%m/%Y")
        if data in date_note or minuti < 5 or (t.hour < 6 and ieri in date_note):
            continue        # gia' nel foglio (una live iniziata dopo mezzanotte puo' avere la data del giorno prima)
        out.append({"data": data, "iso": t.strftime("%Y-%m-%d"), "giorno": GIORNI[t.weekday()], "ora": t.strftime("%H:%M"),
                    "durata": "%d:%02d" % divmod(minuti, 60), "minuti": minuti, "titolo": v.get("title", "")})
    out.sort(key=lambda x: x["iso"] + x["ora"], reverse=True)
    if out:
        with open(os.path.join(HERE, "nuove_live.csv"), "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["Data", "Giorno", "Ora inizio (circa)", "Durata", "Titolo live"])
            for x in out:
                w.writerow([x["data"], x["giorno"], x["ora"], x["durata"], x["titolo"]])
    return out


def run_sito(cid, tok, giochi, ospiti):
    import datetime as dt, shutil
    modello = os.path.join(HERE, "modello_sito.html")
    if not os.path.exists(modello):
        print("Sito saltato: manca modello_sito.html accanto allo script.")
        return
    st = tab_rows("Storico live", "storico.csv")
    gi = tab_rows("Giochi", "giochi.csv")
    if not st or not gi:
        print("Sito saltato: servono le schede Storico live e Giochi.")
        return
    if giochi is None:      # non ricalcolati in questo giro: uso l'ultimo salvataggio
        p = os.path.join(BASE, "igdb.json")
        giochi = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    if ospiti is None:
        p = os.path.join(HERE, "ospiti_dati", "ospiti.json")
        ospiti = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}

    def cols(rows, *names):
        head = [h.strip().lower() for h in rows[0]]
        return [next((i for i, h in enumerate(head) if h.startswith(n)), None) for n in names]
    cell = lambda r, i: (r[i].strip() if i is not None and i < len(r) else "")
    def minuti(s):
        p = s.split(":")
        try: return int(p[0]) * 60 + int(p[1])
        except Exception: return 0
    def numero(s):
        try: return float(s.replace(",", "."))
        except Exception: return None

    # giochi: nomi ufficiali e console giocata
    cg, cc = cols(gi, "gioco", "console giocata")
    canon, console = {}, {}
    for r in gi[1:]:
        n = cell(r, cg)
        if n:
            canon[n.lower()] = n
            console[n] = [x.strip() for x in cell(r, cc).split(",") if x.strip()]
    def lista_giochi(s):
        out = []
        for x in s.split(";"):
            x = x.strip().rstrip(",").strip()
            if x:
                x = ALIAS.get(x.lower(), x)
                x = canon.get(x.lower(), x)
                if x not in out: out.append(x)
        return out
    lista_ospiti = lambda s: [x.strip() for x in re.split(r"[;,:]", s) if x.strip()]

    c = cols(st, "data", "giorno", "durata", "titolo live", "gioco", "attivit", "rubrica", "ospite", "spettatori medi", "spettatori max", "tipo di live", "tema")
    righe = [r for r in st[1:] if cell(r, c[0]) and cell(r, c[6]).upper() != "TEST_PREINIZIO"]
    conta = {}
    for r in righe:
        for x in lista_ospiti(cell(r, c[7])): conta[x] = conta.get(x, 0) + 1
    gcanon = {}
    for x, _ in sorted(conta.items(), key=lambda kv: -kv[1]): gcanon.setdefault(x.lower(), x)
    R, date_note = [], set()
    for r in righe:
        try: d = dt.datetime.strptime(cell(r, c[0]), "%d/%m/%Y").date()
        except ValueError: continue
        date_note.add(d.strftime("%d/%m/%Y"))
        R.append([d.isoformat(), cell(r, c[1]), minuti(cell(r, c[2])), cell(r, c[3]), lista_giochi(cell(r, c[4])), cell(r, c[5]),
                  [x.strip() for x in cell(r, c[6]).split(";") if x.strip()],
                  list(dict.fromkeys(gcanon[x.lower()] for x in lista_ospiti(cell(r, c[7])))), [],
                  numero(cell(r, c[8])), numero(cell(r, c[9])), cell(r, c[10]), cell(r, c[11])])
    nuove = nuove_live(cid, tok, date_note)
    for x in nuove:       # nel sito compaiono subito, con solo data, durata e titolo
        R.append([x["iso"], x["giorno"], x["minuti"], x["titolo"], [], "", [], [], [], None, None, "", ""])
    R.sort(key=lambda x: x[0], reverse=True)

    sito = os.path.join(HERE, "sito")
    os.makedirs(os.path.join(sito, "covers"), exist_ok=True)
    os.makedirs(os.path.join(sito, "ospiti"), exist_ok=True)
    META, COV, CONS = {}, {}, {}
    for n in {x for r in R for x in r[4]}:
        d = giochi.get(n)
        if d:
            META[n] = {"n": d.get("name"), "y": d.get("year"), "p": d.get("platforms", []), "g": d.get("genres", []), "d": d.get("developers", [])}
            src = os.path.join(COVERS, "%d.jpg" % d["id"])
            if os.path.exists(src):
                dst = os.path.join(sito, "covers", "%d.jpg" % d["id"])
                if not os.path.exists(dst): shutil.copyfile(src, dst)
                COV[n] = str(d["id"])
        CONS[n] = console.get(n) or stima_console(d) or ["Non indicata"]
    GUEST = {}
    imgdir = os.path.join(HERE, "ospiti_dati")
    for n, z in ospiti.items():
        e = {}
        desc = z.get("desc") or z.get("desc_twitch", "")
        link = z.get("link") or (("https://www.twitch.tv/" + z["login"]) if z.get("login") else "")
        if desc: e["d"] = desc.strip()
        if link: e["l"] = link
        if z.get("img") and os.path.exists(os.path.join(imgdir, z["img"])):
            fn = os.path.basename(z["img"])
            shutil.copyfile(os.path.join(imgdir, z["img"]), os.path.join(sito, "ospiti", fn))
            e["f"] = "ospiti/" + fn
        if e: GUEST[gcanon.get(n.lower(), n)] = e
    j = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = open(modello, encoding="utf-8").read()
    for k, v in (("__DATA__", j(R)), ("__COVERS__", j(COV)), ("__META__", j(META)), ("__CONS__", j(CONS)), ("__GUEST__", j(GUEST)),
                 ("__FILES__", "true"), ("__DATE__", dt.date.today().strftime("%d/%m/%Y"))):
        html = html.replace(k, v)
    open(os.path.join(sito, "index.html"), "w", encoding="utf-8").write(html)
    print("Sito pronto nella cartella: %s  (%d live, %d giochi, %d ospiti con scheda)" % (sito, len(R), len(CONS), len(GUEST)))
    if nuove:
        print("Nuove live trovate su Twitch e non ancora nel foglio: %d. Le righe da incollare nello Storico sono in nuove_live.csv" % len(nuove))
    else:
        print("Nessuna nuova live su Twitch rispetto al foglio.")


def main():
    what = (sys.argv[1].lower() if len(sys.argv) > 1 else "tutto")
    if what not in ("tutto", "giochi", "ospiti", "sito"):
        sys.exit("Uso: python narpo_dati.py [giochi|ospiti|sito]")
    cid = os.environ.get("TWITCH_CLIENT_ID") or input("Client ID Twitch: ").strip()
    secret = os.environ.get("TWITCH_CLIENT_SECRET") or input("Client Secret Twitch: ").strip()
    try:
        tok = token(cid, secret)
    except Exception as e:
        sys.exit("Accesso a Twitch non riuscito: controlla Client ID e Secret. (%s)" % e)
    giochi = run_giochi(cid, tok) if what in ("tutto", "giochi") else None
    ospiti, images = run_ospiti(cid, tok) if what in ("tutto", "ospiti") else (None, {})
    if ospiti is not None:      # salvo ospiti e immagini su disco: servono al sito anche nei giri successivi
        od = os.path.join(HERE, "ospiti_dati")
        os.makedirs(os.path.join(od, "img"), exist_ok=True)
        json.dump(ospiti, open(os.path.join(od, "ospiti.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for name, b in images.items():
            open(os.path.join(od, name), "wb").write(b)
    if giochi is not None or ospiti is not None:
        zpath = os.path.join(HERE, "narpo_dati.zip")
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            if giochi is not None:
                z.writestr("igdb.json", json.dumps(giochi, ensure_ascii=False, indent=1))
                used = {"%d.jpg" % d["id"] for d in giochi.values() if d}
                for fn in sorted(os.listdir(COVERS)):
                    if fn in used:
                        z.write(os.path.join(COVERS, fn), "covers/" + fn)
            if ospiti is not None:
                z.writestr("ospiti.json", json.dumps(ospiti, ensure_ascii=False, indent=1))
                for name, b in images.items():
                    z.writestr(name, b)
        print("Zip dei dati: %s" % zpath)
    run_sito(cid, tok, giochi, ospiti)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
