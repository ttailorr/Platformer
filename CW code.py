from string import printable
import pygame
from pygame.locals import *

import platform     #to identify Operating system

pygame.init()
pygame.font.init()


my_os = platform.system()   #'Darwin' for macOS, 'Cygwin' for windows
print(my_os)
if my_os == "Cygwin":
    from pygame import mixer       #use this for windows
    pygame.mixer.pre_init(44100, -16, 2, 512)   #initialising some variables for the mixer
    mixer.init()
elif my_os == "Darwin":
    import subprocess       #use this for mac


myfont = pygame.font.SysFont('Bodoni 72', 30)

frames = 90     #this is the fps that the game will be Played at.   Use 90 for mac, 60 for windows
clock = pygame.time.Clock()     #the Clock method is used to 'clock' the game at the fps above


screen_w = 1000     #this is the width of the window
screen_h = 800      #this is the height of the window where the game is Played

screen = pygame.display.set_mode((screen_w, screen_h))  #this creates the game window

square_size = 50    #each square in my world array will have pixel size 50*50

level_status = 0    #1 for level restart, 2 for ongoing, 3 for completed and display completed screem, 4 for next level.

in_menu = True
in_level_selector = False
in_leaderboard = False

map = 0
change_map = False

thetime = 0
timearray = []
timearray1 = []

lives = 3
change_lives = True

appendable = True
appendable1 = True
printable = True

played_gameover_sound = False
completed_sound_played = False


#loading in core images
background_image = pygame.image.load('images/darkbackground.bmp')
background_image = pygame.transform.scale(background_image, (screen_w, screen_h))
restart_image = pygame.image.load('images/restart_btn.bmp')
outer_blocks = pygame.image.load('images/reddirt.bmp')     #these are the blocks that surround the world
platforms = pygame.image.load('images/goodblock.bmp')    #these are what the user jumps onto
menu_background = pygame.image.load('images/MenuBackground.bmp')
menu_background = pygame.transform.scale(menu_background, (screen_w, screen_h))
start_image = pygame.image.load('images/start.bmp')
start_image = pygame.transform.scale(start_image, (100, 50))
completed = pygame.image.load('images/next.bmp')
completed = pygame.transform.scale(completed, (100, 50))
game_over_image = pygame.image.load('images/GameOver.bmp')
level_select = pygame.image.load('images/LevelSelect.bmp')
level_select = pygame.transform.scale(level_select, (150, 50))
icon1 = pygame.image.load('images/1.bmp')
icon1 = pygame.transform.scale(icon1, (100, 100))
icon2 = pygame.image.load('images/2.bmp')
icon2 = pygame.transform.scale(icon2, (100, 100))
level_completed = pygame.image.load('images/LevelCompleted.bmp')
level_completed = pygame.transform.scale(level_completed, (screen_w, screen_h))
leaderboard_image = pygame.image.load('images/leaderboardimage.bmp')
leaderboard_image = pygame.transform.scale(leaderboard_image, (100, 60))
back_image = pygame.image.load('images/back_to_menu.bmp')
back_image = pygame.transform.scale(back_image, (70, 56))



#loading in core sounds
if my_os == "Cygwin":
    button_click_sound = pygame.mixer.Sound('Sounds/button_sound.wav') #cannot use mp3 format
    button_click_sound.set_volume(0.2)
    game_over_sound = pygame.mixer.Sound('Sounds/roblox_oof.wav')
    game_over_sound.set_volume(0.3)
    level_complete_sound = pygame.mixer.Sound('Sounds/level_win_sound.wav')
    level_complete_sound.set_volume(0.2)


world_data1 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 2, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1]
]

