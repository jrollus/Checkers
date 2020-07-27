import pygame.sysfont


class PlayersTurn:
    """A class to print a message expliciting the player's turn"""
    def __init__(self, game_settings, screen):
        """Initialize class attributes"""
        self.game_settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, self.game_settings.font_size)

        self.msg_image = None
        self.msg_image_rect = None

    def print_message(self, player_turn):
        """Draw the message"""
        if player_turn == -1:
            msg = "Dark player's turn"
        else:
            msg = "Light player's turn"

        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()

        self.msg_image_rect.centerx = ((self.game_settings.screen_width - self.game_settings.screen_height) / 2) / 2
        self.msg_image_rect.centery = self.game_settings.screen_height / 2

        self.screen.blit(self.msg_image, self.msg_image_rect)


class MoveNotAllowed:
    """A class to print a message expliciting the player's turn"""
    def __init__(self, game_settings, screen):
        """Initialize class attributes"""
        self.game_settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, self.game_settings.font_size)

        self.msg_image = None
        self.msg_image_rect = None

    def print_message(self, move_allowed):
        """Draw the message"""
        if not move_allowed:
            msg = "Move not allowed"

            self.msg_image = self.font.render(msg, True, self.text_color)
            self.msg_image_rect = self.msg_image.get_rect()

            self.msg_image_rect.centerx = ((self.game_settings.screen_width - self.game_settings.screen_height) / 2) / 2
            self.msg_image_rect.centery = (self.game_settings.screen_height / 2) + self.game_settings.font_size

            self.screen.blit(self.msg_image, self.msg_image_rect)


class PawnNotAllowed:
    """A class to print a message expliciting the player's turn"""
    def __init__(self, game_settings, screen):
        """Initialize class attributes"""
        self.game_settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, self.game_settings.font_size)

        self.msg_image = None
        self.msg_image_rect = None

    def print_message(self, pawn_allowed):
        """Draw the message"""
        if not pawn_allowed:
            msg = "Pawn not allowed"

            self.msg_image = self.font.render(msg, True, self.text_color)
            self.msg_image_rect = self.msg_image.get_rect()

            self.msg_image_rect.centerx = ((self.game_settings.screen_width - self.game_settings.screen_height) / 2) / 2
            self.msg_image_rect.centery = (self.game_settings.screen_height / 2) + self.game_settings.font_size

            self.screen.blit(self.msg_image, self.msg_image_rect)


class PlayerWin:
    """A class to print a message expliciting the player's turn"""
    def __init__(self, game_settings, screen):
        """Initialize class attributes"""
        self.game_settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, self.game_settings.font_size)

        self.msg_image = None
        self.msg_image_rect = None

    def print_message(self, player_color):
        """Draw the message"""
        if player_color == -1:
            msg = "Dark player wins"
        else:
            msg = "Light player wins"

        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()

        self.msg_image_rect.centerx = ((self.game_settings.screen_width - self.game_settings.screen_height) / 2) / 2
        self.msg_image_rect.centery = (self.game_settings.screen_height / 2)

        self.screen.blit(self.msg_image, self.msg_image_rect)