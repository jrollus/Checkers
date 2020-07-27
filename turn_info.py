class TurnInfo():
    """A class to store the necessary info of the current turn."""
    def __init__(self):
        # -1 for Dark / 1 for Light
        self.player_turn = -1
        self.move_authorized = True
        self.pawn_authorized = True
        self.nbr_jumps = 0
        self.turn_over = False
        self.game_over = False

    def change_turn(self):
        self.player_turn *= -1
        self.move_authorized = True
        self.pawn_authorized = True
        self.nbr_jumps = 0
        self.turn_over = False
        self.game_over = False