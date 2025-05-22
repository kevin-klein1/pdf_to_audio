# 📁 PDF to Audio 🎧

This is a simple, flexible Python CLI app that converts any `.pdf` file into spoken `.mp3` audio.

You can choose between:

- **Online Mode** (default): Uses Google Text-to-Speech (gTTS) — fast and lightweight  
- **Offline Mode** (`--offline`): Uses macOS's built-in `say` command with `ffmpeg` — works without internet and is unlimited (macOS only)

---

## Features

- Converts multi-page PDFs to speech  
- Outputs `.mp3` 


---

## Setup

1. **Clone this repository:**

```bash
git clone https://github.com/kevin-klein1/pdf_to_audio.git
cd pdf_to_audio
```

2. **Create and activate a virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Offline mode (macOS compatible only)** — make sure `ffmpeg` is installed and accessible from your terminal:

- **macOS:**  
  - Download from: https://evermeet.cx/ffmpeg/  
  - Move `ffmpeg` to `/usr/local/bin` and run `chmod +x /usr/local/bin/ffmpeg`

- **Linux:**

```bash
sudo apt install ffmpeg
```


5. **Add your PDF file** — Place the `.pdf` you want to convert into the root of the project directory


---

## Usage

### Online Mode (default, uses gTTS):

```bash
python app.py "your_file.pdf"
```

- Requires internet  
- Cross Platform (Windows, macOS, etc)
- Better voice to text but limited usage



### Offline Mode (macOS only, uses `say` + `ffmpeg`):

```bash
python app.py "your_file.pdf" --offline
```

- No internet required  
- macOS required with 'say' command pre-installed
- Unlimited Usage


---

## Example

```bash
python app.py "Sociology Lecture.pdf" --offline
```

Produces:

```
Sociology Lecture.mp3
```
📍 **Note**: Audio file will be saved in your working directory.

---

## Requirements

- Python 3.10+  
- macOS for offline mode (uses `say`)  
- `ffmpeg` installed and on your system PATH for offline mode

---

## License

MIT — feel free to use, modify, and share.
MIT — feel free to use, modify, and share.