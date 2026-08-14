import time
from flask import Flask, request, jsonify
from core.brain import run_agent_step
from core.tts import speak

app = Flask(__name__)

def initialize_demon_cell():
    """Boot sequence for the DEMON Cell architecture."""
    print("==================================================")
    print(" DEMON CELL: Brain Server Online (WSL)")
    print("==================================================")
    startup_message = "DEMON Cell Brain initialized. Awaiting sensory input from Windows client."
    speak(startup_message)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """Endpoint to receive text from the Windows client."""
    data = request.json
    user_input = data.get("text", "")
    
    if not user_input:
        return jsonify({"reply": "No input received."}), 400
        
    print(f"\n[DEMON Cell Brain]: Received input: '{user_input}'")
    
    # Process through Nemotron Brain (which handles Tool Execution)
    response_text = run_agent_step(user_input)
    
    # Speak the result (WSL handles audio out just fine)
    if response_text:
        speak(response_text)
        
    return jsonify({"reply": response_text}), 200

if __name__ == "__main__":
    initialize_demon_cell()
    # Run the server on port 5000, accessible to the Windows host
    app.run(host='0.0.0.0', port=5000)