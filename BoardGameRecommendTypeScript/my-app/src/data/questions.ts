import { genres, players, playTimes, difficulties } from "./options";

export const questions = [
  { key: "genre", text: "What type of game do you want?", options: genres },
  { key: "players", text: "How many players?", options: players },
  { key: "playTime", text: "Preferred play time?", options: playTimes },
  { key: "difficulty", text: "Difficulty level?", options: difficulties },
];
