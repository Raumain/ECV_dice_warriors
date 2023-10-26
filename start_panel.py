from rich import print
from rich.panel import Panel

from character import Character, Mage, Thief, Warrior
from dice import Dice


# Créer une class `StartPanel` qui contient différentes méthodes :
# - `display` qui affiche le panel de démarrage
# - `choose_character` qui demande à l'utilisateur de choisir un personnage
# - `choose_opponent` qui demande à l'utilisateur de choisir un adversaire
# Il y a 3 classes de personnages : `Warrior`, `Mage` et `Thief`
# Le tout doit être présenté dans un seul et unique panel de la librairie Rich
# Le déroulement est le suivant :
# - Afficher le panel de démarrage
# - Demander à l'utilisateur de choisir un personnage
# - Demander à l'utilisateur de choisir un adversaire
# - Lancer le combat


class StartPanel:
    def __init__(self, characters):
        self._characters = characters

    def display(self):
        print(Panel("Welcome to the Arena !",
              title="[yellow]Arena", border_style="yellow"))

    def choose_character(self):
        text = ""
        for i, character in enumerate(self._characters):
            text += f"{i+1}. {character._label} {character._name}\n"
        print(Panel(text, title="[blue]Characters", border_style="blue"))
        choice = int(input("Choose a character: "))
        return self._characters[choice-1]

    def choose_opponent(self, character):
        text = ""
        for i, opponent in enumerate(self._characters):
            if (opponent != character):
                text += f"{i+1}. {opponent._label} {opponent._name}\n"
        print(Panel(text, title="[red]Opponents", border_style="red"))
        choice = int(input("Choose an opponent: "))
        return self._characters[choice-1]

    def choose_action(self, character: Character):
        text = ""
        text += "1. Attack\n"
        text += f"2. Potion (x{character._potions})\n"
        text += "3. Give up\n"
        print(
            Panel(text, title="[green]Actions", border_style="green"))
        choice = int(input("Choose an action: "))
        return choice
    
    def choose_attack(self, character):
        text = ""
        text += "1. Normal attack\n"
        if (type(character) == Warrior):
            text += "2. Axe in face (deals +5 damages but has 50% chances to harm yourself for 2 wounds instead)\n"
        if (type(character) == Mage):
            text += "2. Magic attack (deals damages -3 but heals 1-4 HP)\n"
        if (type(character) == Thief):
            text += "2. Backstab (ignore opponent defense but either gain 1 attack point or lose it )\n"
        print(Panel(text, title="[red]Attacks", border_style="red"))
        choice = int(input("Choose an attack: "))
        return choice


if __name__ == "__main__":
    start_panel = StartPanel()
    start_panel.display()
    character = start_panel.choose_character()
    opponent = start_panel.choose_opponent(character)
    print(f"You: {character._label} {character._name}")
    print(f"Opponent: {opponent._label} {opponent._name}")
