import requests
from pdf2image import convert_from_path
import os


def extract_text_from_image(image_path, api_key):
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": api_key,
        "language": "eng",
    }
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        response = requests.post(url, files=files, data=payload)
        result = response.json()
        if "ParsedResults" in result and result["ParsedResults"]:
            extracted_text = result["ParsedResults"][0]["ParsedText"]
            return extracted_text
        else:
            return None


def extract_text_from_pdf_with_images(pdf_path, api_key):
    text = ""
    images = convert_from_path(pdf_path)
    for idx, image in enumerate(images):
        image_path = f"{pdf_path}_image{idx}.png"
        image.save(image_path, "PNG")
        print(f"Extracted image {idx} to {image_path}")

        extracted_image_text = extract_text_from_image(image_path, api_key)
        if extracted_image_text is not None:
            print("Extracted Image Text:", extracted_image_text)
            text += extracted_image_text + "\n"
        else:
            print("Failed to extract text from the image")
            text += "Text extraction failed for this image\n"
        # Remove the temporary image file
        os.remove(image_path)
    return text


# OCR.space API key
api_key = "K83551900988957"
pdf_path = "test.pdf"

# Extract text from the PDF
extracted_text = extract_text_from_pdf_with_images(pdf_path, api_key)
print("Extracted Text:", extracted_text)

# Summarize the text using the Gemini API


def summarize_text_with_gemini(text, img_content, gemini_api_key):
# def summarize_text_with_gemini(text, gemini_api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Please summarize the text content:\n" + text
                    }
                ]
            }
        ]
    }
    params = {
        "key": gemini_api_key
    }
    try:
        response = requests.post(
            url, json=data, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        if "candidates" in result and result["candidates"]:
            summarized_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return summarized_text
        else:
            print("Gemini API response does not contain valid data:", result)
    except requests.exceptions.RequestException as e:
        print("Gemini API request failed:", e)
    except Exception as e:
        print("An error occurred:", e)
    return None


# Replace 'YOUR_GEMINI_API_KEY' with your actual Gemini API key
gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"

# Text to summarize
extracted_text = extract_text_from_pdf_with_images(pdf_path, api_key)
img_content = "Here the text of image will be: " + extracted_text

# Summarize the text
summary = summarize_text_with_gemini(extracted_text, img_content, gemini_api_key)
# summary = summarize_text_with_gemini(extracted_text, gemini_api_key)
print("Summary:", summary)
