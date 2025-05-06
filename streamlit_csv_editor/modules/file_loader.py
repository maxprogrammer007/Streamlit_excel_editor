# modules/file_loader.py
import pandas as pd
import streamlit as st

def load_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        return df, None
    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
        xls = pd.ExcelFile(uploaded_file)
        return None, xls
    else:
        st.error("Unsupported file format.")
        return None, None

def get_sheet(xls, sheet_name=None):
    if sheet_name:
        return xls.parse(sheet_name)
    return xls.parse(xls.sheet_names[0])  # default first sheet
