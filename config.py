import fitz  # PyMuPDF
import os
import tempfile
import streamlit as st
import nltk
import genanki
import csv
from pathlib import Path
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

# Handle file upload or raw text
def handle_file_upload(uploaded_file, text_input):
    if uploaded_file:
        suffix = Path(uploaded_file.name).suffix.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name
        if suffix == ".pdf":
            return extract_text_from_pdf(file_path)
        elif suffix in [".txt", ".docx"]:
            return Path(file_path).read_text()
        else:
            return "Unsupported file type."
    elif text_input:
        return text_input
    else:
        return ""

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

# Chunk into digestible flashcard units
def extract_flashcard_chunks(text, max_sentences=3):
    sentences = sent_tokenize(text)
    chunks = []
    buffer = []
    for sent in sentences:
        buffer.append(sent)
        if len(buffer) >= max_sentences:
            chunks.append(" ".join(buffer))
            buffer = []
    if buffer:
        chunks.append(" ".join(buffer))
    return chunks

# Generate different types of flashcards
def generate_anki_cards(chunks, card_type="Basic"):
    cards = []
    for chunk in chunks:
        front, back = "", ""
        if card_type == "Cloze":
            front = chunk.replace(" is ", " {{c1::is}} ", 1)
            back = chunk
        elif card_type == "Memo":
            front = f"What does the following mean?\n\n{chunk[:100]}"
            back = chunk + " (with explanation and page reference)"
        elif card_type == "Reverse":
            front = chunk.split(".")[0]
            back = chunk
        elif card_type == "MCQ":
            front = f"Q: {chunk.split('.')[0]}\n(a) Option A\n(b) Option B\n(c) Option C\n(d) Option D"
            back = "Correct Answer: (b) Option B"
        else:
            front = chunk.split(".")[0]
            back = chunk
        cards.append({"Front": front, "Back": back})
    return cards

# Preview generated cards
def show_flashcards(cards):
    st.subheader("🧠 Flashcard Preview")
    for i, card in enumerate(cards[:20]):
        st.markdown(f"**Q{i+1}:** {card['Front']}")
        st.markdown(f"**A{i+1}:** {card['Back']}")
        st.markdown("---")

# Export to Anki format
def export_apkg(cards, deck_name="BatAnkiDeck"):
    model = genanki.Model(
        1607392319,
        'BatAnki Model',
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[{
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": "{{Front}}<hr id='answer'>{{Back}}"
        }]
    )
    deck = genanki.Deck(2059400110, deck_name)
    for card in cards:
        note = genanki.Note(model=model, fields=[card["Front"], card["Back"]])
        deck.add_note(note)

    file_name = f"{deck_name.replace(' ', '_')}.apkg"
    genanki.Package(deck).write_to_file(file_name)
    with open(file_name, "rb") as f:
        st.download_button("📥 Download Anki Package (.apkg)", f, file_name, mime="application/octet-stream")
    os.remove(file_name)

# Export to CSV
def export_csv(cards, deck_name="BatAnkiDeck"):
    file_name = f"{deck_name.replace(' ', '_')}.csv"
    with open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Front", "Back"])
        for card in cards:
            writer.writerow([card["Front"], card["Back"]])
    with open(file_name, "rb") as f:
        st.download_button("📥 Download CSV", f, file_name, mime="text/csv")
    os.remove(file_name)