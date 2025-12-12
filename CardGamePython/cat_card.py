import arcade

# ------------------------------------------------------------
# Global hit sound (lazy-loaded so we don't crash if missing)
# ------------------------------------------------------------
_HIT_SOUND = None


def get_hit_sound():
    """
    Load and cache the hit sound the first time we need it.
    If the file is missing, just return None to avoid crashes.
    """
    global _HIT_SOUND
    if _HIT_SOUND is None:
        try:
            _HIT_SOUND = arcade.load_sound("assets/cat_hiss.wav")
        except Exception:
            _HIT_SOUND = None
    return _HIT_SOUND


class CatCard:
    """
    Represents a Cat Unit in the TCG.
    Supports:
    - Attack once per turn
    - Receiving item buffs
    - Simultaneous damage resolution
    """

    # Card frame size (background outline behind each cat)
    FRAME_W = 180
    FRAME_H = 220

    # How big the sprite is allowed to be inside the frame
    MAX_SPRITE_W = FRAME_W * 0.80
    MAX_SPRITE_H = FRAME_H * 0.80

    def __init__(self, name, max_health, attack, cat_type, rarity,
                 description, image_path, attack_cost=1):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.attack = attack
        self.attack_cost = attack_cost

        self.cat_type = cat_type
        self.rarity = rarity
        self.description = description
        self.image_path = image_path

        # Status modifiers
        self.armor = 0
        self.shield_active = False
        self.can_attack = True  # refreshed each turn

        # Planning state (for simultaneous turns)
        self.planned_attack_target = None
        self.planned_item_effects = []
        self.has_planned_attack = False

        # UI
        self.is_selected = False

        # --- Sprite: load and scale to fit inside the frame ---
        self.sprite = arcade.Sprite(self.image_path)

        orig_w = self.sprite.width
        orig_h = self.sprite.height

        if orig_w > 0 and orig_h > 0:
            # Scale factors for width and height limits
            scale_w = self.MAX_SPRITE_W / orig_w
            scale_h = self.MAX_SPRITE_H / orig_h
            # Use the smaller so we never exceed the frame in either dimension
            self.sprite.scale = min(scale_w, scale_h)
        else:
            self.sprite.scale = 1.0

    # ============================================================
    # DRAWING HELPERS
    # ============================================================

    def draw_stats(self):
        """
        Draw HP, ATK, Armor above the frame.
        """
        stats_text = f"ATK {self.attack} | HP {self.current_health}/{self.max_health}"
        # Place text slightly above the top of the frame
        text_y = self.sprite.center_y + (self.FRAME_H / 2) + 5

        arcade.draw_text(
            stats_text,
            self.sprite.center_x - 60,
            text_y,
            arcade.color.BLACK,
            13,
        )

        # Draw armor near the top-right of the frame
        if self.armor > 0:
            arcade.draw_text(
                f"ARMOR: {self.armor}",
                self.sprite.center_x - 40,
                self.sprite.center_y + (self.FRAME_H / 2) + 22,
                arcade.color.DARK_BLUE,
                12,
            )

        # Draw shield indicator
        if self.shield_active:
            arcade.draw_text(
                "SHIELD",
                self.sprite.center_x - 30,
                self.sprite.center_y + (self.FRAME_H / 2) + 38,
                arcade.color.PURPLE,
                12,
                bold=True,
            )

    def draw_highlight(self):
        """
        Highlight selected cat with a glowing outline.
        """
        if self.is_selected:
            arcade.draw_rectangle_outline(
                self.sprite.center_x,
                self.sprite.center_y,
                self.FRAME_W * 1.08,
                self.FRAME_H * 1.08,
                arcade.color.YELLOW,
                4,
            )

    def draw_planned_action_marker(self):
        """
        Shows a small icon if the cat has a planned attack this turn.
        """
        if self.has_planned_attack:
            arcade.draw_text(
                "⚔",
                self.sprite.center_x + self.FRAME_W * 0.35,
                self.sprite.center_y + self.FRAME_H * 0.35,
                arcade.color.RED,
                20,
            )

    def draw_frame(self):
        """
        Draws the fixed-size card frame behind the cat.
        """
        arcade.draw_rectangle_filled(
            self.sprite.center_x,
            self.sprite.center_y,
            self.FRAME_W,
            self.FRAME_H,
            (255, 255, 255, 220),
        )

        arcade.draw_rectangle_outline(
            self.sprite.center_x,
            self.sprite.center_y,
            self.FRAME_W,
            self.FRAME_H,
            arcade.color.BLACK,
            3,
        )

    # ============================================================
    # LOGIC HELPERS
    # ============================================================

    def reset_for_new_turn(self):
        """
        Called at the start of each turn.
        """
        self.can_attack = True
        self.has_planned_attack = False
        self.planned_attack_target = None
        self.planned_item_effects = []

    def apply_damage(self, dmg):
        """
        Process incoming damage after shield and armor mitigation.
        Also plays a hit sound if any damage actually goes through.
        """
        original = dmg

        # Shield fully blocks first hit
        if self.shield_active:
            self.shield_active = False
            final_damage = 0
        else:
            # Armor absorbs some damage
            if self.armor > 0:
                absorbed = min(self.armor, dmg)
                dmg -= absorbed
                self.armor -= absorbed

            final_damage = max(0, dmg)
            self.current_health -= final_damage

        # Play sound only if something actually hurt
        if final_damage > 0:
            snd = get_hit_sound()
            if snd is not None:
                arcade.play_sound(snd)

        return final_damage


    def is_dead(self) -> bool:
        return self.current_health <= 0
