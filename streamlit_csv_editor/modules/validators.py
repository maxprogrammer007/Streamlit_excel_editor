# modules/validators.py

def enforce_types(df, schema_dict):
    for col, col_type in schema_dict.items():
        try:
            df[col] = df[col].astype(col_type)
        except Exception:
            pass  # You can also highlight cells with errors if needed
    return df
