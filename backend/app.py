# from textFromPDF import extract_text_from_pdf_with_images
# from textFromPDF import summarize_text_with_gemini
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import requests
# from pdf2image import convert_from_path

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# textValue = {}

# UPLOAD_FOLDER = 'uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/')
# def home():
#     return "Hello Flask APP"


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
#     if file:
#         try:
#             api_key = "K83551900988957"
#             gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"
#             file_path = os.path.join(
#                 app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(file_path)
#             # Extract text from the uploaded PDF file
#             extracted_text = extract_text_from_pdf_with_images(file_path, api_key)
#             textValue['answer'] = extracted_text
#             # print(textValue["answer"])
#             # print("Extracted Text:", extracted_text)
#             img_content = "Here the text of image: " + extracted_text
#             summary = summarize_text_with_gemini(extracted_text, img_content, gemini_api_key)
#             print("Summary:", summary)
#             return jsonify({'message': 'File uploaded successfully', 'extracted_text': extracted_text, 'summary' : summary}), 200
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# @app.route("/promptAnswer", methods=["POST"])
# def promptAnswer():
#     print(textValue["answer"])
#     question = request.get_json()
#     gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"
    
#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = {
#         "contents": [
#             {
#                 "parts": [
#                     {
#                         "text": "Please answer this question:\n" + str(question) + "based upon this text content: \n" + str(textValue["answer"]) 
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

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from io import BytesIO
from pdf2image import convert_from_bytes

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

textValue = {}

@app.route('/')
def home():
    return "Hello Flask APP"

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
                        "text": "Please summarize the text content and if the content is too much large increase your summarization:\n" + text
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

@app.route('/upload', methods=['POST'])
def upload_file():
    file_url = request.form.get('fileURL')
    if not file_url:
        return jsonify({'error': 'No file URL provided'}), 400
    
    try:
        api_key = "K83551900988957"
        gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"
        
        # Extract text from the uploaded PDF file
        extracted_text = extract_text_from_pdf_with_images(file_url, api_key)
        textValue['answer'] = extracted_text
        
        # Generate the summary
        summary = summarize_text_with_gemini(extracted_text, gemini_api_key)
        
        return jsonify({'message': 'File uploaded successfully', 'extracted_text': extracted_text, 'summary': summary}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/promptAnswer", methods=["POST"])
def promptAnswer():
    print(textValue["answer"])
    question = request.get_json()
    gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Please answer this question:\n" + str(question) + " based upon this text content: \n" + str(textValue["answer"]) 
                    }
                ]
            }
        ]
    }
    params = {
        "key": gemini_api_key
    }
    print(textValue["answer"])
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

if __name__ == '__main__':
    app.run(debug=True)
