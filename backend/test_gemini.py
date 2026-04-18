import google.generativeai as genai
from PIL import Image
genai.configure(api_key="AIzaSyC-Es0lKWG4MX9lzg_CUhc_1oBL7mUQrac")
model = genai.ImageGenerationModel("imagen-3.0-generate-001")
print("Model loaded.")
# try to call with image
try:
    img = Image.new('RGB', (256, 256), color = 'red')
    resp = model.generate_images(prompt="add a chair", number_of_images=1)
    print("Text-to-image worked.", len(resp.images))
except Exception as e:
    print("T2I failed:", e)

try:
    resp = model.generate_images(prompt="add a chair", image=img, number_of_images=1)
    print("Image-to-image worked.")
except Exception as e:
    print("I2I failed:", e)
