export interface Game {
  id: number;
  name: string;
  players: string;
  playTime: string;
  genre: string;
  difficulty: "Easy" | "Medium" | "Hard";
  description: string;
}

export const games: Game[] = [
  {
    id: 1,
    name: "Catan",
    players: "3-4",
    playTime: "60-90 min",
    genre: "Strategy",
    difficulty: "Medium",
    description:
      "Build settlements, trade resources, and expand your territory.",
  },
  {
    id: 2,
    name: "Codenames",
    players: "2-8",
    playTime: "15-30 min",
    genre: "Party",
    difficulty: "Easy",
    description:
      "Give one-word clues to help your team find secret agents on the board.",
  },
  {
    id: 3,
    name: "Terraforming Mars",
    players: "1-5",
    playTime: "90-120 min",
    genre: "Sci-Fi",
    difficulty: "Hard",
    description:
      "Compete to develop Mars by managing resources and building projects.",
  },
  {
    id: 4,
    name: "Wingspan",
    players: "1-5",
    playTime: "40-70 min",
    genre: "Engine Building",
    difficulty: "Medium",
    description:
      "Attract birds to your wildlife preserves and build powerful combos.",
  },
  {
    id: 5,
    name: "Ticket to Ride",
    players: "2-5",
    playTime: "30-60 min",
    genre: "Family",
    difficulty: "Easy",
    description:
      "Collect train cards to claim railway routes across the country.",
  },
  {
    id: 6,
    name: "Gloomhaven",
    players: "1-4",
    playTime: "90-150 min",
    genre: "Adventure",
    difficulty: "Hard",
    description:
      "Team up for tactical combat in a world of quests and branching storylines.",
  },
  {
    id: 7,
    name: "Skull King",
    players: "2-8",
    playTime: "30-45 min",
    genre: "Trick-Taking / Card",
    difficulty: "Medium",
    description:
      "A trick-taking pirate card game where players blindly bid how many tricks they'll win. Bonus cards like pirates, mermaids, and the Skull King itself add chaos and strategy.",
  },
  {
    id: 8,
    name: "Azul: Summer Pavilion",
    players: "2-4",
    playTime: "30-45 min",
    genre: "Abstract Strategy / Tile-Drafting",
    difficulty: "Medium",
    description:
      "Designers compete to decorate Portugal's Summer Pavilion over six rounds, drafting & placing tiles, using wild colors, and balancing bonuses while avoiding waste.",
  },
  {
    id: 9,
    name: "Skip-Bo",
    players: "2-6",
    playTime: "30-45 min",
    genre: "Card / Family",
    difficulty: "Easy",
    description:
      "A sequencing card game where players build stacks in numerical order to empty their stockpile. Simple rules make it great for family game nights.",
  },
  {
    id: 10,
    name: "Reign of Dragoness",
    players: "3–8",
    playTime: "20–40 min",
    genre: "Ladder Climbing / Card",
    difficulty: "Medium",
    description:
      "A strategic card game where players use dragons to form sets and runs, aiming to outplay opponents in a battle of wits and timing.",
  },
  {
    id: 11,
    name: "Beez",
    players: "2-4",
    playTime: "20-30 min",
    genre: "Abstract / Strategy",
    difficulty: "Medium",
    description:
      "A fast-paced abstract game where players use bee-shaped pieces to capture flowers, control the board, and outmaneuver opponents.",
  },
  {
    id: 12,
    name: "Candy Land",
    players: "2-4",
    playTime: "15-30 min",
    genre: "Children / Family",
    difficulty: "Easy",
    description:
      "A simple race-to-the-finish board game where players move along a colorful path by drawing cards, perfect for young children and family play.",
  },
  {
    id: 13,
    name: "Cat in the Box",
    players: "2-5",
    playTime: "15-30 min",
    genre: "Party / Deduction",
    difficulty: "Medium",
    description:
      "A lighthearted party game where players guess which cards are cats and which are not, balancing memory, deduction, and a bit of luck.",
  },
  {
    id: 14,
    name: "Chutes and Ladders",
    players: "2-4",
    playTime: "15-30 min",
    genre: "Children / Family",
    difficulty: "Easy",
    description:
      "A classic race-to-the-finish board game where players spin the spinner to move along the board, climbing ladders and sliding down chutes.",
  },
  {
    id: 15,
    name: "Communist Cats",
    players: "2–6",
    playTime: "5–10 min",
    genre: "Party / Bluffing",
    difficulty: "Easy",
    description:
      "A fast-paced party card game where players use bluffing and strategy to gain influence, defeat opponents, or capture the elusive capitalist mouse.",
  },
  {
    id: 16,
    name: "Cover Your Assets",
    players: "2-6",
    playTime: "30-45 min",
    genre: "Card / Strategy",
    difficulty: "Medium",
    description:
      "A fast-paced card game where players collect and stack assets while trying to steal from opponents. Strategic risk-taking and timing are key to winning.",
  },
  {
    id: 17,
    name: "Cover Your Kingdom",
    players: "2-6",
    playTime: "30-45 min",
    genre: "Card / Strategy",
    difficulty: "Medium",
    description:
      "Players use cards to build their kingdoms while attempting to sabotage opponents' kingdoms. Strategic card play and timing are essential to dominate the board.",
  },
  {
    id: 18,
    name: "CrossTalk",
    players: "4-8",
    playTime: "30-45 min",
    genre: "Party / Word",
    difficulty: "Medium",
    description:
      "A team-based word-guessing game where one team gives clues to their teammate while the opposing team tries to intercept. Communication, timing, and clever hints are key.",
  },
  {
    id: 19,
    name: "Curses!",
    players: "2-6",
    playTime: "30-45 min",
    genre: "Card / Strategy",
    difficulty: "Medium",
    description:
      "A strategic card game where players use curses and counter-curses to disrupt opponents while advancing their own position. Timing and hand management are key to victory.",
  },
  {
    id: 20,
    name: "Defenders of the Realm",
    players: "2-5",
    playTime: "45-60 min",
    genre: "Cooperative / Fantasy",
    difficulty: "Medium",
    description:
      "Players work together to defend the kingdom from invading monsters. Each hero has unique abilities, and teamwork is essential to overcome challenging scenarios.",
  },
  {
    id: 21,
    name: "Disney Villainous",
    players: "2-6",
    playTime: "30-60 min",
    genre: "Strategy / Thematic",
    difficulty: "Medium",
    description:
      "Players take on the role of Disney villains, each with unique objectives. Use your special abilities, manipulate the board, and thwart opponents to achieve your villainous goals.",
  },
  {
    id: 22,
    name: "Doomlings",
    players: "2-6",
    playTime: "30-45 min",
    genre: "Card / Party",
    difficulty: "Easy",
    description:
      "A fast-paced card game where players evolve quirky creatures to survive and score points. Fun, unpredictable, and full of humorous interactions.",
  },
  {
    id: 23,
    name: "Exploding Kittens",
    players: "2-5",
    playTime: "15-20 min",
    genre: "Card / Party",
    difficulty: "Easy",
    description:
      "A fast-paced, humorous card game where players draw cards until someone explodes. Use strategy and sabotage to survive while making others go boom!",
  },
  {
    id: 24,
    name: "Sushi Go!",
    players: "2-5",
    playTime: "15-20 min",
    genre: "Card / Family",
    difficulty: "Easy",
    description:
      "Draft adorable sushi cards to make the best meal combination. Quick to learn and full of clever choices each round.",
  },
  {
    id: 25,
    name: "Love Letter",
    players: "2-6",
    playTime: "20 min",
    genre: "Card / Deduction",
    difficulty: "Medium",
    description:
      "A game of bluffing, deduction, and luck. Deliver your love letter to the princess while intercepting others' letters before they reach her.",
  },
  {
    id: 26,
    name: "The Crew: The Quest for Planet Nine",
    players: "2-5",
    playTime: "20-45 min",
    genre: "Card / Cooperative",
    difficulty: "Hard",
    description:
      "A cooperative trick-taking game where players complete space missions through communication, teamwork, and precise play.",
  },
  {
    id: 27,
    name: "Point Salad",
    players: "2-6",
    playTime: "15-30 min",
    genre: "Card / Strategy",
    difficulty: "Medium",
    description:
      "A quick card drafting game where every card can be a vegetable or a scoring condition. Endless combinations make each game unique.",
  },
  {
    id: 28,
    name: "Just One",
    players: "3-7",
    playTime: "20 min",
    genre: "Party / Word",
    difficulty: "Easy",
    description:
      "A cooperative word game where players give one-word clues to help a teammate guess a secret word — but duplicate clues are discarded!",
  },
  {
    id: 29,
    name: "Wavelength",
    players: "2-12",
    playTime: "30-45 min",
    genre: "Party / Communication",
    difficulty: "Easy",
    description:
      "Teams compete to align their minds by guessing where a hidden target lies on a spectrum (e.g., hot ↔ cold, good ↔ evil).",
  },
  {
    id: 30,
    name: "Decrypto",
    players: "3-8",
    playTime: "30-45 min",
    genre: "Party / Deduction",
    difficulty: "Medium",
    description:
      "Teams give coded clues to transmit secret words without letting the opposing team intercept them. A game of communication and clever phrasing.",
  },
  {
    id: 31,
    name: "Telestrations",
    players: "4-8",
    playTime: "30 min",
    genre: "Party / Drawing",
    difficulty: "Easy",
    description:
      "Like 'Telephone' but with drawings! Players draw, guess, and laugh as the original word transforms hilariously through misinterpretation.",
  },
  {
    id: 32,
    name: "Monikers",
    players: "4-16",
    playTime: "30-60 min",
    genre: "Party / Guessing",
    difficulty: "Easy",
    description:
      "A hilarious guessing game played over three rounds — describe, use one word, then mime to get your team to guess famous people and concepts.",
  },
  {
    id: 33,
    name: "Talisman: 4th Edition",
    players: "2-6",
    playTime: "90-120 min",
    genre: "Fantasy / Adventure",
    difficulty: "Medium",
    description:
      "A classic fantasy board game where heroes race through perilous lands, battle monsters, collect treasures, and seek the powerful Crown of Command.",
  },
];
