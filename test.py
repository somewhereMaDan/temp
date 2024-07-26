import requests
 
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
 
def read_image_as_bytes(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()
 
# Example usage
image_path = "imx.png"  # Replace with your image path
api_key = "K83551900988957"  # Replace with your actual API key
image_bytes = read_image_as_bytes(image_path)
extracted_text = extract_text_from_image(image_bytes, api_key)
 
print(extracted_text)