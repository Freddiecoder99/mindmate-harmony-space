import React from "react";

export default function MoodLogButton({ emotion, intensity }) {
  return (
    <button onClick={() => alert(`Emotion: ${emotion}, Intensity: ${intensity}`)}>
      Log Mood
    </button>
  );
}
