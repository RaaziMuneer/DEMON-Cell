import os
import speech_recognition as sr
from faster_whisper import WhisperModel

# Initialize the model (using 'base' or 'small' for Data Efficiency)
# compute_type="int8" reduces memory usage for CPU/standard GPU execution
MODEL_SIZE = "base"
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

def listen_and_transcribe() -> str:
    """Listens to the microphone and transcribes speech to text."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("[DEMON Cell STT]: Calibrating ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[DEMON Cell STT]: Listening...")
        
        try:
            # Capture the audio data
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            
            # Save temporarily as a WAV file for faster-whisper to process
            temp_file = "temp_audio.wav"
            with open(temp_file, "wb") as f:
                f.write(audio_data.get_wav_data())
                
            print("[DEMON Cell STT]: Processing audio...")
            
            # Transcribe the audio
            segments, info = model.transcribe(temp_file, beam_size=5)
            transcription = "".join([segment.text for segment in segments])
            
            # Cleanup temporary file
            os.remove(temp_file)
            
            print(f"[User Input]: {transcription.strip()}")
            return transcription.strip()
            
        except sr.WaitTimeoutError:
            print("[DEMON Cell STT]: Listening timed out. No speech detected.")
            return ""
        except Exception as e:
            print(f"[DEMON Cell STT Error]: {str(e)}")
            return ""

if __name__ == "__main__":
    # Standalone test execution
    result = listen_and_transcribe()