import os

# ==========================================
# DEMON CELL: SYSTEM CONFIGURATION
# ==========================================

# 1. Brain (LLM) Settings
# Ensure you have set this in your WSL terminal: export NVIDIA_API_KEY="your-key"
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY") 
NVIDIA_API_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Updated to match your chosen model
NEMOTRON_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"

# 2. STT (Speech-to-Text) Settings
# Options: 'tiny', 'base', 'small', 'medium', 'large-v3'
WHISPER_MODEL_SIZE = "base"
WHISPER_COMPUTE_TYPE = "int8"
WHISPER_DEVICE = "cpu"
# Audio limits in seconds
STT_TIMEOUT = 5
STT_PHRASE_TIME_LIMIT = 15

# 3. TTS (Text-to-Speech) Settings
# Options: 'en-US-ChristopherNeural', 'en-GB-RyanNeural', 'en-US-AriaNeural'
TTS_VOICE_MODEL = "en-US-ChristopherNeural"
TTS_OUTPUT_FILE = "demon_response.mp3"

# 4. Wake Word Settings (For future implementation with pvporcupine)
WAKE_WORD = "demon"