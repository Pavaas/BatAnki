import nltk
nltk.download("punkt")

import streamlit as st
from config import (
    process_input,
    generate_flashcards,
    export_flashcards,
    export_apkg,
    generate_image_occlusion_cards,
    launch_ai_assistant,
    schedule_smart_review,
    show_study_planner,
    show_analytics_dashboard,
    load_offline_deck_pack,
    run_gamification_engine
)

st.set_page_config(page_title="🦇 BatAnki", layout="wide")
st.title("🦇 BatAnki – AI Flashcard Wizard")

st.sidebar.header("🛠 Feature Toggles")
enable_ai = st.sidebar.checkbox("💡 Enable AI Teaching Assistant", value=True)
enable_occlusion = st.sidebar.checkbox("🖼️ Image Occlusion Cards", value=True)
enable_transcription = st.sidebar.checkbox("🎙️ MP3 & YouTube Transcription", value=True)
enable_scheduler = st.sidebar.checkbox("⏱️ Smart Review Scheduler", value=True)
enable_gamify = st.sidebar.checkbox("🎮 Gamification Engine", value=True)
theme_mode = st.sidebar.radio("🎨 Theme Mode", ["Light", "Dark"])

if theme_mode == "Dark":
    st.markdown("""<style>body { background-color: #1e1e2f; color: white; }</style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>body { background-color: #ffffff; color: black; }</style>""", unsafe_allow_html=True)

st.sidebar.markdown("## 🔮 Labs & Analytics")
if st.sidebar.button("📆 Open Study Planner"):
    show_study_planner()

if st.sidebar.button("📊 Open Analytics Dashboard"):
    show_analytics_dashboard()

st.sidebar.markdown("## 🧪 Load Offline Deck Pack")
offline_pack = st.sidebar.selectbox("Deck Pack", ["None", "Pharmacology", "Anatomy", "Forensic"])
if offline_pack != "None":
    load_offline_deck_pack(offline_pack)

st.markdown("### 📥 Input Zone")
text_input = st.text_area("Paste text or notes:", height=200)
file_input = st.file_uploader("Upload PDF, TXT, or MP3", type=["pdf", "txt", "mp3"])
youtube_url = st.text_input("📺 YouTube Link")

if st.button("✨ Generate Flashcards"):
    with st.spinner("Working on your content..."):
        content = process_input(text_input, file_input, youtube_url, enable_transcription)

        if enable_ai:
            content = launch_ai_assistant(content)

        cards = generate_flashcards(content)

        if enable_occlusion:
            cards += generate_image_occlusion_cards(content)

        if enable_scheduler:
            schedule_smart_review(cards)

        if enable_gamify:
            run_gamification_engine(len(cards))

        st.success(f"✅ {len(cards)} flashcards generated!")

        for i, card in enumerate(cards[:10]):
            st.markdown(f"**Q{i+1}:** {card['question']}")
            st.markdown(f"**A{i+1}:** {card['answer']}")
            st.markdown("---")

        export_flashcards(cards)
        export_apkg(cards)