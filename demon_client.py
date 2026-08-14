import speech_recognition as sr
import requests
import time

# The URL of your WSL Server
WSL_SERVER_URL = "http://127.0.0.1:5000/process_audio"

def send_to_brain(text: str):
    """Sends transcribed or typed text to the WSL Brain."""
    print("[Windows Client]: Sending to DEMON Cell Brain (WSL)...")
    try:
        # Sends the text payload to the Flask server in WSL
        response = requests.post(WSL_SERVER_URL, json={"text": text})
        
        if response.status_code == 200:
            print(f"[DEMON Cell Response]: {response.json().get('reply')}")
        else:
            print(f"[Error]: Brain returned status code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[Client Error]: Could not connect to DEMON Cell Brain. Is main.py running in WSL?")
    except Exception as e:
        print(f"[Client Error]: {str(e)}")

def capture_voice() -> str:
    """Captures microphone input natively on Windows."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[Windows Senses]: Calibrating ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[Windows Senses]: Listening... (Speak now)")
        
        try:
            # Capture audio natively on Windows
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            
            print("[Windows Senses]: Transcribing audio locally...")
            # Using Google's free cloud STT for the client to keep it lightweight
            text = recognizer.recognize_google(audio_data)
            
            print(f"[Voice Input Detected]: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("[Windows Senses]: Listening timed out. No speech detected.")
            return ""
        except sr.UnknownValueError:
            print("[Windows Senses]: Could not understand audio.")
            return ""
        except Exception as e:
            print(f"[Audio Error]: {str(e)}")
            return ""

def main_sense_loop():
    """Main loop allowing choice between typing and speaking."""
    while True:
        print("\n" + "="*50)
        print("Type your command, or press [ENTER] to use the microphone.")
        
        # Await user choice
        choice = input("USER > ").strip()
        
        # Hard exit command for the client
        if choice.lower() in ["exit", "quit", "shutdown client"]:
            print("Shutting down Windows Senses. Goodbye.")
            break
            
        # If the user just pressed Enter, trigger the microphone
        if choice == "":
            text_to_send = capture_voice()
        # Otherwise, use the typed text
        else:
            text_to_send = choice
            
        # If we successfully captured text (either typed or spoken), send it
        if text_to_send:
            send_to_brain(text_to_send)

if __name__ == "__main__":
    print("==================================================")
    print(" DEMON CELL: Windows Sensory Client Online")
    print("==================================================")
    main_sense_loop()