import pdfplumber
from gtts import gTTS
from sys import argv
from sys import exit




# Check for no args in terminal
if len(argv) == 1:
   print("Please enter a file name.")
   exit()
# Check for too many args in terminal
if len(argv) != 2:
   print("Please Enter only one file arguement.")
   exit()


## Function defs
# Function to extract text from a PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
   with pdfplumber.open(pdf_path) as pdf:
       full_text = ""
       for page in pdf.pages:
           page_text = page.extract_text()
           full_text += page_text if page_text else ""
   return full_text


# Convert text to speech and save as MP3
def text_to_speech(text, output_mp3):
   tts = gTTS(text=text, lang='en')
   print("Attempting to Convert PDF to audio...")
   tts.save(output_mp3)






# Main workflow
pdf_path = argv[1]  # PDF file path
mp3_name = argv[1].strip(".pdf") # name reformated for mp3 output
output_mp3 = f"{mp3_name}.mp3" #


# Check if file is of type 'pdf'
if not pdf_path.lower().endswith(".pdf"):
   print("Please enter file of type 'pdf'.")
   exit()


# Extract text from the PDF
try:
   text = extract_text_from_pdf(pdf_path)
except FileNotFoundError:
   print("File not found. Please check file name.")
   exit()


# Convert the extracted text into an MP3 file. Message if request fails.
try:
   text_to_speech(text, output_mp3)
except Exception:
   print("ERROR: Something went wrong. Please make sure you are connected to wifi.")
   exit()


print("Done!")
