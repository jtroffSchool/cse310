import arcade

class ItemCard:
    """
    Represents a consumable item card.
    """

    def __init__(self, name, effect_type, value, cost, description, image_path):
        self.name = name
        self.effect_type = effect_type
        self.value = value
        self.cost = cost
        self.description = description
        self.image_path = image_path

        # --- Sprite: load and auto-scale to a target height ---
        self.sprite = arcade.Sprite(self.image_path)
        TARGET_HEIGHT = 140  # a bit smaller than cats

        if self.sprite.height > 0:
            scale_factor = TARGET_HEIGHT / self.sprite.height
        else:
            scale_factor = 1.0

        self.sprite.scale = scale_factor

        self.is_selected = False

    # ------------------------------------------------------------
    # Drawing Helpers
    # ------------------------------------------------------------

    def draw_info(self):
        """
        Show item name + cost vertically under the sprite.
        """
        label = f"{self.name}\nCOST {self.cost}"
        arcade.draw_text(
            label,
            self.sprite.center_x - 45,
            self.sprite.center_y - (self.sprite.height * 0.55),
            arcade.color.BLACK,
            12
        )

    def draw_highlight(self):
        """
        Highlights item during planning.
        """
        if self.is_selected:
            arcade.draw_rectangle_outline(
                self.sprite.center_x,
                self.sprite.center_y,
                self.sprite.width * 1.18,
                self.sprite.height * 1.18,
                arcade.color.LIGHT_GREEN,
                3
            )
