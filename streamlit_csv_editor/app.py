import streamlit as st
import pandas as pd
import os
from modules import file_loader, grid_editor, data_ops, validators, export, state_manager
from modules.mysql_handler import MySQLHandler
from utils.helpers import get_default_row

# --- Config ---
st.set_page_config(page_title="Streamlit Data Editor", layout="wide")

# --- Theme + JS ---
with open("streamlit_csv_editor\\assets\custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if os.path.exists("streamlit_csv_editor\\assets\\custom.js"):
    with open("streamlit_csv_editor\\assets\\custom.js") as f:
        st.components.v1.html(f"<script>{f.read()}</script>", height=0)

# --- Init Session ---
if "df" not in st.session_state:
    st.session_state.df = None
    st.session_state.original_df = None
    st.session_state.history = state_manager.init_history()
if "mysql_handler" not in st.session_state:
    st.session_state.mysql_handler = None

st.title("📊 CSV / Excel / MySQL Data Editor")

# --- SIDEBAR: MYSQL LOGIN ---
st.sidebar.header("🔐 MySQL Login")
with st.sidebar.form("mysql_login"):
    host = st.text_input("Host", "localhost")
    user = st.text_input("Username", "root")
    password = st.text_input("Password", type="password")
    submit_btn = st.form_submit_button("Connect")

if submit_btn:
    try:
        handler = MySQLHandler(host, user, password)
        handler.connect()
        st.session_state.mysql_handler = handler
        st.success("✅ Connected to MySQL!")
    except Exception as e:
        st.session_state.mysql_handler = None
        st.error(f"Connection failed: {e}")

# --- MYSQL BROWSER ---
if st.session_state.mysql_handler:
    dbs = st.session_state.mysql_handler.list_databases()
    db = st.sidebar.selectbox("Database", dbs)
    st.session_state.mysql_handler.database = db
    tables = st.session_state.mysql_handler.list_tables(db)
    tbl = st.sidebar.selectbox("Table", tables)

    if st.sidebar.button("📥 Load from MySQL"):
        df = st.session_state.mysql_handler.fetch_table(tbl)
        st.session_state.df = df.copy()
        st.session_state.original_df = df.copy()
        st.session_state.history = state_manager.init_history()

    if st.sidebar.button("📤 Save to MySQL"):
        try:
            st.session_state.mysql_handler.write_dataframe(st.session_state.df, tbl)
            st.success("✅ Table saved to MySQL")
        except Exception as e:
            st.error(f"Failed to write: {e}")

# --- FILE UPLOAD (Optional) ---
st.sidebar.markdown("---")
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV / Excel", type=["csv", "xlsx"])
if uploaded_file:
    df, xls = file_loader.load_file(uploaded_file)
    if xls:
        sheet = st.sidebar.selectbox("Sheet", xls.sheet_names)
        df = file_loader.get_sheet(xls, sheet)
    st.session_state.df = df.copy()
    st.session_state.original_df = df.copy()
    st.session_state.history = state_manager.init_history()

# --- EDITOR CONTROLS ---
if st.session_state.df is not None:
    st.sidebar.markdown("### 🛠 Editor")
    col1, col2 = st.sidebar.columns(2)
    if col1.button("➕ Add Row"):
        st.session_state.df = data_ops.add_blank_row(st.session_state.df)
        state_manager.push_undo(st.session_state.history, st.session_state.df)
    if col2.button("🔄 Reset"):
        st.session_state.df = data_ops.reset_to_original(st.session_state.original_df)
        st.session_state.history = state_manager.init_history()

    if st.sidebar.button("↩️ Undo"):
        st.session_state.df = state_manager.undo(st.session_state.history, st.session_state.df)

    if st.sidebar.button("↪️ Redo"):
        st.session_state.df = state_manager.redo(st.session_state.history, st.session_state.df)

    # --- Grid Editor ---
    st.subheader("📋 Editable Grid")
    updated_df = grid_editor.render_editable_grid(st.session_state.df)

    with st.expander("⚙️ Enforce Column Types"):
        col_types = {col: st.selectbox(col, ["str", "int", "float", "bool"], key=col)
                     for col in updated_df.columns}
        updated_df = validators.enforce_types(updated_df, col_types)

    st.session_state.df = updated_df

    # --- Export ---
    st.sidebar.markdown("### ⬇️ Export")
    fmt = st.sidebar.radio("Format", ["CSV", "Excel", "JSON"])
    if fmt == "CSV":
        st.sidebar.download_button("Download CSV", export.to_csv(updated_df), "edited.csv")
    elif fmt == "Excel":
        st.sidebar.download_button("Download Excel", export.to_excel(updated_df), "edited.xlsx")
    else:
        st.sidebar.download_button("Download JSON", export.to_json(updated_df), "edited.json")

    # --- Preview ---
    st.markdown("---")
    st.subheader("📊 Final Preview")
    st.dataframe(updated_df, use_container_width=True)
else:
    st.info("📤 Upload a file or connect to MySQL to begin.")
