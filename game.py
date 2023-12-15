import pygame, os
import sys
from menu import*
from view import View

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing =True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY =False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 956,727
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name=pygame.font.get_default_font()
        self.BACK_COLOR, self.WHITE, self.BLACK = (30, 54, 45), (255,255,255), (0, 0, 0)
        self.main_menu = MainMenu(self)
        self.moods= MoodsMenu(self)
        self.levels= levelsMenu(self)
        self.options = OptionsMenu(self)
        self.rules = RulesMenu(self)
        self.win_screen = WinScreen(self)
        self.lose_screen = LoseScreen(self)
        self.gameView = View(self)
        self.curr_menu= self.main_menu
    
    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BACK_COLOR) 
            self.draw_text('THANKS FOR PLAYING',20,self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display,(0,0))    #reset each frame, (0.0) for aligning.
            pygame.display.update()
            self.reset_keys()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display= False
            if event.type == pygame.KEYDOWN: #keyboard key is pressed down
                if event.key == pygame.K_RETURN:
                    self.START_KEY =True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY =True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY =False, False, False, False
    
    def draw_text(self, text, size, x, y):
        font=pygame.font.Font(self.font_name,size)
        text_serface = font.render(text, True, self.WHITE)
        text_rect=text_serface.get_rect()
        text_rect.center =(x,y) #make the center of the rectag\ngle the given x and y
        self.display.blit(text_serface,text_rect)
    
    def quit(self):
        pygame.quit()
        sys.exit()