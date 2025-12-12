"""
ai_controller.py

Contains the AI logic for simultaneous-turn planning.
The AI receives:
    - enemy cats on battlefield
    - its own cats on battlefield
    - AI item hand
    - AI energy
And returns a list of TurnAction objects representing its planned actions.
"""

from actions import TurnAction
import random


class AIController:
    """
    Basic tactical AI that:
        1. Uses healing/armor/shield items on low HP or high-value allies.
        2. Uses refresh when it makes sense.
        3. Chooses the best attack target (weakest enemy, strong attacker).
        4. Never exceeds its energy budget.
        5. Plans all actions silently.
    """

    def __init__(self):
        pass

    # ==============================================================    
    # MAIN ENTRY POINT
    # ==============================================================

    def plan_turn(
        self,
        ai_cats,
        enemy_cats,
        ai_items,
        ai_energy
    ):
        """
        ai_cats:      list[CatCard]
        enemy_cats:   list[CatCard]
        ai_items:     list[ItemCard]
        ai_energy:    int

        Returns:
            planned_actions: list[TurnAction]
            remaining_energy: int
            items_to_remove: list[ItemCard]
        """

        actions = []
        items_used = []
        energy = ai_energy

        # ----------------------------------------------------------
        # 1. If no units, save all energy
        # ----------------------------------------------------------
        if len(ai_cats) == 0:
            return actions, energy, items_used

        # ----------------------------------------------------------
        # 2. ITEM PHASE — use items intelligently
        # ----------------------------------------------------------
        # Sort cats by increasing HP (heal low-health units first)
        wounded = sorted(
            [c for c in ai_cats if c.current_health < c.max_health],
            key=lambda c: c.current_health
        )

        # --- Heal low HP cats ---
        for item in ai_items:
            if item.effect_type == "heal" and energy >= item.cost:
                if len(wounded) > 0:
                    target = wounded[0]  # lowest HP cat
                    actions.append(
                        TurnAction("heal", source=None, target=target,
                                   value=item.value, item_used=item)
                    )
                    energy -= item.cost
                    items_used.append(item)

                    # Re-sort wounded after healing
                    wounded = sorted(
                        [c for c in ai_cats if c.current_health < c.max_health],
                        key=lambda c: c.current_health
                    )

        # --- Shield high-value cats (attackers or lowest HP) ---
        for item in ai_items:
            if item.effect_type == "shield" and energy >= item.cost:
                # Pick a cat that is likely to be attacked
                # Use heuristic: weakest enemy targets strongest ally
                if len(ai_cats) > 0:
                    target = sorted(ai_cats, key=lambda c: -c.attack)[0]
                    actions.append(
                        TurnAction("shield", source=None, target=target,
                                   value=1, item_used=item)
                    )
                    energy -= item.cost
                    items_used.append(item)

        # --- Armor for tanks (chonky cat or highest HP) ---
        for item in ai_items:
            if item.effect_type == "armor" and energy >= item.cost:
                target = sorted(ai_cats, key=lambda c: -c.max_health)[0]
                actions.append(
                    TurnAction("armor", source=None, target=target,
                               value=item.value, item_used=item)
                )
                energy -= item.cost
                items_used.append(item)

        # --- Refresh cats if they have high attack ---
        for item in ai_items:
            if item.effect_type == "refresh" and energy >= item.cost:
                # Refresh highest attack cat
                hitters = sorted(ai_cats, key=lambda c: -c.attack)
                if hitters:
                    target = hitters[0]
                    if not target.can_attack:
                        # Only refresh if it's already used attack
                        actions.append(
                            TurnAction("refresh", source=None, target=target,
                                       value=item.value, item_used=item)
                        )
                        energy -= item.cost
                        items_used.append(item)

        # ----------------------------------------------------------
        # 3. ATTACK PLANNING PHASE
        # ----------------------------------------------------------
        # Skip if no energy or no enemies
        if len(enemy_cats) == 0 or energy <= 0:
            return actions, energy, items_used

        # Sort enemy cats by:
        # 1. Lowest HP (easy kill)
        # 2. Highest attack (dangerous)
        targets = sorted(
            enemy_cats,
            key=lambda c: (c.current_health, -c.attack)
        )

        for cat in ai_cats:
            # Must have energy to attack
            if not cat.can_attack:
                continue
            if energy < cat.attack_cost:
                continue

            # Choose the best target
            target = targets[0]

            # Add attack action
            actions.append(
                TurnAction("attack", source=cat, target=target)
            )
            cat.has_planned_attack = True
            energy -= cat.attack_cost

            # Re-sort targets after predicting kill
            # (AI tries to coordinate attacks)
            targets = sorted(
                enemy_cats,
                key=lambda c: (c.current_health, -c.attack)
            )

        # ----------------------------------------------------------
        # Return results
        # ----------------------------------------------------------
        return actions, energy, items_used
