import { useEffect, useState } from "react";
import { supabase } from "../lib/supabaseClient";
import type { Database } from "../types/supabase";

type GameRow = Database["public"]["Tables"]["games"]["Row"];

export interface Game {
  id: number;
  name: string;
  players: string;
  playTime: string;
  genre: string;
  difficulty: "Easy" | "Medium" | "Hard";
  description: string;
  bggId?: number; // new field
}

export function useGames() {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchGames() {
      const { data, error } = (await supabase
        .from("games" as const)
        .select("*")) as { data: GameRow[] | null; error: any };

      if (error) {
        console.error("Error fetching games:", error);
      } else if (data) {
        const formatted: Game[] = data.map((g) => ({
          id: g.id,
          name: g.name,
          players: g.players,
          playTime: g.play_time,
          genre: g.genre,
          difficulty: g.difficulty,
          description: g.description,
          bggId: g.bgg_id ?? undefined, // map the new field
        }));
        setGames(formatted);
      }

      setLoading(false);
    }

    fetchGames();
  }, []);

  return { games, loading };
}
