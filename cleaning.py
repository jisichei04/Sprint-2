
# cleaning_script.py
import pandas as pd
import numpy as np

def load_data(path):
    df = pd.read_csv(path, low_memory=False)
    return df

def basic_clean(df):
    # Drop exact duplicate rows
    df = df.drop_duplicates()
    # Standardize column names
    df.columns = [c.strip() for c in df.columns]
    # Convert common datetime columns if present
    for dt_col in ['game_date']:
        if dt_col in df.columns:
            df[dt_col] = pd.to_datetime(df[dt_col], errors='coerce')
    # Create target: positive EPA
    if 'expected_points_added' in df.columns:
        df['target_positive_epa'] = (df['expected_points_added'] > 0).astype(int)
    # Fill simple missing values for numeric with median (example)
    num_cols = df.select_dtypes(include=[np.number]).columns
    for c in num_cols:
        df[c] = df[c].fillna(df[c].median())
    # Fill categorical missing with 'MISSING'
    cat_cols = df.select_dtypes(include=['object','category']).columns
    for c in cat_cols:
        df[c] = df[c].fillna('MISSING')
    return df

if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv)>1 else '/mnt/data/supplementary_data.csv'
    df = load_data(path)
    df_clean = basic_clean(df)
    df_clean.to_csv('/mnt/data/supplementary_data_cleaned.csv', index=False)
    print('Cleaned data saved to /mnt/data/supplementary_data_cleaned.csv')
