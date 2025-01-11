from pyspark.sql import DataFrame
import os

def load_data_to_s3(df: DataFrame, output_path: str):
    """
    CSV file로 S3 버킷에 저장
    """
    try:
        print(f"Saving transformed data to S3 at: {output_path}")
        df.write.csv(output_path, header=True, mode="overwrite")
        print("Data saved successfully to S3!")
    except Exception as e:
        print(f"Error saving data to S3: {e}")
        raise



def load_data_to_postgresql(df: DataFrame):
    # PostgreSQL 연결 정보
    postgres_url = os.getenv("POSTGRES_URL")  # PostgreSQL URL
    postgres_table = os.getenv("POSTGRES_TABLE")  # 저장할 테이블 이름
    postgres_user = os.getenv("POSTGRES_USER")  # 사용자 이름
    postgres_password = os.getenv("POSTGRES_PASSWORD")  # 비밀번호


    print(f"Postgres password: {os.getenv('POSTGRES_PASSWORD')}")
    
    # PostgreSQL데이터베이스 테이블 저장
    try:
        print(f"Saving transformed data to PostgreSQL table: {postgres_table}")
        df.write \
            .format("jdbc") \
            .option("url", postgres_url) \
            .option("dbtable", postgres_table) \
            .option("user", postgres_user) \
            .option("password", postgres_password) \
            .option("driver", "org.postgresql.Driver") \
            .mode("overwrite") \
            .save()
        print("Data saved successfully to PostgreSQL!")
    except Exception as e:
        print(f"Error saving data to PostgreSQL: {e}")
        raise
