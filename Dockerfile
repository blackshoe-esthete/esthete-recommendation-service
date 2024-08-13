# 베이스 이미지로 Python 3.9 사용
FROM python:3.9

# 작업 디렉토리 생성
WORKDIR /app

# 타임존 데이터 설치 및 타임존 설정 추가
RUN apt-get update && apt-get install -y \
    tzdata \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# 한국 시간대(Asia/Seoul) 설정
ENV TZ=Asia/Seoul

# 필요 패키지들을 복사
COPY requirements.txt ./

# 필요한 파이썬 패키지들을 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# 환경 변수 설정
ENV CONFIG_FILE=config.ini

# 스크립트 실행
ENTRYPOINT ["python3", "app.py"]