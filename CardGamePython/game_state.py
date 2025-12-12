from enum import Enum, auto
from typing import List, Optional

from cat_card import CatCard
from item_card import ItemCard


class Phase(Enum):
    PLAYER_PLANNING = auto()
    RESOLVE = auto()
    GAME_OVER = auto()


class GameState:
    """
    Holds the rules / logic for the Cat TCG.
    This version is intentionally simple and NEVER removes cats
    except when their HP drops to 0 or below during RESOLVE.
    """

    def __init__(
        self,
        player_cats: List[CatCard],
        player_items: List[ItemCard],
        ai_cats: List[CatCard],
        ai_items: List[ItemCard],
    ):
        self.player_cats = player_cats
        self.player_items = player_items
        self.ai_cats = ai_cats
        self.ai_items = ai_items

        self.max_energy = 10
        self.player_energy = self.max_energy
        self.ai_energy = self.max_energy

        self.phase: Phase = Phase.PLAYER_PLANNING
        self.turn_number: int = 1

        # Selection / planning
        self.selected_player_cat: Optional[CatCard] = None
        self.awaiting_attack_target: bool = False

        # Attack plans: (attacker, target)
        self.player_attack_plans: list[tuple[CatCard, CatCard]] = []
        self.ai_attack_plans: list[tuple[CatCard, CatCard]] = []

        self.game_over_message: Optional[str] = None

    # ===================================================================
    # TURN FLOW
    # ===================================================================

    def start_new_turn(self):
        """Reset energy, clear planning, refresh cats."""
        self.phase = Phase.PLAYER_PLANNING
        self.player_energy = self.max_energy
        self.ai_energy = self.max_energy

        self.selected_player_cat = None
        self.awaiting_attack_target = False

        self.player_attack_plans.clear()
        self.ai_attack_plans.clear()

        # Reset status flags on all cats
        for cat in self.player_cats + self.ai_cats:
            cat.reset_for_new_turn()

        # (Optional) AI could plan here; we'll do it when resolving instead.

    def update(self):
        """GameState isn't doing any per-frame animation yet."""
        if self.phase == Phase.GAME_OVER:
            return
        # No automatic changes to cat lists here!

    # ===================================================================
    # PLAYER INPUT HELPERS
    # ===================================================================

    def select_player_cat(self, cat: CatCard):
        """Highlight the chosen cat."""
        if self.phase != Phase.PLAYER_PLANNING:
            return
        if cat not in self.player_cats:
            return

        # Clear selection first
        for c in self.player_cats:
            c.is_selected = False

        self.selected_player_cat = cat
        cat.is_selected = True
        self.awaiting_attack_target = False

    def player_choose_attack(self):
        """
        Player clicked 'ATTACK' on the radial menu.
        Next click on an AI cat will choose the target.
        """
        if self.phase != Phase.PLAYER_PLANNING:
            return
        if not self.selected_player_cat:
            return

        attacker = self.selected_player_cat

        # Check energy and attack availability
        if not attacker.can_attack:
            return
        if self.player_energy < attacker.attack_cost:
            return

        # Wait for target click
        self.awaiting_attack_target = True

    def player_assign_attack_target(self, target: CatCard):
        """
        Player clicked an AI cat as the target.
        """
        if self.phase != Phase.PLAYER_PLANNING:
            return
        if not self.awaiting_attack_target:
            return
        if not self.selected_player_cat:
            return
        if target not in self.ai_cats:
            return

        attacker = self.selected_player_cat

        if not attacker.can_attack:
            return
        if self.player_energy < attacker.attack_cost:
            return

        # Spend energy and register the attack
        self.player_energy -= attacker.attack_cost
        attacker.can_attack = False
        attacker.has_planned_attack = True
        attacker.planned_attack_target = target

        self.player_attack_plans.append((attacker, target))

        # Done choosing target
        self.awaiting_attack_target = False

    def player_use_item(self, item: ItemCard, target: CatCard):
        """
        Player dragged an item onto a friendly cat.
        Effect resolves immediately (before the combat phase).
        """
        if self.phase != Phase.PLAYER_PLANNING:
            return
        if item not in self.player_items:
            return
        if target not in self.player_cats:
            return

        if self.player_energy < item.cost:
            return

        # Pay cost
        self.player_energy -= item.cost

        # Apply item effect
        if item.effect_type == "heal":
            target.current_health = min(
                target.max_health, target.current_health + item.value
            )
        elif item.effect_type == "armor":
            target.armor += item.value
        elif item.effect_type == "shield":
            target.shield_active = True
        elif item.effect_type == "refresh":
            target.can_attack = True

        # Remove item from hand
        if item in self.player_items:
            self.player_items.remove(item)

    def player_confirm(self):
        """
        Player is done planning; resolve the turn:
        - AI picks simple attacks
        - All attacks resolve simultaneously
        - Remove dead cats
        - Either start a new turn or end the game
        """
        if self.phase != Phase.PLAYER_PLANNING:
            return

        self.phase = Phase.RESOLVE

        # Have AI plan some very simple attacks
        self._ai_plan_attacks()

        # Resolve all damage at once
        self._resolve_combat()

        # Remove dead cats
        self._remove_dead_cats()

        # Check win/lose
        if not self.player_cats:
            self.phase = Phase.GAME_OVER
            self.game_over_message = "You lost! All your cats are defeated."
            return
        if not self.ai_cats:
            self.phase = Phase.GAME_OVER
            self.game_over_message = "You win! All enemy cats are defeated."
            return

        # If game continues, next turn
        self.turn_number += 1
        self.start_new_turn()

    # ===================================================================
    # AI HELPERS
    # ===================================================================

    def _ai_plan_attacks(self):
        """Very simple AI: each cat attacks a random living player cat."""
        self.ai_attack_plans.clear()

        if not self.player_cats:
            return

        for attacker in self.ai_cats:
            if not attacker.can_attack:
                continue
            if self.ai_energy < attacker.attack_cost:
                continue

            # Pick a random living player cat
            alive_targets = [c for c in self.player_cats if c.current_health > 0]
            if not alive_targets:
                break

            import random

            target = random.choice(alive_targets)

            self.ai_energy -= attacker.attack_cost
            attacker.can_attack = False
            attacker.has_planned_attack = True
            attacker.planned_attack_target = target
            self.ai_attack_plans.append((attacker, target))

    # ===================================================================
    # COMBAT RESOLUTION
    # ===================================================================

    def _resolve_combat(self):
        """
        Apply all damage simultaneously.
        """
        damage_map: dict[CatCard, int] = {}

        def deal(attacker: CatCard, target: CatCard):
            if attacker.current_health <= 0:
                return
            if target.current_health <= 0:
                return
            damage_map[target] = damage_map.get(target, 0) + attacker.attack

        # Player attacks
        for attacker, target in self.player_attack_plans:
            deal(attacker, target)

        # AI attacks
        for attacker, target in self.ai_attack_plans:
            deal(attacker, target)

        # Apply damage using cat.apply_damage (handles armor / shield)
        for target, dmg in damage_map.items():
            if target.current_health > 0:
                target.apply_damage(dmg)

    def _remove_dead_cats(self):
        """Strip out defeated cats from each side."""
        self.player_cats = [c for c in self.player_cats if not c.is_dead()]
        self.ai_cats = [c for c in self.ai_cats if not c.is_dead()]
