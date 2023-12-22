import pygame
from random import randint, choice
from pathlib import Path
from os import path

FPS = 60 # Frames Per Second (FPS)
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
WORDS = [] # WORDS holds all the words available for the game
WORDS_ON_SCREEN = [] # WORDS_ON_SCREEN contains words currently displayed on the game screen.
DIFFICULTY = 3 # The initial difficulty level of the game. This value is used to adjust the game's difficulty based on the player's performance.
DELAY = FPS * DIFFICULTY # the delay (in frames) between generating new words during gameplay. It's calculated based on the product of FPS and DIFFICULTY.
WORD_MOVE_TIME = FPS * 1 # The time (in frames) for a word to move across the screen. This value is set to represent 1 second's duration in terms of frames.
WORDS_POSITION = [-1*x for x in range(0,round(WORD_MOVE_TIME/6))] # WORDS_POSITION is a list of integers that represent the y-axis positions of the words displayed on the screen. The list is used to make sure that words are not displayed on the same line.
user_input = ""
current_score = 0
BG_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
life_count = 3
ANTI_ALIASING = True
FONT_FILE = Path(path.dirname(__file__)) / 'data' / 'font.ttf'
WORDS_FILE = Path(path.dirname(__file__)) / 'data' / 'words.txt'


def main() -> None:
    pygame.init() # Initialize all imported pygame modules

    new_word_delay_counter = 0 # Delay for new word
    move_delay_counter = 0 # Delay for word move
    global BASIC_FONT, game_surface, FPS_CLOCK, words, char, DIFFICULTY, DELAY, WORD_MOVE_TIME 
    FPS_CLOCK = pygame.time.Clock() # Create an object to help track time
    game_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Create a new Surface object that is the same size as the display Surface object
    pygame.display.set_caption("TurboType") # Set the current window caption
    BASIC_FONT = pygame.font.Font(FONT_FILE, 20)

    with open(WORDS_FILE) as file:
        words = file.readlines() # words is a list stores the possible words for the game

    select_rand_word()
    draw_start_screen("Start")

    
    while True:
        if process_input() == "enter":
            break # start the game

    game_surface.fill(BG_COLOR) # Fill Surface object with a solid color, remove the start screen
    draw_ui()


    while True:
        refresh_score()
        update_difficulty()
        redraw_life_count()
        new_word_delay_counter += 1 
        move_delay_counter += 1
        char = process_input()
        show_text(char)
        if new_word_delay_counter >= DELAY: 
            select_rand_word() # select a random word from words list
            new_word_delay_counter = 0 # reset new_word_delay_counter
        for word in WORDS_ON_SCREEN: # remove words that are not in WORDS list
            if word.name not in WORDS: # the word is correct
                word.word_remove()
        if move_delay_counter == WORD_MOVE_TIME:
            for word in WORDS_ON_SCREEN:
                word.word_move()
                word.word_draw()
            move_delay_counter = 0
        FPS_CLOCK.tick(FPS) # wait for the next frame


def terminate() -> None:
    pygame.quit()
    exit()


def process_input() -> str:
    global user_input, current_score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN: # KEYDOWN means a key is pressed
            if (event.key != pygame.K_RETURN) and (event.key != pygame.K_BACKSPACE): #? K_RETURN is the enter key #? K_BACKSPACE is the backspace key
                if (len(user_input)) <= 45: # 45 is the maximum number of characters allowed to be entered, (the longest word in the English dictionary is 45 characters long)
                    user_input+=event.unicode # unicode is the string of the key pressed
            elif event.key == pygame.K_RETURN and (user_input in WORDS): # a valid word is entered
                WORDS.remove(user_input)
                current_score+=1 # increase the current score
                user_input="" # reset user_input
                return "enter"
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[0:len(user_input) - 1] # remove last character
                return "backspace" # return backspace to show_text
            else:
                user_input = "" 
                return "enter"
    return ''

def select_rand_word() -> None:
    word = choice(words).rstrip("\n") # random.choice(words: list)
    WORDS.append(word) # add the word to WORDS list
    WORDS_ON_SCREEN.append(WordOnScreen(word)) # create a WordOnScreen object and add it to WORDS_ON_SCREEN list
        

def show_text(char: str) -> None:
    global user_input
    text_sufrace = BASIC_FONT.render(user_input,ANTI_ALIASING,WHITE)
    text_rectangle = text_sufrace.get_rect()
    text_rectangle.bottomleft = (WINDOW_WIDTH / 50,WINDOW_HEIGHT / 10 * 9.8)
    pygame.draw.rect(game_surface, BG_COLOR, text_rectangle) # remove previous text
    game_surface.blit(text_sufrace,text_rectangle) # draw the text on the screen

    if char == "backspace":
        remove_text = text_rectangle
        remove_text[2] = WINDOW_WIDTH / 1.5
        pygame.draw.rect(game_surface, BG_COLOR, remove_text)
        game_surface.blit(text_sufrace,text_rectangle)

    if char == "enter":
        remove_text = text_rectangle
        remove_text[2] = WINDOW_WIDTH / 1.5
        pygame.draw.rect(game_surface, BG_COLOR, remove_text)

    pygame.display.update() # update the display Surface to the screen


def draw_ui():
    
    def draw_line() -> None:
        left_point = (0,WINDOW_HEIGHT/10 * 9.2) # 9.2/10 of the screen
        right_point = (WINDOW_WIDTH,WINDOW_HEIGHT/10 * 9.2)
        pygame.draw.line(game_surface,GREEN,left_point,right_point)
        
    def draw_score_label() -> None:
        text_sufrace = BASIC_FONT.render("Score:",ANTI_ALIASING,WHITE)
        text_rectangle = text_sufrace.get_rect()
        text_rectangle.bottomleft = (WINDOW_WIDTH / 1.4,WINDOW_HEIGHT / 10 * 9.8)
        game_surface.blit(text_sufrace,text_rectangle)
    
    draw_line()
    draw_score_label()