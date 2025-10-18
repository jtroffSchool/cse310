import { games } from "./games";

// Helper to get unique values
const getUnique = (arr: string[]) => Array.from(new Set(arr));

// Genres + add Random
export const genres = ["Random", ...getUnique(games.map((game) => game.genre))];

// Players + playTimes could be more complex if we want ranges
export const players = getUnique(games.map((game) => game.players));
export const playTimes = getUnique(games.map((game) => game.playTime));
export const difficulties = getUnique(games.map((game) => game.difficulty));
