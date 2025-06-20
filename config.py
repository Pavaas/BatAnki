import fitz, docx2txt
from ebooklib import epub
import tempfile
import streamlit as st
from pathlib import Path
import pandas as pd
import random

# 1. INPUT LOADER
def load_and_process_input(file, text):
    data = ""
    if file:
        ext = Path(file.name).suffix.lower()
        if ext == ".pdf":
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                data = "\n".join(page.get_text() for page in doc)
        elif ext == ".docx":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(file.read())
                data = docx2txt.process(tmp.name)
        elif ext == ".epub":
            book = epub.read_epub(file)
            data = "\n".join([item.get_content().decode() for item in book.get_items() if item.get_type() == 9])
        elif ext == ".txt":
            data = file.read().decode("utf-8")
        elif ext == ".mp3":
            data = "🎤 Audio transcription coming soon"
    elif text:
        data = text

    if data:
        st.session_state["content"] = data
        st.success("✅ Material processed!")

# 2. FLASHCARDS
def generate_flashcards():
    if "content" not in st.session_state:
        st.warning("Please upload or input some text first.")
        return []
    lines = st.session_state["content"].split("\n")
    flashcards = []
    for line in lines:
        if len(line.strip()) > 30:
            flashcards.append({
                "question": f"What is: {line.strip()[:60]}?",
                "answer": line.strip()
            })
    st.session_state["flashcards"] = flashcards
    return flashcards

def flashcard_viewer(cards):
    st.subheader("🧠 Preview Flashcards")
    for i, card in enumerate(cards[:20]):
        with st.expander(f"Flashcard {i+1}"):
            st.markdown(f"**Q:** {card['question']}")
            st.markdown(f"**A:** {card['answer']}")

def export_flashcards(cards):
    if st.button("⬇️ Export Flashcards"):
        df = pd.DataFrame(cards)
        st.download_button("Download CSV", df.to_csv(index=False), "flashcards.csv")

# 3. MCQ GENERATOR
def generate_mcqs():
    if "content" not in st.session_state:
        st.warning("Please upload content first.")
        return
    st.subheader("📝 MCQs")
    for i in range(5):
        q = f"Q{i+1}. What is the role of XYZ?"
        options = ["A", "B", "C", "D"]
        correct = random.choice(options)
        ans = st.radio(q, options, key=f"mcq{i}")
        if st.button(f"Submit {i+1}"):
            if ans == correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Wrong! Answer is {correct}")

# 4. AI ASSISTANT
def ai_assistant_reply():
    query = st.text_input("Ask your study assistant")
    if query and "content" in st.session_state:
        st.success(f"🧠 Answer: This is a simulated AI reply to: {query}")
    elif query:
        st.warning("Please upload content first.")

# 5. PLANNER
def show_planner():
    st.subheader("📅 Your Study Planner")
    goal = st.text_input("📘 Today's Goal")
    duration = st.slider("⏱️ Study Duration (mins)", 0, 240, 60)
    st.checkbox("✅ Mark Done")

# 6. ANALYTICS
def show_analytics():
    if "flashcards" in st.session_state:
        total = len(st.session_state["flashcards"])
        st.metric("🧠 Flashcards Made", total)
        st.progress(min(1.0, total/100))

# 7. THEME SWITCH
def switch_theme():
    theme = st.sidebar.selectbox("🌓 Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""<style>body { background-color: #111; color: white; }</style>""", unsafe_allow_html=True)

# 8. FUTURE LABS
def future_lab_features():
    st.markdown("""
    ### 🧪 Future Lab Features
    - 📽️ YouTube to Flashcards
    - 🎨 Image Occlusion Cards
    - 🎤 Voice to Flashcard
    - 📈 Adaptive Review Engine
    - ☁️ Cloud Sync + AI Analytics
    """)