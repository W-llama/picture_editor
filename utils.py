import os
import numpy as np
import torch
from PIL import Image, ImageOps
from torchvision import transforms
from diffusers import StableDiffusionPipeline
from model import U2NET  # U2Net 모델 정의 파일 필요

# U2Net 모델 로드
model_path = "save_models/u2net.pth"
u2net_model = U2NET(3, 1)  # U2Net 모델 객체 생성
u2net_model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
u2net_model.eval()

# Dreambooth 모델 경로 설정
dreambooth_model_path = "save_models/dreambooth_model"
model_name = "CompVis/stable-diffusion-v1-4"

# Dreambooth 모델 로드 또는 다운로드
if not os.path.exists(dreambooth_model_path):
    print("Downloading Dreambooth model...")
    pipeline = StableDiffusionPipeline.from_pretrained(model_name)
    pipeline.save_pretrained(dreambooth_model_path)
    print("Model downloaded and saved to", dreambooth_model_path)
else:
    print("Loading Dreambooth model from local path...")

# Dreambooth 파이프라인 로드
dreambooth_pipeline = StableDiffusionPipeline.from_pretrained(dreambooth_model_path)
dreambooth_pipeline.to("cpu")  # GPU 사용 시 "cuda"로 변경 가능

# 이미지 전처리 함수
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = transform(image).unsqueeze(0)
    return image

# 후처리 함수
def postprocess_mask(mask, original_size):
    mask = mask.squeeze().cpu().detach().numpy()
    mask = (mask > 0.5).astype(np.uint8) * 255
    mask = Image.fromarray(mask).resize(original_size, Image.LANCZOS)
    return mask

# U2Net을 통한 배경 제거 (투명 배경)
def remove_background(image):
    pil_image = Image.open(image).convert("RGB")
    original_size = pil_image.size
    input_image = preprocess_image(pil_image)

    with torch.no_grad():
        prediction = u2net_model(input_image)[0][:, 0, :, :]
        mask = postprocess_mask(prediction, original_size)

    # 투명한 배경 생성
    rgba_image = pil_image.convert("RGBA")
    data = np.array(rgba_image)
    data[:, :, 3] = mask  # 알파 채널에 마스크 적용해 투명도 설정
    transparent_image = Image.fromarray(data, "RGBA")
    return transparent_image, mask  # 투명 배경 이미지 반환

# Dreambooth를 통한 배경 생성
def generate_background(prompt, size=(512, 512)):
    width, height = map(int, size)  # size 값을 정수로 변환하여 height와 width에 전달
    generated_image = dreambooth_pipeline(prompt, height=height, width=width).images[0]
    return generated_image
