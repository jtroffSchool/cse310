//Public BGG API doesn't appear to be working any more

import "dotenv/config";
import { createClient } from "@supabase/supabase-js";
import fetch from "node-fetch";
import { XMLParser } from "fast-xml-parser";

const supabaseUrl = process.env.VITE_SUPABASE_URL!;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!; // Must be service key
const supabase = createClient(supabaseUrl, supabaseServiceKey);

/**
 * Fetch BGG ID for a given game name.
 * Handles queue responses (202) and rate limits (429).
 */
async function fetchBGGId(
  gameName: string,
  retries = 10
): Promise<number | null> {
  const searchUrl = `https://boardgamegeek.com/xmlapi2/search?query=${encodeURIComponent(
    gameName
  )}&type=boardgame`;

  for (let i = 0; i < retries; i++) {
    try {
      console.log(`Fetching BGG ID for: ${gameName}`);
      const res = await fetch(searchUrl);
      console.log(`BGG HTTP status: ${res.status}`);

      if (res.status === 202) {
        // BGG queues the request, wait and retry
        console.log(
          `BGG queued "${gameName}", retrying (${i + 1}/${retries})...`
        );
        await new Promise((r) => setTimeout(r, 3000 + i * 500));
        continue;
      }

      if (res.status === 429) {
        // Rate limit hit, wait longer
        console.warn(`Rate limited by BGG for "${gameName}", retrying...`);
        await new Promise((r) => setTimeout(r, 5000));
        continue;
      }

      if (!res.ok) {
        console.error(`HTTP error for "${gameName}": ${res.status}`);
        return null;
      }

      const xml = await res.text();
      const parser = new XMLParser({ ignoreAttributes: false });
      const json = parser.parse(xml);

      const items = json.items?.item;
      if (!items) {
        console.log(
          `No items found for "${gameName}", retrying (${i + 1}/${retries})...`
        );
        await new Promise((r) => setTimeout(r, 2000));
        continue;
      }

      const item = Array.isArray(items) ? items[0] : items;
      if (item?.["@_id"]) return Number(item["@_id"]);

      return null;
    } catch (err) {
      console.error(`Error fetching BGG for "${gameName}":`, err);
      await new Promise((r) => setTimeout(r, 3000));
    }
  }

  console.warn(
    `Failed to fetch BGG ID for "${gameName}" after ${retries} retries`
  );
  return null;
}

async function updateGamesWithBGG() {
  // Fetch all games from Supabase
  const { data: games, error } = await supabase.from("games").select("*");
  if (error || !games) {
    console.error("Error fetching games from Supabase:", error);
    return;
  }

  for (const game of games) {
    if (game.bgg_id) continue; // Skip already updated

    const bggId = await fetchBGGId(game.name);
    if (!bggId) {
      console.log(`Skipping "${game.name}" (no BGG ID found)`);
      continue;
    }

    const { error: updateError } = await supabase
      .from("games")
      .update({ bgg_id: bggId })
      .eq("id", game.id);

    if (updateError) {
      console.error(
        `Failed to update "${game.name}" in Supabase:`,
        updateError
      );
    } else {
      console.log(`Updated "${game.name}" with BGG ID ${bggId}`);
    }

    // Delay between requests to avoid hitting BGG rate limits
    await new Promise((r) => setTimeout(r, 3500));
  }

  console.log("Done updating all BGG IDs!");
}

// Run the update
updateGamesWithBGG();
