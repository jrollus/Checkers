class GameSettings:
    """Class to store all game settings"""
    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.screen_caption = "Checkers"

        # Game area settings
        self.top_left_square = "light"
        self.nbr_squares_row = 8
        self.nbr_squares_col = 8
        self.light_squares_color = (255, 222, 173)
        self.dark_squares_color = (0, 0, 0)

        # Pieces settings
        self.nbr_pawns = 24
        self.light_pieces_color = (255, 255, 255)
        self.dark_pieces_color = (105, 105, 105)

        # Pawn selector
        self.pawn_selector_base_color = (218, 165, 32)
        self.pawn_selector_active_color = (249, 166, 2)
        self.pawn_selector_initial_position = (0, 0)

        # Messages
        self.font_size = 25