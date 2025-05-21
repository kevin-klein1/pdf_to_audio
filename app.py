import pdfplumber
import subprocess
import tempfile
from gtts import gTTS
import os
import argparse
import sys


# Argument Parsing

parser = argparse.ArgumentParser(description="Convert PDF to audio.")
parser.add_argument("pdf_file", help="Path to the PDF file")
parser.add_argument("--offline", action="store_true", help="Use offline TTS instead of gTTS")
args = parser.parse_args()

# Function defs

# PDF Text Extraction
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            full_text += page_text if page_text else ""
    return full_text


# Online Text-to-Speech (gTTS)
def text_to_speech_online(text, output_mp3):
    print("🌐 Converting PDF to audio using gTTS (online mode)...")
    tts = gTTS(text=text, lang='en')
    tts.save(output_mp3)
    print(f"✅ Done! Audio saved as: {output_mp3}")


# Offline Text-to-Speech (macOS say + ffmpeg)
def text_to_speech_offline(text, output_wav):
    print("🔊 Converting PDF to audio using offline mode...")

    chunk_size = 1500
    chunks = [text[i:i + chunk_size].strip().replace('"', '') for i in range(0, len(text), chunk_size) if text[i:i + chunk_size].strip()]
    aiff_files = []

    for chunk in chunks:
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tf:
            tf.write(chunk)
            tf.flush()

            temp_aiff = tempfile.NamedTemporaryFile(delete=False, suffix=".aiff")
            temp_aiff.close()

            subprocess.run(["say", "-v", "Samantha", "-o", temp_aiff.name, "-f", tf.name], check=True)
            aiff_files.append(temp_aiff.name)
            os.remove(tf.name)

    concat_file = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt")
    for path in aiff_files:
        concat_file.write(f"file '{path}'\n")
    concat_file.close()

    combined_aiff = tempfile.NamedTemporaryFile(delete=False, suffix=".aiff")
    combined_aiff.close()

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file.name,
        "-c", "copy", combined_aiff.name
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    subprocess.run(["ffmpeg", "-y", "-i", combined_aiff.name, output_wav],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    os.remove(concat_file.name)
    os.remove(combined_aiff.name)
    for path in aiff_files:
        os.remove(path)

    print(f"✅ Done! Full audio saved as: {output_wav}")





# Main 
def main():
    pdf_path = args.pdf_file

    if not pdf_path.lower().endswith(".pdf"):
        print("❌ Please provide a file with .pdf extension.")
        sys.exit(1)

    try:
        text = extract_text_from_pdf(pdf_path)
    except FileNotFoundError:
        print("❌ File not found. Please check the filename and path.")
        sys.exit(1)

    output_file = os.path.splitext(pdf_path)[0] + (".wav" if args.offline else ".mp3")

    try:
        if args.offline:
            print("Using OFFLINE")
            text_to_speech_offline(text, output_file)
        else:
            print("Using ONLINE")
            text_to_speech_online(text, output_file)
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__} — something went wrong during audio conversion.")
        sys.exit(1)

if __name__ == "__main__":
    main()