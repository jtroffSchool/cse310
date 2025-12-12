"""
actions.py

Defines the action system for simultaneous-turn resolution.

Each action is stored as a TurnAction object, and all actions
from both the player and AI are resolved together in a clean,
deterministic order:

1. Apply all item effects (heal, armor, shield, refresh)
2. Resolve all attacks simultaneously
3. Process deaths
4. Cleanup action references
"""

class TurnAction:
    """
    Represents a single action in the simultaneous turn system.
    Supports:
    - "attack"
    - "heal"
    - "armor"
    - "shield"
    - "refresh"
    """

    def __init__(self, action_type, source=None, target=None, value=None, item_used=None):
        self.action_type = action_type  # "attack", "heal", etc.

        # For attacks: source = cat, target = enemy cat
        # For items: source = player, target = friendly cat, item_used = ItemCard
        self.source = source
        self.target = target
        self.value = value
        self.item_used = item_used

    def __repr__(self):
        return f"TurnAction({self.action_type}, src={self.source}, tgt={self.target}, val={self.value})"



# ============================================================
# ACTION QUEUE FOR SIMULTANEOUS TURN RESOLUTION
# ============================================================

class ActionQueue:
    """
    Manages all actions collected during the planning phase
    and resolves them in correct order for simultaneous turns.
    """

    def __init__(self):
        self.actions = []

    # --------------------------------------------------------
    def add(self, action: TurnAction):
        self.actions.append(action)

    # --------------------------------------------------------
    def clear(self):
        self.actions.clear()

    # --------------------------------------------------------
    def resolve_all(self):
        """
        Execute all actions in the correct simultaneous-turn order.

        ORDER:
            1. Healing
            2. Armor
            3. Shield
            4. Refresh (allows cat to attack again)
            5. Attacks (simultaneous)
            6. Apply final deaths

        Returns:
            dead_cats → list of units that died this turn
        """

        # Separate actions by type
        heal_actions = [a for a in self.actions if a.action_type == "heal"]
        armor_actions = [a for a in self.actions if a.action_type == "armor"]
        shield_actions = [a for a in self.actions if a.action_type == "shield"]
        refresh_actions = [a for a in self.actions if a.action_type == "refresh"]
        attack_actions = [a for a in self.actions if a.action_type == "attack"]

        # =====================================================
        # 1. HEALING (items)
        # =====================================================
        for action in heal_actions:
            if action.target and not action.target.is_dead():
                healed_amount = min(
                    action.value,
                    action.target.max_health - action.target.current_health
                )
                action.target.current_health += healed_amount

        # =====================================================
        # 2. ARMOR
        # =====================================================
        for action in armor_actions:
            if action.target and not action.target.is_dead():
                action.target.armor += action.value

        # =====================================================
        # 3. SHIELDS
        # =====================================================
        for action in shield_actions:
            if action.target and not action.target.is_dead():
                action.target.shield_active = True

        # =====================================================
        # 4. REFRESH (allows second attack)
        # =====================================================
        for action in refresh_actions:
            if action.target and not action.target.is_dead():
                action.target.can_attack = True

        # =====================================================
        # 5. ATTACKS (SIMULTANEOUS)
        # =====================================================

        # First gather all attack outcomes without applying deaths
        damage_results = []  # (attacker, defender, final_damage)

        for action in attack_actions:
            attacker = action.source
            defender = action.target

            if attacker is None or defender is None:
                continue

            if attacker.is_dead():
                # Still deals damage anyway! (simultaneous rule)
                pass

            raw_damage = attacker.attack
            final_damage = defender.apply_damage(raw_damage)

            damage_results.append((attacker, defender, final_damage))

        # =====================================================
        # 6. PROCESS DEATHS
        # =====================================================

        dead_cats = []
        for _, defender, _ in damage_results:
            if defender.is_dead() and defender not in dead_cats:
                dead_cats.append(defender)

        # Also check attackers (they may have died from item effects)
        for attacker, _, _ in damage_results:
            if attacker.is_dead() and attacker not in dead_cats:
                dead_cats.append(attacker)

        # Remove references from dead cats
        for cat in dead_cats:
            cat.planned_attack_target = None
            cat.planned_item_effects = []
            cat.has_planned_attack = False

        # Clean up for next turn
        self.clear()

        return dead_cats
