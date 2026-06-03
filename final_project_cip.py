import random

# ---- CLASES ----

class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.used_evasion = False
        self.used_immunity = False
        
        if player_class == "Warrior":
            self.health = 200
            self.max_health = 200
            self.abilities = {
                "1": ("Mortal Strike", 25),
                "2": ("Heroic Strike", 40),
                "3": ("Execute", 100),
                "4": ("Shield Block", 40),
                "5": ("Info", 0)
            }
        elif player_class == "Mage":
            self.health = 100
            self.max_health = 100
            self.abilities = {
                "1": ("Frostbolt", 45),
                "2": ("Arcane Blast", 60),
                "3": ("Ice Barrier", 35),
                "4": ("Ice Block", 50),
                "5": ("Info", 0)
            }
        elif player_class == "Rogue":
            self.health = 150
            self.max_health = 150
            self.abilities = {
                "1": ("Sinister Strike", 30),
                "2": ("Slice and Dice", 45),
                "3": ("Cloak of Shadows", 40),
                "4": ("Vanish", 30),
                "5": ("Info", 0)
            }

    def immunity_attack(self, enemy):
        ability_name, damage = self.abilities["3"]
        self.used_immunity = True
        enemy.health -= damage
        return f"{ability_name} deals {damage} damage! (50% chance to dodge incoming attack)"

    def attack(self, ability_key, enemy):
        ability_name, damage = self.abilities[ability_key]
        verificar_vida = (30 * enemy.max_health) / 100
        
        if self.player_class == "Warrior" and ability_key == "3":
            if enemy.health <= verificar_vida:
                enemy.health -= damage
                return f"EXECUTE! {ability_name} deals {damage} damage!"
            else:
                return f"Execute can only be used when enemy is below 30% HP!"

        if self.player_class == "Rogue" and ability_key == "2":
            if random.random() < 0.4:
                damage = damage * 2
                enemy.health -= damage
                return f"CRITICAL HIT! {ability_name} deals {damage} damage!"
            else:
                enemy.health -= damage
                return f"{ability_name} deals {damage} damage!"

        enemy.health -= damage
        return f"{ability_name} deals {damage} damage!"

    def heal(self, ability_key):
        heal_amounts = {
            "Warrior": 40,
            "Mage": 50,
            "Rogue": 30
        }
        heal_amount = heal_amounts[self.player_class]
        self.health = min(self.health + heal_amount, self.max_health)
        self.used_evasion = True
        return f"You heal for {heal_amount} HP!"


class Enemy:
    def __init__(self, name, health, damage):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage

    def attack(self, player):
        actual_damage = random.randint(self.damage - 5, self.damage + 5)

        if player.used_evasion:
            player.used_evasion = False
            dodge_chance = {
                "Warrior": 0.5,
                "Mage": 1.0,
                "Rogue": 0.7
            }
            if random.random() < dodge_chance[player.player_class]:
                return "Dodge!! No damage taken!"

        if player.used_immunity:
            player.used_immunity = False
            if random.random() < 0.5:
                return "Immune! No damage taken!"

        player.health -= actual_damage
        return f"{self.name} attacks you for {actual_damage} damage!"

# ---- LÓGICA DEL JUEGO ----

def choose_class():
    print("Choose your class:")
    print("1. Warrior  - 200 HP | High physical damage | Execute & Shield Block")
    print("2. Mage     - 100 HP | Powerful spells      | Ice Barrier & Ice Block")
    print("3. Rogue    - 150 HP | Critical hits        | Cloak of Shadows & Vanish")
    
    while True:
        choice = input("Enter 1, 2 or 3: ")
        if choice == "1":
            return "Warrior"
        elif choice == "2":
            return "Mage"
        elif choice == "3":
            return "Rogue"
        else:
            print("Invalid option. Please enter 1, 2 or 3.")


def health_bar(current, max_hp):
    filled = int((current / max_hp) * 10)
    return "[" + "█" * filled + "░" * (10 - filled) + "]"


