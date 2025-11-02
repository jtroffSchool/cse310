import React, { useState, useMemo } from "react";
import { useGames } from "../hooks/useGames";

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
      {/* Progress bar */}
      <div className="w-full bg-white/20 rounded-full h-3 overflow-hidden">
        <div
          className={`h-3 transition-all duration-500 ${progressColor}`}
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="text-sm text-gray-200 font-medium">
        Question {step} of {totalSteps}
      </p>

      <h2 className="text-2xl font-semibold">{title}</h2>

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
  const { games, loading } = useGames();
  const [answers, setAnswers] = useState({
    genre: "",
    difficulty: "",
    players: "",
  });

  const totalSteps = 3;

  // --- Compute unique options dynamically ---
  const availableGenres = useMemo(() => {
    if (loading) return [];
    const genres = games.flatMap((g) =>
      g.genre ? g.genre.split("/").map((s) => s.trim()) : []
    );
    return Array.from(new Set(genres)).sort();
  }, [games, loading]);

  const availableDifficulties = useMemo(() => {
    if (loading) return [];
    return Array.from(
      new Set(
        games
          .filter((g) => !answers.genre || g.genre.includes(answers.genre))
          .map((g) => g.difficulty)
      )
    );
  }, [games, answers.genre, loading]);

  const availablePlayers = useMemo(() => {
    if (loading) return [];
    return Array.from(
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
  }, [games, answers.genre, answers.difficulty, loading]);

  const handleSelect = (key: keyof typeof answers, value: string) => {
    const options =
      key === "genre"
        ? availableGenres
        : key === "difficulty"
          ? availableDifficulties
          : availablePlayers;

    const chosen =
      value === "Random"
        ? options.length
          ? options[Math.floor(Math.random() * options.length)]
          : ""
        : value;

    setAnswers((prev) => ({ ...prev, [key]: chosen }));
  };

  // --- Filter games based on answers ---
  const matches = useMemo(() => {
    if (loading) return [];
    return games.filter(
      (g) =>
        (!answers.genre || g.genre.includes(answers.genre)) &&
        (!answers.difficulty || g.difficulty === answers.difficulty) &&
        (!answers.players || g.players === answers.players)
    );
  }, [games, answers, loading]);

  const recommended =
    answers.genre && answers.difficulty && answers.players && matches.length
      ? matches[Math.floor(Math.random() * matches.length)]
      : null;

  const progressColor = "bg-yellow-400";

  if (loading) return <p className="text-white">Loading games...</p>;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-indigo-900 to-blue-600 text-white p-8 space-y-8">
      {!answers.genre && (
        <Question
          step={1}
          totalSteps={totalSteps}
          title="What genre of game do you enjoy?"
          options={["Random", ...availableGenres]}
          onSelect={(v) => handleSelect("genre", v)}
          progressColor={progressColor}
        />
      )}

      {answers.genre && !answers.difficulty && (
        <Question
          step={2}
          totalSteps={totalSteps}
          title="What difficulty level do you prefer?"
          options={["Random", ...availableDifficulties]}
          onSelect={(v) => handleSelect("difficulty", v)}
          progressColor={progressColor}
        />
      )}

      {answers.genre && answers.difficulty && !answers.players && (
        <Question
          step={3}
          totalSteps={totalSteps}
          title="How many players will be playing?"
          options={["Random", ...availablePlayers]}
          onSelect={(v) => handleSelect("players", v)}
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

          <div className="flex flex-col sm:flex-row justify-center gap-3 mt-4">
            {/* BGG Link Button (only if bggId exists) */}
            {recommended.bggId ? (
              <a
                href={`https://boardgamegeek.com/boardgame/${recommended.bggId}`}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-blue-500 hover:bg-blue-600 text-white px-5 py-2 rounded-xl transition"
                title="View detailed review on BoardGameGeek"
              >
                View on BoardGameGeek
              </a>
            ) : null}

            {/* Restart Button */}
            <button
              onClick={() =>
                setAnswers({ genre: "", difficulty: "", players: "" })
              }
              className="bg-yellow-400 hover:bg-yellow-500 text-black px-5 py-2 rounded-xl transition"
              title="Restart the quiz"
            >
              Restart Quiz
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecommendationQuiz;
