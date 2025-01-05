def load_data(df, output_path):
    # 데이터 저장
    df.write.csv(output_path, header=True, mode="overwrite")
    print(f"Data loaded successfully to {output_path}")
