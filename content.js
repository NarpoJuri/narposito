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
    tiktok: '', instagram: 'https://www.instagram.com/narpo_juri/', x: 'https://x.com/narpo_juri', bluesky: 'https://bsky.app/profile/narpojuri.bsky.social',    // se vuoti i link non compaiono
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

  // Carte collezionabili (NarpoTGC). Il sito le legge in tempo reale dall'app web di Apps Script:
  // il Google Sheet NON deve essere pubblico.
  // api: l'indirizzo dell'app web, quello che finisce con /exec (Distribuisci > Gestisci distribuzioni).
  // "set", "pacchetti" e "pesi" qui sotto sono solo la copia di riserva (carte coperte) usata se l'app web non risponde.
  carte: {
    nome: 'Console da Collezionare', sigla: 'CdC', logo: '',
    api: 'https://script.google.com/macros/s/AKfycbymqJuJnxBJ6TimGyaapWJrfiJfhi4roqKjNEeGDGt2-CSkbNTZ-_sjRyZMSeRhpH27Ow/exec',
    ogniSecondi: 60,
    set: [
      { id: 'CONSOLE1', nome: 'Console da Collezionare - Set Base', descrizione: 'Colleziona la console che hanno fatto la storia del gaming', dopp: 10, premio: 5, attesa: 1,
        carte: [{"id": "C001", "rarita": "Comune"}, {"id": "C002", "rarita": "Comune"}, {"id": "C003", "rarita": "Non comune"}, {"id": "C004", "rarita": "Non comune"}, {"id": "C005", "rarita": "Comune"}, {"id": "C006", "rarita": "Comune"}, {"id": "C007", "rarita": "Non comune"}, {"id": "C008", "rarita": "Non comune"}, {"id": "C009", "rarita": "Comune"}, {"id": "C010", "rarita": "Rara"}, {"id": "C011", "rarita": "Rara"}, {"id": "C012", "rarita": "Non comune"}, {"id": "C013", "rarita": "Leggendaria"}, {"id": "C014", "rarita": "Rara"}, {"id": "C015", "rarita": "Leggendaria"}, {"id": "C016", "rarita": "Comune"}, {"id": "C017", "rarita": "Comune"}, {"id": "C018", "rarita": "Comune"}, {"id": "C019", "rarita": "Comune"}, {"id": "C020", "rarita": "Comune"}, {"id": "C021", "rarita": "Comune"}, {"id": "C022", "rarita": "Comune"}, {"id": "C023", "rarita": "Non comune"}, {"id": "C024", "rarita": "Non comune"}, {"id": "C025", "rarita": "Non comune"}, {"id": "C026", "rarita": "Non comune"}, {"id": "C027", "rarita": "Non comune"}, {"id": "C028", "rarita": "Non comune"}, {"id": "C029", "rarita": "Non comune"}, {"id": "C030", "rarita": "Rara"}, {"id": "C031", "rarita": "Rara"}, {"id": "C032", "rarita": "Rara"}, {"id": "C033", "rarita": "Leggendaria"}, {"id": "C034", "rarita": "Leggendaria"}, {"id": "C035", "rarita": "Leggendaria"}] }
    ],
    pacchetti: [
      { nome: 'Set Base - 1 Carta', costo: 1000, carte: 1, garantita: '' },
      { nome: 'Set Base - 3 Carte', costo: 2500, carte: 3, garantita: 'Non comune' },
      { nome: 'Set Base - 5 Carte', costo: 4000, carte: 5, garantita: 'Rara' }
    ],
    pesi: { 'Comune': 60, 'Non comune': 25, 'Rara': 12, 'Leggendaria': 3 }
  },

  // Moderazione minima di chat e guestbook: parole da bloccare (minuscole).
  paroleVietate: []
};
