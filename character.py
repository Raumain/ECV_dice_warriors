from __future__ import annotations
from dice import Dice, RiggedDice

from rich import print
from rich.text import Text

print("\n")


class Character:
    _label = "Character"

    def __init__(
        self, name: str, max_health: int, attack: int, defense: int, dice: Dice
    ):
        self._name = name
        self._max_health = max_health
        self._health = self._max_health
        self._attack_value = attack
        self._defense_value = defense
        self._dice = dice
        self._potions = 2
        self.initial_stats = {
            "name": name,
            "max_health": max_health,
            "attack": attack,
            "defense": defense,
            "dice": dice,
            "potion": 2
        }

    def reset(self):
        self._name = self.initial_stats["name"]
        self._max_health = self.initial_stats["max_health"]
        self._health = self._max_health
        self._attack_value = self.initial_stats["attack"]
        self._defense_value = self.initial_stats["defense"]
        self._dice = self.initial_stats["dice"]

    def __str__(self):
        return f"{type(self)._label} {self._name} is starting the fight with {self._health}/{self._max_health}hp ({self._attack_value}atk / {self._defense_value}def)"

    def get_name(self):
        return self._name

    def get_defense_value(self):
        return self._defense_value

    def get_attack_value(self):
        return self._attack_value

    def set_defense_value(self, value):
        self._defense_value = self._defense_value + value

    def set_attack_value(self, value):
        self._attack_value = self._attack_value + value

    def is_alive(self):
        return self._health > 0

    def show_healthbar(self):
        missing_hp = self._max_health - self._health
        print(
            f"{type(self)._label} {self._name}: [{'●' * self._health}{' ' *
                                                                      missing_hp}] {self._health}/{self._max_health}hp"
        )

    def update_health(self, amount):
        if (amount > 0):
            if (self._health + amount >= self._max_health):
                self._health = self._max_health
            else:
                self._health += amount
        else:
            if (self._health + amount < 0):
                self._health = 0
            else:
                self._health += amount
        self.show_healthbar()

    def drink_potion(self):
        if (self._potions > 0):
            self._potions -= 1
            self.update_health(5)
        else:
            print("No more potions !")

    def compute_damages(self, target: Character, roll: int, option) -> int:
        return self._attack_value + roll

    def attack(self, target: Character, option):
        if self.is_alive():
            roll = self._dice.roll()
            damages = self.compute_damages(target, roll, option)
            print(
                f"⚔️ {type(self)._label} {self._name} [red]attack[/red] {target.get_name()} with {
                    damages} damages ! (attack: {self._attack_value} + roll: {roll})"
            )
            target.defense(self, damages)

    def compute_defense(self, damages, roll):
        return damages - self._defense_value - roll

    def defense(self, attacker: Character, damages: int):
        roll = self._dice.roll()
        wounds = self.compute_defense(damages, roll)
        print(
            f"🛡️ {type(self)._label} {self._name}[green]defend[/green] against {attacker.get_name()} for {damages} damages and {"[bold green]regen[/] " if wounds < 0 else "[bold red]take[/]"} {
                abs(wounds)} {"[bold green]HP[/] " if wounds < 0 else "[bold red]wounds[/]"} ! (damages: {damages} - defense: {self._defense_value} - roll: {roll})"
        )
        self.update_health(-wounds)


class Warrior(Character):
    _label = "Warrior"
    _bonus_dice = Dice(2) == 2

    def special_attack(self):
        return 5 + self.rage()

    def compute_damages(self, target, roll, option):
        if (option == 1):
            print(f"🤺 Normal attack !")
            return super().compute_damages(target, roll, option) + self.rage()
        else:
            if (self._bonus_dice):
                print(f"🪓 Axe in face ! (bonus: +5)")
                return super().compute_damages(target, roll, option) + self.special_attack()
            else:
                if (self._health > self._max_health/2):
                    print(f"🤕 Unlucky axe ! (self harmed: -2)")
                    self.update_health(-2)
                return super().compute_damages(target, roll, option) + self.rage()

    def rage(self):
        if (self._health < self._max_health/2):
            print(f"🤬 Rage ! (bonus: +{self._dice._faces})")
            return self._dice._faces
        else:
            return 0


class Mage(Character):
    _label = "Mage"
    _regen_dice = Dice(4)

    def regen(self):
        regenAmount = self._regen_dice.roll()
        return regenAmount

    def compute_damages(self, target: Character, roll: int, option) -> int:
        if (option == 1):
            print(f"🪄 Normal attack !")
            return super().compute_damages(target, roll, option)
        else:
            self.update_health(self.regen())
            print(f"🔥 Magic attack ! (bonus: -3 attack | +{self.regen()} HP)")
            return super().compute_damages(target, roll, option) - 3

    def compute_defense(self, damages, roll):
        print(f"🔮 Magic armor ! (bonus: -3)")
        return super().compute_defense(damages, roll) - 3


class Thief(Character):
    _label = "Thief"
    _bonus_dice = Dice(2).roll() == 2

    def compute_damages(self, target: Character, roll: int, option) -> int:
        if (option == 1):
            print(f"🗡️ Normal attack !")
            return super().compute_damages(target, roll, option)
        else:
            print(
                f"🤶 Sneacky sneacky... ! (bonus: +{target.get_defense_value()})")
            if (self._bonus_dice):
                if (target.get_attack_value() > target.initial_stats["attack"]/2):
                    print(f"🎲 Bonus ! Target lose 1 attack point")
                    target.set_attack_value(-1)
            else:
                print(f"🎲 Unlucky ! You lose 1 attack point")
                self.set_attack_value(-1)
            return super().compute_damages(target, roll, option) + target.get_defense_value()


if __name__ == "__main__":
    char_1: Warrior = Warrior("James", 20, 8, 3, Dice(6))
    char_2: Thief = Thief("Dina", 20, 8, 3, Dice(6))

    print(char_1)
    print(char_2)

    while char_1.is_alive() and char_2.is_alive():
        char_1.attack(char_2)
        char_2.attack(char_1)
