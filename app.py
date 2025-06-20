"""
BatAnki: Next-Gen AI Flashcard Web App (Beta Version)
=======================================================

This unified platform generates multimodal flashcards from a wide range of inputs.
It implements our core stages:
  • Clean & chunk input (Regurgitation & Peristalsis)
  • Summarize and generate flashcards (Digestion & Absorption)
  • Export to CSV/JSON (Excretion)
  • Final UI enhancements (Resurrection)

Advanced Beta functionalities include:
  • Additional flashcard types (Reverse, Memo, Image Occlusion)
  • Adaptive Learning & Gamification (XP, streaks, badges)
  • Smart Review Scheduler (SM-2)
  • AnkiConnect Sync (for direct sync to Anki)
  • Analytics Dashboard (performance tracking)
  • Voice Input & TTS (optional accessibility enhancements)
  
The project supports input from PDF, TXT, DOCX, EPUB, images, and audio (MP3/WAV).
"""

import streamlit as st
import fitz  # PyMuPDF for PDF extraction
import tempfile
import os
import json
import numpy as np
import pandas as pd

# Optional libraries for OCR and Speech Recognition
try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

# ---------------------------------------------
# Utility Functions
# ---------------------------------------------

def extract_pdf_text(pdf_file):
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    try:
        pdf_file.seek(0)
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        st.error("Error reading PDF: " + str(e))
    return text.strip()

def transcribe_audio(audio_file):
    """Transcribes an audio file to text using SpeechRecognition."""
    if sr:
        r = sr.Recognizer()
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                tmp.flush()
                with sr.AudioFile(tmp.name) as source:
                    audio = r.record(source)
                text = r.recognize_google(audio)
                os.unlink(tmp.name)
                return text
        except Exception as e:
            st.error("Error transcribing audio: " + str(e))
            return ""
    else:
        st.warning("SpeechRecognition not available.")
        return ""

def ocr_extract_text(image_file):
    """Extracts text from an image file using pytesseract."""
    if pytesseract:
        try:
            img = Image.open(image_file)
            return pytesseract.image_to_string(img)
        except Exception as e:
            st.error("OCR error: " + str(e))
            return ""
    else:
        st.warning("pytesseract not available.")
        return ""

def preprocess_text(text):
    """Placeholder for cleaning and chunking text."""
    return text.strip()[:5000]

def summarize_text(text):
    """Dummy summarization function."""
    return "Summary: " + (text[:200] + "..." if len(text) > 200 else text)

def generate_flashcards(text, include_beta=False):
    """Generates dummy flashcards from text.
    If include_beta is True, additional beta flashcard types are added.
    """
    cards = []
    # Core flashcards
    cards.append({"type": "Basic", "front": "What is BatAnki?",
                  "back": "A next-gen AI flashcard web app combining multimodal inputs."})
    cards.append({"type": "MCQ", "question": "Which AI engine is used for summarization?",
                  "options": ["Mistral", "BART", "GPT", "T5"], "answer": "Mistral"})
    cards.append({"type": "Cloze", "text": "BatAnki is built using ___ and Python.", "answer": "Streamlit"})
    # Additional beta flashcard types
    if include_beta:
        cards.append({"type": "Reverse", "front": "What is reverse learning in BatAnki?",
                      "back": "It flips Q and A for alternative recall."})
        cards.append({"type": "Memo", "front": "Explain the memo card functionality.",
                      "back": "Provides detailed notes and source references."})
        cards.append({"type": "Image Occlusion", "front": "Identify the hidden part of the image.",
                      "back": "The occluded answer details are revealed."})
    return cards

def export_cards_csv(cards):
    """Exports flashcards to CSV format."""
    csv_data = "type,question/front,answer/back,details\n"
    for card in cards:
        if card["type"] == "Basic":
            csv_data += f"{card['type']},{card['front']},{card['back']},\n"
        elif card["type"] == "MCQ":
            options = ";".join(card["options"])
            csv_data += f"{card['type']},{card['question']},{card['answer']},{options}\n"
        elif card["type"] == "Cloze":
            csv_data += f"{card['type']},{card['text']},{card['answer']},\n"
        elif card["type"] in ["Reverse", "Memo", "Image Occlusion"]:
            csv_data += f"{card['type']},{card['front']},{card['back']},\n"
    return csv_data

def export_cards_json(cards):
    """Exports flashcards to JSON format."""
    return json.dumps(cards, indent=4)

# ---------------------------------------------
# Streamlit App UI with Tabs for Main & Beta Features
# ---------------------------------------------

st.set_page_config(page_title="🦇 BatAnki: AI Flashcards Beta", layout="wide")
st.title("🦇 BatAnki")
st.caption("AI Flashcards with Multimodal Input | Beta Version with Advanced Features")

# Sidebar: Define input method and show future roadmap
st.sidebar.header("Input Options")
input_source = st.sidebar.selectbox("Select Input Source", ["File Upload", "Manual Entry", "Voice Input"])
beta_enabled = st.sidebar.checkbox("Enable Beta Features", value=True)
st.sidebar.markdown("---")
st.sidebar.write("Future Features:")
st.sidebar.write("- Adaptive Learning & Gamification")
st.sidebar.write("- Smart Review Scheduler (SM-2)")
st.sidebar.write("- AnkiConnect Sync")
st.sidebar.write("- Detailed Analytics Dashboard")
st.sidebar.write("- Voice Input/TTS")
st.sidebar.write("- Deck Hub & Marketplace")

