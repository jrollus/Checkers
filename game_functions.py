import sys
import math

import pygame

from checker_board import CheckerBoardSquare
from pawn import Pawn
from current_position import CurrentPosition


def update_screen(game_settings, turn_info, screen, squares, pawn_selector,
                  pawns, player_turn_msg, move_allowed_msg, pawn_allowed_msg, player_win_msg):
    """Redraw the screen during each pass through the loop"""
    screen.fill(game_settings.bg_color)

    if not turn_info.game_over:
        player_turn_msg.print_message(turn_info.player_turn)
        pawn_allowed_msg.print_message(turn_info.pawn_authorized)
        move_allowed_msg.print_message(turn_info.move_authorized)
    else:
        player_win_msg.print_message(turn_info.player_turn)

    for square in squares:
        square.draw_square()

    pawn_selector.draw_pawn_selector()

    for pawn in pawns:
        if not pawn.taken:
            pawn.draw_pawn()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def create_checker_board(game_settings, screen, squares):
    """Create the checker board"""
    for row_nbr in range(game_settings.nbr_squares_row):
        for col_nbr in range(game_settings.nbr_squares_col):
            create_square(game_settings, screen, squares, row_nbr, col_nbr)


def create_square(game_settings, screen, squares, row_nbr, col_nbr):
    """Create an individual square"""
    square = CheckerBoardSquare(game_settings, screen, row_nbr, col_nbr)
    squares.append(square)


def initialize_screen(game_settings):
    """Initialize the game's screen"""
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption(game_settings.screen_caption)
    pygame.mouse.set_visible(False)
    return screen


def check_events(game_stats, turn_info, positions_matrix, pawns, pawn_selector):
    """"Watch for keyboard and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_stats, turn_info, positions_matrix, pawns, pawn_selector)


def check_keydown_events(event, game_stats, turn_info, p_m, pawns, p_s):
    """Check for when keyboard is pressed event."""
    if event.key == pygame.K_RIGHT:
        p_s.update("right")
    elif event.key == pygame.K_LEFT:
        p_s.update("left")
    elif event.key == pygame.K_UP:
        p_s.update("up")
    elif event.key == pygame.K_DOWN:
        p_s.update("down")
    elif event.key == pygame.K_SPACE:
        authorized_pawns_list = get_authorized_pawns_list(turn_info, p_m, pawns)
        p_s.update_status(turn_info, authorized_pawns_list)
        if p_s.status == "active" and ((p_s.sel_x != p_s.curr_xy[0]) or (p_s.sel_y != p_s.curr_xy[1])):
            check_move(turn_info, authorized_pawns_list, p_s)
            # Check whether the move is authorized
            if turn_info.move_authorized:
                # Move the pawn and update the checkerboard
                move_pawn(game_stats, turn_info, p_m, pawns, p_s)
                # If turn is over, change it
                if turn_info.turn_over:
                    change_turn(game_stats, turn_info, p_s)
            # If one player is blocked or does not have any pawn left, end the game
            if game_over(game_stats, turn_info.game_over):
                game_stats.game_active = False
    elif event.key == pygame.K_q:
        sys.exit()


def get_pawn_index(authorized_pawns_list, sel_x, sel_y):
    """Find the pawn index."""
    i = 0
    while i <= len(authorized_pawns_list) - 1:
        if authorized_pawns_list[i][0][0] == sel_x and (authorized_pawns_list[i][0][1] == sel_y):
            return i
        i += 1

    return -1


def get_authorized_pawns_list(turn_info, p_m, pawns):
    """Compute all the possible moves of all of the remaining pawns of the active player to evaluate which pawns
    can be played with."""
    authorized_pawns_list = []
    for x in range(len(p_m)):
        for y in range(len(p_m)):
            if p_m[x][y] != -1:
                if pawns[p_m[x][y]].color_type == turn_info.player_turn:
                    authorized_moves_list = []
                    get_authorized_moves_list(authorized_moves_list, [x, y], [x, y], 0, [0, 0], p_m, pawns[p_m[x][y]], pawns)
                    temp_list = [(x,y), authorized_moves_list]
                    authorized_pawns_list.append(temp_list)

    return authorized_pawns_list


def game_over(game_stats, move_impossible):
    """Check whether the game is over"""
    if move_impossible or game_stats.nbr_dark_pawns == 0 or game_stats.nbr_light_pawns == 0:
        return True
    else:
        return False


def move_pawn(game_stats, turn_info, p_m, pawns, p_s):
    """Move the pawn to the selected location"""
    # Move pawn
    pawns[p_m[p_s.sel_x][p_s.sel_y]].update_pawn(p_s.curr_xy[0], p_s.curr_xy[1])

    # Check whether pawn needs to be promoted
    if ((turn_info.player_turn == -1) and (p_s.curr_xy[0] == len(p_m) - 1)) \
            or ((turn_info.player_turn == 1) and (p_s.curr_xy[0] == 0)):
        pawns[p_m[p_s.sel_x][p_s.sel_y]].promote_pawn()

    # Update position matrix
    p_m[p_s.curr_xy[0]][p_s.curr_xy[1]] = p_m[p_s.sel_x][p_s.sel_y]
    p_m[p_s.sel_x][p_s.sel_y] = -1

    # In case there was a jump, delete the pawn
    if turn_info.nbr_jumps >= 1:
        pawn_jumped_xy = get_pawn_jumped_xy(p_s)

        pawns[p_m[pawn_jumped_xy[0]][pawn_jumped_xy[1]]].taken = True
        p_m[pawn_jumped_xy[0]][pawn_jumped_xy[1]] = -1

        if turn_info.player_turn == -1:
            game_stats.nbr_light_pawns -= 1
        else:
            game_stats.nbr_dark_pawns -= 1

    # Update pawn selector
    p_s.sel_x = p_s.curr_xy[0]
    p_s.sel_y = p_s.curr_xy[1]


def get_pawn_jumped_xy(p_s):
    """Get the coordinates of the pawn jumped"""
    slope = int((p_s.sel_y - p_s.curr_xy[1]) / (p_s.sel_x - p_s.curr_xy[0]))
    if slope > 0:
        if p_s.curr_xy[1] > p_s.sel_y:
            pawn_jumped_xy = [p_s.curr_xy[0] - slope, p_s.curr_xy[1] - slope]
        else:
            pawn_jumped_xy = [p_s.curr_xy[0] + slope, p_s.curr_xy[1] + slope]
    else:
        if p_s.curr_xy[1] > p_s.sel_y:
            pawn_jumped_xy = [p_s.curr_xy[0] - slope, p_s.curr_xy[1] + slope]
        else:
            pawn_jumped_xy = [p_s.curr_xy[0] + slope, p_s.curr_xy[1] - slope]
    return pawn_jumped_xy


def create_pawns_set(game_settings, screen, pawns, positions_matrix):
    """Create the pawn and the matrix to record positions"""
    nbr_pawns_left = game_settings.nbr_pawns
    for row_nbr in range(game_settings.nbr_squares_row):
        temp_list = []
        for col_nbr in range(game_settings.nbr_squares_col):
            if check_create_pawn(nbr_pawns_left, game_settings.nbr_pawns, game_settings.nbr_squares_row,
                                 game_settings.nbr_squares_col, game_settings.top_left_square, row_nbr, col_nbr):
                create_pawn(game_settings, screen, pawns, row_nbr, col_nbr, nbr_pawns_left)
                temp_list.append(game_settings.nbr_pawns - nbr_pawns_left)
                nbr_pawns_left -= 1
            else:
                temp_list.append(-1)
        positions_matrix.append(temp_list)


def check_create_pawn(nbr_pawns_left, nbr_pawns, nbr_squares_row, nbr_squares_col,
                      top_left_square, checker_board_x_position, checker_board_y_position):
    """"Check whether a pawn needs to be created in this square."""
    if nbr_pawns_left > (nbr_pawns / 2):
        return dark_square(top_left_square, checker_board_x_position, checker_board_y_position)
    else:
        if checker_board_x_position >= nbr_squares_row - ((nbr_pawns / 2) / (nbr_squares_col / 2)):
            return dark_square(top_left_square, checker_board_x_position, checker_board_y_position)


