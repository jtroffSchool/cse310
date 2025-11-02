import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import RecommendationIntro from "./pages/RecommendationIntro.tsx";
import RecommendationQuiz from "./pages/RecommendationQuiz.tsx";
import AdventureQuiz from "./pages/AdventureQuiz.tsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RecommendationIntro />} />
        <Route path="/recommend" element={<RecommendationQuiz />} />
        <Route path="/adventure" element={<AdventureQuiz />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
