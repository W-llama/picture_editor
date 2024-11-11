import os
import uuid
from flask import Flask, request, jsonify, url_for, send_file
from utils import remove_background, generate_background, centerize_image, create_composite_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 16MB 설정 (필요에 따라 조정)


# 파일 저장 함수
def save_image(image, folder):
    unique_filename = f"{uuid.uuid4()}.png"
    file_path = os.path.join(folder, unique_filename)
    image.save(file_path)
    return url_for('static', filename=unique_filename, _external=True)

# 단건 배경 제거 엔드포인트
@app.route('/remove_background_single', methods=['POST'])
def remove_background_single():
    image = request.files['image']
    result_image, _ = remove_background(image)
    file_url = save_image(result_image, app.config['UPLOAD_FOLDER'])
    return jsonify({"url": file_url})

# 벌크 배경 제거 엔드포인트
@app.route('/remove_background_bulk', methods=['POST'])
def remove_background_bulk():
    # 전체 파일 요청을 로그로 출력하여 확인
    print("Request files:", request.files)

    images = request.files.getlist('images')
    results = []

    if not images:
        print("No images received")  # 이미지가 없는 경우 로그 출력
    else:
        print(f"Received {len(images)} images")  # 받은 이미지 개수 출력

    for image in images:
        # 각각의 이미지를 처리하고 결과 저장
        result_image, _ = remove_background(image)  # mask는 무시합니다.

        # 결과 이미지를 고유한 파일명으로 저장하고 URL 생성
        file_url = save_image(result_image, app.config['UPLOAD_FOLDER'])
        results.append({"url": file_url})

    # 모든 이미지 URL 리스트를 JSON으로 반환
    print(f"Returning {len(results)} results")  # 처리된 결과 개수 출력
    return jsonify(results)

# 단건 배경 생성 엔드포인트
@app.route('/generate_background_single', methods=['POST'])
def generate_background_single():
    prompt = request.form.get('prompt', 'default background')
    result_image = generate_background(prompt)
    file_url = save_image(result_image, app.config['UPLOAD_FOLDER'])
    return jsonify({"url": file_url})

# 벌크 배경 생성 엔드포인트
@app.route('/generate_background_bulk', methods=['POST'])
def generate_background_bulk():
    prompt = request.form.get('prompt', 'default background')
    images = request.files.getlist('images')
    results = []

    for image in images:
        result_image = generate_background(prompt)
        file_url = save_image(result_image, app.config['UPLOAD_FOLDER'])
        results.append({"url": file_url})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
