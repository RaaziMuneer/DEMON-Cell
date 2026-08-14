import asyncio
import os
import subprocess
import edge_tts

# Select a voice. 'en-US-ChristopherNeural' or 'en-GB-RyanNeural' offer good AI/Controller tones.
VOICE_MODEL = "en-US-ChristopherNeural"
OUTPUT_FILE = "response.mp3"

async def generate_audio(text: str):
    """Generates the audio file using edge-tts."""
    communicate = edge_tts.Communicate(text, VOICE_MODEL)
    await communicate.save(OUTPUT_FILE)

def speak(text: str):
    """Synchronous wrapper to speak text out loud."""
    if not text:
        return
        
    print(f"[DEMON Cell TTS]: {text}")
    
    # Generate the audio file asynchronously
    asyncio.run(generate_audio(text))
    
    # Play the audio file using ffplay (available via ffmpeg in WSL)
    # -nodisp disables the video window, -autoexit closes it after playing
    try:
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", OUTPUT_FILE],
            check=True
        )
    except Exception as e:
        print(f"[DEMON Cell TTS Error]: Audio playback failed. Check WSL audio pass-through. {str(e)}")
    finally:
        # Cleanup audio file after playing
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

if __name__ == "__main__":
    # Standalone test execution
    speak("DEMON Cell initialized. All systems are operating at optimal capacity.")