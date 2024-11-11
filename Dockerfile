FROM ubuntu:latest
LABEL authors="LLama"

# Python 이미지 선택 (필요에 따라 버전을 변경 가능)
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 코드와 의존성 복사
COPY . /app

# 필요한 Python 패키지 설치
RUN pip install -r requirements.txt

# Flask 앱 실행
CMD ["python", "app.py"]