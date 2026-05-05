# 📥 oneTapDownloader

> **Scarica foto e video dai tuoi social preferiti con un solo comando — senza server a pagamento.**
> *Download photos and videos from your favourite social platforms with a single command — no paid servers needed.*

---

## 🇮🇹 Descrizione

**oneTapDownloader** è uno strumento da riga di comando che ti permette di scaricare contenuti multimediali (foto, video, reel, shorts, storie…) dalle principali piattaforme social:

| Piattaforma | Video | Foto / Gallerie | Storie / Reels |
|-------------|:-----:|:---------------:|:--------------:|
| YouTube     | ✅    | —               | —              |
| Instagram   | ✅    | ✅              | ✅             |
| TikTok      | ✅    | ✅              | —              |
| Facebook    | ✅    | ✅              | —              |

Il progetto **non usa alcun server di terze parti a pagamento**: tutto avviene in locale sulla tua macchina, sfruttando [yt-dlp](https://github.com/yt-dlp/yt-dlp) — un potente strumento open-source mantenuto dalla community.

---

## 🇬🇧 Description

**oneTapDownloader** is a command-line tool that lets you download media (photos, videos, reels, shorts, stories…) from the most popular social platforms.

The project uses **no paid third-party servers**: everything runs locally on your machine, powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) — a powerful open-source tool maintained by the community.

---

## 🚀 Installazione / Installation

### Prerequisiti / Requirements

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) (opzionale ma consigliato per la conversione dei formati)

### 1 — Clona il repository / Clone the repository

```bash
git clone https://github.com/doughabriel/oneTapDownloader.git
cd oneTapDownloader
```

### 2 — Installa le dipendenze / Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🎯 Utilizzo / Usage

```
python onetapdownloader.py <URL> [opzioni]
```

### Esempi / Examples

```bash
# Scarica un video YouTube in qualità massima
python onetapdownloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Scarica solo l'audio come MP3
python onetapdownloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --audio-only

# Scarica un reel Instagram
python onetapdownloader.py "https://www.instagram.com/reel/XXXXXXXXXX/"

# Scarica un video TikTok senza watermark
python onetapdownloader.py "https://www.tiktok.com/@user/video/XXXXXXXXXX" --no-watermark

# Specifica la cartella di destinazione
python onetapdownloader.py "https://www.facebook.com/video/XXXXXXXXXX" --output ./downloads

# Scegli la qualità del video (best, worst, 1080, 720, 480, 360)
python onetapdownloader.py "https://www.youtube.com/watch?v=..." --quality 720
```

### Opzioni disponibili / Available options

| Opzione            | Alias | Descrizione                                              |
|--------------------|-------|----------------------------------------------------------|
| `--output`         | `-o`  | Cartella di destinazione (default: `./downloads`)        |
| `--quality`        | `-q`  | Qualità video: `best`, `worst`, `1080`, `720`, `480`, `360` (default: `best`) |
| `--audio-only`     | `-a`  | Scarica solo la traccia audio in formato MP3             |
| `--no-watermark`   |       | Rimuove la watermark (dove supportato, es. TikTok)       |
| `--list-formats`   |       | Elenca i formati disponibili per l'URL fornito           |
| `--cookies`        |       | Percorso al file cookies (necessario per contenuti privati) |
| `--verbose`        | `-v`  | Mostra output dettagliato                                |

---

## 🔒 Privacy & Note legali / Privacy & Legal notes

- **oneTapDownloader** scarica contenuti **esclusivamente** dalla tua macchina locale.
- Nessun dato viene inviato a server di terze parti.
- Rispetta sempre i **Termini di Servizio** della piattaforma da cui scarichi.
- Usa lo strumento solo per contenuti di cui sei il proprietario o per cui hai esplicita autorizzazione.
- Il progetto è distribuito **"così com'è"**, senza garanzie di funzionamento continuo in caso di modifiche alle API delle piattaforme.

---

## 🛠 Come funziona / How it works

```
┌─────────────────────────────────────────┐
│              oneTapDownloader           │
│                                         │
│  1. Riceve l'URL della piattaforma      │
│  2. Rileva la piattaforma automaticamente│
│  3. Applica le opzioni selezionate      │
│  4. Delega il download a yt-dlp         │
│  5. Salva il file nella cartella scelta │
└─────────────────────────────────────────┘
         ▼
   [ yt-dlp ]  ←  cuore del progetto
         ▼
  YouTube / Instagram / TikTok / Facebook
```

**yt-dlp** è un fork di *youtube-dl* con centinaia di miglioramenti: supporta oltre 1000 siti, aggiornamenti frequenti, rimozione watermark TikTok, selezione formato avanzata, e molto altro.

---

## 📦 Dipendenze / Dependencies

| Pacchetto | Versione minima | Scopo                               |
|-----------|-----------------|-------------------------------------|
| yt-dlp    | ≥ 2024.1.0      | Motore di download                  |
| colorama  | ≥ 0.4.6         | Output colorato nel terminale       |

---

## 🤝 Contribuire / Contributing

1. Fai un fork del repository
2. Crea un branch: `git checkout -b feature/nome-feature`
3. Committa le modifiche: `git commit -m "feat: descrizione"`
4. Apri una Pull Request

---

## 📄 Licenza / License

Distribuito sotto licenza **MIT**. Vedi il file [LICENSE](LICENSE) per i dettagli.

---

## ⭐ Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — il cuore del progetto / the heart of the project
- [FFmpeg](https://ffmpeg.org/) — conversione audio/video
- Tutti i contributori open-source che rendono possibili questi strumenti
