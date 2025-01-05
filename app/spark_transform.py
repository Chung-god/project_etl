from pyspark.sql.functions import col

def transform_data(df):
    # 결측치 처리
    df = df.fillna({"column_name": 0})


    print("Data transformed successfully!")
    return filtered_df