# Create tabs for the main pipeline and advanced beta modules
tabs = st.tabs(["Main Pipeline", "Beta Features"])

# ---------------------------------------------
# Input Handling (applies to both tabs)
# ---------------------------------------------
text_input = ""
with st.container():
    if input_source == "File Upload":
        uploaded_file = st.file_uploader("📄 Upload a file (PDF, TXT, DOCX, EPUB, PNG, JPG, MP3, WAV)", 
                                         type=["pdf", "txt", "docx", "epub", "png", "jpg", "mp3", "wav"])
        if uploaded_file:
            ext = uploaded_file.name.lower().split(".")[-1]
            if ext == "pdf":
                text_input = extract_pdf_text(uploaded_file)
            elif ext in ["txt", "docx", "epub"]:
                try:
                    text_input = uploaded_file.read().decode("utf-8", errors="ignore")
                except Exception as e:
                    st.error("Error reading file: " + str(e))
            elif ext in ["png", "jpg"]:
                text_input = ocr_extract_text(uploaded_file)
            elif ext in ["mp3", "wav"]:
                text_input = transcribe_audio(uploaded_file)
    elif input_source == "Manual Entry":
        text_input = st.text_area("Enter or paste your text here:", height=300)
    elif input_source == "Voice Input":
        audio_file = st.file_uploader("Upload an audio file (MP3, WAV)", type=["mp3", "wav"])
        if audio_file:
            text_input = transcribe_audio(audio_file)

# ---------------------------------------------
# Main Pipeline Tab
# ---------------------------------------------
with tabs[0]:
    st.subheader("Extracted/Entered Text")
    if text_input:
        st.text_area("Review and edit:", text_input, height=300)
        processed_text = preprocess_text(text_input)
        summary = summarize_text(processed_text)

        st.subheader("Summarized Content")
        st.write(summary)

        cards = generate_flashcards(processed_text, include_beta=beta_enabled)
        st.subheader("Generated Flashcards")
        for idx, card in enumerate(cards):
            st.markdown(f"**Flashcard {idx + 1} ({card['type']})**")
            if card["type"] == "Basic":
                st.write(f"**Q:** {card['front']}")
                st.write(f"**A:** {card['back']}")
            elif card["type"] == "MCQ":
                st.write(f"**Q:** {card['question']}")
                st.write(f"**Options:** {', '.join(card['options'])}")
                st.write(f"**Answer:** {card['answer']}")
            elif card["type"] == "Cloze":
                st.write(f"**Text:** {card['text']}")
                st.write(f"**Answer:** {card['answer']}")
            elif card["type"] in ["Reverse", "Memo", "Image Occlusion"]:
                st.write(f"**Front:** {card['front']}")
                st.write(f"**Back:** {card['back']}")
                
        st.subheader("Export Options")
        csv_data = export_cards_csv(cards)
        json_data = export_cards_json(cards)
        st.download_button("Download as CSV", data=csv_data, file_name="BatAnki_flashcards.csv", mime="text/csv")
        st.download_button("Download as JSON", data=json_data, file_name="BatAnki_flashcards.json", mime="application/json")
    else:
        st.info("Awaiting input. Please select an input method in the sidebar and upload or enter your content.")

# ---------------------------------------------
# Beta Features Tab
# ---------------------------------------------
with tabs[1]:
    st.subheader("Beta Features & Advanced Modules")
    st.markdown("### Advanced Flashcard Types")
    st.write("- **Reverse Cards:** Flip Q and A for alternative learning.")
    st.write("- **Memo Cards:** Provide detailed notes and source references.")
    st.write("- **Image Occlusion Cards:** Hide parts of an image for recall challenges.")
    
    st.markdown("### Adaptive Learning & Gamification")
    st.write("This module will adapt your review schedule and reward progress with XP, streaks, and badges.")
    
    st.markdown("### Smart Review Scheduler (SM-2)")
    st.write("Optimizes review timings based on your performance. (Currently in beta)")
    
    st.markdown("### AnkiConnect Integration")
    st.write("Directly sync your flashcards with Anki Desktop. (Beta integration coming soon)")
    
    st.markdown("### Analytics Dashboard")
    st.write("Dummy Performance Analytics (Beta):")
    # Generate dummy analytics data
    data = pd.DataFrame({
        'Day': pd.date_range(start="2025-01-01", periods=7),
        'XP': [50, 70, 80, 120, 150, 130, 170]
    })
    st.line_chart(data.set_index('Day'))
    
    st.markdown("### Voice Input & Text-to-Speech (TTS)")
    st.write("Voice transcription is enabled. TTS functionality for flashcards review is in early beta.")
    
    st.markdown("### Upcoming Features")
    st.write("- Enhanced OCR for scanned documents")
    st.write("- Direct export to Anki package (.apkg)")
    st.write("- Detailed review analytics & smart scheduling")
    st.write("- Expanded voice and TTS integration")
    
    st.info("Beta features are experimental. Your feedback is greatly appreciated to help BatAnki evolve!")

# ---------------------------------------------
# Final Footer
# ---------------------------------------------
st.markdown("---")
st.caption("BatAnki Beta – Evolving AI Flashcards powered by Streamlit")
