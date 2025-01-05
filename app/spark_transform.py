from pyspark.sql.functions import col

def transform_data(df):
  # 예제: null 값을 0으로 대체
    df = df.fillna({"PRODUCT_LENGTH": 0, "PRODUCT_TYPE_ID": -1})
    df.printSchema()
    print("Data transformed successfully!")
    return df
