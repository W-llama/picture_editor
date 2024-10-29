from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import remove_background_with_fal
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)  # CORS 허용

@app.route('/api/remove-background', methods=['POST'])
def handle_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image = request.files['image']
        image_bytes = image.read()
        print(f"Received file: {image.filename}, Size: {len(image_bytes)} bytes")

        # FAL API를 사용해 배경 제거 수행
        result = remove_background_with_fal(image_bytes, "Remove the background.")

        if result is None:
            return jsonify({'error': 'Background removal failed'}), 500

        # 성공적으로 결과 반환
        return jsonify({'message': 'Background removed successfully', 'result': result}), 200

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({'error': f'Background removal failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
