import random

def une_fonction():
    pass

class Dice:
    
    def __init__(self, faces):
        self._faces = faces
    
    def roll(self):
        return random.randint(1, self._faces)
    
    def __str__(self):
        return f"I'm a dice with {self._faces} faces"
    
class RiggedDice(Dice):
    
    def roll(self, rigged = False):
        
        return self._faces if rigged else super().roll()
    
if __name__ == "__main__":  
    a_dice = Dice(6)
    print(a_dice)

    # for i in range(0, 10):
    #     print(a_dice.roll())
        
    a_rigged_dice = RiggedDice(20)
    print(a_rigged_dice.roll())
    print(a_rigged_dice.roll(True))