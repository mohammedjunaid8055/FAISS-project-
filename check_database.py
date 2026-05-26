import pandas as pd
import os

def check():
    csv_path = "data/products.csv"
    if not os.path.exists(csv_path):
        print("CSV does not exist.")
        return
    df = pd.read_csv(csv_path)
    print(f"Total rows: {len(df)}")
    print("\nDuplicate Titles:")
    print(df[df.duplicated(subset=['title'], keep=False)]['title'].value_counts())
    
    print("\nDuplicate IDs:")
    print(df[df.duplicated(subset=['id'], keep=False)]['id'].value_counts())
    
    print("\nDuplicate Images (local_path):")
    print(df[df.duplicated(subset=['local_path'], keep=False)]['local_path'].value_counts())

if __name__ == '__main__':
    check()
