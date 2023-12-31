import pygame

class Menu():
    def __init__(self,game):
        self.game = game
        self.mid_w,self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20) #left top width height
        self.offset = -100 #to avoid cursur to be on the menu 
        self.mouse_pos =pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pressed()

    def draw_cursor(self,addDist=0):
        self.game.draw_text('»',20 ,self.cursor_rect.x ,self.cursor_rect.y+addDist)
    
    def blit_screen(self):
        self.game.window.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.spacing = 30  # Adjust the vertical spacing
        self.startx, self.starty = self.mid_w, self.mid_h+30
        self.optionsx, self.optionsy = self.mid_w, self.starty + self.spacing
        self.rulesx, self.rulesy = self.mid_w, self.optionsy + self.spacing
        self.quitx, self.quity = self.mid_w, self.rulesy + self.spacing
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text('Start Game', 20, self.startx, self.starty)
            self.game.draw_text('Options', 20, self.optionsx, self.optionsy)
            self.game.draw_text('Rules', 20, self.rulesx, self.rulesy)
            self.game.draw_text('Quit', 20, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.rulesx + self.offset, self.rulesy)
                self.state = "Rules"
            elif self.state == "Rules":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)  # Move to Quit
                self.state = "Quit"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)  # Wrap around to Start
                self.state = "Start"
        if self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)  # Move to Quit
                self.state = "Quit"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.rulesx + self.offset, self.rulesy)
                self.state = "Rules"
            elif self.state == "Rules":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"

    def check_input(self):
        self.move_cursor()
        # Handle mouse click events
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # Left mouse button is clicked
            if self.startx < mouse_x < self.startx + 100 and self.starty < mouse_y < self.starty+20 :
                self.state = "Start"
            elif self.optionsx < mouse_x < self.optionsx + 100 and self.optionsy < mouse_y < self.optionsy + 20:
                self.state = "Options"
            elif self.rulesx < mouse_x < self.rulesx + 100 and self.rulesy < mouse_y < self.rulesy + 20:
                self.state = "Rules"
            elif self.quitx < mouse_x < self.quitx + 100 and self.quity < mouse_y < self.quity + 20:
                self.state = "Quit"

        if self.game.START_KEY or pygame.mouse.get_pressed()[0]:
            if self.state == "Start":
                self.game.curr_menu = self.game.moods
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            elif self.state == "Rules":
                self.game.curr_menu = self.game.rules
            elif self.state == "Quit":
                self.game.quit()  # Quit the game
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.spacing = 40  # Adjust the vertical spacing
        self.volx, self.voly = self.mid_w,self.mid_h + 20
        self.soundx,self.soundy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.volx +self.offset, self.voly)
        self.backx, self.backy = self.mid_w, self.mid_h + 60  # Add back button

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Options',20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('Volume',20, self.volx, self.voly)
            self.game.draw_text('Sounds',20, self.soundx,self.soundy)
            self.game.draw_text('Back', 20, self.backx, self.backy+20)  # Back button
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == "Volume":
                self.cursor_rect.midtop = (self.soundx + self.offset, self.soundy)
                self.state = "Sounds"
            elif self.state == "Sounds":
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy+20)  # Move to Back
                self.state = "Back"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = "Volume"

        elif self.game.START_KEY:
            if self.state == "Volume":
                self.game.curr_menu = self.game.slide
            elif self.state == "Sounds":
                self.game.curr_menu = self.game.slide
            elif self.state == "Back":
                self.game.curr_menu = self.game.main_menu
            self.run_display = False

class RulesMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.backx, self.backy = self.mid_w, self.mid_h + 60  # Add back button
    
    def display_menu(self):
        self.run_display =True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Rules',20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('The first player to align 4 gobblets in a row wins .', 18, self.mid_w, self.mid_h + 20)
            self.game.draw_text(' The gobblets forming the line do not have to be the same size', 18, self.mid_w, self.mid_h + 20+20)
            self.game.draw_text('it can be lined up vertically,  horizontally or diagonally.', 18, self.mid_w, self.mid_h + 20+20+20)
            self.game.draw_text('Back', 20, self.backx, self.backy+40)  # Back button
            self.draw_cursor()
            self.blit_screen()


    def check_input(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

    # Check for mouse click
        if self.backx < mouse_x < self.backx + 100 and self.backy < mouse_y < self.backy + 20:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button is clicked
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

        # Check for BACK_KEY
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
        self.backx, self.backy = self.mid_w, self.mid_h + 60  # Add back button
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Choose a Mood:', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('Human VS Human', 20, self.mood1x, self.mood1y)
            self.game.draw_text('Human VS Computer', 20, self.mood2x, self.mood2y+20)
            self.game.draw_text('Computer VS Computer', 20, self.mood3x,self.mood3y+40)
            self.game.draw_text('Back', 20, self.backx, self.backy+90)  # Back button
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == "mood1" :
                self.cursor_rect.midtop = (self.mood2x + self.offset-20, self.mood2y+20)
                self.state = "mood2"
            elif self.state == "mood2" :
                self.cursor_rect.midtop = (self.mood3x + self.offset -30, self.mood3y+40)
                self.state = "mood3"
            elif self.state == "mood3" :
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy+90)
                self.state = "back"
            elif self.state=="back":
                self.cursor_rect.midtop=(self.mood1x + self.offset, self.mood1y)
                self.state="mood1"
        elif self.game.UP_KEY:
            if self.state == "mood1" :
                self.cursor_rect.midtop = (self.backx + self.offset -30 , self.backy+90)
                self.state = "back"
            elif(self.state=="back"):
                self.cursor_rect.midtop = (self.mood3x + self.offset -20, self.mood3y+40)
                self.state = "mood3"
            elif self.state == "mood3" :
                self.cursor_rect.midtop = (self.mood2x + self.offset -20, self.mood2y+20)
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
            elif(self.state=="back"):
                self.game.curr_menu=self.game.main_menu
            self.run_display = False

class levelsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Easy"
        self.easx, self.easy = self.mid_w, self.mid_h + 20
        self.medx,self.medy = self.mid_w, self.mid_h + 50
        self.hardx, self.hardy = self.mid_w, self.mid_h + 80

        self.cursor_rect.midtop = (self.easx + self.offset, self.easy)
        self.backx, self.backy = self.mid_w, self.mid_h + 60  # Add back button

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Choose difficulty:', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Easy', 20, self.easx, self.easy)
            self.game.draw_text('Medium',20, self.medx, self.medy)
            self.game.draw_text('Hard', 20, self.hardx, self.hardy)
            self.game.draw_text('Back', 20, self.backx, self.backy + 70)  # Back button
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.moods
            self.run_display = False
        if self.game.DOWN_KEY:
            if self.state == "Easy":
                self.cursor_rect.midtop = (self.medx + self.offset, self.medy)
                self.state = "Medium"
            elif self.state == "Medium" :
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = "Hard"
            elif self.state == "Hard":
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy+70)  # Move to Back
                self.state = "Back"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.easx + self.offset, self.easy)  # Move to Easy
                self.state = "Easy"
        elif self.game.UP_KEY:
            if self.state == "Easy":
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy+70)  # Move to Back
                self.state = "Back"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)  # Move to Hard
                self.state = "Hard"
            elif self.state == "Hard":
                self.cursor_rect.midtop = (self.medx + self.offset, self.medy)  # Move to Easy
                self.state = "Medium"
            elif self.state == "Medium":
                self.cursor_rect.midtop = (self.easx + self.offset, self.easy)  # Move to Easy
                self.state = "Easy"
            
        elif pygame.mouse.get_pressed()[1]:  # Middle mouse button is clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.backx < mouse_x < self.backx + 100 and self.backy < mouse_y < self.backy + 20:
                self.state = "Back"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY or pygame.mouse.get_pressed()[0]:  # Left mouse button is clicked
            if self.state == "Easy":
                # self.game.playing = True
                self.game.curr_menu=self.game.gameView
            elif self.state == "Medium":
                self.game.curr_menu = self.game.gameView
            elif self.state == "Hard":
                self.game.curr_menu = self.game.gameView
            elif self.state == "Back":
                self.game.curr_menu = self.game.main_menu
            self.run_display = False

class WinScreen(Menu):
    def __init__(self, game,msg):
        self.msg=msg
        Menu.__init__(self, game,)
        
    def display_menu(self):
        self.run_display =True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text(self.msg, 40, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.draw_cursor()
            self.blit_screen()
    def setMsg(self,msg):
        self.msg=msg
        
    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False        
                    
                    
class LoseScreen(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        
    def display_menu(self):
        self.run_display =True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text("You Lose!", 40, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False        
                    

class PauseMenu(Menu): #enherite menu
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Resume" #want to the cursor to be placed at start at first
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.rulesx,self.rulesy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset,self.starty)
        
        #pause timer
        self.elapsed_seconds = 0
        self.mins=0

    def display_menu(self):
        self.run_display =True
        self.clock = pygame.time.Clock()
        self.start_pause_time = pygame.time.get_ticks()
        self.paused_mseconds =0
        
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BACK_COLOR)
            self.game.draw_text('Menu',20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 -20)
            self.game.draw_text('Resume',20, self.startx,self.starty)
            self.game.draw_text('Options',20, self.optionsx, self.optionsy)
            self.game.draw_text('Main menu',20, self.rulesx,self.rulesy)
            self.timer()
            self.draw_cursor()
            self.blit_screen()
            
    def move_cursor(self):
        if self.game.BACK_KEY:
            self.game.total_paused_mseconds = 0
            self.game.curr_menu = self.game.main_menu
            self.game.paused_flag=0
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
                self.game.total_paused_mseconds += self.paused_mseconds
                if self.game.game_mood == "hvh":
                    self.game.curr_menu = self.game.gameViewHVH
                elif self.game.game_mood == "v":
                    self.game.curr_menu = self.game.gameView
                    
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            elif self.state == "Main menu":
                self.game.total_paused_mseconds = 0
                self.game.curr_menu = self.game.main_menu
                self.game.paused_flag=0
            self.run_display = False
    
    def timer(self):
        self.current_time = pygame.time.get_ticks()
        self.paused_mseconds = self.current_time - self.start_pause_time
        self.paused_seconds = self.paused_mseconds // 1000
        self.clock.tick(60)
        print("pasued seconds",self.paused_seconds) 
    

##el molahza elwahida,, eni lama basib el cursor 3and hard w dost backspace w rege3t tani d5lt lel level byfdal 3ala hard idk why         
##el molahza elwahida,, eni lama basib el cursor 3and hard w dost backspace w rege3t tani d5lt lel level byfdal 3ala hard idk why 