def dark_square(top_left_square, checker_board_x_position, checker_board_y_position):
    """Check whether a square is dark"""
    is_dark_square = False
    if checker_board_x_position % 2 != 0:
        if checker_board_y_position % 2 != 0:
            is_dark_square = True
    else:
        if checker_board_y_position % 2 == 0:
            is_dark_square = True

    if top_left_square == "dark":
        is_dark_square = not is_dark_square

    return is_dark_square


def create_pawn(game_settings, screen, pawns, row_nbr, col_nbr, nbr_pawns_left):
    """Create an individual pawn"""
    pawn = Pawn(game_settings, screen, row_nbr, col_nbr, nbr_pawns_left, game_settings.nbr_pawns - nbr_pawns_left)
    pawns.append(pawn)


def check_move(turn_info, authorized_pawns_list, p_s):
    """Check whether the move is authorized"""
    pawn_index = get_pawn_index(authorized_pawns_list, p_s.sel_x, p_s.sel_y)
    authorized_moves_list = authorized_pawns_list[pawn_index][1]

    if authorized_moves_list:
        turn_info.nbr_jumps = max([authorized_move[-1] for authorized_move in authorized_moves_list])
        optimal_moves_list = [authorized_move for authorized_move in authorized_moves_list if
                              authorized_move[-1] == turn_info.nbr_jumps]
        if check_move_in_optimal_list(optimal_moves_list, p_s.curr_xy,
                                      [p_s.sel_x, p_s.sel_y]):
            turn_info.move_authorized = True
            if turn_info.nbr_jumps <= 1:
                turn_info.turn_over = True
        else:
            turn_info.move_authorized = False
    else:
        turn_info.game_over = True


