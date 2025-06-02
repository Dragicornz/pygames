# Mario RPG (Terminal Text-Based)
import random
import json
import os

player = {
    "name": "Mario",
    "hp": 30,
    "fp": 10,
    "attack": (4, 8),
    "inventory": ["Mushroom"],
    "special_moves": {
        "Fireball": {"cost": 3, "damage": (6, 12)},
        "Jump Attack": {"cost": 2, "damage": (4, 8)}
    },
    "location": (1, 1),
    "quests": {}
}

world_map = {
    (0, 0): "Dry Dry Desert - Scorching heat and rolling dunes.",
    (0, 1): "Goomba Forest - Rustling leaves and hidden paths.",
    (0, 2): "Koopa Cliffs - Steep paths and falling rocks.",
    (1, 0): "Toad Town - Peaceful hub of the Mushroom Kingdom.",
    (1, 1): "Peach's Castle Courtyard - All is quiet... too quiet.",
    (1, 2): "Thwomp Valley - Watch for crushing surprises.",
    (2, 0): "Yoshi's Island Beach - Calm waves and sunny skies.",
    (2, 1): "Boo Mansion - Spooky and full of secrets.",
    (2, 2): "Bowser's Keep - The final stronghold!"
}

enemies = [
    {"name": "Goomba", "hp": 10, "attack": (2, 4)},
    {"name": "Koopa Troopa", "hp": 12, "attack": (3, 5)},
    {"name": "Bob-omb", "hp": 8, "attack": (4, 6)},
]

def save_game():
    with open("mario_save.json", "w") as f:
        json.dump(player, f)
    print("Game saved.")

def load_game():
    if os.path.exists("mario_save.json"):
        with open("mario_save.json", "r") as f:
            data = json.load(f)
            player.update(data)
        print("Game loaded.")
    else:
        print("No saved game found.")

def use_item():
    if "Mushroom" in player["inventory"]:
        print("You used a Mushroom.")
        player["hp"] += 10
        player["inventory"].remove("Mushroom")
        print(f"HP restored to {player['hp']}")
    else:
        print("You have no Mushrooms.")

def use_special_move(enemy):
    print("\nSpecial Moves:")
    for i, move in enumerate(player["special_moves"]):
        s = player["special_moves"][move]
        print(f"{i + 1}. {move} (FP Cost: {s['cost']}, Damage: {s['damage']})")
    choice = input("Choose a move: ")
    move_names = list(player["special_moves"].keys())
    if not choice.isdigit() or int(choice) - 1 not in range(len(move_names)):
        print("Invalid choice.")
        return
    move = move_names[int(choice) - 1]
    s = player["special_moves"][move]
    if player["fp"] < s["cost"]:
        print("Not enough FP.")
        return
    player["fp"] -= s["cost"]
    dmg = random.randint(*s["damage"])
    enemy["hp"] -= dmg
    print(f"You used {move} and dealt {dmg} damage!")

def fight(enemy):
    print(f"A wild {enemy['name']} appears!")
    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"HP: {player['hp']}  FP: {player['fp']}  |  {enemy['name']} HP: {enemy['hp']}")
        print("1. Attack  2. Special Move  3. Use Item")
        choice = input("Action: ")
        if choice == '1':
            dmg = random.randint(*player["attack"])
            enemy["hp"] -= dmg
            print(f"You hit the {enemy['name']} for {dmg} damage.")
        elif choice == '2':
            use_special_move(enemy)
        elif choice == '3':
            use_item()
        else:
            print("Invalid action.")
            continue

        if enemy["hp"] <= 0:
            print(f"You defeated the {enemy['name']}!")
            player["inventory"].append("Mushroom")
            print("You found a Mushroom.")
            break

        enemy_dmg = random.randint(*enemy["attack"])
        player["hp"] -= enemy_dmg
        print(f"The {enemy['name']} hits you for {enemy_dmg} damage.")

    return player["hp"] > 0

def explore():
    location = player["location"]
    print(f"You are at: {world_map.get(location, 'Unknown area.')}")
    if random.random() < 0.4:
        enemy = random.choice(enemies)
        survived = fight(enemy)
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
    print("Welcome to the Mushroom Kingdom, Mario! Type help for options.")
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
