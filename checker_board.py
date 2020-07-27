import pygame


class CheckerBoard:
    """A class to represent the entire checkerboard"""
    def __init__(self, game_settings, screen):
        """Initialize the checkerboard"""
        self.game_settings = game_settings
        self.screen = screen

        self.checker_board_width = self.game_settings.screen_height
        self.checker_board_height = self.game_settings.screen_height


class CheckerBoardSquare(CheckerBoard):
    """A subclass to represent a single square on the checkerboard"""

    def __init__(self, game_settings, screen, checker_board_x_position, checker_board_y_position):
        """Initialize the checkboard square"""
        super().__init__(game_settings, screen)

        # Square color -1 (dark) or 1 (light)
        self.square_color_index = self.get_square_color(game_settings.top_left_square, checker_board_x_position, checker_board_y_position)
        if self.square_color_index == -1:
            self.square_color = self.game_settings.dark_squares_color
        elif self.square_color_index == 1:
            self.square_color = self.game_settings.light_squares_color

        self.square_width = self.checker_board_width / self.game_settings.nbr_squares_row
        self.square_height = self.checker_board_height / self.game_settings.nbr_squares_col

        self.rect = pygame.Rect(0,0,self.square_width,self.square_height)
        self.rect.left = ((self.game_settings.screen_width - self.checker_board_width) / 2) \
                         + (self.square_width * (checker_board_y_position))
        self.rect.top = (self.square_height * (checker_board_x_position))

    def draw_square(self):
        """Draw the square to the screen"""
        pygame.draw.rect(self.screen,self.square_color,self.rect)

    def get_square_color(self, top_left_square, checker_board_x_position, checker_board_y_position):
        """Get the square color in function of the base setting and the square position"""

        # First check the color assuming the top left square is light
        if checker_board_x_position % 2 != 0:
            if checker_board_y_position % 2 == 0:
                square_color = 1
            else:
                square_color = -1
        else:
            if checker_board_y_position % 2 == 0:
                square_color = -1
            else:
                square_color = 1

        # Then check whether it is the case. If not, invert the colour of the square
        if top_left_square == "dark":
            square_color *= -1

        return square_color


