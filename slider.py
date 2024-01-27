import pygame
from pygame import mixer

class Slider:
    def __init__(self,game):
        self.game = game
        self.width, self.height = 250,10
        self.mid_w,self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.left_pos = self.mid_w - self.width/2
        self.right_pos = self.mid_w + self.width/2
        self.top_pos = self.mid_h - self.height/2
        self.min = 0
        self.max = 100
        self.initial_val = (self.right_pos-self.left_pos)*0.5
        self.slid_rect=pygame.Rect(self.left_pos, self.top_pos, self.width, self.height)
        self.hidden_rect=pygame.Rect(self.left_pos, self.top_pos-20, self.width, 50)
        self.handle_rect=pygame.Rect(self.mid_w -4 ,self.mid_h-10, 8, 20)
    
    def blit_screen(self):
        self.game.window.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display =True
        while self.run_display:
            self.mouse_pos =pygame.mouse.get_pos()
            self.mouse = pygame.mouse.get_pressed()
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            pygame.draw.rect(self.game.display, self.game.BACK_COLOR, self.hidden_rect )
            self.game.draw_text('Volume',20, self.mid_w,self.mid_h -100)
            pygame.draw.rect(self.game.display,(250,250,250), self.slid_rect )
            pygame.draw.rect(self.game.display,(100, 100, 100), self.handle_rect )
            self.move_slider()
            self.blit_screen()
            
            mixer.music.set_volume(self.get_value()/100)

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.options
            self.run_display = False

    def move_slider(self):
        if self.hidden_rect.collidepoint(self.mouse_pos) and self.mouse[0]:
            self.handle_rect.centerx = self.mouse_pos[0]
    
    def get_value(self):
        value_range = self.right_pos - self.left_pos -1
        button_val = self.handle_rect.centerx - self.left_pos

        return (button_val/value_range)*(self.max - self.min)+self.min
    
            
        