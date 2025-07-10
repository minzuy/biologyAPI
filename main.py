import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import detect function - make sure detect.py exists
try:
    from detect import detect_image
except ImportError:
    print("Warning: detect.py not found. Creating placeholder function.")
    def detect_image(image_data):
        return {"error": "Detection model not available", "status": "placeholder"}

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "Plant AI API is running successfully!",
        "status": "healthy",
        "endpoints": {
            "predict": "POST /predict - Upload image for plant detection"
        }
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "plant-ai-api"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Read image data
        image_data = image_file.read()
        
        # Process image
        results = detect_image(image_data)
        
        return jsonify({
            "success": True,
            "results": results,
            "filename": image_file.filename
        })
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)