import streamlit as st
import pandas as pd
from datetime import datetime

# Set page config
st.set_page_config(page_title="Task Matrix", layout="wide")

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = pd.DataFrame({
        'task': [],
        'category': [],
        'created_at': [],
        'completed': []
    })

# Categories with emojis
CATEGORIES = {
    "📥 Inbox": "inbox",
    "⚡ Now (2h)": "now",
    "🌅 Today (8h)": "today",
    "📅 This Week": "week",
    "🎯 This Month": "month",
    "✅ Completed": "completed"
}

def add_task(task, category):
    new_task = pd.DataFrame({
        'task': [task],
        'category': [category],
        'created_at': [datetime.now()],
        'completed': [False]
    })
    st.session_state.tasks = pd.concat([st.session_state.tasks, new_task], ignore_index=True)

# UI Layout
st.title("Task Matrix Manager")

# Add new task
with st.form("new_task"):
    col1, col2 = st.columns([3, 1])
    with col1:
        task = st.text_input("New Task")
    with col2:
        category = st.selectbox("Category", list(CATEGORIES.keys()))

    if st.form_submit_button("Add Task"):
        if task:
            add_task(task, CATEGORIES[category])
            st.success("Task added!")

# Display tasks by category
for emoji_cat, cat in CATEGORIES.items():
    st.subheader(emoji_cat)
    cat_tasks = st.session_state.tasks[
        (st.session_state.tasks.category == cat) & 
        (st.session_state.tasks.completed == (cat == "completed"))
    ]

    for idx, task in cat_tasks.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(task['task'])
        with col2:
            if st.button("✅" if cat != "completed" else "🔄", key=f"btn_{idx}"):
                st.session_state.tasks.loc[idx, 'completed'] = not task['completed']
                st.rerun()
