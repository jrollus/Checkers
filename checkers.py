import pygame

import game_functions as gf

from game_settings import GameSettings
from pawn_selector import PawnSelector
from game_stats import GameStats
from turn_info import TurnInfo
from game_messages import PlayersTurn
from game_messages import MoveNotAllowed
from game_messages import PawnNotAllowed
from game_messages import PlayerWin

def run_game():
    # Initialize game and create a screen object
    pygame.init()
    game_settings = GameSettings()
    game_stats = GameStats()
    screen = gf.initialize_screen(game_settings)
    turn_info = TurnInfo()
    player_turn_msg = PlayersTurn(game_settings, screen)
    move_allowed_msg = MoveNotAllowed(game_settings, screen)
    pawn_allowed_msg = PawnNotAllowed(game_settings, screen)
    player_win_msg = PlayerWin(game_settings, screen)

    # Make a list to store squares in.
    squares = []

    # Create the checker board out of a group of individual squares
    gf.create_checker_board(game_settings, screen, squares)

    # Create the pawn selector
    pawn_selector = PawnSelector(game_settings, screen)

    # Make a list to store pawns in.
    pawns = []

    # Initialize matrix of positions
    positions_matrix = []

    # Create the full set of pawns
    gf.create_pawns_set(game_settings, screen, pawns, positions_matrix)

    # Start the main loop for the game
    while True:
        if game_stats.game_active:
            gf.check_events(game_stats, turn_info, positions_matrix, pawns, pawn_selector)
            gf.update_screen(game_settings, turn_info, screen, squares,
                             pawn_selector, pawns, player_turn_msg, move_allowed_msg, pawn_allowed_msg, player_win_msg)


run_game()