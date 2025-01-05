from spark_extract import extract_data
from spark_transform import transform_data
from spark_load import load_data

def run_spark_etl():
    # S3에서 데이터 읽기
    input_path = "s3a://commen-myaws-bucket/data/raw/concatenated.csv"
    df = extract_data(input_path)

    # 데이터 변환
    transformed_df = transform_data(df)

    # S3에 저장
    output_path = "s3a://commen-myaws-bucket/data/processed/processed_data.csv"
    load_data(transformed_df, output_path)

if __name__ == "__main__":
    run_spark_etl()
