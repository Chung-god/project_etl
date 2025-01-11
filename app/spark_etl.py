from spark_extract import extract_data
from spark_transform import transform_data
from spark_load import load_data_to_s3, load_data_to_postgresql
from pyspark.sql import DataFrame
import os



def run_spark_etl():
    # ETL 파이프라인 실행 함수.
    
    # 데이터 소스 경로 설정
    input_path = os.getenv("INPUT_PATH", "data/raw/train.csv")  # 기본값은 로컬 경로
    output_path = os.getenv("OUTPUT_PATH", "s3a://commen-myaws-bucket/data/processed/processed_data.csv")  # 기본값은 S3 경로

    # 데이터 추출
    print(f"데이터를 추출할 경로: {input_path}")
    df = extract_data(input_path)

    # 데이터 변환
    print("데이터 변환 중...")
    transformed_df = transform_data(df)

    # 변환된 데이터 S3에 저장
    print(f"데이터를 저장할 S3 경로: {output_path}")
    load_data_to_s3(transformed_df, output_path)

    # 변환된 데이터 PostgreSQL에 저장
    load_data_to_postgresql(transformed_df)

if __name__ == "__main__":
    run_spark_etl()
