export type Database = {
  public: {
    Tables: {
      games: {
        Row: {
          id: number;
          name: string;
          players: string;
          play_time: string;
          genre: string;
          difficulty: "Easy" | "Medium" | "Hard";
          description: string;
          bgg_id: number;
        };
        Insert: {
          id?: number;
          name: string;
          players: string;
          play_time: string;
          genre: string;
          difficulty: "Easy" | "Medium" | "Hard";
          description: string;
          bgg_id?: number;
        };
        Update: {
          id?: number;
          name?: string;
          players?: string;
          play_time?: string;
          genre?: string;
          difficulty?: "Easy" | "Medium" | "Hard";
          description?: string;
          bgg_id?: number;
        };
      };
    };
  };
};
