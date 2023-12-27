import pygame

class Menu():
    def __init__(self,game):
        self.game = game
        self.mid_w,self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) #left top width height
        self.offset = -100 #to avoid cursur to be on the menu 

    def draw_cursor(self):
        self.game.draw_text('»',20 ,self.cursor_rect.x ,self.cursor_rect.y)
    
    def blit_screen(self):
        self.game.window.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu): #enherite menu
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start" #want to the cursor to be placed at start at first
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.rulesx,self.rulesy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset,self.starty)

    def display_menu(self):
        self.run_display =True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Main Menu',20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('Start Game',20, self.startx,self.starty)
            self.game.draw_text('Options',20, self.optionsx, self.optionsy)
            self.game.draw_text('Rules',20, self.rulesx,self.rulesy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start" :
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options" :
                self.cursor_rect.midtop = (self.rulesx + self.offset, self.rulesy)
                self.state = "Rules"
            elif self.state == "Rules" :
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        if self.game.UP_KEY:
            if self.state == "Start" :
                self.cursor_rect.midtop = (self.rulesx + self.offset, self.rulesy)
                self.state = "Rules"
            elif self.state == "Rules" :
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options" :
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.curr_menu = self.game.moods
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            elif self.state == "Rules":
                self.game.curr_menu = self.game.rules
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w,self.mid_h + 20
        self.soundx,self.soundy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.volx +self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Options',20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('Volume',20, self.volx, self.voly)
            self.game.draw_text('Sounds',20, self.soundx,self.soundy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == "Volume" :
                self.cursor_rect.midtop = (self.soundx + self.offset, self.soundy)
                self.state = "Sounds"
            elif self.state == "Sounds" :
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = "Volume"
        elif self.game.START_KEY:
            if self.state == "Volume":
                self.game.curr_menu=self.game.slide
            elif self.state == "Sounds":
                self.game.curr_menu=self.game.slide
            self.run_display = False

class RulesMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    
    def display_menu(self):
        self.run_display =True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Rules',20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('The first player to align 4 gobblets in a row wins. The gobblets forming the line do not have to be the same size and can be lined up vertically, horizontally or diagonally.', 18, self.mid_w, self.mid_h + 20)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        
class MoodsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "mood1"
        self.mood1x, self.mood1y = self.mid_w,self.mid_h + 30
        self.mood2x,self.mood2y = self.mid_w, self.mid_h + 50
        self.mood3x,self.mood3y = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.mood1x +self.offset, self.mood1y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Choose a Mood:', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('Human VS Human', 20, self.mood1x, self.mood1y)
            self.game.draw_text('Human VS Computer', 20, self.mood2x, self.mood2y)
            self.game.draw_text('Computer VS Computer', 20, self.mood3x,self.mood3y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == "mood1" :
                self.cursor_rect.midtop = (self.mood2x + self.offset-20, self.mood2y)
                self.state = "mood2"
            elif self.state == "mood2" :
                self.cursor_rect.midtop = (self.mood3x + self.offset -30, self.mood3y)
                self.state = "mood3"
            elif self.state == "mood3" :
                self.cursor_rect.midtop = (self.mood1x + self.offset, self.mood1y)
                self.state = "mood1"
        elif self.game.UP_KEY:
            if self.state == "mood1" :
                self.cursor_rect.midtop = (self.mood3x + self.offset -30 , self.mood3y)
                self.state = "mood3"
            elif self.state == "mood3" :
                self.cursor_rect.midtop = (self.mood2x + self.offset -20, self.mood2y)
                self.state = "mood2"
            elif self.state == "mood2" :
                self.cursor_rect.midtop = (self.mood1x + self.offset, self.mood1y)
                self.state = "mood1"
    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "mood1":
                self.game.curr_menu=self.game.gameViewHVH
            elif self.state == "mood2":
                self.game.curr_menu=self.game.levels
            elif self.state == "mood3":
                self.game.curr_menu=self.game.gameViewCVC
                #self.game.playing = True
            self.run_display = False

class levelsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self,game)
        self.state = "Easy"
        self.easx, self.easy = self.mid_w,self.mid_h + 20
        self.medx,self.medy = self.mid_w, self.mid_h + 50
        self.hardx,self.hardy = self.mid_w, self.mid_h + 80

        self.cursor_rect.midtop = (self.easx +self.offset, self.easy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Choose difficulty:',20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('Easy',20, self.easx, self.easy)
            self.game.draw_text('Medium',20, self.medx, self.medy)
            self.game.draw_text('Hard',20, self.hardx,self.hardy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.moods
            self.run_display = False
        elif self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == "Easy" :
                self.cursor_rect.midtop = (self.medx + self.offset, self.medy)
                self.state = "Medum"
            elif self.state == "Medium" :
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = "Hard"
            elif self.state == "Hard" :
                self.cursor_rect.midtop = (self.easx + self.offset, self.easy)
                self.state = "Easy"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Easy":
                # self.game.playing = True
                self.game.curr_menu=self.game.gameView
            elif self.state == "Medium":
                # self.game.playing = True
                self.game.curr_menu=self.game.gameView
            elif self.state == "Hard":
                # self.game.playing = True
                self.game.curr_menu=self.game.gameView
            self.run_display = False

class WinScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
    def display_menu(self):
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("You Win!", 48, self.mid_w, self.mid_h + self.offset)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.run_display = False        
                    
                    
class LoseScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("You Lose!", 48, self.mid_w, self.mid_h + self.offset)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.run_display = False
                    

class PauseMenu(Menu): #enherite menu
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Resume" #want to the cursor to be placed at start at first
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.rulesx,self.rulesy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset,self.starty)

    def display_menu(self):
        self.run_display =True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Menu',20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('Resume',20, self.startx,self.starty)
            self.game.draw_text('Options',20, self.optionsx, self.optionsy)
            self.game.draw_text('Main menu',20, self.rulesx,self.rulesy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Resume" :
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options" :
                self.cursor_rect.midtop = (self.rulesx + self.offset, self.rulesy)
                self.state = "Main menu"
            elif self.state == "Rules" :
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Resume"
        if self.game.UP_KEY:
            if self.state == "Resume" :
                self.cursor_rect.midtop = (self.rulesx + self.offset, self.rulesy)
                self.state = "Main menu"
            elif self.state == "Main menu" :
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options" :
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Resume"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Resume":
                self.game.curr_menu = self.game.gameView
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            elif self.state == "Main menu":
                self.game.curr_menu = self.game.main_menu
            self.run_display = False

        if self.game.DOWN_KEY:
            if self.state == "Resume" :
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options" :
                self.cursor_rect.midtop = (self.rulesx + self.offset, self.rulesy)
                self.state = "Main menu"
            elif self.state == "Rules" :
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Resume"
        if self.game.UP_KEY:
            if self.state == "Resume" :
                self.cursor_rect.midtop = (self.rulesx + self.offset, self.rulesy)
                self.state = "Main menu"
            elif self.state == "Main menu" :
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options" :
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Resume"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Resume":
                self.game.curr_menu = self.game.gameView
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            elif self.state == "Main menu":
                self.game.curr_menu = self.game.main_menu
            self.run_display = False
            
##el molahza elwahida,, eni lama basib el cursor 3and hard w dost backspace w rege3t tani d5lt lel level byfdal 3ala hard idk why         
##el molahza elwahida,, eni lama basib el cursor 3and hard w dost backspace w rege3t tani d5lt lel level byfdal 3ala hard idk why 