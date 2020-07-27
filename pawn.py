import pygame


class Pawn:
    """A class to represent an individual pawn"""
    def __init__(self, game_settings, screen, checker_board_x_position, checker_board_y_position, nbr_pawns_left, pawn_id):
        """Initialize the pawn"""
        self.game_settings = game_settings
        self.screen = screen


        self.radius = (self.game_settings.screen_height / self.game_settings.nbr_squares_row) / 2

        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.left = ((self.game_settings.screen_width - self.game_settings.screen_height) / 2) \
                         + (self.radius * 2 * (checker_board_y_position))
        self.rect.top = (self.radius * 2 * (checker_board_x_position))

        self.taken = False
        self.promoted = 0
        self.moving_range = 1
        self.direction = 1

        if nbr_pawns_left > (self.game_settings.nbr_pawns / 2):
            self.color = self.game_settings.dark_pieces_color
            self.color_type = -1
            self.image = pygame.image.load("images/crown_dark.png")
        else:
            self.color = self.game_settings.light_pieces_color
            self.color_type = 1
            self.image = pygame.image.load("images/crown_light.png")

        self.image_rect = self.image.get_rect()
    def draw_pawn(self):
        """Draw the pawn to the screen"""
        pygame.draw.circle(self.screen, self.color, self.rect.center, int(self.radius))
        if self.promoted == 1:
            self.image_rect.centerx = self.rect.centerx
            self.image_rect.centery = self.rect.centery

            self.screen.blit(self.image, self.image_rect)

    def update_pawn(self, checker_board_x_position, checker_board_y_position):
        """Update the position of the pawn"""
        self.rect.left = ((self.game_settings.screen_width - self.game_settings.screen_height) / 2) \
                         + (self.radius * 2 * (checker_board_y_position))
        self.rect.top = (self.radius * 2 * (checker_board_x_position))

    def promote_pawn(self):
        """Promote a pawn to King"""
        self.promoted = 1
        self.moving_range = self.game_settings.nbr_squares_row
        self.direction = 2