def show_status(player, enemy, turn, messages=None):
    print("\n" + "=" * 60)
    print(f"{'⚔  TURN ' + str(turn) + '  ⚔':^60}")
    print("=" * 60)
    print(f"  {player.name} ({player.player_class})")
    print(f"  HP: {player.health}/{player.max_health}  {health_bar(player.health, player.max_health)}")
    print("-" * 60)
    print(f"  {enemy.name}")
    print(f"  HP: {enemy.health}/{enemy.max_health}  {health_bar(enemy.health, enemy.max_health)}")
    if messages:
        print("-" * 60)
        for msg in messages:
            print(f"  > {msg}")
    print("=" * 60)


def player_turn(player, enemy):
    while True:
        print("\nChoose your action:")
        for key, (name, value) in player.abilities.items():
            if key == "4" or key == "5":
                print(f"  {key}. {name}")
            else:
                print(f"  {key}. {name} (Damage: {value})")

        choice = input("Enter 1-5: ")

        if choice == "5":
            print("\n=== ABILITIES INFO ===")
            if player.player_class == "Warrior":
                print("  1. Mortal Strike  - Deals 25 damage")
                print("  2. Heroic Strike  - Deals 40 damage")
                print("  3. Execute        - Deals 100 damage (only below 30% enemy HP)")
                print("  4. Shield Block   - Heal 40 HP + 50% chance to dodge next attack")
            elif player.player_class == "Mage":
                print("  1. Frostbolt      - Deals 45 damage")
                print("  2. Arcane Blast   - Deals 60 damage")
                print("  3. Ice Barrier    - Deals 35 damage + 50% chance to dodge")
                print("  4. Ice Block      - Heal 50 HP + 100% dodge next attack")
            elif player.player_class == "Rogue":
                print("  1. Sinister Strike - Deals 30 damage")
                print("  2. Slice and Dice  - Deals 45 damage (40% chance crit x2)")
                print("  3. Cloak of Shadows- Deals 40 damage + 50% chance to dodge")
                print("  4. Vanish          - Heal 30 HP + 70% dodge next attack")
            print("======================")

        elif choice in ["1", "2", "3", "4"]:
            if choice == "4":
                return player.heal(choice)
            elif choice == "3":
                if player.player_class == "Warrior":
                    return player.attack("3", enemy)
                else:
                    return player.immunity_attack(enemy)
            else:
                return player.attack(choice, enemy)
        else:
            print("Invalid option. Please enter 1-5.")


def combat(player, enemy):
    turn = 1
    print("\n" + "=" * 60)
    print(f"  A wild {enemy.name} appears!")
    print("=" * 60)
    
    while player.health > 0 and enemy.health > 0:
        show_status(player, enemy, turn)
        player_msg = player_turn(player, enemy)
        
        if enemy.health <= 0:
            show_status(player, enemy, turn, [player_msg, f"You defeated {enemy.name}!"])
            return True
        
        enemy_msg = enemy.attack(player)
        show_status(player, enemy, turn, [player_msg, enemy_msg])
        
        if player.health <= 0:
            print("\n  You died... Game Over.")
            return False
        
        turn += 1
    
    return False


def main():
    print("=" * 60)
    print(f"{'⚔  Echoes of Azeroth  ⚔':^60}")
    print("=" * 60 + "\n")
    name = input("Enter your character's name: ")
    player_class = choose_class()
    player = Player(name, player_class)
    
    enemies = [
        Enemy("Murloc", 60, 10),
        Enemy("Orc Warrior", 120, 20),
        Enemy("Dragon", 200, 35)
    ]
    
    for enemy in enemies:
        result = combat(player, enemy)
        if not result:
            break
        if enemy.name != "Dragon":
            print("\n" + "=" * 60)
            print("  Prepare for the next enemy...")
            player.health = min(player.health + 30, player.max_health)
            print(f"  You recovered 30 HP! HP: {player.health}/{player.max_health}")
            print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print(f"{'🏆  YOU WIN!  🏆':^60}")
        print("=" * 60)


if __name__ == "__main__":
    main()