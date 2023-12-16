""" class Move:
    def __init__(self, from_x, from_y, to_x, to_y, piece, player):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.piece = piece
        self.player = player

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def get_player(self):
        return self.player

    def set_player(self, player):
        self.player = player

    def get_from_x(self):
        return self.from_x

    def set_from_x(self, from_x):
        self.from_x = from_x

    def get_from_y(self):
        return self.from_y

    def set_from_y(self, from_y):
        self.from_y = from_y

    def get_to_x(self):
        return self.to_x

    def set_to_x(self, to_x):
        self.to_x = to_x

    def get_to_y(self):
        return self.to_y

    def set_to_y(self, to_y):
        self.to_y = to_y

#   def __str__(self):
#        return f"Piece: {self.piece}, Player: {self.player}, [{chr(self.from_x + 65)},{self.from_y}] -> [{chr(self.to_x + 65)},{self.to_y}]"
 """