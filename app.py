"""
BatAnki: Next-Gen AI Flashcard Web App (Beta Version)
=======================================================

This app extracts text from various inputs, generates flashcards (including beta types),
and provides export options. It supports multiple input sources:
  - File Upload (PDF, TXT, DOCX, EPUB, PNG, JPG, MP3, WAV)
  - Manual Entry
  - Voice Input (audio file upload)
  - YouTube Link (simulate transcript extraction)
  - OneNote (paste HTML/MHT content)

A centralized configuration (config.py) holds key settings.
"""

import streamlit as st
import fitz  # PyMuPDF for PDF extraction
import tempfile
import os
import json
import numpy as np
import pandas as pd
import config  # Import centralized configuration

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

# ------------------ Utility Functions ----------------------

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

def get_youtube_transcript(youtube_url):
    """
    Dummy function to simulate transcript extraction from a YouTube link.
    In a production version, you can integrate a YouTube API or youtube-dl based solution.
    """
    return f"Dummy transcript for YouTube video:\n{youtube_url}\n[Transcript extraction not implemented]"

def preprocess_text(text):
    """Placeholder for cleaning and chunking text."""
    return text.strip()[:config.MAX_TEXT_LENGTH]

def summarize_text(text):
    """Dummy summarization function."""
    if len(text) > config.SUMMARY_LENGTH:
        return "Summary: " + text[:config.SUMMARY_LENGTH] + "..."
    else:
        return "Summary: " + text

def generate_flashcards(text, include_beta=False):
    """Generates flashcards based on the provided text.
    
    Creates a dynamic flashcard from your content (first 100 characters), then adds dummy cards.
    """
    cards = []
    if text:
        dynamic_card = {
            "type": "Basic",
            "front": "What is this document about?",
            "back": text[:100] + ("..." if len(text) > 100 else "")
        }
    else:
        dynamic_card = {
            "type": "Basic",
            "front": "What is BatAnki?",
            "back": "A next-gen AI flashcard web app combining multimodal inputs."
        }
    cards.append(dynamic_card)
    
    # Append additional dummy flashcards
    cards.append({
        "type": "MCQ",
        "question": "Which AI engine is used for summarization?",
        "options": ["Mistral", "BART", "GPT", "T5"],
        "answer": "Mistral"
    })
    cards.append({
        "type": "Cloze",
        "text": "BatAnki is built using ___ and Python.",
        "answer": "Streamlit"
    })
    if include_beta and config.ENABLE_BETA_FEATURES:
        cards.append({
            "type": "Reverse",
            "front": "What is reverse learning in BatAnki?",
            "back": "It flips Q and A for alternative recall."
        })
        cards.append({
            "type": "Memo",
            "front": "Explain the memo card functionality.",
            "back": "Provides detailed notes and source references."
        })
        cards.append({
            "type": "Image Occlusion",
            "front": "Identify the hidden part of the image.",
            "back": "The occluded answer details are revealed."
        })
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

def export_cards_apkg(cards):
    """Exports flashcards to an APKG file using genanki.
    
    This function returns the path to a temporary APKG file.
    """
    try:
        import genanki
    except ImportError:
        st.error("The genanki library is not installed. Install it via pip to enable APKG export.")
        return None
    
    deck_id = 2059400110  # Use a unique deck ID here.
    model_id = 1607392319  # Use a unique model ID.
    
    my_deck = genanki.Deck(
        deck_id,
        'BatAnki Deck'
    )
    
    my_model = genanki.Model(
        model_id,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ]
    )
    
    # Create a note for each flashcard.
    for card in cards:
        if card["type"] == "Basic":
            question = card.get("front", "")
            answer = card.get("back", "")
        elif card["type"] == "MCQ":
            question = f"{card.get('question', '')}\nOptions: {', '.join(card.get('options', []))}"
            answer = card.get("answer", "")
        elif card["type"] == "Cloze":
            question = card.get("text", "")
            answer = card.get("answer", "")
        elif card["type"] in ["Reverse", "Memo", "Image Occlusion"]:
            question = card.get("front", "")
            answer = card.get("back", "")
        else:
            question, answer = "", ""
        note = genanki.Note(
            model=my_model,
            fields=[question, answer]
        )
        my_deck.add_note(note)
    
    pkg = genanki.Package(my_deck)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.apkg')
    pkg.write_to_file(temp_file.name)
    return temp_file.name

