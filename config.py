# config.py

# General configuration for BatAnki
DEBUG = True
PAGE_TITLE = "🦇 BatAnki: AI Flashcards Beta"
PAGE_LAYOUT = "wide"

# Input / processing parameters
MAX_TEXT_LENGTH = 5000       # Maximum number of characters to process
SUMMARY_LENGTH = 200         # Characters to use for generating a dummy summary

# Export formats supported (for documentation)
EXPORT_FORMATS = ["csv", "json", "apkg"]

# Paths (if needed later for assets or logs)
ASSETS_PATH = "assets/"
LOGS_PATH = "logs/"

# Beta features toggle
ENABLE_BETA_FEATURES = True