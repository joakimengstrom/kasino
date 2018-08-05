class Player:
    
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.mokki = 0
        self.cards_hand = []
        self.cards_deck = []
        
    def __str__(self):
        return self.name