# ------------------ Streamlit App UI with Tabs -----------------------

st.set_page_config(page_title=config.PAGE_TITLE, layout=config.PAGE_LAYOUT)
st.title("🦇 BatAnki")
st.caption("AI Flashcards with Multimodal Input | Beta Version with Advanced Features")

# Sidebar: Configure input and show future roadmap
st.sidebar.header("Input Options")

# Comprehensive input source list
input_source = st.sidebar.selectbox("Select Input Source", 
                                    ["File Upload", "Manual Entry", "Voice Input", "YouTube Link", "OneNote"])
beta_enabled = st.sidebar.checkbox("Enable Beta Features", value=config.ENABLE_BETA_FEATURES)
st.sidebar.markdown("---")
st.sidebar.write("Future Features:")
st.sidebar.write("- Adaptive Learning & Gamification")
st.sidebar.write("- Smart Review Scheduler (SM-2)")
st.sidebar.write("- AnkiConnect Sync")
st.sidebar.write("- Detailed Analytics Dashboard")
st.sidebar.write("- Voice Input/TTS")
st.sidebar.write("- Deck Hub & Marketplace")

# Create tabs for Main Pipeline and Beta Features
tabs = st.tabs(["Main Pipeline", "Beta Features"])

# ------------------ Input Handling ---------------------------
text_input = ""
with st.container():
    if input_source == "File Upload":
        uploaded_file = st.file_uploader(
            "📄 Upload a file (PDF, TXT, DOCX, EPUB, PNG, JPG, MP3, WAV)", 
            type=["pdf", "txt", "docx", "epub", "png", "jpg", "mp3", "wav"]
        )
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
    elif input_source == "YouTube Link":
        youtube_url = st.text_input("Enter YouTube Video URL")
        if youtube_url:
            text_input = get_youtube_transcript(youtube_url)
    elif input_source == "OneNote":
        text_input = st.text_area("Paste OneNote HTML/MHT content here:", height=300)

# ------------------ Main Pipeline Tab ---------------------------
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
        
        # Export APKG file if genanki is available
        apkg_file_path = export_cards_apkg(cards)
        if apkg_file_path:
            with open(apkg_file_path, 'rb') as f:
                apkg_binary = f.read()
            st.download_button("Download as APKG", data=apkg_binary, file_name="BatAnki_deck.apkg", mime="application/octet-stream")
    else:
        st.info("Awaiting input. Please select an input method in the sidebar and upload or enter your content.")

# ------------------ Beta Features Tab ---------------------------
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
    data = pd.DataFrame({
        'Day': pd.date_range(start="2025-01-01", periods=7),
        'XP': [50, 70, 80, 120, 150, 130, 170]
    })
    st.line_chart(data.set_index('Day'))
    
    st.markdown("### Voice Input & TTS")
    st.write("Voice transcription is enabled. TTS functionality for flashcards review is in early beta.")
    
    st.markdown("### Upcoming Features")
    st.write("- Enhanced OCR for scanned documents")
    st.write("- Direct export to Anki package (.apkg)")
    st.write("- Detailed analytics & smart scheduling")
    st.write("- Expanded voice and TTS integration")
    
    st.info("Beta features are experimental. Your feedback is greatly appreciated to help BatAnki evolve!")

# ------------------ Final Footer ---------------------------
st.markdown("---")
st.caption("BatAnki Beta – Evolving AI Flashcards powered by Streamlit")