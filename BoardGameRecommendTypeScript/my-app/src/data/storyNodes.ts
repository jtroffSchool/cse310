import type { StoryNode } from "../types/storyNode.ts";

export const storyNodes: StoryNode[] = [
  {
    id: "start",
    text: "A dragon threatens your village! What will you do?",
    options: [
      {
        label: "Slay the dragon",
        next: "battle_prepare",
        addGenres: ["Adventure", "Strategy"],
        setDifficulty: "Hard",
      },
      {
        label: "Save the dragon",
        next: "rescue_plan",
        addGenres: ["Adventure", "Fantasy / Adventure"],
        setDifficulty: "Medium",
      },
      {
        label: "Negotiate with the dragon",
        next: "talk_plan",
        addGenres: ["Party", "Family"],
        setDifficulty: "Easy",
      },
      {
        label: "Sneak into the dragon's lair",
        next: "stealth_plan",
        addGenres: ["Abstract", "Misc"],
        setDifficulty: "Medium",
      },
    ],
  },
  // --- Slay path ---
  {
    id: "battle_prepare",
    text: "You gather weapons and warriors. How many companions join you?",
    options: [
      {
        label: "Small team (2-3 players)",
        next: "battle_fight",
        setPlayers: "2-3",
      },
      {
        label: "Moderate team (3-5 players)",
        next: "battle_fight",
        setPlayers: "3-5",
      },
      {
        label: "Whole village (6+ players)",
        next: "battle_fight",
        setPlayers: "6-12",
      },
    ],
  },
  {
    id: "battle_fight",
    text: "The dragon appears! How do you attack?",
    options: [
      {
        label: "Direct assault",
        next: "battle_treasure",
        addGenres: ["Strategy"],
      },
      {
        label: "Use cunning traps",
        next: "battle_treasure",
        addGenres: ["Abstract", "Strategy"],
      },
    ],
  },
  {
    id: "battle_treasure",
    text: "You defeat the dragon! What do you claim from its hoard?",
    options: [
      { label: "Ancient weapons", next: "end", addGenres: ["Strategy"] },
      {
        label: "Magical artifacts",
        next: "end",
        addGenres: ["Adventure", "SciFi"],
      },
      {
        label: "Shiny trinkets for everyone",
        next: "end",
        addGenres: ["Family", "Party"],
      },
    ],
  },

  // --- Save path ---
  {
    id: "rescue_plan",
    text: "You find the dragon trapped. How do you free it?",
    options: [
      {
        label: "Use strength to lift rocks",
        next: "rescue_friends",
        addGenres: ["Adventure"],
      },
      {
        label: "Solve a puzzle to unlock the cage",
        next: "rescue_friends",
        addGenres: ["Abstract"],
      },
    ],
  },
  {
    id: "rescue_friends",
    text: "Do you recruit villagers to help?",
    options: [
      {
        label: "Yes, small team (2-3)",
        next: "rescue_reward",
        setPlayers: "2-3",
      },
      {
        label: "Yes, moderate team (3-5)",
        next: "rescue_reward",
        setPlayers: "3-5",
      },
      {
        label: "No, I can handle it alone",
        next: "rescue_reward",
        setPlayers: "1-1",
      },
    ],
  },
  {
    id: "rescue_reward",
    text: "The dragon is free! How do you celebrate?",
    options: [
      { label: "Party with games", next: "end", addGenres: ["Party"] },
      { label: "Host a feast", next: "end", addGenres: ["Family"] },
    ],
  },

  // --- Negotiate path ---
  {
    id: "talk_plan",
    text: "You approach the dragon with words. How will you persuade it?",
    options: [
      { label: "Offer treasure", next: "talk_result", addGenres: ["Family"] },
      {
        label: "Tell a clever joke",
        next: "talk_result",
        addGenres: ["Party"],
      },
      {
        label: "Appeal to its honor",
        next: "talk_result",
        addGenres: ["Strategy"],
      },
    ],
  },
  {
    id: "talk_result",
    text: "The dragon listens. How do you solidify peace?",
    options: [
      {
        label: "Form a pact",
        next: "end",
        addGenres: ["Adventure", "Strategy"],
      },
      {
        label: "Host a games tournament",
        next: "end",
        addGenres: ["Party", "Family"],
      },
    ],
  },

  // --- Stealth path ---
  {
    id: "stealth_plan",
    text: "You enter the dragon's lair silently. What's your approach?",
    options: [
      {
        label: "Distract the dragon with a decoy",
        next: "stealth_find",
        addGenres: ["Party"],
      },
      {
        label: "Solve a puzzle to unlock treasures",
        next: "stealth_find",
        addGenres: ["Abstract", "Strategy"],
      },
    ],
  },
  {
    id: "stealth_find",
    text: "You reach the treasure chamber. What do you take?",
    options: [
      {
        label: "Rare artifacts",
        next: "end",
        addGenres: ["Adventure", "SciFi"],
      },
      {
        label: "Fun items for everyone",
        next: "end",
        addGenres: ["Party", "Family"],
      },
    ],
  },

  // --- End node ---
  {
    id: "end",
    text: "Your adventure concludes! Based on your choices, a board game is recommended for you.",
    options: [],
  },
];
