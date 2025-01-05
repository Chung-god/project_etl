def load_data(df, output_path):
    print(f"Saving transformed data to: {output_path}")
    df.write.csv(output_path, header=True, mode="overwrite")
    print("Data saved successfully!")

