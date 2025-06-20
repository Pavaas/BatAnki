import streamlit as st
from configure import (
    process_file, generate_flashcards, export_deck,
    SUPPORTED_FORMATS, ABOUT_TEXT, CONTACT_DETAILS, SIDEBAR_FEATURES
)

# App Title
st.set_page_config(page_title="BatAnki - AI Flashcard Generator", layout="wide")
st.title("🦇 BatAnki - AI Flashcard Wizard")
st.caption("Upload. Generate. Master.")

# Sidebar navigation
st.sidebar.title("🧠 BatAnki Sidebar")
tab = st.sidebar.radio("Navigate", options=["📂 Upload", "🃏 Flashcards", "📤 Export", "📌 About", "📫 Contact Us", "🧪 Labs"])

for item in SIDEBAR_FEATURES:
    st.sidebar.markdown(f"- {item}")

# File upload tab
if tab == "📂 Upload":
    st.subheader("Upload Study Material")
    uploaded_file = st.file_uploader("Choose a file", type=SUPPORTED_FORMATS)

    if uploaded_file:
        with st.spinner("🔍 Processing file..."):
            content = process_file(uploaded_file)
        st.success("✅ File loaded successfully! Proceed to Flashcards tab.")

# Flashcard generation tab
elif tab == "🃏 Flashcards":
    st.subheader("AI-Generated Flashcards")
    if "content" not in st.session_state:
        st.warning("Please upload a file in the 'Upload' tab first.")
    else:
        with st.spinner("⚙️ Generating flashcards..."):
            flashcards = generate_flashcards(st.session_state.content)
        st.session_state.flashcards = flashcards
        for idx, card in enumerate(flashcards):
            st.markdown(f"**Q{idx+1}:** {card['question']}")
            with st.expander("Show Answer"):
                st.markdown(card['answer'])

# Export tab
elif tab == "📤 Export":
    st.subheader("Export Your Flashcards")
    if "flashcards" not in st.session_state:
        st.warning("Generate flashcards first.")
    else:
        export_format = st.selectbox("Choose format", ["CSV", "Anki (.apkg)"])
        if st.button("Export Now"):
            export_deck(st.session_state.flashcards, export_format)
            st.success(f"🎉 Exported flashcards as {export_format}")

# About tab
elif tab == "📌 About":
    st.subheader("About BatAnki")
    st.markdown(ABOUT_TEXT)

# Contact tab
elif tab == "📫 Contact Us":
    st.subheader("Contact Information")
    st.markdown(CONTACT_DETAILS)

# Labs tab
elif tab == "🧪 Labs":
    st.subheader("Experimental Features")
    st.info("New AI Teaching Assistant, Adaptive Scheduler, and Analytics Dashboard coming soon!")