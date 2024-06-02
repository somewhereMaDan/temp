from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from io import BytesIO
from pdf2image import convert_from_bytes
import subprocess
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

textValue = {}

@app.route('/')
def home():
    return "Hello Flask APP"

def is_valid_url(url):
    try:
        result = requests.utils.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def get_content_type(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('Content-Type')
        return content_type
    except requests.RequestException as e:
        return str(e)
        
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
    temp_pdf_path = None
    try:
        # Check if the input is a URL or a file path
        if is_valid_url(pdf_url):
            response = requests.get(pdf_url)
            response.raise_for_status()
            pdf_bytes = BytesIO(response.content)
        else:
            with open(pdf_url, 'rb') as f:
                pdf_bytes = BytesIO(f.read())
                # Save PDF to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf:
                    temp_pdf.write(pdf_bytes.getbuffer())
                    temp_pdf_path = temp_pdf.name

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
    finally:
        # Clean up the temporary PDF file
        if temp_pdf_path and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

    return text

def download_file_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return BytesIO(response.content)

def extract_text_from_docx_with_images(docx_url, api_key):
    text = ""
    try:
        response = requests.get(docx_url)
        response.raise_for_status()
        docx_bytes = BytesIO(response.content)

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_docx:
            temp_docx.write(docx_bytes.read())
            temp_docx_path = temp_docx.name

        temp_pdf_path = temp_docx_path.replace('.docx', '.pdf')
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(temp_docx_path), temp_docx_path], stderr=subprocess.DEVNULL)
        
        # return temp_pdf_path
        text = extract_text_from_pdf_with_images(temp_pdf_path,api_key)
    except Exception as e:
        print(f"An error occurred while extracting text from DOCX: {e}")

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
        response = requests.post(url, json=data, headers=headers, params=params)
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

        # content_type = str(get_content_type(file_urls))
        # print(content_type)

        for url in file_urls:
            content_type = get_content_type(url)
            if 'pdf' in content_type:
                print("this is a pdf file")
                extracted_text = extract_text_from_pdf_with_images(url, api_key)
            elif 'word' in content_type:
                print("The file is a DOCX.")
                extracted_text = extract_text_from_docx_with_images(url, api_key)
            all_extracted_texts.append(extracted_text)
            summary = summarize_text_with_gemini(extracted_text, gemini_api_key)
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

def save_prompt_if_new(prompt):
    try:
        with open("prompts.txt", "r") as file:
            existing_prompts = file.readlines()
        existing_prompts = [p.strip() for p in existing_prompts]
        if prompt not in existing_prompts:
            with open("prompts.txt", "a") as file:
                file.write(prompt + "\n")
    except FileNotFoundError:
        with open("prompts.txt", "w") as file:
            file.write(prompt + "\n")
    except Exception as e:
        print(f"An error occurred while saving the prompt: {e}")

@app.route("/promptAnswer", methods=["POST"])
def promptAnswer():
    question = request.json.get('prompt')
    TotalFileNames = request.json.get('TotalFileNames')

    print(question)
    print(TotalFileNames)

    all_extracted_texts = textValue['all_extracted_texts']

    final_prompt = ''

    for index, text in enumerate(all_extracted_texts):
        final_prompt += f"Starting Point of the text Content of the File starts from here-\File: {index + 1}, File Name: {TotalFileNames[index]}\nTextValue of File:\n{text}\nEnding Point of text content of the File is ends here.\n\n\n"

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
                        "text": "Hi I'm gonna give you some text Contents of PDFs(for better understanding I'm using a Starting point and Ending point so you can know from where a text content of PDF starts and where it ends, also it contains the name of the pdf and serial number), please analyze it and after that please answer a question. So text Contents of PDFs are:\n" + final_prompt + "\nNow after analyzing it please answer the following question:" + question
                    }
                ]
            }
        ]
    }
    params = {
        "key": gemini_api_key
    }

    try:
        response = requests.post(url, json=data, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        print("Gemini API response:", result)  # Log the response

        if "candidates" in result and result["candidates"]:
            summarized_text = result["candidates"][0]["content"]["parts"][0]["text"]
            
            save_prompt_if_new(question)  # Save the prompt if it's new

            return summarized_text
        else:
            error_message = "Gemini API response does not contain valid data"
            print(error_message, result)
            return jsonify({'error': error_message}), 500
    except requests.exceptions.RequestException as e:
        error_message = f"Gemini API request failed: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return jsonify({'error': error_message}), 500


@app.route("/getPrompts", methods=["GET"])
def get_prompts():
    try:
        with open("prompts.txt", "r") as file:
            prompts = file.readlines()
        return jsonify({"prompts": [prompt.strip() for prompt in prompts]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
