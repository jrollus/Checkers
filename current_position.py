class CurrentPosition:
    """A class to represent the current X,Y position."""
    def __init__(self, x_position, y_position):
        self.x = x_position
        self.y = y_position

    def move(self, move_direction, move_type):
        if move_type == "next":
            self.x += move_direction[0]
            self.y += move_direction[1]
        elif move_type == "previous":
            self.x -= move_direction[0]
            self.y -= move_direction[1]