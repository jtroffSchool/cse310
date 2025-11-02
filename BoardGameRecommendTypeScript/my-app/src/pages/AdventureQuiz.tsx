import React, { useState } from "react";
import { useAdventureQuiz } from "../hooks/useAdventureQuiz";
import type { StoryOption } from "../types/storyNode";

const AdventureQuiz: React.FC = () => {
  const { currentNode, handleChoice, recommended, loading, resetAdventure } =
    useAdventureQuiz();

  // Keep track of visited path (choices + node ids)
  const [path, setPath] = useState<
    { label: string; nodeId: string; option: StoryOption | null }[]
  >([{ label: "Start", nodeId: "start", option: null }]);

  const onChoice = (option: StoryOption) => {
    setPath((prev) => [
      ...prev,
      { label: option.label, nodeId: option.next || "end", option },
    ]);
    handleChoice(option);
  };

  const handleRewind = (index: number) => {
    const newPath = path.slice(0, index + 1);
    setPath(newPath);
    const last = newPath[newPath.length - 1];
    if (last?.option?.next) handleChoice(last.option);
    else if (last?.nodeId) handleChoice({ next: last.nodeId } as StoryOption);
  };

  // Reset adventure without reload
  const handleRestart = () => {
    resetAdventure(); // resets all state: node, genres, difficulty, players
    setPath([{ label: "Start", nodeId: "start", option: null }]); // reset path
  };

  if (loading) return <p className="text-white">Loading games...</p>;
  if (!currentNode) return <p className="text-white">Story not found!</p>;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-indigo-900 to-blue-600 text-white p-8 space-y-8">
      {/* Breadcrumb trail */}
      {path.length > 1 && (
        <div className="flex flex-wrap justify-center gap-2 text-sm text-gray-300 max-w-2xl">
          {path.map((step, i) => (
            <span
              key={i}
              onClick={() => handleRewind(i)}
              className={`cursor-pointer hover:underline ${
                i === path.length - 1 ? "text-yellow-300" : ""
              }`}
            >
              {step.label}
              {i < path.length - 1 && " → "}
            </span>
          ))}
        </div>
      )}

      {/* Story text */}
      <div className="text-center max-w-2xl space-y-6 bg-white/10 p-6 rounded-2xl shadow-lg">
        <p className="text-xl">{currentNode.text}</p>

        {/* Options */}
        {currentNode.options.length > 0 && (
          <div className="flex flex-wrap justify-center gap-3 mt-4">
            {currentNode.options.map((option) => (
              <button
                key={option.label}
                onClick={() => onChoice(option)}
                className="bg-yellow-400 hover:bg-yellow-500 text-black px-5 py-2 rounded-xl transition"
              >
                {option.label}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Recommendation */}
      {currentNode.id === "end" && recommended && (
        <div className="text-center max-w-md space-y-4 bg-white/20 p-6 rounded-2xl shadow-lg">
          <h2 className="text-3xl font-bold">{recommended.name}</h2>
          <p className="text-lg">{recommended.description}</p>
          <p className="text-sm text-gray-300">
            <strong>Players:</strong> {recommended.players} |{" "}
            <strong>Playtime:</strong> {recommended.playTime} |{" "}
            <strong>Difficulty:</strong> {recommended.difficulty}
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4 mt-4">
            {recommended.bggId && (
              <a
                href={`https://boardgamegeek.com/boardgame/${recommended.bggId}`}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-blue-500 hover:bg-blue-600 text-white px-5 py-2 rounded-xl transition text-center"
              >
                View on BGG
              </a>
            )}
            <button
              onClick={handleRestart}
              className="bg-yellow-400 hover:bg-yellow-500 text-black px-5 py-2 rounded-xl transition"
            >
              Restart Adventure
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdventureQuiz;
