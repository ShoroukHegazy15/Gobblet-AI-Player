import pygame
import os

class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, color, size, piece_id, position):
        super().__init__()
        self.color = color
        self.size = size
        self.piece_id = piece_id
        self.image = pygame.image.load(os.path.join(f"Assets/{color}{size}.png")).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        

class View():
    def __init__(self, game):
        self.game = game
        self.run_display = True
        self.bg = pygame.image.load(os.path.join("Assets/board.png")).convert()
        self.BACK_COLOR = (30, 54, 45)
        # self.piece_data = {
        #     "white": {
        #         "large": pygame.image.load(os.path.join("Assets/whiteL.png")).convert_alpha(),
        #         "medium": pygame.image.load(os.path.join("Assets/whiteM.png")).convert_alpha(),
        #         "small": pygame.image.load(os.path.join("Assets/whiteS.png")).convert_alpha(),
        #         "smallX": pygame.image.load(os.path.join("Assets/whiteXS.png")).convert_alpha()
        #     },
        #     "black": {
        #         "large": pygame.image.load(os.path.join("Assets/blackL.png")).convert_alpha(),
        #         "medium": pygame.image.load(os.path.join("Assets/blackM.png")).convert_alpha(),
        #         "small": pygame.image.load(os.path.join("Assets/blackS.png")).convert_alpha(),
        #         "smallX": pygame.image.load(os.path.join("Assets/blackXS.png")).convert_alpha()
        #     }
        # }
        self.board_positions = [
            (215, 110), (386, 110), (555, 110), (724, 110),
            (215, 280), (386, 280), (555, 280), (724, 280),
            (215, 450), (386, 450), (555, 450), (724, 450),
            (215, 620), (386, 620), (555, 620), (724, 620),
        ]
        #self.pieces = {pos: [] for pos in self.board_centers}
        self.piece_positions = [(57, 107), (57, 274), (57, 447),
                                (898, 274), (898, 447), (898, 617)]
        self.pieces = {pos: [] for pos in self.piece_positions + self.board_positions}

        self.chess_pieces = pygame.sprite.Group()  # Group to store all chess pieces
        self.create_pieces()

        # Store the currently dragged piece and its offset
        self.dragged_piece = None
        self.drag_offset = (0, 0)

    def create_pieces(self):
        white_positions = [(57, 107), (57, 274), (57, 447)]
        black_positions = [(898, 274), (898, 447), (898, 617)]

        sizes = ["XS", "S", "M", "L"]


        white_piece_count = {"L": 0, "M": 0, "S": 0, "XS": 0}
        black_piece_count = {"L": 0, "M": 0, "S": 0, "XS": 0}

        for color, positions, piece_count in [("white", white_positions, white_piece_count),
                                            ("black", black_positions, black_piece_count)]:
            for size in sizes:
                for piece_id, start_center in enumerate(positions):
                    # Check the size of the piece and update the count
                    if piece_count[size] < 3:
                        piece = ChessPiece(color, size, piece_id, start_center)
                        self.chess_pieces.add(piece)
                        self.pieces[start_center].append(piece)
                        piece_count[size] += 1
                        
 
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.BACK_COLOR)
            self.game.display.blit(self.bg, (0, 0))
            # Draw chess pieces
            self.chess_pieces.draw(self.game.display)
            self.handle_drag_and_drop()
            self.blit_screen()


    def handle_drag_and_drop(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Check for piece dragging in reverse order
        for piece in reversed(self.chess_pieces.sprites()):
            if piece.rect.collidepoint(mouse_x, mouse_y) and mouse_pressed and not self.dragged_piece:
                # Only allow dragging if the piece's position is in piece_positions
                if piece.rect.center in self.piece_positions or piece.rect.center in self.board_positions:
                    self.dragged_piece = piece
                    self.drag_offset = (piece.rect.centerx - mouse_x, piece.rect.centery - mouse_y)
                    break

        # If a piece is being dragged, update its position
        if self.dragged_piece and mouse_pressed:
            self.dragged_piece.rect.center = (mouse_x , mouse_y )

        # If the mouse button is released and a piece is being dragged
        elif self.dragged_piece and not mouse_pressed:
            self.handle_dropped_piece()

    def handle_dropped_piece(self):
        old_position = self.dragged_piece.rect.center
        new_position = None  # Initialize new_position to None

        # Check if the piece is close to a board position, then snap it
        for board_position in self.board_positions:
            if self.dragged_piece and self.is_close_to_position(self.dragged_piece.rect.center, board_position):
                new_position = board_position
                break
            # else:
            #     new_position = old_position
            #     # break

        # Update the pieces dictionary if the new position is in board_positions
        if new_position in self.board_positions:
            self.dragged_piece.rect.center = new_position
            if old_position in self.pieces:
                self.pieces[old_position].remove(self.dragged_piece)
                self.chess_pieces.remove(self.dragged_piece)
            if new_position in self.pieces:
                self.pieces[new_position].append(self.dragged_piece)
                self.chess_pieces.add(self.dragged_piece)

            # Reorder the sprites to ensure the dragged piece is drawn last
            self.chess_pieces.remove(self.dragged_piece)
            self.chess_pieces.add(self.dragged_piece)
        else:
            # If the new position is not in board_positions, keep the piece at its old position
            self.dragged_piece.rect.center = old_position

        self.dragged_piece = None


    def is_close_to_position(self, pos1, pos2, threshold=100):
        # """Check if two positions are close within a given threshold."""
        return abs(pos1[0] - pos2[0]) < threshold and abs(pos1[1] - pos2[1]) < threshold

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.rules
            self.run_display = False

    