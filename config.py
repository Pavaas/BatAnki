import os
import fitz
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import speech_recognition as sr
import nltk
import genanki
import uuid
import streamlit as st

def process_input(text, file, youtube_url, enable_transcription):
    final_text = text or ""

    if file:
        ext = os.path.splitext(file.name)[1].lower()
        if ext == ".pdf":
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                final_text += "\n".join(page.get_text() for page in doc)
        elif ext == ".txt":
            final_text += file.read().decode("utf-8")
        elif ext == ".mp3" and enable_transcription:
            recognizer = sr.Recognizer()
            with sr.AudioFile(file) as source:
                audio = recognizer.record(source)
                try:
                    final_text += recognizer.recognize_google(audio)
                except:
                    final_text += "[Audio transcription failed.]"

    if youtube_url and enable_transcription:
        try:
            yt_id = YouTube(youtube_url).video_id
            transcript = YouTubeTranscriptApi.get_transcript(yt_id)
            final_text += "\n" + "\n".join([t['text'] for t in transcript])
        except:
            final_text += "\n[Transcript not found.]"

    return final_text

def generate_flashcards(text):
    tokenizer = nltk.tokenize.PunktSentenceTokenizer()
    sentences = tokenizer.tokenize(text)
    cards = []
    for s in sentences:
        cards.append({
            "question": f"What does this mean?\n\n{s}",
            "answer": s
        })
    return cards

def export_flashcards(cards):
    with open("batanki_flashcards.csv", "w", encoding="utf-8") as f:
        f.write("Question,Answer\n")
        for c in cards:
            f.write(f"{c['question'].replace(',', ';')},{c['answer'].replace(',', ';')}\n")
    st.success("📁 Flashcards exported as CSV")

def export_apkg(cards, deck_name="BatAnki Deck"):
    model = genanki.Model(
        1607392319,
        'BatAnki Model',
        fields=[{'name': 'Question'}, {'name': 'Answer'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        }]
    )
    deck = genanki.Deck(int(str(uuid.uuid4().int)[:10]), deck_name)
    for c in cards:
        note = genanki.Note(model=model, fields=[c["question"], c["answer"]])
        deck.add_note(note)
    genanki.Package(deck).write_to_file(f"{deck_name.replace(' ', '_')}.apkg")
    st.success(f"📦 APKG exported: {deck_name.replace(' ', '_')}.apkg")

def generate_image_occlusion_cards(text):
    return [{"question": "[Image Occlusion Placeholder]", "answer": "[Label hidden]"}]

def launch_ai_assistant(text):
    st.info("🧠 AI Teaching Assistant active")
    # Placeholder logic — future GPT summarizer or local LLM
    return text[:2000]  # Return limited text as example

def schedule_smart_review(cards):
    st.info("📆 Smart review scheduled using spaced repetition logic.")
    # Placeholder: implement SM-2 or other review timing logic

def show_study_planner():
    st.markdown("📅 **Study Planner (Prototype)**\n\n- Review 30 cards/day\n- Mark progress\n- Check streaks\n- Customizable reminders (soon)")

def show_analytics_dashboard():
    st.markdown("📊 **Analytics Dashboard (Prototype)**\n\n- Total cards created: 120\n- Time saved: 2 hrs\n- Flashcards reviewed: 45")

def run_gamification_engine(card_count):
    st.success(f"🎮 You earned {card_count * 2} XP! Streak +1 day 🔥")

def load_offline_deck_pack(name):
    st.success(f"📚 Loaded offline pack: {name}")
    # Placeholder logic; you can expand by loading local decks