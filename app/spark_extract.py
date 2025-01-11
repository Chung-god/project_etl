from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os

def extract_data(input_path):
    """
    데이터 추출 함수. 로컬 파일 또는 S3에서 데이터를 읽어 Spark DataFrame으로 반환.
    
    Parameters:
        inESput_path (str): 데이터 파일 경로. 로컬 경로 또는 S3 경로(s3a://).
    
    Returns:
        pyspark.sql.DataFrame: 추출된 데이터 프레임.
    """
    # .env 파일 로드
    env_loaded = load_dotenv()
    if not env_loaded:
        raise EnvironmentError(".env 파일을 로드할 수 없습니다.")

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
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.sql.shuffle.partitions", "8") \
        .getOrCreate()

    # S3 접근 설정
    hadoop_conf = spark._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3a.access.key", aws_access_key)
    hadoop_conf.set("fs.s3a.secret.key", aws_secret_key)
    hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

    # S3 또는 로컬 경로에서 데이터 읽기
    try:
        if input_path.startswith("s3a://"):
            print(f"Reading data from S3: {input_path}")
        else:
            print(f"Reading data from local file: {input_path}")

        df = spark.read.csv(input_path, header=True, inferSchema=True).limit(1000)  # 적은 양으로 테스트
        print("Data extracted successfully!")
        print(f"Data Schema:\n{df.printSchema()}")
        return df

    except Exception as e:
        print(f"Error extracting data from {input_path}: {e}")
        raise
