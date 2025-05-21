# 📚 PDF to Audio 🎧

This is a simple, flexible Python app that converts any `.pdf` file into spoken audio.

You can choose between:

- ✅ **Online Mode** (default): Uses Google Text-to-Speech (gTTS) — fast and lightweight  
- ✅ **Offline Mode** (`--offline`): Uses macOS's built-in `say` command with `ffmpeg` — works without internet and is unlimited

---

## Features

- Converts multi-page PDFs to speech  
- Outputs `.mp3` (online) or `.wav` (offline)  
- Cross-platform support with macOS-optimized offline mode  
- Clean, testable Python code with CLI flag support

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

4. *(Offline mode only)* — make sure `ffmpeg` is installed and accessible from your terminal:

- **macOS (recommended):**  
  - Download from: https://evermeet.cx/ffmpeg/  
  - Move `ffmpeg` to `/usr/local/bin` and run `chmod +x /usr/local/bin/ffmpeg`

- **Linux:**

```bash
sudo apt install ffmpeg
```

- **Windows:**  
  - Download from: https://www.gyan.dev/ffmpeg/builds/  
  - Add `ffmpeg/bin` to your system PATH


5. **Add your PDF file** — Place the `.pdf` you want to convert into the root of the project directory.


---

## Usage

### Online Mode (default, uses gTTS):

```bash
python app.py "your_file.pdf"
```

- Requires internet  
- Better voice to text but limited usage
- Outputs an `.mp3` file


### Offline Mode (macOS only, uses `say` + `ffmpeg`):

```bash
python app.py "your_file.pdf" --offline
```

- No internet required  
- Unlimited Usage
- Outputs a `.wav` file  
- Works best on macOS with the `say` command pre-installed

---

## Example

```bash
python app.py "Sociology Lecture.pdf" --offline
```

Produces:

```
Sociology Lecture.wav
```
**Note**: Audio file will be saved in your working directory.

---

## Requirements

- Python 3.10+  
- macOS for offline mode (uses `say`)  
- `ffmpeg` installed and on your system PATH for offline mode

---

## License

MIT — feel free to use, modify, and share.