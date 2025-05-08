import streamlit as st
import pandas as pd
import os
import mysql.connector

from modules import file_loader, grid_editor, data_ops, validators, export, state_manager
from modules.mysql_handler import MySQLHandler
from modules.role_manager_db import get_user_role, get_role_permissions
from utils.helpers import get_default_row

# --- Config ---
st.set_page_config(page_title="Streamlit Data Editor", layout="wide")

# --- Theme + JS ---
with open("streamlit_csv_editor/assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if os.path.exists("streamlit_csv_editor/assets/custom.js"):
    with open("streamlit_csv_editor/assets/custom.js") as f:
        st.components.v1.html(f"<script>{f.read()}</script>", height=0)

# --- Init Session ---
if "df" not in st.session_state:
    st.session_state.df = None
    st.session_state.original_df = None
    st.session_state.history = state_manager.init_history()
if "mysql_handler" not in st.session_state:
    st.session_state.mysql_handler = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "permissions" not in st.session_state:
    st.session_state.permissions = {"permissions": [], "columns": []}

st.title("📊 CSV / Excel / MySQL Data Editor")

# --- User Login + MySQL ---
st.sidebar.header("🔐 Login")
with st.sidebar.form("login_form"):
    db_host = st.text_input("MySQL Host", "localhost")
    db_user = st.text_input("DB User")
    db_pass = st.text_input("DB Password", type="password")
    app_user = st.text_input("App Username")
    app_pass = st.text_input("App Password", type="password")
    login_btn = st.form_submit_button("Login")

if login_btn:
    try:
        conn = mysql.connector.connect(host=db_host, user=db_user, password=db_pass)
        role = get_user_role(conn, app_user, app_pass)
        if role:
            st.session_state.mysql_handler = MySQLHandler(db_host, db_user, db_pass)
            st.session_state.mysql_handler.connect()
            st.session_state.user_role = role
            st.success(f"✅ Logged in as {app_user} ({role})")
        else:
            st.error("Invalid credentials or role not assigned.")
    except Exception as e:
        st.error(f"MySQL connection error: {e}")

# --- MySQL Database & Table Selection ---
if st.session_state.mysql_handler:
    dbs = st.session_state.mysql_handler.list_databases()
    db = st.sidebar.selectbox("Database", dbs)
    st.session_state.mysql_handler.database = db
    tables = st.session_state.mysql_handler.list_tables(db)
    tbl = st.sidebar.selectbox("Table", tables)

    if tbl and st.session_state.user_role:
        access = get_role_permissions(
            st.session_state.mysql_handler.conn,
            st.session_state.user_role,
            tbl
        )
        st.session_state.permissions = access
        allowed_cols = access["columns"]
        can_edit = "edit" in access["permissions"]
        can_insert = "insert" in access["permissions"]
        can_delete = "delete" in access["permissions"]
    else:
        can_edit = can_insert = can_delete = False
        allowed_cols = []

    if st.sidebar.button("📥 Load Table"):
        df = st.session_state.mysql_handler.fetch_table(tbl)
        st.session_state.df = df.copy()
        st.session_state.original_df = df.copy()
        st.session_state.history = state_manager.init_history()

    if st.sidebar.button("📤 Save Table") and can_edit:
        st.session_state.mysql_handler.write_dataframe(st.session_state.df, tbl)
        st.success("✅ Saved to database")

# --- Upload CSV/Excel (Optional) ---
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
    can_edit = True
    allowed_cols = "all"

# --- Editor ---
if st.session_state.df is not None:
    st.sidebar.markdown("### 🛠 Editor")

    if can_insert:
        if st.sidebar.button("➕ Add Row"):
            st.session_state.df = data_ops.add_blank_row(st.session_state.df)
            state_manager.push_undo(st.session_state.history, st.session_state.df)

    if st.sidebar.button("🔄 Reset"):
        st.session_state.df = data_ops.reset_to_original(st.session_state.original_df)
        st.session_state.history = state_manager.init_history()

    if st.sidebar.button("↩️ Undo"):
        st.session_state.df = state_manager.undo(st.session_state.history, st.session_state.df)

    if st.sidebar.button("↪️ Redo"):
        st.session_state.df = state_manager.redo(st.session_state.history, st.session_state.df)

    # --- Grid ---
    st.subheader("📋 Editable Grid")
    if can_edit:
        updated_df = grid_editor.render_editable_grid(st.session_state.df, allowed_cols)
    else:
        st.warning("Read-only access. You do not have permission to edit.")
        updated_df = st.session_state.df

    st.session_state.df = updated_df

    with st.expander("⚙️ Enforce Column Types"):
        col_types = {col: st.selectbox(col, ["str", "int", "float", "bool"], key=col)
                     for col in updated_df.columns}
        updated_df = validators.enforce_types(updated_df, col_types)

    # --- Export Options ---
    st.sidebar.markdown("### ⬇️ Export")
    fmt = st.sidebar.radio("Format", ["CSV", "Excel", "JSON"])
    if fmt == "CSV":
        st.sidebar.download_button("Download CSV", export.to_csv(updated_df), "edited.csv")
    elif fmt == "Excel":
        st.sidebar.download_button("Download Excel", export.to_excel(updated_df), "edited.xlsx")
    else:
        st.sidebar.download_button("Download JSON", export.to_json(updated_df), "edited.json")

    # --- Final Preview ---
    st.markdown("---")
    st.subheader("📊 Final Preview")
    st.dataframe(updated_df, use_container_width=True)
else:
    st.info("📤 Upload a file or connect to MySQL to begin.")
