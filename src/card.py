class Card:
    
    def __init__(self, name, table_value, hand_value):
        self.name = name
        self.table_value = table_value
        self.hand_value = hand_value
        
    def __str__(self):
        return self.name 