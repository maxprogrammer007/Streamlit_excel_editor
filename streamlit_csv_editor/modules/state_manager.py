# modules/state_manager.py

def init_history():
    return {"undo": [], "redo": []}

def push_undo(history, df):
    history["undo"].append(df.copy())
    history["redo"].clear()

def undo(history, current_df):
    if history["undo"]:
        history["redo"].append(current_df.copy())
        return history["undo"].pop()
    return current_df

def redo(history, current_df):
    if history["redo"]:
        history["undo"].append(current_df.copy())
        return history["redo"].pop()
    return current_df
