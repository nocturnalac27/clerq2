# Clerq

> AI-powered file renamer that lives in your system tray

Clerq watches your Downloads folder and automatically renames files the moment they arrive — using AI to read their contents and generate a clean, descriptive name. No more `document_v3_FINAL(2).pdf` or `IMG_4821.jpg`. Works with any browser.

---

## What it does

When you download a file, Clerq:

1. Detects the new file instantly
2. Extracts a snippet of its contents
3. Sends it to Claude AI
4. Renames the file to something human-readable
5. Shows a toast notification with an undo button

All of this happens in 2–4 seconds, silently in the background.

---

## Features

- **Browser-agnostic** — works with Chrome, Firefox, Edge, Arc, or any browser
- **Watches multiple folders** — Downloads, Desktop, or any folder you add
- **Folder renaming** — point Clerq at a folder and it renames it based on what's inside
- **Smart undo** — every rename is logged locally; revert any file with one click
- **Re-rename protection** — files already renamed by Clerq won't get touched again even if you move them between watched folders
- **Configurable** — control which file types get renamed, max file size, naming style, output language, and more
- **Blacklists** — exclude specific folders, filename patterns, or files containing certain keywords
- **Privacy-first** — only a small text snippet (~500 chars) is ever sent to the API, never the file itself
- **History** — full rename log stored locally, auto-expires after 30 days
- **Auto-start** — launches silently on system boot

---

## How it looks

Clerq lives as a small dot in your system tray:

| Dot color | Meaning |
|----|
|  Green | Watching, idle |
|  Amber | Currently renaming a file |
|  Red | Paused |

**Left click** the dot to open the main window — rename history, folder settings, undo buttons.

**Right click** for a quick menu — pause, open Downloads folder, settings, quit.

---

## Supported file types

| Type | How content is extracted |
|---|---|
| PDF | Text extracted via `pdfplumber` |
| DOCX | Read via `python-docx` |
| XLSX / CSV | Headers and first few rows via `pandas` |
| TXT / MD | Read directly |
| JPG / PNG | EXIF metadata via `Pillow` |
| Unknown | Filename and extension used as context |

---

## Getting started

### Prerequisites

- Python 3.10+
- An Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)

### Installation

```bash
git clone https://github.com/yourname/clerq.git
cd clerq
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

Clerq will appear in your system tray and start watching your Downloads folder immediately.

### First-time setup

1. Right-click the tray icon → Settings
2. Enter your Anthropic API key under the API tab
3. Hit Test to verify the connection
4. Optionally add more folders to watch

---

## Configuration

All settings are accessible from the tray icon → Settings.

| Setting | Default | Description |
|---|---|---|
| Watched folders | `~/Downloads` | Folders to monitor |
| Model | `claude-sonnet-4-6` | Claude model to use |
| Name length | Medium (3–5 words) | How descriptive the generated name is |
| Max file size | 50MB | Files larger than this are skipped |
| Max content sent | 500 chars | How much text is sent to the API per file |
| History retention | 30 days | How long rename history is kept |
| Auto-start | On | Launch on system boot |
| Notifications | On | Show toast when a file is renamed |

---

## Tech stack

| Component | Technology |
|---|---|
| Language | Python |
| File watching | `watchdog` |
| PDF extraction | `pdfplumber` |
| Word doc extraction | `python-docx` |
| Excel / CSV extraction | `pandas` |
| Image metadata | `Pillow` |
| AI | Anthropic Python SDK |
| System tray | `pystray` |
| Notifications | `plyer` |
| UI window | `tkinter` |
| Undo / history log | JSON (local) |
| File fingerprinting | `hashlib` |
| Auto-start | `winreg` (Windows) |
| Packaging | `PyInstaller` |

---

## Privacy

- Files are never uploaded. Only extracted text (~500 characters) is sent to the Anthropic API.
- API calls are not used to train Anthropic's models.
- All rename history is stored locally on your machine.
- Sensitive folders can be blacklisted entirely.
- You can optionally use a local Ollama model so nothing leaves your machine at all.

---

## Building from source

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name Clerq main.py
```

The output `.exe` will be in the `dist/` folder.

---

## Roadmap

- [ ] macOS support
- [ ] Linux support
- [ ] Local model support via Ollama
- [ ] Batch rename existing files
- [ ] Recursive folder renaming
- [ ] File type filters per watched folder
- [ ] Export rename history as CSV

---

## License

