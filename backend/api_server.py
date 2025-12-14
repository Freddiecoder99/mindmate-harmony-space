from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)

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

if __name__ == '__main__':
    print("🚀 MindMate API Server Starting...")
    print("📍 Running on http://localhost:5000")
    print("🧠 Backend: Jaseci + JacLang")
    print("⚡ Ready for connections!")
    app.run(debug=True, host='0.0.0.0', port=5000)
