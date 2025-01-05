from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

def extract_data(input_path):
    # AWS 자격 증명 및 S3 설정
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("REGION")

    if not aws_access_key or not aws_secret_key or not aws_region:
        raise ValueError("AWS 자격 증명이 설정되지 않았습니다. .env 파일을 확인하세요.")

    # SparkSession 생성
    spark = SparkSession.builder \
        .appName("ETL") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.11.1026") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .getOrCreate()

    # S3 접근 설정
    hadoop_conf = spark._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3a.access.key", aws_access_key)
    hadoop_conf.set("fs.s3a.secret.key", aws_secret_key)
    hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

    # S3에서 데이터 읽기
    try:
        df = spark.read.csv(input_path, header=True, inferSchema=True).limit(1000)#적은양으로 테스트
        print("Data extracted successfully!")
        return df
    except Exception as e:
        print(f"Error extracting data from {input_path}: {e}")
        raise
