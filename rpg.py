import random

player = {
    "name": "Mario",
    "hp": 30,
    "fp": 10,
    "attack": (4, 8),
    "inventory": ["Mushroom", "Poison Mushroom"],
    "location": (1, 1),
}

world_map = {
    (1, 1): "Peach's Castle Courtyard",
    (1, 2): "Goomba Hills",
    (2, 1): "Yoshi's Island",
}

enemies = [
    {"name": "Goomba", "hp": 10, "attack": (2, 4)},
    {"name": "Koopa", "hp": 12, "attack": (3, 6)},
]

def use_item():
    print("Your inventory:", player["inventory"])
    item = input("Which item do you want to use? ").strip().title()
    if item not in player["inventory"]:
        print("You don’t have that!")
        return
    if item == "Mushroom":
        print("You eat a Mushroom. Mmm... Tasty!")
        player["hp"] += 10
        player["inventory"].remove("Mushroom")
        print(f"Your HP is now {player['hp']}")
    elif item == "Poison Mushroom":
        print("You look at the Poison Mushroom.")
        print("It looks suspicious... but you eat it anyway.")
        print("You feel a strange tingle...")
        print("Your vision fades... Was this really worth it?")
        print("Mario collapses dramatically. The Toads will sing sad songs.")
        player["hp"] = 0

def fight(enemy):
    print(f"A wild {enemy['name']} appears!")
    while enemy["hp"] > 0 and player["hp"] > 0:
        print(f"\nYour HP: {player['hp']} | {enemy['name']} HP: {enemy['hp']}")
        action = input("Attack, Use, or Run? ").lower()
        if action == "attack":
            dmg = random.randint(*player["attack"])
            enemy["hp"] -= dmg
            print(f"You hit the {enemy['name']} for {dmg} damage.")
        elif action == "use":
            use_item()
            if player["hp"] <= 0:
                break
        elif action == "run":
            print("You ran away!")
            return True
        else:
            print("Invalid action.")

        if enemy["hp"] > 0:
            dmg = random.randint(*enemy["attack"])
            player["hp"] -= dmg
            print(f"{enemy['name']} hits you for {dmg} damage.")

    if player["hp"] <= 0:
        print("You were defeated!")
        return False
    print(f"You defeated the {enemy['name']}!")
    return True

def explore():
    print(f"You are at {world_map[player['location']]}")
    if random.random() < 0.5:
        enemy = random.choice(enemies)
        return fight(enemy)
    else:
        print("It's quiet... maybe too quiet.")
        return True

def move():
    x, y = player["location"]
    direction = input("Which direction? (n/s/e/w): ").lower()
    new_pos = {
        "n": (x - 1, y),
        "s": (x + 1, y),
        "e": (x, y + 1),
        "w": (x, y - 1)
    }.get(direction)

    if new_pos in world_map:
        player["location"] = new_pos
        print(f"You moved to {world_map[new_pos]}")
        return explore()
    else:
        print("You can't go that way.")
        return True

def game_loop():
    print("🎮 Welcome to Mario's Mini RPG")
    print("Type 'move', 'explore', 'use', or 'quit'")

    while player["hp"] > 0:
        command = input("> ").lower()
        if command == "move":
            if not move():
                break
        elif command == "explore":
            if not explore():
                break
        elif command == "use":
            use_item()
        elif command == "quit":
            print("Goodbye!")
            break
        else:
            print("Unknown command.")

    if player["hp"] <= 0:
        print("\nGAME OVER.")

if __name__ == "__main__":
    game_loop()
