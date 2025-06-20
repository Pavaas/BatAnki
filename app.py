import streamlit as st
from configure import (
    process_file, generate_flashcards, export_deck, SUPPORTED_FORMATS,
    ABOUT_TEXT, CONTACT_DETAILS, SIDEBAR_FEATURES
)

st.set_page_config(page_title="AnkiGamify", layout="wide")

# Sidebar UI
st.sidebar.title("📚 AnkiGamify")
st.sidebar.markdown("### Features")
for feature in SIDEBAR_FEATURES:
    st.sidebar.markdown(f"- {feature}")
st.sidebar.markdown("---")
st.sidebar.markdown(CONTACT_DETAILS)

# Main UI
st.title("🧠 AnkiGamify - Flashcard Generator")
uploaded_file = st.file_uploader("Upload Study Material (PDF, DOCX, TXT, YouTube Link, etc.)", type=SUPPORTED_FORMATS)

if uploaded_file:
    with st.spinner("Processing your material..."):
        raw_text = process_file(uploaded_file)
    st.success("Material extracted successfully!")

    flashcard_type = st.selectbox("Choose Flashcard Type", ["Basic", "Cloze", "Memo Card", "Image Occlusion"])
    if st.button("✨ Generate Flashcards"):
        with st.spinner("Generating flashcards using AI..."):
            cards = generate_flashcards(raw_text, flashcard_type)
            st.session_state["cards"] = cards
        st.success(f"{len(cards)} cards generated!")

    if "cards" in st.session_state:
        st.subheader("📤 Export Your Deck")
        export_format = st.radio("Export Format", ["CSV", "APKG"])
        if st.button("Export Flashcards"):
            export_deck(st.session_state["cards"], export_format)

else:
    st.info("Upload a file or YouTube link to begin.")

st.markdown("---")
st.markdown(ABOUT_TEXT)