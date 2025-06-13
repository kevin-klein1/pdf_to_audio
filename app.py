import subprocess
import tempfile
import os
import argparse
import sys
import shutil
from gtts import gTTS
import pdfplumber


# Argument Parsing setup using argparse

parser = argparse.ArgumentParser(description="Convert PDF to audio.")
parser.add_argument("pdf_file", help="Path to the PDF file")
parser.add_argument("--offline", action="store_true", help="Use offline TTS instead of gTTS")
args = parser.parse_args()




# Function defs

# PDF Text Extraction
def extract_text_from_pdf(pdf_path):
    # Create pdf file pointer and read each page of pdf, summing to full text and then return full text
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            full_text += page_text if page_text else ""
    return full_text


# Online Text-to-Speech (gTTS)
def text_to_speech_online(text, output_mp3):
    print("Converting PDF to audio using gTTS using online mode (This may take a bit)...")

    # Call Google tts API on text and save audio to output param
    tts = gTTS(text=text, lang='en')
    tts.save(output_mp3)
    print(f"Done! Audio saved as: {os.path.join(os.getcwd(), output_mp3)}")


# Offline Text-to-Speech (macOS say + ffmpeg)
def text_to_speech_offline(text, output_mp3):
    print("Converting PDF to audio using offline mode...")

    # Create chunks for apple 'say' to read 
    chunk_size = 1500
    chunks = []  

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]

        if chunk.strip():  
            clean_chunk = chunk.strip().replace('"', '')  
            chunks.append(clean_chunk)  
    # List for aiff audio file paths
    aiff_files = []

    # Iterate through chunks 
    for chunk in chunks:

        # Create temporary file on disk to write chunks to, so we can use 'say' command to read
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as tf:
            # Write and flush text on temp file 
            tf.write(chunk)
            tf.flush()

            # Create temporary aiff file 
            temp_aiff = tempfile.NamedTemporaryFile(delete=False, suffix=".aiff")
            temp_aiff.close()

            # Main process - run 'say' and save audio output to temporary aiff file, read from temp text file.
            subprocess.run(["say", "-v", "Samantha", "-o", temp_aiff.name, "-f", tf.name], check=True)

            # Append that aiff audio path to aiff_files list
            aiff_files.append(temp_aiff.name)
            # Clear the temporary txt file for next chunk
            os.remove(tf.name)


    # Create temp text file to hold all aiff paths for ffmpeg to concat
    concat_file = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt")
    for path in aiff_files:
        concat_file.write(f"file '{path}'\n")
    concat_file.close()

    # Creates new empty aiff file to hold combined result
    combined_aiff = tempfile.NamedTemporaryFile(delete=False, suffix=".aiff")
    combined_aiff.close()

    # Merges all seperate audio aiff chunks to new combined_aiff audio file, using ffmpeg command 
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_file.name,
        "-c", "copy", combined_aiff.name
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # converts aiff to .mp3 
    subprocess.run(["ffmpeg", "-y", "-i", combined_aiff.name, output_mp3],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Disk clean up of temp files
    os.remove(concat_file.name)
    os.remove(combined_aiff.name)
    for path in aiff_files:
        os.remove(path)

    # Print success message and path 
    print(f"Done! Full audio saved as: {os.path.join(os.getcwd(), output_mp3)}")


# =======================
# Main 
# =======================
def main():
    # Check if ffmpeg is installed
    if args.offline and shutil.which("ffmpeg") is None:
        print("Error: ffmpeg not found. Please install and add to PATH.")
        sys.exit(1)

    # PDF file path    
    pdf_path = args.pdf_file
    

    # Check if extension is .pdf
    if not pdf_path.lower().endswith(".pdf"):
        print("Please provide a file with .pdf extension.")
        sys.exit(1)

    # Call extract_text_from_pdf function to extract text from PDF
    try:    
        text = extract_text_from_pdf(pdf_path)
    except FileNotFoundError:
        print("File not found. Please check the filename and path.")
        sys.exit(1)

    # Case where PDF has no text, exit program
    if not text.strip():
        print("PDF appears to contain no readable text. Please enter PDF with text.")
        sys.exit(1)

    # Get the output file name by replacing the .pdf extension with .mp3
    output_file = os.path.splitext(pdf_path)[0] + ".mp3"

    # Try to convert text to audio using either online or offline method
    try:
        if args.offline:
            print("Using OFFLINE")
            text_to_speech_offline(text, output_file)
        else:
            print("Using ONLINE")
            text_to_speech_online(text, output_file)
    except Exception as e:
        print(f"ERROR: {type(e).__name__} — something went wrong during audio conversion. Please try again or try offline version (--offline).")
        sys.exit(1)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C interruption
        output_file = os.path.splitext(args.pdf_file)[0] + ".mp3"
        print("\nProcess interrupted. Cleaning up temporary files...")

        # Remove the incomplete audio file if it exists
        if os.path.exists(output_file):
            os.remove(output_file)

        print("\nProgram Ended.")
