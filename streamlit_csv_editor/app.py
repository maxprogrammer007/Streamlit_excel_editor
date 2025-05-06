import streamlit as st
import pandas as pd
from modules import file_loader, grid_editor, data_ops, validators, export, state_manager
from utils.helpers import get_default_row
import os

# --- Page Config ---
st.set_page_config(page_title="📊 Streamlit Data Editor", layout="wide")

# --- Theme Selection ---
theme = st.sidebar.radio("🌗 Theme", ["Light", "Dark"])
theme_file = "/workspaces/Streamlit_excel_editor/streamlit_csv_editor/assets/dark_theme.css" if theme == "Dark" else "/workspaces/Streamlit_excel_editor/streamlit_csv_editor/assets/custom.css"
with open(theme_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Load Custom JS ---
if os.path.exists("/workspaces/Streamlit_excel_editor/streamlit_csv_editor/assets/custom.js"):
    with open("/workspaces/Streamlit_excel_editor/streamlit_csv_editor/assets/custom.js") as f:
        st.components.v1.html(f"<script>{f.read()}</script>", height=0)

# --- Title ---
st.title("📋 Interactive CSV/Excel Editor (AgGrid + Streamlit)")

# --- Session Initialization ---
if "df" not in st.session_state:
    st.session_state.df = None
    st.session_state.original_df = None
    st.session_state.history = state_manager.init_history()

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    df, xls = file_loader.load_file(uploaded_file)

    if xls:
        sheet = st.selectbox("Select sheet", xls.sheet_names)
        df = file_loader.get_sheet(xls, sheet)

    st.session_state.df = df.copy()
    st.session_state.original_df = df.copy()
    st.session_state.history = state_manager.init_history()
    state_manager.push_undo(st.session_state.history, df)

# --- Sidebar Editor Controls ---
if st.session_state.df is not None:
    st.sidebar.header("🛠 Editor Actions")

    col1, col2 = st.sidebar.columns(2)
    if col1.button("➕ Add Row"):
        st.session_state.df = data_ops.add_blank_row(st.session_state.df)
        state_manager.push_undo(st.session_state.history, st.session_state.df)

    if col2.button("🗑 Reset"):
        st.session_state.df = data_ops.reset_to_original(st.session_state.original_df)
        st.session_state.history = state_manager.init_history()

    if st.sidebar.button("↩️ Undo"):
        st.session_state.df = state_manager.undo(st.session_state.history, st.session_state.df)

    if st.sidebar.button("↪️ Redo"):
        st.session_state.df = state_manager.redo(st.session_state.history, st.session_state.df)

    # --- Display AgGrid Table ---
    st.subheader("🧾 Editable Table")
    updated_df = grid_editor.render_editable_grid(st.session_state.df)

    # --- Optional: Enforce Column Types ---
    with st.expander("⚙️ Enforce Column Types"):
        col_types = {col: st.selectbox(f"{col}", ["str", "int", "float", "bool"], key=col)
                     for col in updated_df.columns}
        updated_df = validators.enforce_types(updated_df, col_types)

    st.session_state.df = updated_df

    # --- Export Section ---
    st.sidebar.header("⬇️ Export File")
    export_format = st.sidebar.radio("Format", ["CSV", "Excel", "JSON"])

    if export_format == "CSV":
        st.sidebar.download_button("📥 Download CSV", export.to_csv(updated_df), "edited.csv", "text/csv")
    elif export_format == "Excel":
        st.sidebar.download_button("📥 Download Excel", export.to_excel(updated_df),
                                   "edited.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.sidebar.download_button("📥 Download JSON", export.to_json(updated_df), "edited.json", "application/json")

    # --- Final Preview ---
    st.markdown("---")
    st.subheader("📊 Final Data Preview")
    st.dataframe(updated_df, use_container_width=True)
else:
    st.info("📤 Upload a CSV or Excel file to begin editing.")
