import random, itertools

class Round:
    # Last player who took cards from table
    last_player = None
    
    def __init__(self, next_player):
        self.table_cards = []
        self.deck_cards = []
        self.next_player = next_player
        
    def deal_cards(self, cards, players):
        random.shuffle(cards)
        for i in range(4):
            for player in players:
                player.cards_hand.append(cards.pop(0))
            self.table_cards.append(cards.pop(0))
        self.deck_cards = cards
        
    def change_player(self, players):
        if players.index(self.next_player) == len(players) - 1:
            self.next_player = players[0]
        else:
            self.next_player = players[players.index(self.next_player) + 1]
            
    def show_table_cards(self):
        print("Poyta:")
        for idx, card in enumerate(self.table_cards):
            print("{}. [{}]".format(idx + 1, card), end=" ")
        print("\n")
    
    def show_player_cards(self):
        print("Katesi:")
        for idx, card in enumerate(self.next_player.cards_hand):
            print("{}. [{}]".format(idx + 1, card), end=" ")
        print("\n")
            
    # Method that deals with a player's turn. Calls other methods to handle specific tasks.         
    def the_play(self):
        print("Vuorossa oleva pelaaja: {} \n".format(self.next_player))
        if not self.next_player.cards_hand:
            print("Koska sinulla ei ole kortteja, siirtyy vuoro seuraavalle pelaajalle\n")
        elif not self.table_cards:
            print("Koska poyta on tyhja, joudut laittamaan yhden korteistasi poytaan.\n")
            # Returns -1 when player wants to quit game
            if self.add_table_card(self.add_card()) == -1:
                return -1
        else:
            self.show_table_cards()
            self.show_player_cards()
            while True:
                choice = input("Haluatko ottaa poydasta kortteja (k/e)?\n")
                choice = choice.lower()
                if choice == "k":
                    success = self.take_cards()
                    # success == -1 when player wants to quit game
                    if success == -1:
                        return -1
                    # success == false when player decided not to take cards from table
                    elif success:
                        break
                    else:
                        print("Joudut laittamaan yhden korteistasi poytaan\n")
                        self.add_table_card(self.add_card())
                        break
                elif choice == "e":
                    print("Joudut laittaamaan yhden korteistasi poytaan\n")
                    if self.add_table_card(self.add_card()) == -1:
                        return -1
                    break
                elif choice == "q":
                        if self.quit():
                            return -1
                else:
                    self.invalid_input()            
    # Method for taking cards from table. Calls other methods for specific tasks
    def take_cards(self):
        while True:
            player_card = self.add_card()
            if player_card == -1:
                return -1
            table_cards = self.pic_cards()
            if table_cards == -1:
                return -1
            if self.check_validity(player_card, table_cards):
                self.cards_to_player_deck(player_card, table_cards)
                self.check_mokki()
                self.card_to_player_hand()
                Round.last_player = self.next_player
                return True
            else:
                print("Liikkeesi on laiton!\n")
                while True:
                    choice = input("Haluatko yrittaa uudestaan ottaa poydasta kortteja (k/e)?\n")
                    choice = choice.lower()
                    if choice == "k":
                        break
                    elif choice == "e":
                        return False
                    else:
                        self.invalid_input()
        
    # Asks player which of his cards he wants to use    
    def add_card(self):
        while True:
            self.show_table_cards()
            self.show_player_cards()
            card = input("Valitse minka kortin kaytat. Anna kortin indeksi: \n")
            try: 
                card = int(card)
                if card > len(self.next_player.cards_hand) or card < 1:
                    print("Virheellinen numero!\n")
                else:
                    return self.next_player.cards_hand[card - 1]
            except ValueError:
                if card == "q":
                        if self.quit():
                            return -1
                else:
                    print("Syotteen pitaa olla kokonaisluku!\n")
                
    # Moves one card from player's hand to table
    def add_table_card(self, card):
        # Card is -1 if player wants to quit game
        if card == -1:
            return -1
        else:
            self.table_cards.append(card)
            self.next_player.cards_hand.remove(card)
            self.card_to_player_hand()
            
    # Asks player which cards he wants to take from table
    def pic_cards(self):
        while True:
            cards = []
            try:
                # success will stay true if all user inputs are valid
                success = True
                self.show_table_cards()
                self.show_player_cards()
                choice = input("Anna kokonaislukuina haluamasi korttien indeksit valilyonnein erotettuna: \n")
                if choice == "q" or choice == "Q":
                    return -1
                card_numbers = [int(i) for i in choice.split()]
                if not card_numbers:
                    raise ValueError
                # Removes duplicates
                card_numbers = list(set(card_numbers))
                for number in card_numbers:
                    if number < 1 or number > len(self.table_cards):
                        print("Virheellinen kokonaisluku!\n")
                        success = False
                        break
                    else:
                        cards.append(self.table_cards[number - 1])
                if success: 
                    return cards
            except ValueError:
                print("Syotteiden pitaa olla kokonaislukuja! \n")
                
    # Moves cards from table and player's hand to player's deck            
    def cards_to_player_deck(self, player_card, table_cards):
        # Removes a card from player's hand and inserts it in player's deck
        self.next_player.cards_deck.append(player_card)
        self.next_player.cards_hand.remove(player_card)
        for card in table_cards:
            # Removes cards from table and inserts them in player's deck
            self.next_player.cards_deck.append(card)
            self.table_cards.remove(card)
    
    # Moves card from deck to player's hand if there are still cards left in deck
    def card_to_player_hand(self):
        if len(self.next_player.cards_hand) < 4 and self.deck_cards:
            self.next_player.cards_hand.append(self.deck_cards.pop())
            
    
    # Checks if a player can take the cards he wants from the table. 
    def check_validity(self, player_card, table_cards):
        #Copies the table_cards list to an new list "table"
        table = list(table_cards)
        i = len(table)
        while i > 0:
            comb_sum = 0
            found = False
            for comb in itertools.combinations(table, i):
                for item in comb:
                    comb_sum += item.table_value
                if comb_sum == player_card.hand_value:
                    sublist = list(comb)
                    for value in sublist:
                        table.remove(value)
                    # When a sublist is found we need to update table list before looking for new sublists
                    found = True
                    break
                comb_sum = 0
            if found:
                pass
            elif i > len(table):
                i = len(table)
            else:
                i -= 1
        if len(table) == 0:
            return True
        else:
            return False
            
    def check_mokki(self):
        if not self.table_cards:
            self.next_player.mokki += 1
            
    def check_end(self, players):
        for player in players:
            if player.cards_hand:
                return False
        table_cards = list(self.table_cards)
        # The player who last took cards from table gets the rest of the cards in table
        for card in table_cards:
            # Removes cards from table and inserts them in player's deck
            Round.last_player.cards_deck.append(card)
            self.table_cards.remove(card)
        return True
    
    def calculate_points(self, players):
        most_cards = [players[0]]
        most_spades = [players[0]]
        # Keeps track of the highest spade amount
        high_spades = 0
        for player in players:
            spades = 0
            if player.mokki:
                player.points += 1
                player.mokki = 0
            for card in player.cards_deck:
                if card.name == "Ruutu-10":
                    player.points += 2
                elif card.name == "Pata-2":
                    player.points += 1
                # Gives points for aces
                elif card.hand_value == 14:
                    player.points += 1
                if "Pata" in card.name:
                    spades += 1
            # Checks which player has most cards and spades
            if player is not players[0]:
                if len(player.cards_deck) == len(most_cards[0].cards_deck):
                    most_cards.append(player)
                elif len(player.cards_deck) > len(most_cards[0].cards_deck):
                    most_cards = [player]
                if spades == high_spades:
                    most_spades.append(player)
                elif spades > high_spades:
                    most_spades = [player]
            if spades > high_spades:
                high_spades = spades
        for player in most_spades:
            player.points += 2
        for player in most_cards:
            player.points += 1
            
    def invalid_input(self):
        print("Virheellinen syote! Syota joko k tai e")
        
    def quit(self):
        while True:
            choice = input("Haluatko varmasti lopettaa pelin (k/e)?\n")
            choice = choice.lower()
            if choice == "e":
                return False
            elif choice == "k":
                return True
            else: 
                self.invalid_input()
    
    # Empties players' decks after each round
    def empty_players_decks(self, players):
        for player in players:
            player.cards_deck = []
                    
            