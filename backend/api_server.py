from flask import Flask, request, jsonify
from flask_cors import CORS
from groq_companion import IntelligentCompanion
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)

companion = IntelligentCompanion()
print("✅ Groq AI Companion initialized!")

@app.route('/api/track-mood', methods=['POST'])
def track_mood():
    """Track mood using Jac walker"""
    try:
        data = request.json
        mood = data.get('mood', 'happy')
        situation = data.get('situation', 'testing')
        
        # Run Jac walker with inputs
        cmd = [
            'jac', 'run', 'backend/main.jac',
            '-w', 'track_mood',
            '-i', f'input_mood={mood}',
            '-i', f'input_situation={situation}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return jsonify({
            "success": True,
            "mood": mood,
            "situation": situation,
            "message": "Mood tracked successfully!",
            "backend_output": result.stdout
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Check if API is running"""
    return jsonify({
        "status": "healthy",
        "message": "MindMate API is running! 🧠"
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "app": "MindMate Harmony Space",
        "status": "running",
        "endpoints": {
            "/api/health": "Health check",
            "/api/track-mood": "Track mood (POST)"
        }
    })

@app.route('/api/chat/send', methods=['POST'])
def chat_send():
    """Send message to AI companion - INSTANT response"""
    try:
        data = request.json
        message = data.get('message', '')
        conversation_id = data.get('conversation_id', 'default')
        
        # Get instant AI response
        result = companion.process_message(message)
        
        return jsonify({
            "success": True,
            "response": result['response'],
            "emotion": result['emotion'],
            "intensity": result['intensity'],
            "triggers": result['triggers'],
            "urgency": result['urgency'],
            "timestamp": result['timestamp']
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    """Get chat conversation history"""
    try:
        cmd = ['jac', 'run', 'backend/chat_companion.jac', '-w', 'get_chat_history']
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = json.loads(result.stdout) if result.stdout else {}
        
        return jsonify(output)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/chat/insights', methods=['GET'])
def chat_insights():
    """Get mood insights from chat history"""
    try:
        cmd = ['jac', 'run', 'backend/chat_companion.jac', '-w', 'get_mood_summary']
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = json.loads(result.stdout) if result.stdout else {}
        
        return jsonify(output)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 MindMate API Server Starting...")
    print("📍 Running on http://localhost:5000")
    print("🧠 Backend: Jaseci + JacLang")
    print("⚡ Ready for connections!")
    app.run(debug=True, host='0.0.0.0', port=5000)
