from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import remove_background
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)  # CORS 허용

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/api/remove-background', methods=['POST'])
def handle_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    result = remove_background(image, OPENAI_API_KEY)

    if result is None:
        return jsonify({'error': 'Background removal failed'}), 500

    return jsonify({'message': 'Background removed successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