def change_turn(game_stats, turn_info, pawn_selector):
    """Change the turn."""
    turn_info.change_turn()
    pawn_selector.status = "passive"


def check_move_in_optimal_list(optimal_moves_list, curr_move, sel_move):
    """Check whether the selected move is in the optimal move list."""
    for move in optimal_moves_list:
        # If there is a jump, the move must be exactly the jump
        if move[-1] >= 1:
            if (move[0] == curr_move[0]) and (move[1] == curr_move[1]):
                return True
        # If not it can be any move between the allowed move and the current position
        else:
            if (move[0] == curr_move[0]) and (move[1] == curr_move[1]) or is_between(move, curr_move, sel_move):
                return True

    return False


def get_authorized_moves_list(authorized_moves_list, start_pos, initial_start_pos, nbr_moves, previous_move_direction, positions_matrix, pawn, pawns):
    """Recursive function to get the number of remaining moves."""
    for curr_path in range(pawn.direction * 2):
        move_direction = get_move_direction(curr_path, pawn)

        if (start_pos[0] == initial_start_pos[0]) and (start_pos[1] == initial_start_pos[1]):
            nbr_moves = 0

        path_blocked = False
        jump_possible = False
        nbr_squares_moved = 1

        curr_pos = CurrentPosition(start_pos[0], start_pos[1])
        curr_pos.move(move_direction, "next")

        # Loop (in case of kings they can move more than one square at a time) till the path is blocked
        # or an adversary pawn is found and can be jumped
        while (not path_blocked) and (nbr_squares_moved <= pawn.moving_range) and (not jump_possible):
            # Check whether the pawn would still be in-bound
            if (0 <= curr_pos.x <= len(positions_matrix)-1) and (0 <= curr_pos.y <= len(positions_matrix)-1):
                # Check whether the square is empty
                if positions_matrix[curr_pos.x][curr_pos.y] == -1:
                    if nbr_moves == 0 or pawn.moving_range > 1:
                        curr_pos.move(move_direction, "next")
                        nbr_squares_moved += 1
                    else:
                        path_blocked = True
                        jump_possible = False
                # Check whether the square is occupied by a pawn of the same color
                elif pawns[positions_matrix[curr_pos.x][curr_pos.y]].color_type == pawn.color_type:
                    path_blocked = True
                    jump_possible = False
                # Check whether the square is occupied by a pawn of the other color
                elif pawns[positions_matrix[curr_pos.x][curr_pos.y]].color_type == -pawn.color_type:
                    # Condition to check whether the iterative process is trying to come back from where it came from
                    # in the case of kings and jump the same piece infinitely going back and forth.
                    if (curr_pos.x != start_pos[0] - previous_move_direction[0]) or \
                            (curr_pos.y != start_pos[1] - previous_move_direction[1]):
                        curr_pos.move(move_direction, "next")
                        # If the next one is empty and within bounds, allow the jump
                        if (0 <= curr_pos.x <= len(positions_matrix) - 1) and \
                                (0 <= curr_pos.y <= len(positions_matrix) - 1) and \
                                (positions_matrix[curr_pos.x][curr_pos.y] == -1):
                            jump_possible = True
                        else:
                            curr_pos.move(move_direction, "previous")
                            path_blocked = True
                            jump_possible = False
                    else:
                        path_blocked = True
                        jump_possible = False
            else:
                path_blocked = True
                jump_possible = False

        # If no jump is possible, then finalize the path
        if not jump_possible:
            if nbr_moves == 0:
                if nbr_squares_moved > 1:
                    curr_pos.move(move_direction, "previous")
                    authorized_moves_list.append([curr_pos.x, curr_pos.y, 0])
                    nbr_moves = 0

        # If a jump is possible, proceed to reinitialize the process
        else:
            nbr_moves += 1
            # If first jump
            if nbr_moves == 1:
                authorized_moves_list.append([curr_pos.x, curr_pos.y, 1])
            # If posterior jump
            else:
                authorized_moves_list[-1][-1] += 1

            get_authorized_moves_list(authorized_moves_list, [curr_pos.x, curr_pos.y], initial_start_pos, nbr_moves, move_direction, positions_matrix,
                                      pawn, pawns)


def get_move_direction(curr_path, pawn):
    """Depending on the path number, generate the X,Y move"""
    if curr_path < 2:
        if curr_path % 2 == 0:
            move_direction = [- pawn.color_type, - 1]
        else:
            move_direction = [- pawn.color_type, + 1]
    else:
        if curr_path % 2 == 0:
            move_direction = [pawn.color_type, - 1]
        else:
            move_direction = [pawn.color_type, + 1]

    return move_direction


def distance(a, b):
    """Get the distance between two points"""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def is_between(a, c, b):
    """Get whether a point C is between points A dn B"""
    return int(distance(a, c) + distance(c, b)) == int(distance(a, b))
