# app.py

import streamlit as st
from config import (
    handle_file_upload,
    generate_flashcards,
    export_flashcards,
    show_sidebar_options,
    apply_custom_theme,
)
from pathlib import Path

# Set up Streamlit page configuration
st.set_page_config(
    page_title="BatAnki - AI Flashcard Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_theme()

# Sidebar
show_sidebar_options()

# Main App Interface
st.title("📘 BatAnki - AI Flashcard Generator")
st.markdown("Create Anki-style decks with AI from PDF, text, DOCX, EPUB, audio, or YouTube.")

uploaded_file = st.file_uploader("📂 Upload your input file", type=["pdf", "txt", "docx", "epub", "mp3", "wav", "mp4"])
user_text = st.text_area("✍️ Or paste/type your own content here")

if uploaded_file or user_text.strip():
    with st.spinner("Processing input and generating flashcards..."):
        input_data = handle_file_upload(uploaded_file, user_text)
        flashcards = generate_flashcards(input_data)

        if flashcards:
            st.success(f"✅ Generated {len(flashcards)} flashcards.")
            export_format = st.selectbox("📤 Export flashcards as:", ["CSV", "Anki .apkg"])
            if st.button("Download Flashcards"):
                export_flashcards(flashcards, export_format)
        else:
            st.warning("⚠️ No flashcards generated.")
else:
    st.info("📥 Upload a file or enter content to begin.")