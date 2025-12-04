import React from "react";

export default function MoodIntensity({ intensity, setIntensity }) {
  return (
    <div>
      <label>Intensity: {intensity}</label>
      <input
        type="range"
        min="0"
        max="10"
        value={intensity}
        onChange={e => setIntensity(e.target.value)}
      />
    </div>
  );
}
