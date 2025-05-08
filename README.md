
# 📊 Streamlit-Based CSV/Excel/MySQL Data Editor

An interactive and secure data editor built with **Streamlit**, **AgGrid**, and **MySQL** — supporting:

- 🔐 User login with role-based permissions
- 📤 CSV/Excel upload and editing
- 🧾 MySQL table editor with cell-level control
- 💾 Export to CSV, Excel, JSON
- 🎨 Modern dark UI with custom JS

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| **User Login** | Users log in with their credentials stored in a `users` table in MySQL |
| **Role-Based Access** | Access controlled by `role_permissions` table: edit/insert/delete at column-level |
| **MySQL Integration** | Load and edit tables from MySQL, with secure commit back |
| **CSV/Excel Upload** | Upload a `.csv` or `.xlsx` file to preview and edit |
| **Editable Grid** | Powered by AgGrid for responsive editing |
| **Column Type Casting** | Optional casting of columns using dropdowns |
| **Export Options** | Export as `.csv`, `.xlsx`, or `.json` |
| **Modern UI** | Custom CSS theme + JS ripple effects for smooth experience |

---

## 🗃️ Database Schema

### `users` Table

```sql
CREATE TABLE users (
  username VARCHAR(50) PRIMARY KEY,
  password VARCHAR(255),
  role VARCHAR(50)
);
```

### `role_permissions` Table

```sql
CREATE TABLE role_permissions (
  role VARCHAR(50),
  table_name VARCHAR(50),
  permission ENUM('edit', 'insert', 'delete'),
  column_name VARCHAR(50)
);
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourname/streamlit-data-editor.git
cd streamlit-data-editor
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Tables

Use the schema above to create `users` and `role_permissions`. Insert users and permissions:

```sql
INSERT INTO users VALUES ('admin_user', 'admin123', 'admin');
INSERT INTO role_permissions VALUES ('admin', 'employees', 'edit', 'all');
```

### 4. Launch the App

```bash
streamlit run app.py
```

---

## 🔑 Access Control Flow

1. User logs in from sidebar using MySQL credentials and app username/password.
2. App authenticates using `users` table and determines role.
3. Role permissions are fetched from `role_permissions` table.
4. Based on permission:

   * Certain columns are editable
   * Add/Delete buttons are shown/hidden
   * Grid restricts input at column-level

---

## 🧠 File Structure

```
streamlit_csv_editor/
├── app.py
├── requirements.txt
├── assets/
│   ├── custom.css       # Dark mode styling
│   ├── custom.js        # Ripple effects & interactivity
├── modules/
│   ├── mysql_handler.py       # MySQL wrapper
│   ├── role_manager_db.py     # Role + permission loader from DB
│   └── (other editor modules)
├── utils/
│   └── helpers.py
├── data/
│   └── sample_test_file.xlsx
```

---

## ✅ Permissions Example

### Role: `editor`

| Table     | Permission | Editable Columns         |
| --------- | ---------- | ------------------------ |
| employees | `edit`     | name, salary, department |
| products  | `edit`     | name, price              |

### Role: `viewer`

* No permissions. Read-only UI.

---

## 📦 Future Enhancements

* ✅ Role management via UI
* ✅ Token-based login with hashing
* ✅ Row-level permissions
* ✅ Audit logging of edits

