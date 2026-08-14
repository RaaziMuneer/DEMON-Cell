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
* **`requests`**: Sends the transcribed text payloads to the WSL server[cite: 338].

### 2. The Brain (WSL Linux Server)
[cite_start]Runs the core LLM logic, executes system tools, and generates Text-to-Speech (TTS)[cite: 223, 400].
* [cite_start]**`flask`**: Creates the lightweight web server listening for client inputs[cite: 237].
* [cite_start]**`openai`**: The standard SDK used to connect to the NVIDIA Nemotron API[cite: 42, 43].
* [cite_start]**`edge-tts`**: Generates high-quality, natural-sounding voice output[cite: 61].
* [cite_start]**`ffmpeg`** *(System Package)*: Required by Linux to process and play the audio files back through the Windows audio pass-through[cite: 62, 70].

---

## ⚙️ Installation & Setup

Because this project spans two environments, you must set up both the Windows Host and the WSL environment separately.

### Part 1: Windows Client Setup ("The Senses")
**Important:** You must use **Python 3.12 (Stable)** on Windows. [cite_start]Experimental versions (like 3.14) will fail to build the C++ PortAudio headers required by PyAudio[cite: 350, 352, 355].

1. [cite_start]Open a standard Windows Command Prompt or PowerShell[cite: 358].
2. Install the required libraries by targeting Python 3.12:
   ```cmd
   py -3.12 -m pip install SpeechRecognition requests PyAudio
