import React from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

import MindMateApp from "./components/MindMateApp.jsx";

createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <MindMateApp />
  </React.StrictMode>
);
