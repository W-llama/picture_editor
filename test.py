import requests
import os
from io import BytesIO

# Flask 서버의 로컬 URL (localhost를 사용하여 직접 접근)
BASE_URL = "http://127.0.0.1:5000"  # Flask 기본 로컬 URL

# 테스트에 사용할 이미지 파일 경로
image_paths = [
    'C:\\Users\\tmdqj\\Desktop\\project\\picture_editor\\image\\image1.jpg',
    'C:\\Users\\tmdqj\\Desktop\\project\\picture_editor\\image\\image2.jpg',
    'C:\\Users\\tmdqj\\Desktop\\project\\picture_editor\\image\\image3.jpg'
]

# 단건 배경 제거 테스트
def test_remove_background_single():
    url = f"{BASE_URL}/remove_background_single"
    files = {'image': open(image_paths[0], 'rb')}
    response = requests.post(url, files=files)
    print("Single Background Removal Response:", response.json())

# 벌크 배경 제거 테스트
def test_remove_background_bulk():
    url = f"{BASE_URL}/remove_background_bulk"
    files = [('images', open(image_path, 'rb')) for image_path in image_paths]
    response = requests.post(url, files=files)
    print("Bulk Background Removal Response:", response.json())

# 단건 배경 생성 테스트
def test_generate_background_single():
    url = f"{BASE_URL}/generate_background_single"
    files = {'image': open(image_paths[0], 'rb')}
    data = {'prompt': 'a beautiful sunset'}
    response = requests.post(url, files=files, data=data)
    print("Single Background Generation Response:", response.json())

# 벌크 배경 생성 테스트
def test_generate_background_bulk():
    url = f"{BASE_URL}/generate_background_bulk"
    files = [('images', open(image_path, 'rb')) for image_path in image_paths]
    data = {'prompt': 'a snowy mountain'}
    response = requests.post(url, files=files, data=data)
    print("Bulk Background Generation Response:", response.json())

# 단건 Centerizing 테스트
def test_centerize_single():
    url = f"{BASE_URL}/centerize_single"
    files = {'image': open(image_paths[0], 'rb')}
    response = requests.post(url, files=files)
    print("Single Centerizing Response:", response.json())

# 벌크 Centerizing 테스트
def test_centerize_bulk():
    url = f"{BASE_URL}/centerize_bulk"
    files = [('images', open(image_path, 'rb')) for image_path in image_paths]
    response = requests.post(url, files=files)
    print("Bulk Centerizing Response:", response.json())

# 이미지 배경 제거 후 Dreambooth 배경 생성 및 합성 테스트
def test_create_composite_image():
    url = f"{BASE_URL}/create_composite_image"
    files = {'image': open(image_paths[0], 'rb')}
    data = {'prompt': 'a tropical beach'}
    response = requests.post(url, files=files, data=data)
    print("Composite Image Creation Response:", response.json())

# 모든 테스트 실행
def run_tests():
    print("Testing Single Background Removal:")
    test_remove_background_single()

    print("\nTesting Bulk Background Removal:")
    test_remove_background_bulk()

    print("\nTesting Single Background Generation:")
    test_generate_background_single()

    print("\nTesting Bulk Background Generation:")
    test_generate_background_bulk()

    print("\nTesting Single Centerizing:")
    test_centerize_single()

    print("\nTesting Bulk Centerizing:")
    test_centerize_bulk()

    print("\nTesting Composite Image Creation:")
    test_create_composite_image()

if __name__ == "__main__":
    run_tests()
