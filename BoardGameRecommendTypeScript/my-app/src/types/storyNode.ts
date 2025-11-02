export interface StoryOption {
  label: string;
  next?: string; // id of the next node
  addGenres?: string[]; // genres to add
  setDifficulty?: "Easy" | "Medium" | "Hard";
  setPlayers?: string;
}

export interface StoryNode {
  id: string;
  text: string;
  options: StoryOption[];
}
