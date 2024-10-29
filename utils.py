import os
import base64
from fal_client import SyncClient

def remove_background_with_fal(image_bytes, prompt: str):
    """FAL API를 사용하여 이미지의 배경을 제거합니다."""
    try:
        # SyncClient 인스턴스 생성
        client = SyncClient()

        # 이미지 데이터를 Base64로 인코딩
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        # API 호출
        handler = client.submit(
            "fal-ai/lora",
            arguments={
                "model_name": "stabilityai/stable-diffusion-xl-base-1.0",
                "prompt": prompt,
                "image": encoded_image  # Base64 인코딩된 이미지 사용
            },
        )

        # API 응답 받기
        result = handler.get()
        return result

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return None
