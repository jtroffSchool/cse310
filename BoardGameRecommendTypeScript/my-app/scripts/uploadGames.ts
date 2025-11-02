/// <reference types="node" />
import "dotenv/config";
import { createClient } from "@supabase/supabase-js";
import { games } from "../src/data/games.js"; // adjust path if needed

// --- Supabase setup ---
const supabaseUrl = process.env.VITE_SUPABASE_URL!;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // service_role key
const supabase = createClient(supabaseUrl, supabaseKey);

// --- Type for your Supabase table ---
interface GameRow {
  id: number;
  name: string;
  players: string;
  play_time: string;
  genre: string;
  difficulty: "Easy" | "Medium" | "Hard";
  description: string;
  bgg_id?: number; // add this
}

// --- Upload function ---
async function uploadGames() {
  console.log(`Uploading ${games.length} games...`);

  // Format games for Supabase (snake_case)
  const formatted: GameRow[] = games.map((g) => ({
    id: g.id,
    name: g.name,
    players: g.players,
    play_time: g.playTime,
    genre: g.genre,
    difficulty: g.difficulty,
    description: g.description,
    bgg_id: g.bggId, // add this line
  }));

  try {
    // Upsert games
    const { data, error } = (await supabase
      .from("games")
      .upsert(formatted)) as { data: GameRow[] | null; error: any };

    if (error) {
      console.error("Error uploading:", error);
    } else if (data) {
      console.log(`Successfully uploaded ${data.length} games.`);
    } else {
      console.log("No games were uploaded.");
    }
  } catch (err) {
    console.error("Unexpected error:", err);
  }
}

// --- Run the upload ---
uploadGames();
