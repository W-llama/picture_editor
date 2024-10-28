import openai

def remove_background(image_file, api_key):
    try:
        openai.api_key = api_key

        # 이미지를 바이트로 변환
        image_bytes = image_file.read()

        # OpenAI API 호출 (예시)
        response = openai.Image.create_edit(
            image=image_bytes,
            instructions="Remove the background."
        )

        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Exception: {str(e)}")
        return None
