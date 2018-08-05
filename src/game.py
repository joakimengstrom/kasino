import csv, datetime
from card import Card
from round import Round
from player import Player


class Game:
    
    card_numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jatka', 'rouva', 'kuningas', 'assa']
    card_suits = ['Pata', 'Risti', 'Hertta', 'Ruutu']
    
    
    def __init__(self):
        self.players = []
        self.cards = []
        self.dealer = None
        
    # Creates deck of cards
    def initialize_cards(self):
        i = 2
        for card_number in self.card_numbers:
            for suit in self.card_suits:
                if card_number == "jatka" or card_number == "rouva" or card_number == "kuningas" or card_number == "assa":
                    name = suit + card_number
                else:
                    name = suit + "-" + card_number
                if i == 14:
                    hand_value = 14
                    table_value = 1
                elif i == 10 and suit == "Ruutu":
                    hand_value = 16
                    table_value = 10
                elif i == 2 and suit =="Pata":
                    hand_value = 15
                    table_value = 2
                else:
                    hand_value, table_value = i, i
                self.cards.append(Card(name, table_value, hand_value))
            i += 1
    
    # A round in game
    def round(self):
        r = Round(self.set_dealer())
        cards = list(self.cards)
        r.deal_cards(cards, self.players)
        # While loop continues until all players are out of cards or player wants to quit game
        while not r.check_end(self.players):
            # the.play() returns -1 when player wants to quit game
            if r.the_play() == -1:
                return -1 
            r.change_player(self.players)
        r.calculate_points(self.players)
        r.empty_players_decks(self.players)

              
    def set_dealer(self):
        if not self.dealer or self.dealer == self.players[-1]:
            self.dealer = self.players[0]
        else:
            self.dealer = self.players[self.players.index(self.dealer) + 1]
        return self.dealer
            
    def save_game(self):
        while True:
            file = input("Minka nimen haluat antaa tiedostolle?\n")
            csv_file = file + (".csv")
            date = datetime.datetime.today().strftime ("%d.%m.%Y")
            data = ["Kasino", date]
            headings = ["Nimi", "Pisteet"]
            try:
                with open (csv_file, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile, delimiter=";")
                    writer.writerow(data)
                    writer.writerow(headings)
                    for player in self.players:
                        data = [player.name, player.points]
                        writer.writerow(data)
                    break
            except Exception:
                print("Jotain meni pieleen ja tiedoston tallentaminen epaonnistui! Tarkista etta samanniminen tiedosto ei ole parhailaan auki\n")
            
    def load_game(self):
        while True:
            csv_file = input("Minka tiedoston haluat avata?\n")
            try:
                with open(csv_file) as csvfile:
                    reader = csv.reader(csvfile, delimiter=";")
                    row1 = next(reader)
                    row2 = next(reader)
                    try:
                        if row1[0] != "Kasino" or row2[0] != "Nimi" or row2[1] != "Pisteet":
                            print("Virheellinen tiedosto!\n") 
                        for row in reader:
                            try:
                                success = True
                                player = Player(row[0])
                                player.points = int(row[1])
                                self.players.append(player)
                            except ValueError:
                                print("Virheellinen tiedosto!\n")
                                success = False
                        if success:
                            return success
                    except Exception:
                        print("Virheellinen tiedosto!\n")
            except Exception:
                print("Tiedostoa ei loytynyt!\n")
            while True:
                choice = input("Haluatko yrittaa tiedoston avaamista uudelleen (e/k)?\n")
                choice = choice.lower()
                if choice == "k":
                    break
                elif choice == "e":
                    return False
                elif choice == "q":
                    return -1
                else:
                    self.invalid_input()
            
    def check_end(self):
        for player in self.players:
            if player.points >= 16:
                return True
        print("Pisteet kierroksen jalkeen:\n")
        self.print_scores()
        return False
    
    def show_results(self):
        print("Peli loppui!\nTassa ovat lopulliset pisteet:\n")
        self.print_scores()
            
    def start_game(self):
        print("Tervetuloa pelaamaan kasinoa!\nMikali haluat lopettaa pelaamisen kesken pelin, syota q.")
        while True:
            choice = input("Haluatko ladata kesken jaaneen pelin (k/e)?\n")
            choice = choice.lower()
            if choice == "k":
                load_game = self.load_game()
                if load_game:
                    # load_game == -1 if player wants to quit
                    if load_game == -1:
                        return -1
                    else:
                        break
                else:
                    if self.give_players() == -1:
                        return -1
                    break
            elif choice == "e":
                if self.give_players() == -1:
                    return -1
                break
            elif choice == "q":
                return -1
            else:
                self.invalid_input()
                
    # Asks user to give players
    def give_players(self):
        print("Aloitetaan uusi peli!\n")
        print("Sallittu pelaajien lukumaara on 2-6.\n")
        while True:
            amount = input("Anna pelaajien lukumaara:\n")
            if amount == "q" or amount == "Q":
                return -1
            try:
                amount = int(amount)
                if amount > 6 or amount < 2:
                    print("Virheellinen syote! Syotteen pitaa olla 2 ja 6 valissa!")
                else:
                    for i in range(amount):
                        name = input("Anna pelaajan nimi: ")
                        self.players.append(Player(name))
                    break
            except ValueError:
                print("Virheellinen syote! Syotteen pitaa olla kokonaisluku!\n")
                
    def end_game(self):
        while True:
            choice = input("Haluatko tallentaa pelin (k/e)?\n")
            choice = choice.lower()
            if choice == "k":
                self.save_game()
                break
            elif choice == "e":
                break
            else:
                self.invalid_input()
                
    def invalid_input(self):
        print("Virheellinen syote! Syota joko k tai e")
        
    def print_scores(self):
        ordered = sorted(self.players, key=lambda x: x.points, reverse = True)
        for player in ordered:
            print("{}: {} pistetta".format(player.name, player.points))
        print("\n")
            
    def new_game(self):
        while True:
            choice = input("Haluatko pelata uudestaan (k/e)?\n")
            choice = choice.lower()
            if choice == "k":
                return True
            elif choice == "e":
                return False
            else:
                self.invalid_input()
                
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