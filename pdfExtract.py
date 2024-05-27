# import requests
# from pdf2image import convert_from_path
# import os


# def extract_text_from_image(image_path, api_key):
#     url = "https://api.ocr.space/parse/image"
#     payload = {
#         "apikey": api_key,
#         "language": "eng",
#     }
#     with open(image_path, "rb") as image_file:
#         files = {"file": image_file}
#         response = requests.post(url, files=files, data=payload)
#         result = response.json()
#         if "ParsedResults" in result and result["ParsedResults"]:
#             extracted_text = result["ParsedResults"][0]["ParsedText"]
#             return extracted_text
#         else:
#             return None


# def extract_text_from_pdf_with_images(pdf_path, api_key):
#     text = ""
#     images = convert_from_path(pdf_path)
#     for idx, image in enumerate(images):
#         image_path = f"{pdf_path}_image{idx}.png"
#         image.save(image_path, "PNG")
#         print(f"Extracted image {idx} to {image_path}")

#         extracted_image_text = extract_text_from_image(image_path, api_key)
#         if extracted_image_text is not None:
#             print("Extracted Image Text:", extracted_image_text)
#             text += extracted_image_text + "\n"
#         else:
#             print("Failed to extract text from the image")
#             text += "Text extraction failed for this image\n"
#         # Remove the temporary image file
#         os.remove(image_path)
#     return text


# # OCR.space API key
# api_key = "K83551900988957"
# pdf_path = "test.pdf"

# # Extract text from the PDF
# extracted_text = extract_text_from_pdf_with_images(pdf_path, api_key)
# print("Extracted Text:", extracted_text)

# # Summarize the text using the Gemini API


# def summarize_text_with_gemini(text, img_content, gemini_api_key):
# # def summarize_text_with_gemini(text, gemini_api_key):
#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = {
#         "contents": [
#             {
#                 "parts": [
#                     {
#                         "text": "Please summarize the text content:\n" + text
#                     }
#                 ]
#             }
#         ]
#     }
#     params = {
#         "key": gemini_api_key
#     }
#     try:
#         response = requests.post(
#             url, json=data, headers=headers, params=params)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         result = response.json()
#         if "candidates" in result and result["candidates"]:
#             summarized_text = result["candidates"][0]["content"]["parts"][0]["text"]
#             return summarized_text
#         else:
#             print("Gemini API response does not contain valid data:", result)
#     except requests.exceptions.RequestException as e:
#         print("Gemini API request failed:", e)
#     except Exception as e:
#         print("An error occurred:", e)
#     return None


# gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"

# extracted_text = extract_text_from_pdf_with_images(pdf_path, api_key)
# img_content = "Here the text of image will be: " + extracted_text

# # Summarize the text
# summary = summarize_text_with_gemini(extracted_text, img_content, gemini_api_key)
# # summary = summarize_text_with_gemini(extracted_text, gemini_api_key)
# print("Summary:", summary)

import requests
from io import BytesIO
from pdf2image import convert_from_bytes

def extract_text_from_image(image_bytes, api_key):
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": api_key,
        "language": "eng",
    }
    files = {"file": ("image.png", image_bytes, "image/png")}
    response = requests.post(url, files=files, data=payload)
    result = response.json()
    if "ParsedResults" in result and result["ParsedResults"]:
        extracted_text = result["ParsedResults"][0]["ParsedText"]
        return extracted_text
    else:
        return None

def extract_text_from_pdf_with_images(pdf_url, api_key):
    text = ""
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_bytes = BytesIO(response.content)
        
        # Convert all pages of the PDF to images
        images = convert_from_bytes(pdf_bytes.getvalue())
        
        for idx, image in enumerate(images):
            image_bytes = BytesIO()
            image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            extracted_image_text = extract_text_from_image(image_bytes, api_key)
            if extracted_image_text:
                text += f"Page {idx + 1}:\n{extracted_image_text}\n"
            else:
                text += f"Page {idx + 1}:\nText extraction failed for this image\n"
        print(text)
    except Exception as e:
        print(f"An error occurred while extracting text from PDF: {e}")
    
    return text

def summarize_text_with_gemini(text, gemini_api_key):
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

# Example usage
gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"
api_key = "K83551900988957"
# pdf_url = "https://firebasestorage.googleapis.com/v0/b/pdfextract-7d18a.appspot.com/o/images%2Ftest.pdf7b9113c8-f48c-4918-ace2-1f8776f46659?alt=media&token=15732dcf-8930-4de6-8cc9-bc0a2eb837bc"
pdf_url = "https://firebasestorage.googleapis.com/v0/b/pdfextract-7d18a.appspot.com/o/images%2Fmeddra2013_0.pdfb8d29b9d-eaa0-4654-a6e6-f19ffc5f7363?alt=media&token=f1ff5f16-dc06-43de-bd10-82a2f0b6c7e2";
extracted_text = extract_text_from_pdf_with_images(pdf_url, api_key)
img_content = "Here the text of image will be: " + extracted_text

# Summarize the text
summary = summarize_text_with_gemini(extracted_text, gemini_api_key)
print("Summary:", summary)
