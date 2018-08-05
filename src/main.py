from game import Game

while True:
    game = Game()
    game.initialize_cards()
    while True:
        if game.start_game() == -1:
            if game.quit():
                exit()
        else:
            break
    while True:
        if game.round() == -1:
            game.end_game()
            break
        elif game.check_end():
            game.show_results()
            break
    if not game.new_game():
        break