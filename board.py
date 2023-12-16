""" class Board:
    WHITE_PLAYER = 0
    BLACK = 4
    BOARD_SIZE = 4
    PIECES_COUNT = 4
    UNUSED_SETS = 3
    W_UNUSED_ROW = BOARD_SIZE
    B_UNUSED_COLUMN = BOARD_SIZE

    WHITE_MASK = 15
    BLACK_MASK = 15 << BLACK

    PIECES = [1, 1 << 1, 1 << 2, 1 << 3]

    DUMMY = -1
    DRAW = -2

    def __init__(self):
        self.tiles = [[0] * (self.BOARD_SIZE + 1) for _ in range(self.BOARD_SIZE + 1)]
        self.draw = False
        self.positions_counter = {}

        self.init()

    def generate_possible_moves(self, player):
        result = []

        from_pieces = [[0] * (self.BOARD_SIZE + 1) for _ in range(self.BOARD_SIZE + 1)]
        to_pieces = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]

        for i in range(self.BOARD_SIZE + 1):
            for j in range(self.BOARD_SIZE + 1):
                from_pieces[i][j] = self.get_movable_piece(i, j, player)
                if i < self.BOARD_SIZE and j < self.BOARD_SIZE:
                    to_pieces[i][j] = self.get_placeable_pieces(i, j)

        # Correct indentation for the nested loops and the return statement
        for i in range(self.BOARD_SIZE + 1):
            for j in range(self.BOARD_SIZE + 1):
                for k in range(self.BOARD_SIZE):
                    for l in range(self.BOARD_SIZE):
                        if (from_pieces[i][j] & to_pieces[k][l]) > 0:
                            # Fix the method call by passing correct arguments
                            result.append(Move(i, j, k, l, self.get_movable_piece(i, j, player), player))

        return result
    
    def make_move(self, move):
        return self.make_move_internal(move.from_x, move.from_y, move.to_x, move.to_y, move.piece, move.player)

    def make_move_internal(self, from_x, from_y, to_x, to_y, piece, player):
        if piece != self.get_movable_piece(from_x, from_y, player):
            return False
        if not self.is_piece_placeable(to_x, to_y, piece, player):
            return False

        # remove from old tile
        self.tiles[from_x][from_y] &= ~(piece << player)

        # put to a new tile
        self.tiles[to_x][to_y] |= (piece << player)

        # add the new board to the history
        count = 1
        simple_hash = self.calculate_simple_hash()
        if simple_hash in self.positions_counter:
            count += self.positions_counter[simple_hash]
        self.positions_counter[simple_hash] = count

        # draw check
        if count >= 3:
            self.draw = True

        return True

    def init(self):
        for i in range(self.UNUSED_SETS):
            for p in range(self.PIECES_COUNT):
                self.tiles[self.W_UNUSED_ROW][i] |= self.PIECES[p] << self.WHITE_PLAYER
                self.tiles[i][self.B_UNUSED_COLUMN] |= self.PIECES[p] << self.BLACK

    def evaluate_tile(self, x, y):
        white = 0
        black = 0

        weak_tile = 2 if (x - y == 0) or (x + y == self.BOARD_SIZE - 1) else 1

        w_tile = (self.tiles[x][y] & self.WHITE_MASK) >> self.WHITE_PLAYER
        b_tile = (self.tiles[x][y] & self.BLACK_MASK) >> self.BLACK

        stones = 0
        for i in range(self.PIECES_COUNT - 1, -1, -1):
            white += ((w_tile & self.PIECES[i]) >> i) * (i + 1) * (1 - stones / self.PIECES_COUNT)
            black += ((b_tile & self.PIECES[i]) >> i) * (i + 1) * (1 - stones / self.PIECES_COUNT)
            stones += ((w_tile & self.PIECES[i]) >> i) + ((b_tile & self.PIECES[i]) >> i)

        return (white - black) * weak_tile

    def evaluate_board(self):
        if self.draw:
            return 0

        groups_map = self.get_groups_map()

        result = 0

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                result += groups_map[i][j] * self.evaluate_tile(i, j)

        return result

    def map_group_length_to_bonus(self, length):
        if length == 1:
            return 1
        elif length == 2:
            return 10
        elif length == 3:
            return 20
        elif length == 4:
            return 1000
        else:
            raise ValueError("Illegal Group Length: " + str(length))

    def get_player_map(self):
        result = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                w_tile = (self.tiles[i][j] & self.WHITE_MASK) >> self.WHITE_PLAYER
                b_tile = (self.tiles[i][j] & self.BLACK_MASK) >> self.BLACK
                if w_tile == 0 and b_tile == 0:
                    result[i][j] = self.DUMMY
                else:
                    result[i][j] = self.WHITE_PLAYER if w_tile > b_tile else self.BLACK
        return result

    def get_groups_map(self):
        groups_map = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        row_groups_map = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        col_groups_map = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        diag_groups_map = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        player_map = self.get_player_map()

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if player_map[i][j] == self.DUMMY:
                    continue

                # checks the groups in rows
                if row_groups_map[i][j] == 0:
                    size = 0
                    for l in range(j, self.BOARD_SIZE):
                        if player_map[i][j] == player_map[i][l]:
                            size += 1
                        else:
                            break
                    bonus = self.map_group_length_to_bonus(size)
                    for l in range(j, j + size):
                        row_groups_map[i][l] += bonus

                # checks the groups in columns
                if col_groups_map[i][j] == 0:
                    size = 0
                    for l in range(i, self.BOARD_SIZE):
                        if player_map[i][j] == player_map[l][j]:
                            size += 1
                        else:
                            break
                    bonus = self.map_group_length_to_bonus(size)
                    for l in range(i, i + size):
                        col_groups_map[l][j] += bonus

                # checks the groups for the diagonals
                if (diag_groups_map[i][j] == 0) and (((i - j) == 0) or ((i + j) == self.BOARD_SIZE - 1)):
                    size = 0
                    if (i - j) == 0:
                        for l in range(i, self.BOARD_SIZE):
                            if player_map[i][j] == player_map[l][l]:
                                size += 1
                            else:
                                break
                        bonus = self.map_group_length_to_bonus(size)
                        for l in range(i, i + size):
                            diag_groups_map[l][l] += bonus
                    else:  # (i+j) == BOARD_SIZE-1)
                        for l in range(i, self.BOARD_SIZE):
                            if player_map[i][j] == player_map[l][self.BOARD_SIZE - 1 - l]:
                                size += 1
                            else:
                                break
                        bonus = self.map_group_length_to_bonus(size)
                        for l in range(i, i + size):
                            diag_groups_map[l][self.BOARD_SIZE - 1 - l] += bonus

                # sums together
                groups_map[i][j] = row_groups_map[i][j] + col_groups_map[i][j] + diag_groups_map[i][j]

        return groups_map

    def get_placeable_pieces(self, x, y):
        result = 0
        for i in range(self.PIECES_COUNT - 1, -1, -1):
            if not self.is_piece_on(x, y, self.PIECES[i]):
                result |= self.PIECES[i]
            else:
                break
        return result

    def is_piece_placeable(self, x, y, piece, player):
        highest_w_piece = self.get_piece_on_top(x, y, self.WHITE_PLAYER)
        highest_b_piece = self.get_piece_on_top(x, y, self.BLACK)

        return piece > highest_w_piece and piece > highest_b_piece

    def get_piece_on_top(self, x, y, player):
        mask = self.WHITE_MASK if player == self.WHITE_PLAYER else self.BLACK_MASK
        player_tile = (self.tiles[x][y] & mask) >> player
        if player_tile > 0:
            piece_index = int((player_tile & -player_tile).bit_length()) - 1
            return 1 << piece_index
        else:
            return 0

    def get_movable_piece(self, x, y, player):
        highest_w_piece = self.get_piece_on_top(x, y, self.WHITE_PLAYER)
        highest_b_piece = self.get_piece_on_top(x, y, self.BLACK)

        if player == self.WHITE_PLAYER:
            return highest_w_piece if highest_w_piece > highest_b_piece else 0
        else:
            return highest_b_piece if highest_b_piece > highest_w_piece else 0

    def is_piece_on(self, x, y, piece, player):
        return (self.tiles[x][y] & (piece << player)) > 0

    def is_piece_on(self, x, y, piece):
        return self.is_piece_on(x, y, piece, self.WHITE_PLAYER) or self.is_piece_on(x, y, piece, self.BLACK)

    def is_terminate(self, player_to_move):
        win_player = self.DUMMY
        if self.draw:
            return self.DRAW
        groups_map = self.get_groups_map()
        player_map = self.get_player_map()
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if win_player != player_to_move and groups_map[i][j] >= 1000:
                    win_player = player_map[i][j]
        return win_player

    def calculate_simple_hash(self):
        hash_value = 0
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                hash_value = 31 * hash_value + self.tiles[i][j]
        return hash_value

    def __hash__(self):
        return int(self.calculate_simple_hash())

    def __eq__(self, other):
        if hash(self) != hash(other):
            return False
        for i in range(self.BOARD_SIZE + 1):
            for j in range(self.BOARD_SIZE + 1):
                if self.tiles[i][j] != other.tiles[i][j]:
                    return False
        return True

    def __str__(self):
        result = "-----------------------------------------------------------------\n"
        for x in range(self.BOARD_SIZE - 1, -1, -1):
            result += chr(65 + x) + " |\t"
            for y in range(self.BOARD_SIZE):
                result += str(self.tiles[x][y]) + "\t|\t"
            result += "\n"
        result += "-----------------------------------------------------------------\n"
        result += "  |\t"
        for i in range(self.BOARD_SIZE):
            result += str(i) + "\t|\t"
        result += "\n\nW: "
        for i in range(self.UNUSED_SETS):
            result += str(self.tiles[self.W_UNUSED_ROW][i]) + " "
        result += "\nB: "
        for i in range(self.UNUSED_SETS):
            result += str(self.tiles[i][self.B_UNUSED_COLUMN]) + " "

        return result



 """