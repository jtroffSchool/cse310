import React, { useState } from "react";
import { games } from "../data/games";

interface QuestionProps {
  title: string;
  options: string[];
  onSelect: (value: string) => void;
  step: number;
  totalSteps: number;
  progressColor: string;
}

const Question: React.FC<QuestionProps> = ({
  title,
  options,
  onSelect,
  step,
  totalSteps,
  progressColor,
}) => {
  const progress = (step / totalSteps) * 100;

  return (
    <div className="text-center space-y-6 w-full max-w-2xl">
      {/* Progress Indicator */}
      <div className="w-full bg-white/20 rounded-full h-3 overflow-hidden">
        <div
          className={`h-3 transition-all duration-500 ${progressColor}`}
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <p className="text-sm text-gray-200 font-medium">
        Question {step} of {totalSteps}
      </p>

      {/* Question Title */}
      <h2 className="text-2xl font-semibold">{title}</h2>

      {/* Options */}
      <div className="flex flex-wrap justify-center gap-3 mt-4">
        {options.map((option) => (
          <button
            key={option}
            onClick={() => onSelect(option)}
            className="bg-blue-500 hover:bg-blue-600 text-white px-5 py-2 rounded-xl transition"
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
};

const RecommendationQuiz: React.FC = () => {
  const [answers, setAnswers] = useState({
    genre: "",
    difficulty: "",
    players: "",
  });

  // Map genre keywords to Tailwind colors
  const genreColors: Record<string, string> = {
    Strategy: "bg-red-500",
    Trading: "bg-orange-400",
    Party: "bg-yellow-400",
    Word: "bg-pink-400",
    Fantasy: "bg-purple-500",
    SciFi: "bg-blue-500",
    Nature: "bg-green-500",
    Adventure: "bg-emerald-400",
    Card: "bg-indigo-400",
    default: "bg-blue-400",
  };

  // Dynamically extract unique genres
  const availableGenres = Array.from(
    new Set(games.flatMap((g) => g.genre.split("/").map((part) => part.trim())))
  ).sort();

  // Filter other question options
  const availableDifficulties = Array.from(
    new Set(
      games
        .filter((g) => !answers.genre || g.genre.includes(answers.genre))
        .map((g) => g.difficulty)
    )
  );

  const availablePlayers = Array.from(
    new Set(
      games
        .filter(
          (g) =>
            (!answers.genre || g.genre.includes(answers.genre)) &&
            (!answers.difficulty || g.difficulty === answers.difficulty)
        )
        .map((g) => g.players)
    )
  );

  // Selection logic
  const handleSelect = (key: keyof typeof answers, value: string) => {
    const filteredOptions =
      key === "genre"
        ? availableGenres
        : key === "difficulty"
          ? availableDifficulties
          : availablePlayers;

    const chosenValue =
      value === "Random"
        ? filteredOptions[Math.floor(Math.random() * filteredOptions.length)]
        : value;

    setAnswers((prev) => ({ ...prev, [key]: chosenValue }));
  };

  // Matching logic
  const finalMatches = games.filter(
    (g) =>
      (!answers.genre || g.genre.includes(answers.genre)) &&
      (!answers.difficulty || g.difficulty === answers.difficulty) &&
      (!answers.players || g.players === answers.players)
  );

  const recommended =
    answers.genre &&
    answers.difficulty &&
    answers.players &&
    finalMatches.length
      ? finalMatches[Math.floor(Math.random() * finalMatches.length)]
      : null;

  const totalSteps = 3;

  // Pick the appropriate color
  const progressColor =
    genreColors[
      Object.keys(genreColors).find((key) =>
        answers.genre.toLowerCase().includes(key.toLowerCase())
      ) || "default"
    ];

  // UI Rendering
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-indigo-900 to-blue-600 text-white p-8 space-y-8">
      {!answers.genre && (
        <Question
          step={1}
          totalSteps={totalSteps}
          title="What genre of game do you enjoy?"
          options={["Random", ...availableGenres]}
          onSelect={(value) => handleSelect("genre", value)}
          progressColor={progressColor}
        />
      )}

      {answers.genre && !answers.difficulty && (
        <Question
          step={2}
          totalSteps={totalSteps}
          title="What difficulty level do you prefer?"
          options={["Random", ...availableDifficulties]}
          onSelect={(value) => handleSelect("difficulty", value)}
          progressColor={progressColor}
        />
      )}

      {answers.genre && answers.difficulty && !answers.players && (
        <Question
          step={3}
          totalSteps={totalSteps}
          title="How many players will be playing?"
          options={["Random", ...availablePlayers]}
          onSelect={(value) => handleSelect("players", value)}
          progressColor={progressColor}
        />
      )}

      {recommended && (
        <div className="text-center space-y-4 bg-white/10 p-6 rounded-2xl shadow-lg max-w-md">
          <h2 className="text-3xl font-bold">{recommended.name}</h2>
          <p className="text-lg">{recommended.description}</p>
          <p className="text-sm text-gray-300">
            <strong>Players:</strong> {recommended.players} |{" "}
            <strong>Playtime:</strong> {recommended.playTime} |{" "}
            <strong>Difficulty:</strong> {recommended.difficulty}
          </p>
          <button
            onClick={() =>
              setAnswers({ genre: "", difficulty: "", players: "" })
            }
            className="bg-yellow-400 hover:bg-yellow-500 text-black px-5 py-2 rounded-xl mt-4 transition"
          >
            Restart Quiz
          </button>
        </div>
      )}
    </div>
  );
};

export default RecommendationQuiz;
