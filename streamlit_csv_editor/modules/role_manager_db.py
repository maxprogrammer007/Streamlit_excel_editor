# modules/role_manager_db.py

import pandas as pd

def get_user_role(conn, username, password):
    query = f"SELECT role FROM users WHERE username = %s AND password = %s"
    cursor = conn.cursor()
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    return result[0] if result else None

def get_role_permissions(conn, role, table_name):
    query = """
    SELECT permission, column_name
    FROM role_permissions
    WHERE role = %s AND table_name = %s
    """
    df = pd.read_sql(query, conn, params=(role, table_name))
    perms = df["permission"].unique().tolist()
    if "all" in df["column_name"].tolist():
        columns = "all"
    else:
        columns = df["column_name"].unique().tolist()
    return {
        "permissions": perms,
        "columns": columns
    }
