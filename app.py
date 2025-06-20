import streamlit as st
from config import (
    load_and_process_input,
    generate_flashcards,
    generate_mcqs,
    ai_assistant_reply,
    show_analytics,
    show_planner,
    export_flashcards,
    switch_theme,
    flashcard_viewer,
    future_lab_features
)

st.set_page_config(page_title="BatAnki - AI Flashcard Maker", layout="wide")
switch_theme()

st.title("🦇 BatAnki - AI Flashcard & MCQ Wizard")

tab = st.sidebar.radio("📚 Navigation", [
    "📤 Upload & Ingest",
    "🧠 Flashcards",
    "📝 MCQ Generator",
    "🤖 AI Assistant",
    "📅 Daily Planner",
    "📊 Analytics",
    "🧪 Labs"
])

if tab == "📤 Upload & Ingest":
    uploaded_file = st.file_uploader("Upload your material", type=["pdf", "docx", "txt", "epub", "mp3"])
    typed_text = st.text_area("Or paste/type your notes")
    if st.button("📥 Process"):
        load_and_process_input(uploaded_file, typed_text)

elif tab == "🧠 Flashcards":
    cards = generate_flashcards()
    if cards:
        flashcard_viewer(cards)
        export_flashcards(cards)

elif tab == "📝 MCQ Generator":
    generate_mcqs()

elif tab == "🤖 AI Assistant":
    ai_assistant_reply()

elif tab == "📅 Daily Planner":
    show_planner()

elif tab == "📊 Analytics":
    show_analytics()

elif tab == "🧪 Labs":
    future_lab_features()