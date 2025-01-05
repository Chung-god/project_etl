# Python 베이스 이미지
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 필요한 시스템 패키지 설치
RUN apt-get clean && apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    procps \
    && apt-get clean

# JAVA_HOME 환경 변수 설정
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

# Python 의존성 설치
COPY docker/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# .env 파일 복사
COPY config/aws_credentials.env .env

# 모든 소스 코드 복사
COPY app/ .

# 기본 실행 명령어
CMD ["python", "spark_etl.py"]
