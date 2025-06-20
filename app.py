import streamlit as st
from config import (
    handle_file_upload,
    extract_flashcard_chunks,
    generate_anki_cards,
    show_flashcards,
    export_apkg,
    export_csv
)

st.set_page_config(page_title="🦇 BatAnki", layout="wide")
st.title("🦇 BatAnki – AI Flashcard Generator")

# Sidebar: Input
st.sidebar.header("📂 Input Options")
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["pdf", "txt", "docx", "epub", "mp3"])
text_input = st.sidebar.text_area("Or paste raw text here:")

# Sidebar: Card Settings
st.sidebar.header("⚙️ Card Settings")
card_type = st.sidebar.selectbox("Choose Card Type", ["Basic", "Cloze", "Memo", "Reverse", "MCQ"])
deck_name = st.sidebar.text_input("Deck Name", value="BatAnkiDeck")

# Process
if st.sidebar.button("⚡ Generate Flashcards"):
    with st.spinner("Processing and generating flashcards..."):
        text = handle_file_upload(uploaded_file, text_input)
        chunks = extract_flashcard_chunks(text)
        cards = generate_anki_cards(chunks, card_type)
        st.session_state.cards = cards
        st.success(f"✅ Generated {len(cards)} cards!")

# Show Results
if "cards" in st.session_state:
    show_flashcards(st.session_state.cards)
    st.markdown("---")
    export_apkg(st.session_state.cards, deck_name)
    export_csv(st.session_state.cards, deck_name)