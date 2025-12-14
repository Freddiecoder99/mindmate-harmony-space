import { useState } from 'react';
import '../App.css';

const API_URL = 'http://localhost:5000/api';

function MindMateApp() {
  const [emotion, setEmotion] = useState('Neutral');
  const [intensity, setIntensity] = useState(5);
  const [triggers, setTriggers] = useState('');
  const [moods, setMoods] = useState([]);
  const [message, setMessage] = useState('');

  const emotions = ['Happy', 'Sad', 'Anxious', 'Calm', 'Energetic', 'Overwhelmed', 'Neutral'];

  const logMood = async () => {
    try {
      setMessage('Tracking your mood...');
      
      const response = await fetch(`${API_URL}/track-mood`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mood: emotion,
          situation: triggers || 'No specific triggers mentioned',
          intensity: intensity
        })
      });

      const data = await response.json();
      
      if (data.success) {
        setMessage('✅ Mood tracked successfully!');
        setMoods([...moods, { emotion, intensity, triggers, timestamp: new Date().toLocaleString() }]);
        
        setTimeout(() => {
          setMessage('');
          setTriggers('');
        }, 2000);
      } else {
        setMessage('❌ Error tracking mood');
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('❌ Could not connect to backend. Make sure API server is running!');
    }
  };

  const clearLogs = () => {
    setMoods([]);
    setMessage('🗑️ Logs cleared');
    setTimeout(() => setMessage(''), 2000);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🧠 MindMate Harmony Space</h1>
        <p className="subtitle">Your AI-Powered Emotional Wellness Companion</p>
      </header>

      <div className="main-content">
        <div className="mood-tracker-card">
          <h2>✨ How are you feeling?</h2>
          
          <div className="form-group">
            <label>Emotion:</label>
            <select 
              value={emotion} 
              onChange={(e) => setEmotion(e.target.value)}
              className="emotion-select"
            >
              {emotions.map(em => (
                <option key={em} value={em}>{em}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Intensity: {intensity}</label>
            <input 
              type="range" 
              min="1" 
              max="10" 
              value={intensity}
              onChange={(e) => setIntensity(e.target.value)}
              className="intensity-slider"
            />
            <div className="intensity-labels">
              <span>Low</span>
              <span>High</span>
            </div>
          </div>

          <div className="form-group">
            <label>Triggers (comma separated):</label>
            <input 
              type="text"
              placeholder="e.g., work, traffic, argument"
              value={triggers}
              onChange={(e) => setTriggers(e.target.value)}
              className="triggers-input"
            />
          </div>

          <div className="button-group">
            <button onClick={logMood} className="btn btn-primary">
              💾 Log Mood
            </button>
            <button onClick={clearLogs} className="btn btn-secondary">
              🗑️ Clear Logs
            </button>
          </div>

          {message && (
            <div className={`message ${message.includes('❌') ? 'error' : 'success'}`}>
              {message}
            </div>
          )}
        </div>

        <div className="mood-history-card">
          <h2>📊 Logged Moods</h2>
          {moods.length === 0 ? (
            <p className="empty-state">No moods logged yet. Start tracking your emotional journey!</p>
          ) : (
            <div className="mood-list">
              {moods.map((mood, index) => (
                <div key={index} className="mood-item">
                  <div className="mood-emotion">{mood.emotion}</div>
                  <div className="mood-details">
                    <span>Intensity: {mood.intensity}/10</span>
                    {mood.triggers && <span>Triggers: {mood.triggers}</span>}
                    <span className="mood-time">{mood.timestamp}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="stats-card">
          <h2>📈 Current Streak</h2>
          <div className="stat-value">{moods.length}</div>
          <p>moods logged in this session</p>
          <p style={{marginTop: '15px', fontSize: '0.9rem', color: '#666'}}>
            Keep tracking your emotional wellness journey! 🌱
          </p>
        </div>
      </div>

      <footer className="app-footer">
        <p>⚠️ MindMate is a wellness tool, not a replacement for professional mental health care.</p>
        <p>Powered by Jaseci + JacLang | OSP Graph + byLLM AI</p>
      </footer>
    </div>
  );
}

export default MindMateApp;
