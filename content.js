/* CONTENUTI DEL SITO — questo è il file da modificare a mano (o da far riscrivere allo script).
   Tutto quello che è segnato "esempio" è un segnaposto da sostituire. */
window.NJC = {
  canale: {
    nome: 'Narpo_Juri',
    motto: '6 anni di live, un gioco alla volta.',
    annoInizio: 2020,
    twitch: 'https://www.twitch.tv/narpo_juri',
    bio: 'Appassionato di retrogaming tra giochi dimenticati e dimenticabili.',
    youtube: 'https://www.youtube.com/@NarpoTeca',
    youtubeNome: 'NarpoTeca',
    tiktok: '', instagram: '', x: '', bluesky: '',    // se vuoti i link non compaiono
    sito: 'https://narpojuri.github.io',                      // indirizzo definitivo, serve per il banner "Linkami"
    mascotte: ''                                      // percorso immagine (es. img/tamacast.png); se vuoto resta il segnaposto
  },

  // Link a community e canali, mostrati in home come pulsanti (gli stessi del Linktree).
  link: [
    { titolo: 'Canale Twitch di Narpo!', sotto: 'Le live del canale', url: 'https://www.twitch.tv/narpo_juri' },
    { titolo: 'NarpoTeca', sotto: 'Video montati su YouTube', url: 'https://www.youtube.com/@NarpoTeca?sub_confirmation=1' },
    { titolo: 'Hey You Cafè', sotto: 'Ritrovo Discord della community', url: 'https://discord.gg/GQbJ2xh5KF' },
    { titolo: '☕ Narpo\'s Cafè ☕', sotto: 'La chat della community su Telegram', url: 'https://t.me/+SGNKIbAMYA6gyWks' },
    { titolo: 'Narpopostaggio!', sotto: 'News su Telegram', url: 'https://t.me/juricha' },
    { titolo: 'Archivio VOD', sotto: 'Le repliche delle live su YouTube', url: 'https://www.youtube.com/channel/UC8Ing64mI5NEzw5z6ufutfw' }
  ],

  // Schermo ON AIR. Se "quando" è vuoto compare "calendario in arrivo".
  prossimaLive: { quando: '', gioco: '' },

  // Scritta scorrevole: queste voci si aggiungono a quelle automatiche (ultima live, numeri dell'archivio).
  novita: [],

  // Stato dei giochi deciso a mano: vince su quello dedotto dai titoli delle live.
  // Valori: 'finito', 'in corso', 'abbandonato'.   Esempio:  'Suikoden II': 'finito'
  stati: {},

  // Link alle repliche: 'AAAA-MM-GG': 'https://...'
  repliche: {},

  // Weekly Narpoplay. Con pdf:true il sito cerca weekly/narpoplay-vol-012.pdf (e .jpg per la copertina).
  weekly: [
    { n: 8, data: '2026-11-09', sommario: ['Voce di sommario (esempio)', 'Le live della settimana', 'Il gioco del mese'], pdf: false },
    { n: 7, data: '2026-11-02', sommario: ['Voce di sommario (esempio)'], pdf: false },
    { n: 6, data: '2026-10-26', sommario: ['Voce di sommario (esempio)'], pdf: false },
    { n: 5, data: '2026-10-19', sommario: ['Voce di sommario (esempio)'], pdf: false },
    { n: 4, data: '2025-12-15', sommario: ['Voce di sommario (esempio)'], pdf: false },
    { n: 3, data: '2025-12-08', sommario: ['Voce di sommario (esempio)'], pdf: false },
    { n: 2, data: '2025-12-01', sommario: ['Voce di sommario (esempio)'], pdf: false },
    { n: 1, data: '2025-11-24', sommario: ['Voce di sommario (esempio)'], pdf: false }
  ],

  // News e articoli. tipo: 'news' oppure 'articolo'. foto: elenco di { src, didascalia } (src vuoto = riquadro segnaposto).
  news: [
    { id: 'sito-online', tipo: 'news', data: '2026-11-15', autore: 'Narpo_Juri', titolo: 'Il sito del canale prende forma (esempio)',
      anteprima: 'Backlog, Weekly, video e chat in un posto solo. Questo testo è un segnaposto.',
      testo: ['Questo è un testo di esempio: sostituiscilo con la tua news.', 'Ogni paragrafo è una riga di questo elenco.'],
      foto: [{ src: '', didascalia: 'Didascalia della foto (esempio)' }], argomenti: ['sito'] },
    { id: 'articolo-esempio', tipo: 'articolo', data: '2026-11-10', autore: 'Narpo_Juri', titolo: 'Titolo di un articolo lungo (esempio)',
      anteprima: 'Un articolo ha testo più lungo, foto con didascalia e una galleria.',
      testo: ['Primo paragrafo di esempio.', 'Secondo paragrafo di esempio.', 'Terzo paragrafo di esempio.'],
      foto: [{ src: '', didascalia: 'Foto principale (esempio)' }, { src: '', didascalia: 'Galleria 1' }, { src: '', didascalia: 'Galleria 2' }, { src: '', didascalia: 'Galleria 3' }],
      argomenti: ['retrogaming', 'traduzioni'] },
    { id: 'news-esempio-2', tipo: 'news', data: '2026-10-28', autore: 'Narpo_Juri', titolo: 'Titolo di una news (esempio)',
      anteprima: 'Due righe di anteprima della news.', testo: ['Testo di esempio.'], foto: [], argomenti: ['live'] },
    { id: 'articolo-esempio-2', tipo: 'articolo', data: '2026-10-12', autore: 'Narpo_Juri', titolo: 'Un altro articolo (esempio)',
      anteprima: 'Due righe di anteprima dell’articolo.', testo: ['Testo di esempio.'], foto: [{ src: '', didascalia: 'Foto (esempio)' }], argomenti: ['retrogaming'] },
    { id: 'news-esempio-3', tipo: 'news', data: '2026-09-30', autore: 'Narpo_Juri', titolo: 'Ancora una news (esempio)',
      anteprima: 'Due righe di anteprima della news.', testo: ['Testo di esempio.'], foto: [], argomenti: ['weekly'] },
    { id: 'news-esempio-4', tipo: 'news', data: '2026-09-14', autore: 'Narpo_Juri', titolo: 'News più vecchia (esempio)',
      anteprima: 'Serve a far vedere le pagine “più recenti / più vecchie”.', testo: ['Testo di esempio.'], foto: [], argomenti: ['live'] }
  ],

  // Canale video: i numeri li aggiornerà lo script. link vuoto = porta al canale YouTube.
  video: {
    iscrittoDal: '', caricati: '', iscritti: '', visualizzazioni: '',
    descrizione: 'Descrizione del canale (esempio): repliche, speciali e spezzoni delle live.',
    lista: [
      { titolo: 'Titolo del video in primo piano (esempio)', durata: '', data: '', viste: '', link: '', descrizione: 'Descrizione del video (esempio).' },
      { titolo: 'Titolo video 2 (esempio)', durata: '', data: '', viste: '', link: '' },
      { titolo: 'Titolo video 3 (esempio)', durata: '', data: '', viste: '', link: '' },
      { titolo: 'Titolo video 4 (esempio)', durata: '', data: '', viste: '', link: '' },
      { titolo: 'Titolo video 5 (esempio)', durata: '', data: '', viste: '', link: '' },
      { titolo: 'Titolo video 6 (esempio)', durata: '', data: '', viste: '', link: '' }
    ]
  },

  // Lettore musicale: { titolo, src } con src = percorso del file audio (es. musica/brano.mp3).
  // Se l'elenco è vuoto suonano tre brevi loop di prova generati dal sito.
  brani: [],

  // Canali amici: { nome, link, piattaforma, gioca, testo }. Se l'elenco è vuoto uso gli ospiti più presenti nello storico.
  amici: [],

  // Carte collezionabili: il sito le legge in tempo reale dal Google Sheet "NARPOTGC".
  // Il foglio deve essere condiviso come "chiunque abbia il link può visualizzare".
  // Schede lette: Set (ID, Nome), Carte (ID, Nome, Set, Rarità, Immagine (URL), Descrizione, Attiva), Collezioni (Login, CartaID, Quantità).
  // L'elenco "set" qui sotto è la copia di riserva, usata se il foglio non risponde.
  carte: {
    nome: 'Console da Collezionare', sigla: 'CdC', logo: '',
    foglio: { id: '1L3ceDkgHpZWrLcWdWBw8yX3fYdabGknrI4C2nZdILlg', schedaSet: 'Set', schedaCarte: 'Carte', schedaCollezioni: 'Collezioni', ogniSecondi: 60 },
    set: [
      { id: 'CONSOLE1', nome: 'Set Base', carte: [{"n": 1, "id": "C001", "nome": "Super Nintendo", "rarita": "Comune", "img": "https://drive.google.com/file/d/1vzUnMz9PlbtgjwAvEH9NQFjABNk8uyXF/view", "desc": "16 bit di pura potenza"}, {"n": 2, "id": "C002", "nome": "Sega Megadrive", "rarita": "Comune", "img": "https://drive.google.com/file/d/1OSwFoPHNTIaVfULIGqKZVdk2cr1ScNYA/view", "desc": "Genesis does what Nintendon't"}, {"n": 3, "id": "C003", "nome": "Sega Dreamcast", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1aAvOo38juZx376LdwGxort__CvjXMr1n/view", "desc": "L'ultimo sospiro di Sega nel mercato delle Console"}, {"n": 4, "id": "C004", "nome": "Xbox", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1TfQCWL_MLyBCxDetK-8u3aMtluAhsvlK/view", "desc": "L'Ascesa di Microsoft nel mercato console"}, {"n": 5, "id": "C005", "nome": "Sony Playstation", "rarita": "Comune", "img": "https://drive.google.com/file/d/1_2mdllnG8_Tb7QPhSCRioXdrLH8VK759/view", "desc": "La perfetta vendetta di Sony nei confronti del mercato videoludico"}, {"n": 6, "id": "C006", "nome": "Nintendo 64", "rarita": "Comune", "img": "https://drive.google.com/file/d/1wNqYnHooUCgvq0UNxvcPYSzCYgXV3Ykp/view", "desc": "Mario e Zelda approdano al 3D."}, {"n": 7, "id": "C007", "nome": "Sega Saturn", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1jzGAilbTiykGXffHZMBVXFkJzA5fHWAz/view", "desc": "Segata Sanshiro vive in questa descrizione."}, {"n": 8, "id": "C008", "nome": "Atari 2600", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1VgA_O81f8fvZqn12iGdxd-rFj8uj0Rsc/view", "desc": "L'ascesa e il declino di Atari passa da E.T."}, {"n": 9, "id": "C009", "nome": "NES", "rarita": "Comune", "img": "https://drive.google.com/file/d/1IxJNB6qFdu49jmPao1xCTBZ8emTc8byR/view", "desc": "La versione occidentale del Famicom"}, {"n": 10, "id": "C010", "nome": "Atari Jaguar", "rarita": "Rara", "img": "https://drive.google.com/file/d/1Qst26mncSAovybPw_Gg5zlJN8PyX6Pkb/view", "desc": "32+32 non fa 64. Do the Math!"}, {"n": 11, "id": "C011", "nome": "3DO", "rarita": "Rara", "img": "https://drive.google.com/file/d/1hdtlNJQ7eVydXRzQ2LA_VnssMTNGf7K0/view", "desc": "Troppe versioni, troppi fallimenti."}, {"n": 12, "id": "C012", "nome": "Sega Master System", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1bm-5x0yMuvlID4y4zvxeMpmjFkXXluNH/view", "desc": "Merita più attenzione."}, {"n": 13, "id": "C013", "nome": "Philips CD-I", "rarita": "Leggendaria", "img": "https://drive.google.com/file/d/1Ly-CIAncur_G-YN3r2W-TXu5RmLnKIFJ/view", "desc": "Mario e Zelda approdano al CD...malamente."}, {"n": 14, "id": "C014", "nome": "Virtual Boy", "rarita": "Rara", "img": "https://drive.google.com/file/d/1wsJlqr42RAt7N0KTu4_dzYuW5V6hkqnZ/view", "desc": "Troppo rosso fa malissimo."}, {"n": 15, "id": "C015", "nome": "Bandai Playdia", "rarita": "Leggendaria", "img": "https://drive.google.com/file/d/1pRG9m5KRn5zknLYeBJpvTRwnrGBwYmlt/view", "desc": "Un fallimentare connubbio tra giochi e...animazione giapponese?"}, {"n": 16, "id": "C016", "nome": "Sony Playstation 2", "rarita": "Comune", "img": "https://drive.google.com/file/d/1s7018vFzvPkyk85yigCeBnaNFd7oFRxd/view", "desc": "Lo splendore dell' Emotion Engine"}, {"n": 17, "id": "C017", "nome": "Wii", "rarita": "Comune", "img": "https://drive.google.com/file/d/1OfTyM6ZnvvwYItZUc8nIIkg1_iu8KdrM/view", "desc": "Giocare muovendo l'intero braccio."}, {"n": 18, "id": "C018", "nome": "Xbox 360", "rarita": "Comune", "img": "https://drive.google.com/file/d/1e7V53ifGeA-dJIECItDwjnGdgNSvnXRU/view", "desc": "La rivalsa di Xbox nella sua generazione"}, {"n": 19, "id": "C019", "nome": "Intellevision", "rarita": "Comune", "img": "https://drive.google.com/file/d/1hCjw_iR6VrI85BWQIdEaJsqBlB0mW5Nx/view", "desc": "L'eterna rivale di Atari 2600"}, {"n": 20, "id": "C020", "nome": "GameBoy", "rarita": "Comune", "img": "https://drive.google.com/file/d/1rRv2tmWdLdr4C_UPycq5oCurDfxiEqP5/view", "desc": "Il mattone più famoso di sempre"}, {"n": 21, "id": "C021", "nome": "Nintendo DS", "rarita": "Comune", "img": "https://drive.google.com/file/d/1kMjAN-PqfXQTFPQy-8BNk05izZOxULLy/view", "desc": "Due schermi da portare sempre con te."}, {"n": 22, "id": "C022", "nome": "PSP", "rarita": "Comune", "img": "https://drive.google.com/file/d/1NlLWtaaux5SSft9adQi7ABRClB2h39-7/view", "desc": "Come avere una PS2 in tasca"}, {"n": 23, "id": "C023", "nome": "Gamecube", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1q4V5c3s3Sc0Aozlyf4lGYX7WtyTQKpeG/view", "desc": "Il Cubo più bello di sempre"}, {"n": 24, "id": "C024", "nome": "PS3", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1d_6XMablOjKBnbG_nMiBNZJAWJsuNWdQ/view", "desc": "Tanta tecnologia, poco praticità"}, {"n": 25, "id": "C025", "nome": "Atari 5200", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1KrX-RO-tGdoY5_aP4wB3j8tE-xZLTBAV/view", "desc": "Un Atari 2600 pompata"}, {"n": 26, "id": "C026", "nome": "PocketStation", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1Z2f5DAeEgwPu5AcAAmC2inThQPxQvUOZ/view", "desc": "Portare il proprio Chocobo non è mai stato così pixeloso"}, {"n": 27, "id": "C027", "nome": "Sega Game Gear", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1k_cubnj3frDNv8CoeB-wITUc3IbqDDBJ/view", "desc": "L'unico rivale all'altezza del Gameboy"}, {"n": 28, "id": "C028", "nome": "Game Boy Advance", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1Pb_3UpIcFlpp_hKcfArfNQnYAwitLrLq/view", "desc": "E' come avere un Super Nintendo in Tasca"}, {"n": 29, "id": "C029", "nome": "PC-Engine", "rarita": "Non comune", "img": "https://drive.google.com/file/d/1HgJ3HLW-Lu3O-JZ64Z3Zyu_BvEMMf_oO/view", "desc": "La prova che Nec poteva fare sempre di più"}, {"n": 30, "id": "C030", "nome": "N-Gage", "rarita": "Rara", "img": "https://drive.google.com/file/d/109jhos0PivcUeQgCBziuilONYV46oj_H/view", "desc": "Il primo tentativo di mercato mobile in Occidente"}, {"n": 31, "id": "C031", "nome": "Neo Geo", "rarita": "Rara", "img": "https://drive.google.com/file/d/1JRy-okZHrpQWajIu9pLRNRRUHuN3wtPO/view", "desc": "La sala giochi in casa (e costa poco)"}, {"n": 32, "id": "C032", "nome": "Ouya", "rarita": "Rara", "img": "https://drive.google.com/file/d/1B9czXcyVcUzR5XH0CwG4Lt6JC9iA3E-m/view", "desc": "Il più grande flop tratto da un kickstarter"}, {"n": 33, "id": "C033", "nome": "Pc-Fx", "rarita": "Leggendaria", "img": "https://drive.google.com/file/d/1GH6GQWTsd-bY-inuw7AEtZVjO_VvaQJZ/view", "desc": "Una console basata sul misto videogiochi-anime"}, {"n": 34, "id": "C034", "nome": "Casio Loopy", "rarita": "Leggendaria", "img": "https://drive.google.com/file/d/1rh-Yn4JMvundr66QIGoBljoItRaDUnEK/view", "desc": "L'unica console tematica per ragazze giapponesi"}, {"n": 35, "id": "C035", "nome": "Zeebo", "rarita": "Leggendaria", "img": "https://drive.google.com/file/d/1raaU1rTDoRw5An3A_UUKZV4PiPX-BTcl/view", "desc": "L' unica console esclusiva dal Brasile"}] }
    ],
    collezioni: {}
  },

  // Moderazione minima di chat e guestbook: parole da bloccare (minuscole).
  paroleVietate: []
};
