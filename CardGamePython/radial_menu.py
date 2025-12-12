import arcade
import math
import time


class RadialMenuOption:
    """
    A single button in the radial menu.
    """

    def __init__(self, label, angle_deg, radius, color, hover_color):
        self.label = label
        self.angle_deg = angle_deg
        self.radius = radius
        self.color = color
        self.hover_color = hover_color

        # Computed per frame
        self.center_x = 0
        self.center_y = 0
        self.is_hovered = False

        # Visuals
        self.size = 40  # circle radius


class RadialMenu:
    """
    Stylized radial menu with animated pop-in and vibrant circular buttons.

    Usage:
        menu = RadialMenu()
        menu.show(x, y)
        menu.options[...] for configuration
        menu.draw()
        menu.check_click(x, y) → returns selected option
    """

    def __init__(self, radius=80):
        self.radius = radius
        self.options = []

        self.visible = False
        self.center_x = 0
        self.center_y = 0

        # Animation state
        self.animation_start = 0
        self.animation_duration = 0.15  # fast pop

        # Create default options (Attack + Cancel)
        self._build_default_options()

    # =====================================================================
    # MENU SETUP
    # =====================================================================

    def _build_default_options(self):
        """
        Build ATTACK and CANCEL buttons with stylized colors.
        """

        # ATTACK option (red/orange glow)
        self.options.append(
            RadialMenuOption(
                label="ATTACK",
                angle_deg=0,               # right side
                radius=self.radius,
                color=arcade.color.ORANGE_RED,
                hover_color=arcade.color.RED_DEVIL
            )
        )

        # CANCEL option (neon purple)
        self.options.append(
            RadialMenuOption(
                label="CANCEL",
                angle_deg=180,             # left side
                radius=self.radius,
                color=arcade.color.MEDIUM_PURPLE,
                hover_color=arcade.color.PURPLE_HEART
            )
        )

    # =====================================================================
    # SHOW / HIDE
    # =====================================================================

    def show(self, x, y):
        self.center_x = x
        self.center_y = y
        self.visible = True
        self.animation_start = time.time()

    def hide(self):
        self.visible = False

    # =====================================================================
    # UPDATE MENU POSITIONING
    # =====================================================================

    def _compute_button_positions(self):
        """
        Compute each option's center based on angle and menu center.
        """

        for opt in self.options:
            angle_rad = math.radians(opt.angle_deg)
            opt.center_x = self.center_x + math.cos(angle_rad) * opt.radius
            opt.center_y = self.center_y + math.sin(angle_rad) * opt.radius

    # =====================================================================
    # DRAW
    # =====================================================================

    def draw(self):
        if not self.visible:
            return

        # Animation scale factor
        elapsed = time.time() - self.animation_start
        t = max(0.0, min(1.0, elapsed / self.animation_duration))
        scale = 0.3 + 0.7 * t  # grows from 0.3 to 1.0

        # Recompute layout per frame
        self._compute_button_positions()

        # Draw each button
        for opt in self.options:
            # Glow effect behind button
            arcade.draw_circle_filled(
                opt.center_x,
                opt.center_y,
                opt.size * scale * 1.4,
                (opt.color[0], opt.color[1], opt.color[2], 100)
            )

            # Button circle
            color = opt.hover_color if opt.is_hovered else opt.color
            arcade.draw_circle_filled(
                opt.center_x,
                opt.center_y,
                opt.size * scale,
                color
            )

            # Button label
            arcade.draw_text(
                opt.label,
                opt.center_x - 20 * scale,
                opt.center_y - 6 * scale,
                arcade.color.WHITE,
                int(14 * scale),
                bold=True
            )

    # =====================================================================
    # INPUT HANDLING
    # =====================================================================

    def check_hover(self, mouse_x, mouse_y):
        """
        Determine if the cursor is hovering over a button.
        """

        if not self.visible:
            return

        for opt in self.options:
            dx = mouse_x - opt.center_x
            dy = mouse_y - opt.center_y
            dist = math.sqrt(dx * dx + dy * dy)
            opt.is_hovered = dist <= opt.size

    def check_click(self, mouse_x, mouse_y):
        """
        Returns:
            "ATTACK"
            "CANCEL"
            or None
        """
        if not self.visible:
            return None

        for opt in self.options:
            dx = mouse_x - opt.center_x
            dy = mouse_y - opt.center_y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist <= opt.size:
                self.hide()
                return opt.label

        return None
