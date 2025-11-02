import { useState, useMemo } from "react";
import { storyNodes } from "../data/storyNodes.ts";
import type { StoryNode, StoryOption } from "../types/storyNode.ts";
import { useGames } from "./useGames";
import type { Game } from "../data/games";

export function useAdventureQuiz() {
  const { games, loading } = useGames();
  const [currentNodeId, setCurrentNodeId] = useState<string>("start");
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [answers, setAnswers] = useState<{
    difficulty?: "Easy" | "Medium" | "Hard";
    players?: string;
  }>({});

  const currentNode: StoryNode | undefined = useMemo(
    () => storyNodes.find((n) => n.id === currentNodeId),
    [currentNodeId]
  );

  const handleChoice = (option: StoryOption) => {
    if (option.addGenres) {
      setSelectedGenres((prev) => [...prev, ...option.addGenres!]);
    }
    if (option.setDifficulty) {
      setAnswers((prev) => ({ ...prev, difficulty: option.setDifficulty }));
    }
    if (option.setPlayers) {
      setAnswers((prev) => ({ ...prev, players: option.setPlayers }));
    }
    if (option.next) {
      setCurrentNodeId(option.next);
    }
  };

  const resetAdventure = () => {
    setCurrentNodeId("start");
    setSelectedGenres([]);
    setAnswers({});
  };

  const recommended: Game | null = useMemo(() => {
    if (!currentNode || currentNodeId !== "end") return null;

    // Normalize selected genres
    const normalizedSelected = selectedGenres.map((g) =>
      g.trim().toLowerCase()
    );

    // Helper to filter games
    const filterGames = (useDifficulty = true, usePlayers = true) =>
      games.filter((g) => {
        const gameGenres = g.genre
          .split("/")
          .map((g) => g.trim().toLowerCase());
        const matchesGenre =
          normalizedSelected.length === 0 ||
          normalizedSelected.some((genre) => gameGenres.includes(genre));
        const matchesDifficulty =
          !useDifficulty ||
          !answers.difficulty ||
          g.difficulty === answers.difficulty;
        const matchesPlayers =
          !usePlayers ||
          !answers.players ||
          (() => {
            const parseRange = (range: string) => {
              const cleaned = range.replace("–", "-").replace("+", "");
              const [minStr, maxStr] = cleaned.split("-");
              const min = parseInt(minStr);
              const max = maxStr ? parseInt(maxStr) : min;
              return { min, max };
            };
            const gameRange = parseRange(g.players);
            const answerRange = parseRange(answers.players!);
            return (
              gameRange.max >= answerRange.min &&
              gameRange.min <= answerRange.max
            );
          })();
        return matchesGenre && matchesDifficulty && matchesPlayers;
      });

    // Try different levels of strictness
    let filtered = filterGames(true, true);
    if (!filtered.length) filtered = filterGames(true, false);
    if (!filtered.length) filtered = filterGames(false, true);
    if (!filtered.length) filtered = filterGames(false, false);

    return filtered.length
      ? filtered[Math.floor(Math.random() * filtered.length)]
      : null;
  }, [currentNode, selectedGenres, answers, games]);

  return { currentNode, handleChoice, recommended, loading, resetAdventure };
}