world_data0 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 2, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 1, 2, 1, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Trap(pygame.sprite.Sprite):   #my Trap class is the child class of pygame's built in sprite class
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #calls the constructor of pygame's sprite class
        self.image = pygame.image.load('images/trap.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.pointerx = x
        self.rect.y = y
        self.direction = 1

    def update(self):
        self.rect.x += self.direction
        if self.rect.x >= self.pointerx + 50:
            self.direction *= -1
        if self.rect.x <= self.pointerx - 50:
            self.direction *= -1

trap_list = pygame.sprite.Group()   #this creates a list from the parent class that stores all trap objects
trap_list1 = pygame.sprite.Group()


class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #calls the constructor of pygame's sprite class
        image = pygame.image.load('images/fire.bmp')
        self.image = pygame.transform.scale(image, (square_size, square_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

fire_list = pygame.sprite.Group()
fire_list1 = pygame.sprite.Group()


class Destination(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) #calls the constructor of pygame's sprite class
        image = pygame.image.load('images/destination.bmp')
        self.image = pygame.transform.scale(image, (square_size, square_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

destination_list = pygame.sprite.Group()
destination_list1 = pygame.sprite.Group()


#this class will take the world_data and actualise it
class World():
    def __init__(self, array, traps, destinations, fires):  #constructor
        
        self.squares_list = []

        row_number = 0
        for row in array:    #for every row in the data (python takes the 2d array and will examine each list at a time)
            collumn_number = 0
            for square in row:    #for each element in that selected list (like collumns in the array)
                if square == 1:
                    self.image = pygame.transform.scale(outer_blocks, (square_size, square_size))  #scale the image to square size
                    self.image_rect = self.image.get_rect()   #forms a 'rectangle' that holds actionable data on the image
                    self.image_rect.x = collumn_number * square_size   #x co-ordinate of the rectangle
                    self.image_rect.y = row_number * square_size    #y co-ordinate of the rectangle
                    self.square = (self.image, self.image_rect)    #tuple
                    self.squares_list.append(self.square)
                if square == 2:
                    self.image = pygame.transform.scale(platforms, (square_size, square_size))  #scale the image to tile size
                    self.image_rect = self.image.get_rect()   #forms a 'rectangle' that holds actionable data on the image
                    self.image_rect.x = collumn_number * square_size   #x co-ordinate of the rectangle
                    self.image_rect.y = row_number * square_size    #y co-ordinate of the rectangle
                    self.square = (self.image, self.image_rect)  #tuple
                    self.squares_list.append(self.square) #in this array there'll be lots of square variables
                if square == 3:
                    self.trap = Trap(collumn_number * square_size, row_number * square_size) #creates an instance of Trap class
                    traps.add(self.trap) #stores the instance in this list
                if square == 8:
                    self.destination = Destination(collumn_number * square_size, row_number * square_size)
                    destinations.add(self.destination)
                if square == 9:
                    self.fire = Fire(collumn_number * square_size, row_number * square_size + 10)
                    fires.add(self.fire)
                collumn_number += 1
            row_number += 1
    
    def world_to_screen(self):
        for self.square in self.squares_list:
            screen.blit(self.square[0], self.square[1])  # must draw 2 items to screen because each square in the list is a tuple.                                               # square[0] is the image and square[1] is the rect

    def map_change(self, thetime, theworld, fire, condition, trap, destination):
        screen.blit(background_image, (0, 0))
        text_to_screen(thetime, square_size, square_size, True)
        text_to_screen(lives, screen_w - square_size - 17, square_size, False)
        
        theworld.world_to_screen()

        fire.draw(screen)
        
        if condition:
            trap.update()

        trap.draw(screen)

        destination.draw(screen)

real_world0 = World(world_data0, trap_list, destination_list, fire_list)
real_world1 = World(world_data1, trap_list1, destination_list1, fire_list1)


#here I will initialise the player and allow the user to move it
class Player():
    def __init__(self, x ,y):
        self.guy1 = pygame.image.load('images/guy1.bmp')
        self.guy1 = pygame.transform.scale(self.guy1, (40, 80))
        self.guy2 = pygame.image.load('images/guy2.bmp')
        self.guy2 = pygame.transform.scale(self.guy2, (40, 80))
        self.guy3 = pygame.image.load('images/guy3.bmp')
        self.guy3 = pygame.transform.scale(self.guy3, (40, 80))
        self.guy4 = pygame.image.load('images/guy4.bmp')
        self.guy4 = pygame.transform.scale(self.guy4, (40, 80))
        self.dead = pygame.image.load('images/DeadMan.bmp')
        self.dead = pygame.transform.scale(self.dead, (80, 40))
        self.image = pygame.transform.scale(self.guy1, (40, 80))  #scales our guy image to width of 40 height 80
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect.x = x
        self.rect.y = y

        self.y_speed = 0
        self.space_pressed = False
        self.grounded = True

        self.direction = "right"
        self.animation_count = 0

        self.started = False

        self.lives = 3
        self.change_lives = True

    def movement(self, level_status, the_world, traps, destinations, fires):
        #allowing player to move character
        change_x = 0
        change_y = 0
        if level_status == 0:
            press = pygame.key.get_pressed()
            if press[pygame.K_a]:   #if the user presses a
                change_x -= 5
                self.direction = "left"
                self.animation_count -= 1
            if press[pygame.K_d]:  #if the user presses d
                change_x += 5
                self.direction = "right"
                self.animation_count += 1
            if press[pygame.K_SPACE] and self.space_pressed == False and self.grounded == True:
                self.y_speed = -15
                self.space_pressed = True
                self.grounded = False
            if press[pygame.K_SPACE] == False:
                self.space_pressed = False


            #walking animations
            if self.direction == "right":   #when the character is moving right
                if self.animation_count > 24:   #if animation count is out of range 
                    self.animation_count = 0    #restart 
                if self.animation_count == 6:   #as the user keeps moving change the image
                    self.image = self.guy1
                if self.animation_count == 12:
                    self.image = self.guy2 
                if self.animation_count == 18:
                    self.image = self.guy3
                if self.animation_count == 24:
                    self.image = self.guy4
            if self.direction == "left":    #when the character is moving right
                if self.animation_count < 0:
                    self.animation_count = 24
                if self.animation_count == 6:
                    self.image = pygame.transform.flip(self.guy1, True, False)  #flips image so that...
                if self.animation_count == 12:                           #...it looks like player turned around
                    self.image = pygame.transform.flip(self.guy2, True, False) 
                if self.animation_count == 18:
                    self.image = pygame.transform.flip(self.guy3, True, False)
                if self.animation_count == 24:
                    self.image = pygame.transform.flip(self.guy4, True, False)


            #gravity
            self.y_speed += 0.8
            if self.y_speed > 9.8:  #I used 9.8 because gravity = 9.8N
                self.y_speed = 9.8
            change_y += self.y_speed

            #collision detection with blocks
            for square in the_world.squares_list:
                if square[1].colliderect(self.rect.x + change_x, self.rect.y, self.width, self.height): #collision for future x co-ordinate
                    change_x = 0
                    self.grounded = True
                if square[1].colliderect(self.rect.x, self.rect.y + change_y, self.width, self.height):   #checks if the rect of the tile collides with rect of player
                    if self.y_speed < 0: #if player is moving upwards
                        self.y_speed = 0
                        change_y = 0 #allows player to approach the tile but not move beyond    
                    elif self.y_speed > 0: #if player is moving downwards
                        change_y = 0
                        self.y_speed = 0
                        self.grounded = True
            #collision detection with traps
            if pygame.sprite.spritecollide(self, traps, False): #built in pygame collision detection for sprite class
                level_status = 1
                #return level_status
            if pygame.sprite.spritecollide(self, fires, False): #built in pygame collision detection for sprite class
                level_status = 1
                #return level_status
            if pygame.sprite.spritecollide(self, destinations, False):
                level_status = 2

            self.rect.x += change_x
            self.rect.y += change_y

        elif level_status == 1:
            self.image = self.dead
            if self.rect.y < screen_h - 100:
                self.rect.y *= 1.015
        
        #make window show player
        screen.blit(self.image, self.rect)

        return level_status

    def no_lives(self, lives, level_status, thetime, change_lives):
        if lives == 0:
            screen.blit(game_over_image, (0, 0))
            text_to_screen(thetime, screen_w//2 - 30, screen_h//2 + 20, True)
            restart.button_to_screen()
            if restart.pressed():
                player.reset(100, screen_h - 130)
                level_status = 0
                thetime = 0
                change_lives = True
                lives = 3
            
        return lives, change_lives

    def reset(self, x, y):
        player.__init__(100, screen_h - 130)

    def next_level(self, map, level_status, thetime, lives, condition, sound_condition): #condition is for whether or not we can display time
        completed_button.button_to_screen()
        condition = False
        sound_condition = True

        if completed_button.pressed() and map == 0:
            #return level status and change map
            level_status = 0   
            map = 1 
            player.reset(100, screen_h - 130)
            thetime = 0
            lives = 3
            condition = True
            
        elif completed_button.pressed and map == 1:
            level_status = 0
            map = 2
            player.reset(100, screen_h - 130)
            condition = True
            thetime = 0
        

        return map, level_status, thetime, lives, condition, sound_condition
        
player = Player(100, screen_h - 130)


class Button():
    def __init__(self, picture, x, y): 
        self.image = picture
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def button_to_screen(self):
        screen.blit(self.image, self.rect)

    def pressed(self):
        self.clicked = False
        mouse_position = pygame.mouse.get_pos() #variable stores mouse co-ordinates
        if self.rect.collidepoint(mouse_position):  #if button collides with mouse co-ordinates
            if pygame.mouse.get_pressed()[0] == 1:  #and if button has been pressed
                self.clicked = True  
                if my_os == "Cygwin":        
                    button_click_sound.play()      #use for windows
                elif my_os == "Darwin":
                    subprocess.call(["afplay", "Sounds/button_sound.wav"])     #use for mac
               
        return self.clicked    

restart = Button(restart_image, screen_w//2 - 60, screen_h//2 - 41)
start = Button(start_image, screen_w//2 - 120, screen_h//2 - 25)
completed_button = Button(completed, screen_w//2 - 50, screen_h//2 - 75)
level_select = Button(level_select, screen_w // 2, screen_h//2 - 25)
level1_button = Button(icon1, screen_w//2 - 100, screen_h//2 - 200)
level2_button = Button(icon2, screen_w//2, screen_h//2 - 200)
leaderboard_button = Button(leaderboard_image, screen_w//2 + 150, screen_h//2 - 35)
to_menu = Button(back_image, screen_w//2 - 35, 0)




def leaderboard_write(thetime, themap):
    if themap == 0:
        thetime = round(thetime/60, 2)
        if thetime >= 1:
            file = open("Leaderboard0.txt", "a")
            file.write(str(thetime))
            file.write("\n")
            file.close()

    if themap == 1:
        thetime = round(thetime/60, 2)
        if thetime >= 1:
            file = open("Leaderboard1.txt", "a")
            file.write(str(thetime))
            file.write("\n")
            file.close()

    return thetime

def timer(level_status, thetime):
        if level_status == 0:
            thetime += 1
        return thetime

def text_to_screen(text, x, y, condition):    #condition is for if the text is a number with decimals
    if condition:
        text = round(text/90, 2)    #Use 90 for mac, 60 for windows
    text = myfont.render(str(text), True, (255,255,255))
    screen.blit(text, (x, y))

    condition = False
    return condition

def display_leaderboard(document, arr, condition): #condition is for whether or not values have been appended
    level = document + 1

    if document == 0:   #opens corresponding document
        f = open("Leaderboard0.txt", "r")
        horizontalx = 0
    elif document == 1:
        f = open("Leaderboard1.txt", "r")
        horizontalx = 325   #to position the next collumn 325 pixels to the right

    if condition:   
        for line in f:
            if line != "\n":   #if the line is not empty
                arr.append(line)    #append value on line to array
    condition = False

    arr = sorted(arr)   #sort array into ascending order


    x = 0
    text_to_screen(f"Level {level} times:", 100 + horizontalx, 250, False)  #blits a formatted string to show what level
    for i in range(5):  #blit quickest five times to screen
        text_to_screen(arr[i], 100 + horizontalx, 300 + x, False)
        x += 50    

  
    return condition, arr





#game loop below
running = True      #while the player is alive running will be true
while(running):
    clock.tick(frames) #game will clock frames times per second

    if in_menu == True:
        thetime = 0
        map = 0
        lives = 3
        level_status = 0
        screen.blit(menu_background, (0, 0))    
       
        start.button_to_screen()
        if start.pressed(): #presessed method returns true if button was pressed
            in_menu = False
            
        
        level_select.button_to_screen()
        if level_select.pressed():
            in_level_selector = True

        leaderboard_button.button_to_screen()
        if leaderboard_button.pressed():
            in_leaderboard = True

        if in_level_selector:
            screen.blit(menu_background, (0, 0))
            
            to_menu.button_to_screen()
            if to_menu.pressed():
                in_menu = True
                in_level_selector = False

            level1_button.button_to_screen()
            level2_button.button_to_screen()

            if level1_button.pressed():
                in_level_selector = False
                in_menu = False
                map = 0

            if level2_button.pressed():
                in_level_selector = False
                in_menu = False
                map = 1

        if in_leaderboard:  #show the fastest times for each level
            screen.blit(menu_background, (0, 0))

            to_menu.button_to_screen()
            if to_menu.pressed():
                in_menu = True
                in_leaderboard = False

            text_to_screen("LEADERBOARD", screen_w//2 - 90, 100, False)

            #for level 1
            appendable, timearray = display_leaderboard(0, timearray, appendable)            

            #for level 2 
            appendable1, timearray1 = display_leaderboard(1, timearray1, appendable1)                             



    elif in_menu == False:

        if map == 0:            
            thetime = timer(level_status, thetime)

            real_world0.map_change(thetime, real_world0, fire_list, True, trap_list, destination_list)
            level_status = player.movement(level_status, real_world0, trap_list, destination_list, fire_list)

            to_menu.button_to_screen()
            if to_menu.pressed():
                in_menu = True
                thetime = 0
        
        if map == 1:            
            thetime = timer(level_status, thetime)

            real_world1.map_change(thetime, real_world1, fire_list1, False, trap_list1, destination_list1)
            level_status = player.movement(level_status, real_world1, trap_list1, destination_list1, fire_list1)

            to_menu.button_to_screen()
            if to_menu.pressed():
                in_menu = True

       

        if level_status == 1:
            restart.button_to_screen()
            
            if change_lives == True:
                lives -= 1
                change_lives = False

            lives, change_lives = player.no_lives(lives, level_status, thetime, change_lives)

            if played_gameover_sound == False:
                if my_os == "Darwin":
                    #subprocess.call(["afplay", "Sounds/roblox_oof.wav"])       #use for mac
                    pass
                elif my_os == "Cygwin":
                    game_over_sound.play()     #use for windows
                
                played_gameover_sound = True

            if restart.pressed():
                player.reset(100, screen_h - 130)
                level_status = 0
                thetime = 0
                change_lives = True
                played_gameover_sound = False

            to_menu.button_to_screen()
            if to_menu.pressed():
                in_menu = True
                level_status = 0
                played_gameover_sound = False
                
                
        if level_status == 2:
            if completed_sound_played == False:
                if my_os == "Darwin":
                    subprocess.call(["afplay", "Sounds/level_win_sound.wav"])      #use for mac
                elif my_os == "Cygwin":
                    level_complete_sound.play()
                    
            screen.blit(level_completed, (0, 0))

            to_menu.button_to_screen()
            if to_menu.pressed():
                in_menu = True
                level_status = 0
            
            #leaderboard writing
            if map == 0 and printable:
                leaderboard_write(thetime, map)
            elif map == 1 and printable:
                leaderboard_write(thetime, map)

            printable = text_to_screen(thetime, screen_w//2 - 20, screen_h//2 + 100, True)
            
            map, level_status, thetime, lives, printable, completed_sound_played = player.next_level(map, level_status, thetime, lives, printable, completed_sound_played)
            

        
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

