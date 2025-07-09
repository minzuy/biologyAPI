from ultralytics import YOLO
from PIL import Image
import io

# Load model
model = YOLO("best.pt") 

def detect_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = model(image)  # Gọi predict
    return results[0].tojson()  
