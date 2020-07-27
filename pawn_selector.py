import pygame

from game_functions import get_pawn_index


class PawnSelector:
    """A class to represent the pawn selector."""
    def __init__(self, game_settings, screen):
        """Initialize the pawn selector"""
        self.game_settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width = self.game_settings.screen_height / self.game_settings.nbr_squares_row
        self.height = self.game_settings.screen_height / self.game_settings.nbr_squares_col
        self.margin_width = (self.game_settings.screen_width - self.game_settings.screen_height) / 2

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.left =  self.margin_width + (self.width * (game_settings.pawn_selector_initial_position[0]))
        self.rect.top = (self.height * (game_settings.pawn_selector_initial_position[1]))

        self.status = "passive"
        self.sel_x = -1
        self.sel_y = -1
        self.curr_xy = [0, 0]

    def draw_pawn_selector(self):
        """Draw the pawn selector to the screen"""
        if self.status == "passive":
            pygame.draw.rect(self.screen,self.game_settings.pawn_selector_base_color,self.rect)
        elif self.status == "active":
            pygame.draw.rect(self.screen,self.game_settings.pawn_selector_active_color,self.rect)

    def update(self, move_direction):
        """Update the pawn selector's position based on the movement flag."""
        if move_direction == "up" and self.rect.top > self.screen_rect.top:
            self.rect.top -= self.height
        elif move_direction == "down" and self.rect.bottom < self.screen_rect.bottom:
            self.rect.top += self.height
        elif move_direction == "right" and self.rect.right < self.margin_width + self.game_settings.screen_height:
            self.rect.left += self.width
        elif move_direction == "left" and self.rect.left > self.margin_width:
            self.rect.left -= self.width

    def from_rect_to_xy(self):
        """Convert the rect position to X,Y coordinates"""
        self.curr_xy = (int(self.rect.top / self.height), int((self.rect.left - self.margin_width) / self.width))

    def update_status(self, turn_info, authorized_pawns_list):
        """Update the status of the pawn selector."""
        self.from_rect_to_xy()
        if self.status == "passive":
            if self.pawn_authorized(authorized_pawns_list):
                    turn_info.pawn_authorized = True
                    self.status = "active"
                    self.sel_x = self.curr_xy[0]
                    self.sel_y = self.curr_xy[1]
            else:
                turn_info.pawn_authorized = False

        elif self.status == "active":
            # A number of jumps different from 0, means that the player is in the middle of a play
            # involving several moves so he cannot change the underlying
            if turn_info.nbr_jumps == 0:
                if (self.sel_x == self.curr_xy[0]) and (self.sel_y == self.curr_xy[1]):
                    self.status = "passive"

    def pawn_authorized(self, authorized_pawns_list):
        """Check whether a pawn is authorized."""
        nbr_jumps = 0
        for authorized_pawn in authorized_pawns_list:
            for authorized_move in authorized_pawn[-1]:
                if type(authorized_move) is list:
                    if authorized_move[-1] > nbr_jumps:
                        nbr_jumps = authorized_move[-1]

        pawn_index = get_pawn_index(authorized_pawns_list, self.curr_xy[0], self.curr_xy[1])

        if pawn_index != -1:
            for authorized_moves in authorized_pawns_list[pawn_index][1]:
                if authorized_moves:
                    if authorized_moves[-1] == nbr_jumps:
                        return True

        return False


