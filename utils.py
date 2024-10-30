import requests
from fal_client import SyncClient
import os
from uuid import uuid4  # 고유한 파일 이름 생성용
from pathlib import Path
import base64

def remove_background_with_removebg(image_bytes: bytes, api_key: str) -> str:
    """remove.bg API를 사용해 이미지의 배경을 제거하고 파일 경로를 반환합니다."""
    try:
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": ("image.png", image_bytes)},
            data={"size": "auto"},
            headers={"X-Api-Key": api_key},
        )
        if response.status_code == 200:
            # 고유한 파일 이름 생성
            file_name = f"{uuid4()}.png"
            output_path = Path("static") / file_name
            output_path.parent.mkdir(exist_ok=True)  # static 디렉터리 생성

            # 이미지 저장
            with open(output_path, "wb") as f:
                f.write(response.content)

            # 경로 반환
            return f"/static/{file_name}"
        else:
            print(f"remove.bg API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception in remove.bg: {str(e)}")
        return None

def create_ai_image_with_fal(image_bytes: bytes, prompt: str, api_key: str) -> str:
    """FAL API를 사용해 AI 이미지를 생성하고 Base64로 반환합니다."""
    try:
        # SyncClient 인스턴스 생성
        client = SyncClient()

        # 이미지 데이터를 Base64로 인코딩
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        print(f"Encoded image size: {len(encoded_image)}")  # 디버깅용 로그

        # API 호출
        handler = client.submit(
            "fal-ai/lora",
            arguments={
                "model_name": "stabilityai/stable-diffusion-xl-base-1.0",
                "prompt": prompt,
                "image": encoded_image
            },
        )

        # 응답 받기
        result = handler.get()
        print(f"FAL API result: {result}")  # 결과 디버깅용

        if not result:
            print("FAL API returned empty result.")
            return None

        return result

    except Exception as e:
        print(f"Exception in create_ai_image_with_fal: {str(e)}")
        return None