from flask import Flask, request, jsonify
from detect import detect_image
from flask_cors import CORS
import os
    
app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return jsonify({"message": "Plant AI API is running. Use POST /predict to get prediction."})

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image'].read()
    results = detect_image(image)
    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
