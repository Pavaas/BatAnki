# BatAnki

BatAnki is a next‑gen AI flashcard web app that generates dynamic flashcards from multimodal inputs. Combining AnKing‑quality cards with UWorld‑style MCQs and adaptive review, BatAnki is designed to streamline learning through intelligent summarization, varied flashcard types, and immersive beta features—all in one unified platform.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

BatAnki transforms a wide range of inputs—such as PDFs, text documents, images, and audio—into high-quality flashcards. The app extracts and cleans input data, generates summaries, and produces different types of flashcards including Basic, MCQ, Cloze, and advanced beta types like Reverse, Memo, and Image Occlusion. The intuitive UI (built using Streamlit) and planned advanced features (adaptive learning, gamification, smart scheduling, etc.) make BatAnki a powerful tool for both casual learners and professionals.

---

## Features

- **Multimodal Input**
  - Supports PDF, TXT, DOCX, EPUB, images (with optional OCR), and audio (with speech-to-text).
- **Text Extraction & Preprocessing**
  - PDF extraction using PyMuPDF and optional OCR via pytesseract.
  - Audio transcription using SpeechRecognition.
- **Flashcard Generation**
  - Core types: Basic, MCQ, and Cloze cards.
  - **Beta Features**: Advanced card types like Reverse, Memo, and Image Occlusion.
- **Export Options**
  - Download flashcards as CSV and JSON files.
- **Future Enhancements**
  - Adaptive Learning & Gamification (XP, streaks, badges)
  - Smart Review Scheduler (SM‑2 algorithm)
  - Direct AnkiConnect Integration for seamless sync to Anki
  - Comprehensive Analytics Dashboard
  - Enhanced voice input & text-to-speech (TTS)
  - Marketplace & Deck Hub for community sharing

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **PDF Extraction**: PyMuPDF
- **OCR** (optional): pytesseract, Pillow
- **Speech Recognition** (optional): SpeechRecognition
- **Data Handling**: NumPy, Pandas

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Pavaas/BatAnki.git
   cd BatAnki
