from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import create_ai_image_with_fal, remove_background_with_removebg
from error_handler import ErrorHandler
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")
FAL_API_KEY = os.getenv("FAL_API_KEY")

@app.route('/api/create_ai_image', methods=['POST'])
def handle_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image = request.files['image']
        image_bytes = image.read()
        print(f"Received file: {image.filename}, Size: {len(image_bytes)} bytes")

        # FAL API를 사용해 배경 제거 수행
        result = create_ai_image_with_fal(image_bytes, "create ai image.", FAL_API_KEY)

        if result is None:
            return jsonify({'error': 'create ai image failed'}), 500

        # 성공적으로 결과 반환
        return jsonify({'message': 'create ai image successfully', 'result': result}), 200

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify({'error': f'create ai image failed: {str(e)}'}), 500

@app.route('/api/remove_background', methods=['POST'])
def remove_background():
    try:
        if 'image' not in request.files:
            return ErrorHandler.client_error('No image uploaded')

        image = request.files['image']
        image_bytes = image.read()
        print(f"Received file: {image.filename}, Size: {len(image_bytes)} bytes")

        if not REMOVE_BG_API_KEY:
            return ErrorHandler.client_error('Remove.bg API key not configured', 500)

        file_path = remove_background_with_removebg(image_bytes, REMOVE_BG_API_KEY)

        if file_path is None:
            return ErrorHandler.client_error('remove_background failed', 500)

        return jsonify({'message': 'Background removed successfully', 'url': file_path}), 200

    except Exception as e:
        return ErrorHandler.handle_exception(e, 'remove_background failed')

# 정적 파일 제공 엔드포인트
@app.route('/static/<path:filename>')
def serve_static_file(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
