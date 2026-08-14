# DEMON Cell 
(Data Efficient Machine Operated Neuron Cell)

DEMON Cell is a highly optimized, data-efficient Agentic AI voice assistant. It utilizes a Client-Server architecture to bridge native Windows audio hardware with a WSL-based Linux reasoning engine. 

The system leverages NVIDIA Nemotron models for agentic reasoning and PowerShell interop to autonomously control the Windows host environment.

---

## 🏗️ Architecture & Libraries Used

The system is split into two halves to bypass WSL audio limitations and maintain zero-cost efficiency:

### 1. The Senses (Windows Client)
Runs natively on the Windows host to capture microphone audio and transmit it to the brain.
* **`SpeechRecognition`**: Captures voice and handles Speech-to-Text (STT) locally via Google's free tier.
* **`PyAudio`**: Required by `SpeechRecognition` to interface with physical microphone hardware.
* **`requests`**: Sends the transcribed text payloads to the WSL server.

### 2. The Brain (WSL Linux Server)
Runs the core LLM logic, executes system tools, and generates Text-to-Speech (TTS).
* **`flask`**: Creates the lightweight web server listening for client inputs.
* **`openai`**: The standard SDK used to connect to the NVIDIA Nemotron API.
* **`edge-tts`**: Generates high-quality, natural-sounding voice output.
* **`ffmpeg`** *(System Package)*: Required by Linux to process and play the audio files back through the Windows audio pass-through.

---

## ⚙️ Installation & Setup

Because this project spans two environments, you must set up both the Windows Host and the WSL environment separately.


### Part 1: Windows Client Setup ("The Senses")
**Important:** You must use **Python 3.12 (Stable)** on Windows. Experimental versions (like 3.14) will fail to build the C++ PortAudio headers required by PyAudio.

1. Open a standard Windows Command Prompt or PowerShell.
2. Install the required libraries by targeting Python 3.12:
   ```cmd
   py -3.12 -m pip install SpeechRecognition requests PyAudio
**Ensure you have set this in your WSL terminal: export NVIDIA_API_KEY="your-key"**

**suggestion: Open demon_client.py in cmd while wsl is being used for running main.py**
