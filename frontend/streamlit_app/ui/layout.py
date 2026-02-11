import streamlit as st

def prime_layout(title: str):
    st.set_page_config(
        page_title=title,
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(f"# {title}")
    st.divider()
