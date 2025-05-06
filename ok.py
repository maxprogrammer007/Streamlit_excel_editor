import os

# Folder and file structure
structure = {
    "streamlit_csv_editor": {
        "modules": {
            "file_loader.py": "",
            "grid_editor.py": "",
            "data_ops.py": "",
            "validators.py": "",
            "export.py": "",
            "state_manager.py": "",
            "__init__.py": ""
        },
        "utils": {
            "helpers.py": "",
            "__init__.py": ""
        },
        "data": {},
        "assets": {},
        "requirements.txt": """streamlit
pandas
openpyxl
st-aggrid
xlsxwriter
""",
        "app.py": ""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)

if __name__ == "__main__":
    create_structure(".", structure)
    print("✅ Folder structure created successfully.")
