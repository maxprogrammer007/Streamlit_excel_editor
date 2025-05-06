# modules/data_ops.py
import pandas as pd

def add_blank_row(df):
    new_row = {col: "" for col in df.columns}
    return df.append(new_row, ignore_index=True)

def delete_row_by_index(df, index):
    return df.drop(index=index).reset_index(drop=True)

def reset_to_original(original_df):
    return original_df.copy()
