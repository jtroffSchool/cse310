from cat_card import CatCard
from item_card import ItemCard
import os

print("Image exists?", os.path.exists("assets/laser_cat.png"))

# ===============================================================
# CAT DECK
# ===============================================================

def build_cat_deck():
    """
    Creates the deck of Cat Units.
    IMPORTANT: we create NEW CatCard instances for each card,
    so the player and AI don't share the same objects.
    """

    # Define templates once
    templates = [
        dict(
            name="Laser Cat",
            max_health=6,
            attack=4,
            cat_type="Tech",
            rarity="Rare",
            description="Shoots searing laser beams.",
            image_path="assets/laser_cat.png",
            attack_cost=3,
        ),
        dict(
            name="Chonky Cat",
            max_health=10,
            attack=2,
            cat_type="Earth",
            rarity="Common",
            description="Immovable and extremely fluffy.",
            image_path="assets/chonky_cat.png",
            attack_cost=2,
        ),
        dict(
            name="Ninja Cat",
            max_health=4,
            attack=5,
            cat_type="Shadow",
            rarity="Uncommon",
            description="Strikes fast and vanishes.",
            image_path="assets/ninja_cat.png",
            attack_cost=4,
        ),
        dict(
            name="Wizard Cat",
            max_health=5,
            attack=3,
            cat_type="Magic",
            rarity="Rare",
            description="Casts magical furball spells.",
            image_path="assets/wizard_cat.png",
            attack_cost=2,
        ),
    ]

    deck: list[CatCard] = []

    # Make 5 copies of each template as *new objects*
    for _ in range(5):
        for t in templates:
            deck.append(CatCard(**t))

    return deck


# ===============================================================
# ITEM DECK
# ===============================================================

def build_item_deck():
    """
    Creates the deck of items available for the player and AI.
    We also make NEW ItemCard instances so they are independent.
    """

    templates = [
        dict(
            name="Laser Light",
            effect_type="shield",
            value=1,
            cost=2,
            description="Distracts enemy; the next incoming attack deals 0 damage.",
            image_path="assets/laser_light.png",
        ),
        dict(
            name="Cat Food",
            effect_type="heal",
            value=3,
            cost=2,
            description="Heals a cat for 3 HP.",
            image_path="assets/cat_food.png",
        ),
        dict(
            name="Cat Tree",
            effect_type="armor",
            value=2,
            cost=3,
            description="Gives a cat +2 armor.",
            image_path="assets/cat_tree.png",
        ),
        dict(
            name="Catnip Toy",
            effect_type="refresh",
            value=1,
            cost=3,
            description="Refreshes the cat, allowing it to attack again this turn.",
            image_path="assets/catnip_toy.png",
        ),
    ]

    items: list[ItemCard] = []

    # Two copies of each, as distinct objects
    for _ in range(2):
        for t in templates:
            items.append(ItemCard(**t))

    return items
