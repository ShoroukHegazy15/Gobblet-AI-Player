import pygame
import os

class View():
    def __init__(self, game):
        self.game = game
        self.run_display = True
        self.bg = pygame.image.load(os.path.join("Assets/board.png")).convert()
        self.BACK_COLOR = (30, 54, 45)
        self.piece_data = {
            "white": {
                "large": pygame.image.load(os.path.join("Assets/whiteL.png")).convert_alpha(),
                "medium": pygame.image.load(os.path.join("Assets/whiteM.png")).convert_alpha(),
                "small": pygame.image.load(os.path.join("Assets/whiteS.png")).convert_alpha(),
                "smallX": pygame.image.load(os.path.join("Assets/whiteXS.png")).convert_alpha()
            },
            "black": {
                "large": pygame.image.load(os.path.join("Assets/blackL.png")).convert_alpha(),
                "medium": pygame.image.load(os.path.join("Assets/blackM.png")).convert_alpha(),
                "small": pygame.image.load(os.path.join("Assets/blackS.png")).convert_alpha(),
                "smallX": pygame.image.load(os.path.join("Assets/blackXS.png")).convert_alpha()
            }
        }

        # Store the currently dragged piece and its offset
        self.dragged_piece = None
        self.drag_offset = (0, 0)

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

            # Get the center coordinates of the board image
            centers = [
                (57, 107), (57, 274), (57, 447),
                (898, 274), (898, 447), (898, 617)
            ]

            # Draw white pieces on the first 3 centers
            self.draw_pieces("white", centers[:3])

            # Draw black pieces on the other 3 centers
            self.draw_pieces("black", centers[3:])

            self.blit_screen()

    def draw_pieces(self, color, centers):
        for size in ["smallX", "small", "medium", "large"]:
            data = self.piece_data[color][size]
            for center in centers:
                rect = data.get_rect(center=center)
                self.game.display.blit(data, rect.topleft)

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.rules
            self.run_display = False