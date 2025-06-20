import os
import io
import re
import fitz  # PyMuPDF
import docx
import nltk
import tempfile
import speech_recognition as sr
from pathlib import Path
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
from transformers import pipeline
from pydub import AudioSegment

# Ensure nltk punkt is downloaded
nltk.download("punkt", quiet=True)

# Load summarizer
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    SUMMARIZER_AVAILABLE = True
except Exception:
    summarizer = None
    SUMMARIZER_AVAILABLE = False

# -------------------------------
# 📥 INPUT FILE HANDLERS
# -------------------------------

def handle_file_upload(uploaded_file, user_text):
    if uploaded_file:
        suffix = Path(uploaded_file.name).suffix.lower()
        if suffix == ".pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif suffix == ".txt":
            text = uploaded_file.read().decode("utf-8")
        elif suffix in [".mp3", ".wav", ".m4a"]:
            text = transcribe_audio(uploaded_file)
        elif suffix in [".doc", ".docx"]:
            text = extract_text_from_docx(uploaded_file)
        elif suffix in [".epub"]:
            text = extract_text_from_epub(uploaded_file)
        else:
            text = "Unsupported file type."
    elif user_text:
        text = user_text
    else:
        text = ""
    return text

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_epub(file):
    return "EPUB support coming soon..."

def transcribe_audio(file):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        # Convert mp3/m4a to wav
        sound = AudioSegment.from_file(file)
        sound.export(temp_audio.name, format="wav")
        with sr.AudioFile(temp_audio.name) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not transcribe audio."
        finally:
            os.remove(temp_audio.name)

def fetch_youtube_transcript(url):
    try:
        video_id = YouTube(url).video_id
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([line['text'] for line in transcript])
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

# -------------------------------
# 🧠 CHUNKING + SUMMARIZATION
# -------------------------------

def extract_flashcard_chunks(text, max_sentences=4):
    sentences = sent_tokenize(text)
    chunks = []
    current = []
    for sent in sentences:
        current.append(sent)
        if len(current) >= max_sentences:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks

def summarize_text(text):
    if summarizer and SUMMARIZER_AVAILABLE:
        try:
            return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
        except Exception:
            return text[:200] + "..."
    return text[:300] + "..."

# -------------------------------
# 🧠 FLASHCARD GENERATORS
# -------------------------------

def generate_flashcards(chunks, card_type="basic"):
    flashcards = []
    for chunk in chunks:
        question, answer = "", ""
        if card_type == "basic":
            question = f"What is the key concept in:\n\n{chunk}"
            answer = summarize_text(chunk)
        elif card_type == "cloze":
            answer = summarize_text(chunk)
            question = chunk.replace(answer.split(" ")[0], "_____", 1)
        elif card_type == "memo":
            question = "Explain this concept:"
            answer = summarize_text(chunk) + f"\n\n(Page reference simulated)"
        elif card_type == "mcq":
            answer = summarize_text(chunk)
            question = f"Which of the following best summarizes:\n\n{chunk}\n\nA) Random\nB) {answer}\nC) Irrelevant\nD) Incorrect"
        else:
            question = chunk
            answer = summarize_text(chunk)

        flashcards.append({"question": question, "answer": answer})
    return flashcards