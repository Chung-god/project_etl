import argparse
from spark_extract import extract_data
from spark_transform import transform_data
from spark_load import load_data_to_s3, load_data_to_postgresql
from pyspark.sql import DataFrame

def run_spark_etl(input_path, output_path, postgres_url, postgres_user, postgres_password, postgres_table):
    """
    ETL 파이프라인 실행 함수.
    Args:
        input_path (str): 입력 데이터 경로 (로컬 또는 S3).
        output_path (str): 변환된 데이터 출력 경로 (S3).
        postgres_url (str): PostgreSQL JDBC URL.
        postgres_user (str): PostgreSQL 사용자 이름.
        postgres_password (str): PostgreSQL 비밀번호.
        postgres_table (str): 저장할 PostgreSQL 테이블 이름.
    """
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
    print("PostgreSQL에 데이터 저장 중...")
    load_data_to_postgresql(
        df=transformed_df,
        postgres_url=postgres_url,
        postgres_user=postgres_user,
        postgres_password=postgres_password,
        postgres_table=postgres_table
    )
    print("ETL 작업이 완료되었습니다.")

if __name__ == "__main__":
    # 명령행 인자 처리
    parser = argparse.ArgumentParser(description="Spark ETL Pipeline")
    parser.add_argument('--input', required=True, help='Input path for raw data (S3 or local)')
    parser.add_argument('--output', required=True, help='Output path for processed data (S3)')
    parser.add_argument('--postgres_url', required=True, help='PostgreSQL JDBC URL')
    parser.add_argument('--postgres_user', required=True, help='PostgreSQL user')
    parser.add_argument('--postgres_password', required=True, help='PostgreSQL password')
    parser.add_argument('--postgres_table', required=True, help='PostgreSQL table name')
    args = parser.parse_args()

    # ETL 실행
    run_spark_etl(
        input_path=args.input,
        output_path=args.output,
        postgres_url=args.postgres_url,
        postgres_user=args.postgres_user,
        postgres_password=args.postgres_password,
        postgres_table=args.postgres_table
    )
