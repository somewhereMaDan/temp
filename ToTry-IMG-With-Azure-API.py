import requests

def extract_text_from_image_azure(image_bytes, api_key, endpoint):
    url = f"{endpoint}/vision/v3.2/ocr"
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/octet-stream'
    }
    params = {
        'language': 'unk',
        'detectOrientation': 'true'
    }
    response = requests.post(url, headers=headers, params=params, data=image_bytes)
    print(response.status_code)  # Print the HTTP status code
    print(response.json())  # Print the JSON response for debugging
    result = response.json()
    if "regions" in result:
        extracted_text = ""
        for region in result["regions"]:
            for line in region["lines"]:
                for word in line["words"]:
                    extracted_text += word["text"] + " "
                extracted_text += "\n"
        return extracted_text.strip()
    else:
        return None

# Example usage:
# Read the image file in binary mode
with open("imx.png", "rb") as image_file:
    image_bytes = image_file.read()

api_key = "4e40b2a66b5245ebaa7d68eb6f557c3a"
endpoint = "https://translate-app-api.cognitiveservices.azure.com"

extracted_text = extract_text_from_image_azure(image_bytes, api_key, endpoint)
print(extracted_text)