import React from "react";

export default function MoodSelector({ emotion, setEmotion }) {
  return (
    <div>
      <label>Emotion: </label>
      <select value={emotion} onChange={e => setEmotion(e.target.value)}>
        <option value="happy">Happy</option>
        <option value="neutral">Neutral</option>
        <option value="sad">Sad</option>
        <option value="anxious">Anxious</option>
        <option value="angry">Angry</option>
      </select>
    </div>
  );
}
