from textFromPDF import extract_text_from_pdf_with_images
from textFromPDF import summarize_text_with_gemini
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from pdf2image import convert_from_path

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

textValue = {}

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "Hello Flask APP"


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        try:
            api_key = "K83551900988957"
            gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Extract text from the uploaded PDF file
            extracted_text = extract_text_from_pdf_with_images(file_path, api_key)
            textValue['answer'] = extracted_text
            # print(textValue["answer"])
            # print("Extracted Text:", extracted_text)
            img_content = "Here the text of image: " + extracted_text
            summary = summarize_text_with_gemini(extracted_text, img_content, gemini_api_key)
            print("Summary:", summary)
            return jsonify({'message': 'File uploaded successfully', 'extracted_text': extracted_text, 'summary' : summary}), 200
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
                        "text": "Please answer this question:\n" + str(question) + "based upon this text content: \n" + str(textValue["answer"]) 
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

if __name__ == '__main__':
    app.run(debug=True)
