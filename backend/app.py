from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from io import BytesIO
from pdf2image import convert_from_bytes
import logging

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
            extracted_image_text = extract_text_from_image(
                image_bytes, api_key)
            if extracted_image_text:
                text += f"Page {idx + 1}:\n{extracted_image_text}\n"
            else:
                text += f"Page {idx +
                                1}:\nText extraction failed for this image\n"
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
                        "text": "Please summarize the text content and if the content is too large, increase your summarization:\n" + text
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
    file_urls = request.json.get('fileURLs')
    if not file_urls:
        return jsonify({'error': 'No file URLs provided'}), 400

    all_extracted_texts = []
    all_summaries = []

    try:
        api_key = "K83551900988957"
        gemini_api_key = "AIzaSyDvdKaAqQsbJim30noP8mfkHNAl0Y8pwhM"

        for url in file_urls:
            extracted_text = extract_text_from_pdf_with_images(url, api_key)
            summary = summarize_text_with_gemini(extracted_text, gemini_api_key)
            all_extracted_texts.append(extracted_text)
            all_summaries.append(summary)

        textValue["all_extracted_texts"] = all_extracted_texts
        textValue["all_summaries"] = all_summaries

        return jsonify({
            'message': 'Files uploaded successfully',
            'extracted_texts': all_extracted_texts,
            'summaries': all_summaries
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/promptAnswer", methods=["POST"])
def promptAnswer():
    # question = request.get_json()
    question = request.json.get('prompt')
    TotalFileNames = request.json.get('TotalFileNames')

    print(question)
    print(TotalFileNames)


    all_extracted_texts = textValue["all_extracted_texts"]

    final_prompt = ''

    for index, fruit in enumerate(all_extracted_texts):
        final_prompt += f"Starting Point of the text Content of the PDF starts from here-{"\n"}PDF: {index + 1}, PDF Name: {TotalFileNames[index]} {"\n"}TextValue of PDF: {"\n"}{all_extracted_texts[index]}Ending Point of text content of the PDF is ends here. {"\n"}{"\n"}{"\n"}"

    print(final_prompt)

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
                        "text": "Hi I'm gonna give you some text Contents of PDFs(for better understanding I'm using a Starting point and Ending point so you can know from where a text content of PDF starts and where it ends, also it contains the name of the pdf and serial number), please analyze it and after that please answer a question. So text Contents of PDFs are: \n" + final_prompt + "\nNow after analyzing it please answer the following question:" + question
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
