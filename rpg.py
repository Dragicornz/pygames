# === Shadow RPG ===
import random
import json
import os

player = {
    "name": "Shadow",
    "hp": 30,
    "mp": 10,
    "attack": (4, 8),
    "inventory": ["Healing Potion"],
    "spells": {
        "Fireball": {"cost": 3, "damage": (6, 12)},
        "Ice Shard": {"cost": 2, "damage": (4, 8)}
    },
    "location": (1, 1),
    "quests": {}
}

world_map = {
    (0, 0): "Ruins of an ancient tower.",
    (0, 1): "A cold forest with whispering winds.",
    (0, 2): "A rocky mountain path.",
    (1, 0): "A quiet riverbank.",
    (1, 1): "An empty clearing with burnt grass. You feel watched.",
    (1, 2): "Dark cave entrance. Faint growls echo inside.",
    (2, 0): "A sunlit field with chirping insects.",
    (2, 1): "A broken shrine to forgotten gods.",
    (2, 2): "A small abandoned village."
}

monsters = [
    {"name": "Goblin", "hp": 10, "attack": (2, 4)},
    {"name": "Slime", "hp": 12, "attack": (1, 3)},
    {"name": "Orc", "hp": 15, "attack": (3, 6)},
]

def save_game():
    with open("savegame.json", "w") as f:
        json.dump(player, f)
    print("Game saved.")

def load_game():
    if os.path.exists("savegame.json"):
        with open("savegame.json", "r") as f:
            data = json.load(f)
            player.update(data)
        print("Game loaded.")
    else:
        print("No saved game found.")

def use_item():
    if "Healing Potion" in player["inventory"]:
        print("You used a Healing Potion.")
        player["hp"] += 10
        player["inventory"].remove("Healing Potion")
        print(f"HP restored to {player['hp']}")
    else:
        print("You have no potions.")

def cast_spell(monster):
    print("\nSpells:")
    for i, spell in enumerate(player["spells"]):
        s = player["spells"][spell]
        print(f"{i + 1}. {spell} (Cost: {s['cost']}, Damage: {s['damage']})")
    choice = input("Choose a spell: ")
    spell_names = list(player["spells"].keys())
    if not choice.isdigit() or int(choice) - 1 not in range(len(spell_names)):
        print("Invalid choice.")
        return
    spell = spell_names[int(choice) - 1]
    s = player["spells"][spell]
    if player["mp"] < s["cost"]:
        print("Not enough MP.")
        return
    player["mp"] -= s["cost"]
    dmg = random.randint(*s["damage"])
    monster["hp"] -= dmg
    print(f"You cast {spell} and deal {dmg} damage.")

def fight(monster):
    print(f"A wild {monster['name']} appears!")
    while monster["hp"] > 0 and player["hp"] > 0:
        print(f"HP: {player['hp']}  MP: {player['mp']}  |  {monster['name']} HP: {monster['hp']}")
        print("1. Attack  2. Cast Spell  3. Use Potion")
        choice = input("Action: ")
        if choice == '1':
            dmg = random.randint(*player["attack"])
            monster["hp"] -= dmg
            print(f"You hit the {monster['name']} for {dmg} damage.")
        elif choice == '2':
            cast_spell(monster)
        elif choice == '3':
            use_item()
        else:
            print("Invalid action.")
            continue

        if monster["hp"] <= 0:
            print(f"You defeated the {monster['name']}!")
            player["inventory"].append("Healing Potion")
            print("You found a Healing Potion.")
            break

        enemy_dmg = random.randint(*monster["attack"])
        player["hp"] -= enemy_dmg
        print(f"The {monster['name']} hits you for {enemy_dmg} damage.")

    return player["hp"] > 0

def explore():
    location = player["location"]
    print(f"You are at: {world_map.get(location, 'Unknown area.')}")
    if random.random() < 0.4:
        monster = random.choice(monsters)
        survived = fight(monster)
        if not survived:
            print("You have been defeated.")
            return False
    return True

def move():
    x, y = player["location"]
    print("Move direction: n/s/e/w")
    d = input("Direction: ").lower()
    new_loc = {
        'n': (x - 1, y),
        's': (x + 1, y),
        'e': (x, y + 1),
        'w': (x, y - 1)
    }.get(d)

    if new_loc in world_map:
        player["location"] = new_loc
        print(f"You move {d}.")
        return explore()
    else:
        print("You can't go that way.")
        return True

def game_loop():
    print("Welcome, Shadow. Type help for options.")
    while player["hp"] > 0:
        command = input("\n> ").lower()
        if command in ["move", "go"]:
            if not move():
                break
        elif command == "explore":
            if not explore():
                break
        elif command == "inventory":
            print("Inventory:", player["inventory"])
        elif command == "save":
            save_game()
        elif command == "load":
            load_game()
        elif command == "help":
            print("Commands: move, explore, inventory, save, load, help, quit")
        elif command == "quit":
            print("Goodbye.")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    game_loop()
