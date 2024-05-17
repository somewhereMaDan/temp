
from pdf2image import convert_from_path
import tempfile
import requests
import PyPDF2


def extract_text_from_image(image, api_key):
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": api_key,
        "language": "eng",  # Change this if your image contains text in a different language
    }
    response = requests.post(url, files={"file": image}, data=payload)
    result = response.json()
    if "ParsedResults" in result:
        extracted_text = result["ParsedResults"][0]["ParsedText"]
        return extracted_text
    else:
        return None

          
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text
  
def extract_text_from_pdf_with_images(pdf_path, api_key):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        # Check if the image is a JPEG or PNG format
        if image.format == "JPEG" or image.format == "PNG":
            # Extract text from the image using OCR.space API
            text += extract_text_from_image(image, api_key)
        else:
            # Extract text from the PDF
            text += extract_text_from_pdf(pdf_path)
    return text

# Replace 'YOUR_API_KEY' with your actual OCR.space API key
api_key = "K81405423488957"

# Path to the PDF file you want to extract text from
pdf_path = "test.pdf"

extracted_text = extract_text_from_pdf_with_images(pdf_path, api_key)
print(extracted_text)
