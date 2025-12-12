"""
main.py

Top-level game file for Cat TCG.
Handles rendering, input, drag/drop, radial menu,
a custom confirm button, and calls into GameState.
"""

import random
import pyglet
pyglet.options['audio'] = ('directsound',)  # Disable xaudio2, avoid cleanup errors
import arcade

from cat_card import CatCard        # noqa: F401 (imported for type hints / clarity)
from item_card import ItemCard      # noqa: F401
from deck_builder import build_cat_deck, build_item_deck
from radial_menu import RadialMenu
from game_state import GameState, Phase

# --------------------------------------------------
# Window + layout constants
# --------------------------------------------------

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

ITEM_HAND_Y = 120          # Items row
PLAYER_BATTLEFIELD_Y = 260 # Player cats row
AI_BATTLEFIELD_Y = 540     # AI cats row


class CatTCG(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Cat TCG — Simultaneous Turn Engine")
        arcade.set_background_color((245, 245, 245))

        # Build initial game
        self._build_new_game()

        # --------------------------------------------------
        # Radial Menu + drag state
        # --------------------------------------------------
        self.radial_menu = RadialMenu(radius=80)
        self.dragged_item: ItemCard | None = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Mouse + hover tracking
        self._mouse_x = 0
        self._mouse_y = 0
        self.hovered_item: ItemCard | None = None

        # --------------------------------------------------
        # Custom CONFIRM button (no arcade.gui)
        # --------------------------------------------------
        self.confirm_button_width = 230
        self.confirm_button_height = 40
        # Bottom-right so it doesn't overlap items
        self.confirm_button_center_x = SCREEN_WIDTH - (self.confirm_button_width // 2) - 40
        self.confirm_button_center_y = 70
        self.confirm_button_hover = False

        # Game over / restart state
        self.game_over = False
        self.winner_text = ""

    # ================================================================
    # Game (re)build helpers
    # ================================================================

    def _build_new_game(self):
        """Set up decks, hands, and GameState for a fresh game."""
        deck = build_cat_deck()
        item_deck = build_item_deck()
        random.shuffle(deck)
        random.shuffle(item_deck)

        self.player_cats: list[CatCard] = []
        self.ai_cats: list[CatCard] = []
        self.player_items: list[ItemCard] = []
        self.ai_items: list[ItemCard] = []

        # 4 cats for the player
        for _ in range(4):
            self.player_cats.append(deck.pop())

        # 4 cats for the AI
        for _ in range(4):
            self.ai_cats.append(deck.pop())

        # Starting items for the player
        for _ in range(3):
            if not item_deck:
                break
            self.player_items.append(item_deck.pop())

        # Simple starting items for AI (used by AI logic only)
        for _ in range(3):
            if not item_deck:
                break
            self.ai_items.append(item_deck.pop())

        # Hook into GameState
        self.state = GameState(
            player_cats=self.player_cats,
            player_items=self.player_items,
            ai_cats=self.ai_cats,
            ai_items=self.ai_items,
        )
        self.state.start_new_turn()

        # Layout
        self.reposition_ai_cats()
        self.reposition_player_cats()
        self.reposition_player_items()

    def restart_game(self):
        """Called when player presses R after game over."""
        self.game_over = False
        self.winner_text = ""
        self.hovered_item = None
        self.dragged_item = None
        self.radial_menu.hide()
        self.confirm_button_hover = False

        self._build_new_game()

    # ================================================================
    # Board maintenance helpers
    # ================================================================

    def remove_dead_units(self):
        """
        Remove any cat whose HP <= 0 for both player and AI,
        and enter game over if one side has no cats left.
        """
        self.player_cats = [c for c in self.player_cats if not c.is_dead()]
        self.ai_cats = [c for c in self.ai_cats if not c.is_dead()]

        # Keep GameState lists in sync
        self.state.player_cats = self.player_cats
        self.state.ai_cats = self.ai_cats

        # Check for game end
        if not self.game_over:
            player_empty = len(self.player_cats) == 0
            ai_empty = len(self.ai_cats) == 0

            if player_empty and ai_empty:
                self.game_over = True
                self.winner_text = "It's a draw! Press R to restart."
            elif player_empty:
                self.game_over = True
                self.winner_text = "AI wins! Press R to restart."
            elif ai_empty:
                self.game_over = True
                self.winner_text = "Player wins! Press R to restart."

    # ================================================================
    # Layout helpers
    # ================================================================

    def _reposition_row_evenly(self, cards: list, center_y: float, spacing: int = 230):
        """
        Evenly space a list of cards in a row centered on the screen.
        """
        n = len(cards)
        if n == 0:
            return

        total_width = spacing * (n - 1)
        start_x = SCREEN_WIDTH // 2 - total_width // 2

        for i, card in enumerate(cards):
            card.sprite.center_x = start_x + i * spacing
            card.sprite.center_y = center_y

    def reposition_player_cats(self):
        self._reposition_row_evenly(self.player_cats, PLAYER_BATTLEFIELD_Y)

    def reposition_ai_cats(self):
        self._reposition_row_evenly(self.ai_cats, AI_BATTLEFIELD_Y)

    def reposition_player_items(self):
        """
        Center the player's items in a row near the bottom.
        """
        n = len(self.player_items)
        if n == 0:
            return

        spacing = 220
        total_width = spacing * (n - 1)
        start_x = SCREEN_WIDTH // 2 - total_width // 2

        for i, item in enumerate(self.player_items):
            item.sprite.center_x = start_x + i * spacing
            item.sprite.center_y = ITEM_HAND_Y

    # ================================================================
    # Confirm button helpers
    # ================================================================

    def _mouse_in_confirm_button(self, x: float, y: float) -> bool:
        half_w = self.confirm_button_width / 2
        half_h = self.confirm_button_height / 2
        return (
            self.confirm_button_center_x - half_w <= x <= self.confirm_button_center_x + half_w
            and self.confirm_button_center_y - half_h <= y <= self.confirm_button_center_y + half_h
        )

    def _draw_confirm_button(self):
        # Disabled once game is over
        if self.state.phase == Phase.PLAYER_PLANNING and not self.game_over:
            fill_color = arcade.color.LIGHT_GREEN if self.confirm_button_hover else arcade.color.APPLE_GREEN
        else:
            fill_color = arcade.color.LIGHT_GRAY

        # Background
        arcade.draw_rectangle_filled(
            self.confirm_button_center_x,
            self.confirm_button_center_y,
            self.confirm_button_width,
            self.confirm_button_height,
            fill_color,
        )

        # Outline
        arcade.draw_rectangle_outline(
            self.confirm_button_center_x,
            self.confirm_button_center_y,
            self.confirm_button_width,
            self.confirm_button_height,
            arcade.color.BLACK,
            border_width=2,
        )

        label = "CONFIRM ACTIONS"
        text_width = 170
        arcade.draw_text(
            label,
            self.confirm_button_center_x - text_width / 2,
            self.confirm_button_center_y - 10,
            arcade.color.BLACK,
            14,
        )

    # ================================================================
    # Tooltip helper for items
    # ================================================================

    def _draw_item_tooltip(self):
        """Draw a small tooltip near the mouse for the hovered item."""
        if self.hovered_item is None:
            return

        item = self.hovered_item

        title = f"{item.name} (Cost {item.cost})"
        effect_line = f"Effect: {item.effect_type.capitalize()} ({item.value})"
        desc = item.description

        box_w = 320
        box_h = 110

        # Place near the mouse, but keep fully on-screen
        left = min(self._mouse_x + 15, SCREEN_WIDTH - box_w - 10)
        bottom = min(self._mouse_y + 15, SCREEN_HEIGHT - box_h - 10)
        center_x = left + box_w / 2
        center_y = bottom + box_h / 2

        # Background + border
        arcade.draw_rectangle_filled(
            center_x,
            center_y,
            box_w,
            box_h,
            (0, 0, 0, 210),   # semi-transparent dark
        )
        arcade.draw_rectangle_outline(
            center_x,
            center_y,
            box_w,
            box_h,
            arcade.color.LIGHT_GOLDENROD_YELLOW,
            border_width=2,
        )

        # Text
        margin = 10
        text_x = left + margin
        title_y = bottom + box_h - 24
        effect_y = title_y - 20
        desc_y = effect_y - 22

        arcade.draw_text(
            title,
            text_x,
            title_y,
            arcade.color.LIGHT_GOLDENROD_YELLOW,
            14,
            bold=True,
        )
        arcade.draw_text(
            effect_line,
            text_x,
            effect_y,
            arcade.color.WHITE,
            12,
        )
        arcade.draw_text(
            desc,
            text_x,
            desc_y,
            arcade.color.LIGHT_GRAY,
            11,
            width=box_w - 2 * margin,
        )

    # ================================================================
    # Input handling
    # ================================================================

    def on_mouse_press(self, x, y, button, modifiers):
        # 1) Confirm button click (disabled if game over)
        if self._mouse_in_confirm_button(x, y) and not self.game_over:
            if self.state.phase == Phase.PLAYER_PLANNING:
                self.state.player_confirm()
            return

        # 2) Radial menu click (ATTACK / CANCEL)
        result = self.radial_menu.check_click(x, y)
        if result == "ATTACK":
            self.state.player_choose_attack()
            return
        elif result == "CANCEL":
            self.state.selected_player_cat = None
            self.state.awaiting_attack_target = False
            return

        # 3) Selecting an attack target (click an AI cat)
        if self.state.awaiting_attack_target and not self.game_over:
            for cat in self.ai_cats:
                if cat.sprite.collides_with_point((x, y)):
                    self.state.player_assign_attack_target(cat)
                    return

        # 4) Selecting a player cat (to open radial menu)
        if self.state.phase == Phase.PLAYER_PLANNING and not self.game_over:
            for cat in self.player_cats:
                if cat.sprite.collides_with_point((x, y)):
                    self.state.select_player_cat(cat)
                    if cat == self.state.selected_player_cat:
                        self.radial_menu.show(cat.sprite.center_x, cat.sprite.center_y)
                    return

            # 5) Start dragging an item (player items only)
            for item in self.player_items:
                if item.sprite.collides_with_point((x, y)):
                    self.dragged_item = item
                    self.drag_offset_x = item.sprite.center_x - x
                    self.drag_offset_y = item.sprite.center_y - y
                    return

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragged_item:
            self.dragged_item.sprite.center_x = x + self.drag_offset_x
            self.dragged_item.sprite.center_y = y + self.drag_offset_y

    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragged_item:
            # If released on a player cat, use the item on that cat
            for cat in self.player_cats:
                if cat.sprite.collides_with_point((x, y)):
                    self.state.player_use_item(self.dragged_item, cat)
                    self.dragged_item = None
                    self.reposition_player_items()
                    return

            # Otherwise, snap item back to the hand row
            self.dragged_item.sprite.center_y = ITEM_HAND_Y
            self.reposition_player_items()
            self.dragged_item = None

    def on_mouse_motion(self, x, y, dx, dy):
        self._mouse_x = x
        self._mouse_y = y

        self.radial_menu.check_hover(x, y)
        self.confirm_button_hover = self._mouse_in_confirm_button(x, y)

        # Which item is hovered?
        self.hovered_item = None
        for item in self.player_items:
            if item.sprite.collides_with_point((x, y)):
                self.hovered_item = item
                break

    def on_key_press(self, symbol, modifiers):
        # R to restart when game over
        if symbol == arcade.key.R and self.game_over:
            self.restart_game()

    # ================================================================
    # Update loop
    # ================================================================

    def on_update(self, delta_time):
        # Do not update the logic while in game-over state
        if self.game_over:
            return

        # Let GameState handle phase logic, combat resolution, etc.
        self.state.update()

        # Remove dead cats and possibly trigger game over
        self.remove_dead_units()

        # Keep layout tidy each frame
        self.reposition_ai_cats()
        self.reposition_player_cats()
        self.reposition_player_items()

    # ================================================================
    # Drawing
    # ================================================================

    def on_draw(self):
        self.clear()

        # --------------------------------------------------
        # Top HUD: energy + debug counts
        # --------------------------------------------------
        arcade.draw_text(
            f"Player Energy: {self.state.player_energy}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.DARK_BLUE,
            20,
        )
        arcade.draw_text(
            f"AI Energy: {self.state.ai_energy}",
            20,
            SCREEN_HEIGHT - 70,
            arcade.color.DARK_RED,
            20,
        )

        arcade.draw_text(
            f"DEBUG Player cats: {len(self.player_cats)}",
            SCREEN_WIDTH - 260,
            SCREEN_HEIGHT - 40,
            arcade.color.GRAY,
            14,
        )
        arcade.draw_text(
            f"DEBUG AI cats: {len(self.ai_cats)}",
            SCREEN_WIDTH - 260,
            SCREEN_HEIGHT - 60,
            arcade.color.GRAY,
            14,
        )

        # --------------------------------------------------
        # Battlefield labels
        # --------------------------------------------------
        arcade.draw_line(
            0,
            AI_BATTLEFIELD_Y - 80,
            SCREEN_WIDTH,
            AI_BATTLEFIELD_Y - 80,
            arcade.color.BLACK,
            2,
        )
        arcade.draw_text(
            "AI BATTLEFIELD",
            20,
            AI_BATTLEFIELD_Y + 150,
            arcade.color.BLACK,
            16,
        )

        arcade.draw_line(
            0,
            PLAYER_BATTLEFIELD_Y - 80,
            SCREEN_WIDTH,
            PLAYER_BATTLEFIELD_Y - 80,
            arcade.color.BLACK,
            2,
        )
        arcade.draw_text(
            "PLAYER BATTLEFIELD",
            20,
            PLAYER_BATTLEFIELD_Y + 150,
            arcade.color.BLACK,
            16,
        )

        # --------------------------------------------------
        # Draw AI cats (frames, sprites, stats)
        # --------------------------------------------------
        for cat in self.ai_cats:
            cat.draw_frame()
            cat.sprite.draw()
            cat.draw_stats()

        # --------------------------------------------------
        # Draw Player cats (frames, sprites, stats, highlights)
        # --------------------------------------------------
        for cat in self.player_cats:
            cat.draw_frame()
            cat.sprite.draw()
            cat.draw_stats()
            cat.draw_highlight()
            cat.draw_planned_action_marker()

        # --------------------------------------------------
        # Draw Player items
        # --------------------------------------------------
        for item in self.player_items:
            item.sprite.draw()
            item.draw_info()

        # --------------------------------------------------
        # Radial menu + confirm button + item tooltip
        # --------------------------------------------------
        self.radial_menu.draw()
        self._draw_confirm_button()
        self._draw_item_tooltip()

        # --------------------------------------------------
        # Game over banner
        # --------------------------------------------------
        if self.game_over and self.winner_text:
            arcade.draw_text(
                self.winner_text,
                SCREEN_WIDTH / 2 - 220,
                SCREEN_HEIGHT / 2,
                arcade.color.BLACK,
                22,
                width=440,
                align="center",
            )


# ======================================================================
# ENTRY POINT
# ======================================================================

def main():
    window = CatTCG()
    arcade.run()


if __name__ == "__main__":
    main()
