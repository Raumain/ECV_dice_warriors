from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from character import Mage, Thief, Warrior
from dice import Dice

console = Console()

# Dans une classe `StartPanel` :
# Créer un panel interactif dans lequel on peut choisir différentes options :
# -Attack
# -Potion
# -Give up
# Les options doivent être séléctionnable via les flèches du clavier
# et validable via la touche entrée


class StartPanel:
    def __init__(self, characters):
        self._characters = characters

    def display(self):
        console.print(Panel("Welcome to the Arena !",
                      title="[yellow]Arena", border_style="yellow"))

    def choose_character(self):
        text = ""
        for i, character in enumerate(self._characters):
            text += f"{i+1}. {character._label} {character._name}\n"
        console.print(
            Panel(text, title="[blue]Characters", border_style="blue"))
        choice = int(Prompt.ask("Choose a character: "))
        return self._characters[choice-1]

    def choose_opponent(self, character):
        text = ""
        for i, opponent in enumerate(self._characters):
            if (opponent != character):
                text += f"{i+1}. {opponent._label} {opponent._name}\n"
        console.print(Panel(text, title="[red]Opponents", border_style="red"))
        choice = int(Prompt.ask("Choose an opponent: "))
        return self._characters[choice-1]

    def choose_action(self):
        text = ""
        text += "1. Attack\n"
        text += "2. Potion\n"
        text += "3. Give up\n"
        console.print(
            Panel(text, title="[green]Actions", border_style="green"))
        choice = int(Prompt.ask("Choose an action: "))
        return choice

    def choose_potion(self):
        text = ""
        text += "1. Heal\n"
        text += "2. Attack\n"
        console.print(
            Panel(text, title="[green]Potions", border_style="green"))
        choice = int(Prompt.ask("Choose a potion: "))
        return choice

    def choose_potion_target(self, character):
        text = ""
        for i, opponent in enumerate(self._characters):
            if (opponent != character):
                text += f"{i+1}. {opponent._label} {opponent._name}\n"
        console.print(Panel(text, title="[red]Targets", border_style="red"))
        choice = int(Prompt.ask("Choose a target: "))
        return self._characters[choice-1]

    def choose_attack_target(self, character):
        text = ""
        for i, opponent in enumerate(self._characters):
            if (opponent != character):
                text += f"{i+1}. {opponent._label} {opponent._name}\n"
        console.print(Panel(text, title="[red]Targets", border_style="red"))
        choice = int(Prompt.ask("Choose a target: "))
        return self._characters[choice-1]

    def choose_attack(self, character):
        text = ""
        text += "1. Normal attack\n"
        if (type(character) == Warrior):
            text += "2. Axe in face\n"
        if (type(character) == Mage):
            text += "2. Magic attack\n"
        if (type(character) == Thief):
            text += "2. Backstab\n"
        console.print(Panel(text, title="[red]Attacks", border_style="red"))
        choice = int(Prompt.ask("Choose an attack: "))
        return choice

    def choose_attack_roll(self, character):
        text = ""
        text += "1. Normal roll\n"
        if (type(character) == Warrior):
            text += "2. Bonus roll\n"
        if (type(character) == Mage):
            text += "2. Magic roll\n"
        if (type(character) == Thief):
            text += "2. Backstab roll\n"
        console.print(Panel(text, title="[red]Rolls", border_style="red"))
        choice = int(Prompt.ask("Choose a roll: "))
        return choice

    def choose_defense_roll(self, character):
        text = ""
        text += "1. Normal roll\n"
        if (type(character) == Mage):
            text += "2. Magic roll\n"
        console.print(Panel(text, title="[red]Rolls", border_style="red"))
        choice = int(Prompt.ask("Choose a roll: "))
        return choice

    def choose_defense(self, character):
        text = ""
        text += "1. Normal defense\n"
        if (type(character) == Mage):
            text += "2. Magic defense\n"
        console.print(Panel(text, title="[red]Defenses", border_style="red"))
        choice = int(Prompt.ask("Choose a defense: "))
        return choice


if __name__ == "__main__":
    warrior = Warrior("Tom", 20, 8, 3, Dice(6))
    mage = Mage("Gandalf", 20, 8, 3, Dice(6))
    thief = Thief("Jean", 20, 8, 3, Dice(6))
    cars = [warrior, mage, thief]
    start_panel = StartPanel(cars)
    start_panel.display()
    character = start_panel.choose_character()
    opponent = start_panel.choose_opponent(character)
    print(f"You: {character._label} {character._name}")
    print(f"Opponent: {opponent._label} {opponent._name}")

    while character.is_alive() and opponent.is_alive():
        action = start_panel.choose_action()
        if (action == 1):
            attack = start_panel.choose_attack(character)
            attack_roll = start_panel.choose_attack_roll(character)
            attack_target = start_panel.choose_attack_target(character)
            character.attack(attack_target, attack, attack_roll)
        elif (action == 2):
            potion = start_panel.choose_potion()
            potion_target = start_panel.choose_potion_target(character)
            character.potion(potion_target, potion)
        elif (action == 3):
            character.give_up()
        else:
            print("Invalid action")
        if (opponent.is_alive()):
            opponent.attack(character)

    if character.is_alive():
        print(f"{character._name} won !")
    else:
        print(f"{opponent._name} won !")

    print("Game over !")
