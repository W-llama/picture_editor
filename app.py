import os
import uuid
import time
from PIL import Image
from flask import Flask, request, jsonify, url_for, send_file, g
from utils import remove_background, bulk_remove_background, generate_background

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB 설정

# 요청 시작 시간 기록
@app.before_request
def start_timer():
    g.start = time.time()

# 요청 완료 후 처리 시간을 로그로 출력
@app.after_request
def log_request_time(response):
    if hasattr(g, 'start'):
        duration = time.time() - g.start
        print(f"Request to {request.path} took {duration:.2f} seconds.")
    return response

# 파일 저장 함수
def save_image(image, folder, filename=None):
    if not os.path.exists(folder):
        os.makedirs(folder)
    unique_filename = filename if filename else f"{uuid.uuid4()}.png"
    file_path = os.path.join(folder, unique_filename)
    image.save(file_path)
    return url_for('static', filename=unique_filename, _external=True)

# 단건 배경 제거 엔드포인트
@app.route('/remove_background_single', methods=['POST'])
def remove_background_single():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    try:
        result_image, _ = remove_background(image)
        file_url = save_image(result_image, app.config['UPLOAD_FOLDER'])
        return jsonify({"url": file_url})
    except Exception as e:
        print(f"Error removing background: {e}")
        return jsonify({"error": "Failed to remove background"}), 500

# 벌크 배경 제거 엔드포인트
@app.route('/remove_background_bulk', methods=['POST'])
def remove_background_bulk():
    images = request.files.getlist('images')
    if not images:
        return jsonify({"error": "No images provided"}), 400

    # 이미지 파일 경로 리스트 생성 및 저장할 폴더 설정
    input_paths = []
    for image in images:
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{uuid.uuid4()}.png")
        image.save(temp_path)
        input_paths.append(temp_path)

    output_folder = os.path.join(app.config['UPLOAD_FOLDER'], "processed")
    try:
        results = bulk_remove_background(input_paths, output_folder)
        response = [{"original": orig, "url": save_image(Image.open(out), output_folder, os.path.basename(out))} for orig, out in results]
        return jsonify(response)
    except Exception as e:
        print(f"Error during bulk background removal: {e}")
        return jsonify({"error": "Failed to process bulk background removal"}), 500
    finally:
        # 임시 파일 삭제
        for temp_path in input_paths:
            if os.path.exists(temp_path):
                os.remove(temp_path)

# 단건 배경 생성 엔드포인트
@app.route('/generate_background_single', methods=['POST'])
def generate_background_single():
    prompt = request.form.get('prompt', 'default background')
    try:
        result_image = generate_background(prompt)
        file_url = save_image(result_image, app.config['UPLOAD_FOLDER'])
        return jsonify({"url": file_url})
    except Exception as e:
        print(f"Error generating background: {e}")
        return jsonify({"error": "Failed to generate background"}), 500

# 벌크 배경 생성 엔드포인트
@app.route('/generate_background_bulk', methods=['POST'])
def generate_background_bulk():
    prompt = request.form.get('prompt', 'default background')
    images = request.files.getlist('images')
    if not images:
        return jsonify({"error": "No images provided"}), 400

    results = []
    for _ in images:
        try:
            result_image = generate_background(prompt)
            file_url = save_image(result_image, app.config['UPLOAD_FOLDER'])
            results.append({"url": file_url})
        except Exception as e:
            print(f"Error generating background for an image: {e}")
            results.append({"error": "Failed to generate background for an image"})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
