import argparse
import logging
from pyspark.sql import SparkSession
from spark_extract import extract_data
from spark_transform import transform_data
from spark_load import load_data_to_s3, load_data_to_postgresql

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
    spark = None
    try:
        # Spark 세션 생성
        logging.info("Spark 세션 생성 중...")
        spark = SparkSession.builder \
            .appName("Spark ETL Pipeline") \
            .getOrCreate()

        # 데이터 추출
        logging.info(f"데이터를 추출할 경로: {input_path}")
        df = extract_data(spark, input_path)

        # 데이터 변환
        logging.info("데이터 변환 중...")
        transformed_df = transform_data(df)

        # 변환된 데이터 S3에 저장
        logging.info(f"데이터를 저장할 S3 경로: {output_path}")
        load_data_to_s3(transformed_df, output_path)

        # 변환된 데이터 PostgreSQL에 저장
        logging.info("PostgreSQL에 데이터 저장 중...")
        load_data_to_postgresql(
            df=transformed_df,
            postgres_url=postgres_url,
            postgres_user=postgres_user,
            postgres_password=postgres_password,
            postgres_table=postgres_table
        )
        logging.info("ETL 작업이 완료되었습니다.")

    except Exception as e:
        logging.error(f"ETL 작업 중 오류가 발생했습니다: {e}")
        raise
    finally:
        # Spark 세션 종료
        if spark:
            logging.info("Spark 세션 종료 중...")
            spark.stop()
            logging.info("Spark 세션이 정상적으로 종료되었습니다.")

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
