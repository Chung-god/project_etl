from pyspark.sql.functions import col, when

def transform_data(df):
    #null 값을 0으로 대체
    df = df.fillna({"PRODUCT_LENGTH": 0, "PRODUCT_TYPE_ID": -1})
    

    #새로운 컬럼 추가
    df = df.withColumn("IS_LNOG_PRODUCT", when(col("PRODUCT_LENGTH")>1000,1).otherwise(0))
    
    df = df.filter(col("PRODUCT_TYPE_ID") < 10000)
    
    print("Transformation completed successfully!")
    return df
