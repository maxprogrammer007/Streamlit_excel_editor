# modules/export.py
import pandas as pd

def to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def to_json(df):
    return df.to_json(orient="records")
