import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat
from components.sample_pdf import render_sample_pdf_download

st.set_page_config(page_title="AI Medical Assistant", layout="wide")
st.title("🩺 Medical Assistant Chatbot")

# Sidebar uploader
render_uploader()

# Sample PDF download in sidebar
render_sample_pdf_download()

# Main chat UI
render_chat()

# Download chat history
render_history_download()
