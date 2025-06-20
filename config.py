import fitz  # PyMuPDF
import docx
import pytesseract
from PIL import Image
import tempfile
import csv
import genanki
import io

SUPPORTED_FORMATS = ['pdf', 'txt', 'docx', 'mp3', 'mp4', 'epub']

SIDEBAR_FEATURES = [
    "Multimodal Inputs",
    "AI Flashcard Engine",
    "Memo Cards with Explanation",
    "Image Occlusion Cards",
    "Export to CSV / Anki",
    "Smart Review Scheduler (Coming Soon)",
    "Offline + Cloud Ready"
]

CONTACT_DETAILS = """
**Contact Us:**
- [Instagram](https://www.instagram.com/dr.pavanreddy)
- 📧 Pavanreddy337@gmail.com
- [GitHub](https://github.com/Pavaas)
"""

ABOUT_TEXT = """
**About AnkiGamify**  
This is a next-gen AI-powered flashcard builder inspired by apps like Flashka.ai and Memo.cards.  
Your uploads are securely processed and exported as Anki decks.
"""

def process_file(uploaded_file):
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif ext == "txt":
        return uploaded_file.read().decode()
    elif ext == "docx":
        return extract_text_from_docx(uploaded_file)
    else:
        return "Unsupported or upcoming format."

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def generate_flashcards(text, card_type):
    lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 20]
    cards = []

    for i, line in enumerate(lines[:30]):
        if card_type == "Basic":
            cards.append({"front": line.split('.')[0], "back": line})
        elif card_type == "Cloze":
            parts = line.split(" ")
            if len(parts) > 6:
                cloze = f"{' '.join(parts[:2])} [...] {' '.join(parts[5:])}"
                cards.append({"front": cloze, "back": line})
        elif card_type == "Memo Card":
            cards.append({"front": f"Explain: {line[:50]}...", "back": f"{line}\n\n(Page estimated: {i+1})"})
        elif card_type == "Image Occlusion":
            cards.append({"front": f"Image Occlusion Placeholder {i+1}", "back": "Hidden answer image"})
    return cards

def export_deck(cards, export_format):
    if export_format == "CSV":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Front", "Back"])
        for card in cards:
            writer.writerow([card['front'], card['back']])
        st.download_button("Download CSV", output.getvalue(), "flashcards.csv", "text/csv")

    elif export_format == "APKG":
        model = genanki.Model(
            1607392319,
            'Simple Model',
            fields=[{"name": "Front"}, {"name": "Back"}],
            templates=[{
                "name": "Card 1",
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}<hr id='answer'>{{Back}}"
            }]
        )
        deck = genanki.Deck(2059400110, "AnkiGamify Deck")
        for card in cards:
            deck.add_note(genanki.Note(model=model, fields=[card['front'], card['back']]))

        package = genanki.Package(deck)
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            package.write_to_file(tmp_file.name)
            with open(tmp_file.name, "rb") as f:
                st.download_button("Download APKG", f.read(), "flashcards.apkg")