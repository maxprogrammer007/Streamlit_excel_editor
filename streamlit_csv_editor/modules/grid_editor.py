# modules/grid_editor.py
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def render_editable_grid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, filter=True, resizable=True)
    gb.configure_grid_options(enableRowDeletion=True)
    grid_options = gb.build()

    grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    allow_unsafe_jscode=True,
    fit_columns_on_grid_load=True,
    theme="balham"  # or "alpine"
)


    return grid_response['data']
