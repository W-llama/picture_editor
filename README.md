# 🚩 **Picture Editor - Flask 기반 fal API 사용 프로젝트**

이 프로젝트는 Flask 웹 프레임워크를 활용하여 이미지를 업로드하고, FAL API를 통해 이미지를 생성을 제공합니다. </br> Python 3.9 환경에서 실행되며, 로컬에서 손쉽게 개발 및 테스트할 수 있도록 설계되었습니다. 이 API는 RESTful 원칙을 따르며, HTTP 메소드를 사용하여 리소스를 관리합니다.

## 📋 **프로젝트 구조**
```
picture_editor/ 
├── app.py              # Flask 서버 로직
├── utils.py            # FAL API 호출 로직
├── .env                # 환경변수 파일 (API 키 포함)
├── requirements.txt    # 필요한 라이브러리 목록
├── app.py              # Flask 서버 로직
└── README.md           # 프로젝트 설명 파일
```

## ⚙️ **사용된 기술 및 버전**
- **Python**: 3.9
- **Flask**: 웹 프레임워크
- **FAL API**: 배경 제거 기능 제공
- **Requests**: HTTP 요청을 보내기 위한 라이브러리 (utils.py에서 API 호출 시 사용)
- **dotenv**: 환경변수 관리를 위한 라이브러리 (API 키 관리)
- **RESTful API**: HTTP 메소드를 사용하여 리소스를 관리하며, 클라이언트와 서버 간의 상호작용을 명확하게 정의

## 🛠️ **사전 준비**

1. **Python 3.9 설치**:
   - [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드 후 설치합니다.

2. **Miniconda 설치** (선택 사항):
   - [Miniconda 다운로드](https://docs.conda.io/en/latest/miniconda.html)에서 다운로드 후 설치합니다.


## 🏗️ **프로젝트 설정 및 실행**

### 1. 저장소 클론
```bash
git clone https://github.com/W-llama/picture_editor.git
cd picture_editor
```

### 2. 가상 환경 설정
```bash
python -m venv .venv  # 가상 환경 생성
source .venv/bin/activate  # (Windows) .venv\Scripts\activate
```

### 3. 필수 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 4. .env 파일 생성
프로젝트 루트에 .env 파일을 만들고, 아래와 같이 FAL API 키를 작성합니다.
```makefile
FAL_KEY=your_fal_api_key_here
```

API 키는 [FAL](https://fal.ai/dashboard/keys) 공식 웹사이트에서 발급받을 수 있습니다.

### 5. Flask 서버 실행
```bash
python app.py
```

서버가 실행되면 다음과 같은 주소로 접속할 수 있습니다:
```bash
http://localhost:5000/api/remove-background
```

## 🌐 **API 사용 방법**
- Method: POST
- URL: http://localhost:5000/api/remove-background
- Body: form-data
   - Key: image (Type: File)
   - Value: 업로드할 이미지 파일
 
## 📜 **라이센스**

이 프로젝트는 [BiRefNet](https://github.com/ZhengPeng7/BiRefNet)의 라이센스를 따릅니다. 라이센스 파일은 프로젝트 루트 디렉토리에 포함되어 있습니다.
BiRefNet의 라이센스는 [MIT 라이센스](https://opensource.org/licenses/MIT) 하에 배포됩니다.

