# config.py

import streamlit as st
import base64
import io
import tempfile
import os
import csv
from genanki import Note, Deck, Package, Model
import uuid
from PyPDF2 import PdfReader

# Basic Flashcard Model
model = Model(
    model_id=1607392319,
    name="BasicModel",
    fields=[
        {"name": "Question"},
        {"name": "Answer"}
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Question}}",
            "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}",
        }
    ]
)

# Sidebar options
def show_sidebar_options():
    st.sidebar.image("https://i.imgur.com/B6jC5kR.png", width=180)
    st.sidebar.header("🧠 BatAnki Menu")
    st.sidebar.markdown("""
- Upload PDF, DOCX, TXT, Audio, YouTube
- Export to Anki or CSV
- Use AI to generate high-yield cards
- Dark/Light mode toggle
""")

# Theme toggle
def apply_custom_theme():
    dark_mode = st.sidebar.toggle("🌗 Dark Mode", value=False)
    theme_css = """
        <style>
        body { background-color: %s; color: %s; }
        .stButton > button { background-color: #7E57C2; color: white; }
        </style>
    """ % (
        "#121212" if dark_mode else "#ffffff",
        "#ffffff" if dark_mode else "#000000"
    )
    st.markdown(theme_css, unsafe_allow_html=True)

# Input handler
def handle_file_upload(file, text):
    if file:
        suffix = Path(file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        if suffix == ".pdf":
            return extract_text_from_pdf(tmp_path)
        elif suffix in [".txt", ".docx", ".epub"]:
            return extract_text_from_textlike(tmp_path)
        elif suffix in [".mp3", ".wav"]:
            return transcribe_audio(tmp_path)
        elif suffix in [".mp4", ".mov"]:
            return extract_audio_from_video(tmp_path)
    elif text.strip():
        return text.strip()

    return ""

# Text extraction (mocked for now)
def extract_text_from_pdf(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_textlike(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def transcribe_audio(path):
    return "Audio transcription not implemented here."

def extract_audio_from_video(path):
    return "Video to audio not implemented."

# Flashcard generation logic
def generate_flashcards(text):
    lines = text.strip().split("\n")
    flashcards = []

    for line in lines:
        if ":" in line:
            q, a = line.split(":", 1)
            flashcards.append({"question": q.strip(), "answer": a.strip()})
    return flashcards

# Export
def export_flashcards(cards, format_type):
    if format_type == "CSV":
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(["Question", "Answer"])
        for card in cards:
            writer.writerow([card["question"], card["answer"]])

        b64 = base64.b64encode(csv_file.getvalue().encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="flashcards.csv">📥 Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

    elif format_type == "Anki .apkg":
        deck = Deck(deck_id=uuid.uuid4().int >> 64, name="BatAnki Deck")
        for card in cards:
            note = Note(model=model, fields=[card["question"], card["answer"]])
            deck.add_note(note)
        pkg = Package(deck)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".apkg") as tmp:
            pkg.write_to_file(tmp.name)
            with open(tmp.name, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="flashcards.apkg">📥 Download .apkg</a>'
                st.markdown(href, unsafe_allow_html=True)