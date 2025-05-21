import pdfplumber
import subprocess
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


# Convert text to speech
def text_to_speech(text):
   print("Attempting to speak the PDF content...")
   try:
       subprocess.run(['say', text], check=True)
       print("Content spoken successfully.")
   except subprocess.CalledProcessError as e:
       print(f"Error speaking content: {e}")
       # Optionally, re-raise or handle more gracefully
   except FileNotFoundError:
       print("Error: The 'say' command was not found. Ensure you are on macOS and it's installed.")
       # Optionally, re-raise or handle more gracefully






# Main workflow
pdf_path = argv[1]  # PDF file path


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
   text_to_speech(text)
except Exception as error:
   print(f"ERROR: Something went wrong. Please make sure you are connected to wifi. {type(error).__name__}")
   exit()


print("Done! Content has been spoken.")
