import streamlit as st
from config import (
    handle_file_upload,
    extract_flashcard_chunks,
    generate_anki_cards,
    show_flashcards,
    export_apkg,
    export_csv,
    speak_text
)

st.set_page_config(page_title="🦇 BatAnki – AI Flashcard Wizard", layout="wide")
st.title("🦇 BatAnki – AI Flashcard Generator")

# Sidebar: Input
st.sidebar.header("📂 Input Options")
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["pdf", "txt", "docx", "epub", "mp3"])
youtube_url = st.sidebar.text_input("Paste YouTube link (optional):")
text_input = st.sidebar.text_area("Or paste raw text here:")

# Sidebar: Card Settings
st.sidebar.header("⚙️ Flashcard Settings")
card_type = st.sidebar.selectbox("Card Type", ["Basic", "Cloze", "Memo", "Reverse", "MCQ"])
deck_name = st.sidebar.text_input("Deck Name", value="BatAnkiDeck")

# Sidebar: Utilities
st.sidebar.header("🧰 Utilities")
speak_answer = st.sidebar.checkbox("Enable Text-to-Speech (Answer)")

# Process
if st.sidebar.button("⚡ Generate Flashcards"):
    with st.spinner("Processing input..."):
        raw_text = handle_file_upload(uploaded_file, text_input, youtube_url)
        chunks = extract_flashcard_chunks(raw_text)
        cards = generate_anki_cards(chunks, card_type)
        st.session_state.cards = cards
        st.success(f"✅ Generated {len(cards)} cards!")

# Display Cards
if "cards" in st.session_state:
    show_flashcards(st.session_state.cards, speak=speak_answer)
    st.markdown("---")
    export_apkg(st.session_state.cards, deck_name)
    export_csv(st.session_state.cards, deck_name)