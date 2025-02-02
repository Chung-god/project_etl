# Python slim 베이스 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 필요한 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    procps \
    wget \
    curl \
    gcc \
    libffi-dev \
    libssl-dev \
    && apt-get clean

# JAVA_HOME 및 PATH 설정
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="$JAVA_HOME/bin:$PATH"

# Airflow 설치를 위한 제약조건 파일을 복사 (Airflow 공식 문서 참조)
# 제약조건 파일은 Airflow 버전에 맞게 준비해야 합니다.
# 예를 들어, https://raw.githubusercontent.com/apache/airflow/constraints-2.8.0/constraints-3.9.txt 파일을 사용할 수 있습니다.
COPY docker/constraints.txt ./constraints.txt

# Apache Airflow 설치 (예: 버전 2.8.0) - constraints 파일을 사용하여 설치
RUN pip install --no-cache-dir "apache-airflow==2.8.0" --constraint ./constraints.txt

# Airflow Spark Provider 추가 설치
RUN pip install --no-cache-dir apache-airflow-providers-apache-spark

# 추가 Python 의존성 설치 (requirements.txt에 다른 필요한 패키지 명시)
COPY docker/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Spark 및 Hadoop 의존성 설치
ENV SPARK_VERSION=3.3.2

# 로컬에 있는 Spark tar 파일 복사 및 압축 해제
COPY spark-${SPARK_VERSION}-bin-hadoop3.tgz /tmp/
RUN tar -xzf /tmp/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop3 /usr/local/spark && \
    rm -rf /tmp/spark-${SPARK_VERSION}-bin-hadoop3.tgz

# SPARK_HOME 및 PATH 설정
ENV SPARK_HOME="/usr/local/spark"
ENV PATH="$SPARK_HOME/bin:$PATH"

# PostgreSQL JDBC 드라이버 추가
RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.4.jar -P $SPARK_HOME/jars/

# 데이터 디렉토리 복사
COPY data/raw /usr/src/app/data/raw

# 환경 변수 파일 복사 (AWS 자격증명 등)
COPY config/aws_credentials.env .env

# 모든 소스 코드 복사 (예: spark_etl.py 등 포함)
COPY app/ .

# 기본 실행 명령어 (예: spark_etl.py 실행)
CMD ["python", "spark_etl.py"]
    