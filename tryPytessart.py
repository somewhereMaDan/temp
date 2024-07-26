import pytesseract
from PIL import Image

# Example image path
image_path = 'imx.png'
img = Image.open(image_path)

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(img)
print(text)
