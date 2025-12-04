import React, { useState } from "react";
import MoodSelector from "./MoodSelector.jsx";
import MoodIntensity from "./MoodIntensity.jsx";
import MoodLogButton from "./MoodLogButton.jsx";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';

export default function MindMateApp() {
  const [emotion, setEmotion] = useState("neutral");
  const [intensity, setIntensity] = useState(5);
  const [triggers, setTriggers] = useState("");
  const [logs, setLogs] = useState([]);

  // Log mood
  const handleLogMood = () => {
    const newLog = { emotion, intensity, triggers };
    setLogs([newLog, ...logs]);
    setTriggers(""); // reset triggers
  };

  // Clear all logs
  const handleClearLogs = () => setLogs([]);

  // Prepare chart data
  const emotionCounts = logs.reduce((acc, log) => {
    acc[log.emotion] = (acc[log.emotion] || 0) + 1;
    return acc;
  }, {});

  const chartData = Object.keys(emotionCounts).map(key => ({
    emotion: key,
    count: emotionCounts[key]
  }));

  // Emotion color helper
  const getEmotionColor = (emotion) => {
    switch(emotion) {
      case "happy": return "#ffe066";
      case "neutral": return "#a0a0a0";
      case "sad": return "#6c5ce7";
      case "anxious": return "#74b9ff";
      case "angry": return "#ff6b6b";
      default: return "#a0a0a0";
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", backgroundColor: "#f0f4f8", minHeight: "100vh" }}>
      <h1 style={{ color: "#4a90e2" }}>MindMate Prototype</h1>

      <div className="card" style={{ marginBottom: "15px", padding: "20px", borderRadius: "15px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)", backgroundColor: "#ffffff" }}>
        <MoodSelector emotion={emotion} setEmotion={setEmotion} />
      </div>

      <div className="card" style={{ marginBottom: "15px", padding: "20px", borderRadius: "15px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)", backgroundColor: "#ffffff" }}>
        <MoodIntensity intensity={intensity} setIntensity={setIntensity} />
      </div>

      <div className="card" style={{ marginBottom: "15px", padding: "20px", borderRadius: "15px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)", backgroundColor: "#ffffff" }}>
        <label>Triggers (comma separated): </label>
        <input
          type="text"
          value={triggers}
          onChange={e => setTriggers(e.target.value)}
          placeholder="e.g., work, traffic, argument"
          style={{ width: "100%", padding: "8px", borderRadius: "8px", border: "1px solid #ccc", marginTop: "5px" }}
        />
      </div>

      <div className="card" style={{ marginBottom: "15px", padding: "20px", borderRadius: "15px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)", backgroundColor: "#ffffff", display: "flex", gap: "10px" }}>
        <MoodLogButton onClick={handleLogMood} />
        <button onClick={handleClearLogs} style={{ backgroundColor: "#4a90e2", color: "white", border: "none", padding: "10px 15px", borderRadius: "8px", cursor: "pointer" }}>Clear Logs</button>
      </div>

      <div className="card" style={{ marginBottom: "15px", padding: "20px", borderRadius: "15px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)", backgroundColor: "#ffffff" }}>
        <h2>Logged Moods</h2>
        {logs.length === 0 ? <p>No moods logged yet.</p> :
          <ul>
            {logs.map((log, index) => (
              <li key={index} style={{ color: getEmotionColor(log.emotion) }}>
                Emotion: <strong>{log.emotion}</strong>, Intensity: <strong>{log.intensity}</strong>, Triggers: <strong>{log.triggers || "None"}</strong>
              </li>
            ))}
          </ul>
        }
      </div>

      <div className="card" style={{ marginBottom: "15px", padding: "20px", borderRadius: "15px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)", backgroundColor: "#ffffff" }}>
        <h2>Mood Chart</h2>
        {logs.length === 0 ? <p>No moods logged yet.</p> :
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="emotion" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#4a90e2" />
            </BarChart>
          </ResponsiveContainer>
        }
      </div>

      <div className="card" style={{ padding: "20px", borderRadius: "15px", boxShadow: "0 4px 12px rgba(0,0,0,0.08)", backgroundColor: "#ffffff" }}>
        <h2>Current Streak</h2>
        <p>{logs.length} moods logged in a row</p>
      </div>
    </div>
  );
}
