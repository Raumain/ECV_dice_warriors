import random
from rich import print
from rich.pretty import pprint
from dice import Dice
from character import Character, Mage, Warrior, Thief
from start_panel import StartPanel


def autoplay(opponent: Character, character: Character):
    action = random.randint(1, 2)
    if (action == 1):
        attackOption = random.randint(1, 2)
        opponent.attack(character, attackOption)
    else:
        opponent.drink_potion()


def main():
    warrior = Warrior("Tom", 20, 8, 3, Dice(6))
    mage = Mage("Gandalf", 20, 8, 3, Dice(6))
    thief = Thief("Jean", 20, 8, 3, Dice(6))
    cars = [warrior, mage, thief]
    startPanel = StartPanel(cars)
    startPanel.display()
    character: Character = startPanel.choose_character()
    opponent: Character = startPanel.choose_opponent(character)
    print(f"You: {character._label} {character._name}")
    print(f"Opponent: {opponent._label} {opponent._name}")
    print("Let's fight !")
    while character.is_alive() and opponent.is_alive():
        action = startPanel.choose_action(character)
        if (action == 1):
            attackOption = startPanel.choose_attack(character)
            character.attack(opponent, attackOption)
            autoplay(opponent, character)
        elif (action == 2):
            character.drink_potion()
            autoplay(opponent, character)
        else:
            print(f"{character._name} gave up !")
            character.update_health(-character._health)
            break
        # autoplay(opponent, character)
    if character.is_alive():
        print(f"{character._name} won !")
    else:
        print(f"{opponent._name} won !")


if __name__ == "__main__":
    main()
