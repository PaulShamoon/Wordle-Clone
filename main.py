import random, pygame, sys
from pygame.locals import *
pygame.init()

#setting color codes for display and character boxes
white = (255, 255, 255)
yellow = (255, 255, 102)
grey = (211, 211, 211)
black = (0, 0, 0)
green = (0, 255, 0)
light_green = (153, 255, 204)

#setting font for characters
letter_font = pygame.font.SysFont("Helvetica neue", 40)
statement_font = pygame.font.SysFont("Helvetica neue", 35)

#statements to be displayed upon game outcome
winning_statement = statement_font.render("You Win!", True, light_green)
losing_statement = statement_font.render("You Lose!", True, light_green)
word_not_in_list = statement_font.render("Not in Word List", True, light_green)

def main():
    reading_file = open("wordle.txt", "r")
    five_letter_words = []
    for line in reading_file:
        # adding only 5 letter words to the list
        if len(line) == 6:
            five_letter_words.append(line.strip())
    key_word = random.choice(five_letter_words).upper()

    # initalizing display dimensions
    height = 800
    length = 700

    #creating a black window using display measurements
    window = pygame.display.set_mode((length, height))
    window.fill(black)
    user_guess = ""

    # drawing a grid of 5x6 empty squares and adding a caption
    for x in range (0, 5):
        for y in range (0, 6):                         
            pygame.draw.rect(window, grey, pygame.Rect(160 + (x * 80), 130 + (y * 80), 50, 50), 2)                                         
    pygame.display.set_caption("Wordle")

    user_turns = 0
    win = False
    #main loop to keep the game running
    while True:
        #terminates program if game is closed
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            #removes character if user presses backspace or if user inputs more than 5 characters
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE or len(user_guess) > 5:  
                user_guess = user_guess[:-1]

            #adds character to user_guess if the key that is being pressed is not the backspace key
            if event.type == pygame.KEYDOWN and event.key != pygame.K_BACKSPACE:
                user_guess += event.unicode.upper()
             
                #runs the game again if user won and pressed the return key
                if event.key == K_RETURN and win == True:
                    main()

                #runs the game again if user lost and pressed the return key
                if event.key == K_RETURN and user_turns == 6:
                    main()

                # run the function check_user_guess if return key is pressed and user_guess is longer than 4 characters
                if event.key == K_RETURN and len(user_guess) > 4:
                    win = check_user_guess(user_turns, key_word, user_guess, window)
                    user_turns += 1
                    user_guess = ""
                    #covers where the user inputs their answers after the return key is pressed 
                    window.fill(black,(0, 650, 650, 200))

        window.fill(black,(0, 650, 650, 200))
        displaying_user_guess = letter_font.render(user_guess, True, grey)
        window.blit(displaying_user_guess, (290, 650))

        # displays winning statement if user won
        if win == True:
            window.blit(winning_statement, (290, 40))
        
        # displays losing statement and the key word if user loses
        if user_turns == 6 and win != True:
            display_answer = statement_font.render("Answer: ", True, light_green)
            display_key_word = statement_font.render(str(key_word), True, light_green)
            window.blit(losing_statement, (285, 40))
            window.blit(display_answer, (245, 70))
            window.blit(display_key_word, (400, 70))       
        pygame.display.update()
    
#function that will check the users guess 
def check_user_guess(user_turns, key_word, user_guess, window):

    #empty list that will store user_guess[x]
    spacing_list = ["", "", "", "", ""]
    character_spacing = 0
    block_color = [grey, grey, grey, grey, grey]
                
    #checks if user_guess[x] is in the key_word at any index
    #which tells the user that the character is in the word, but not in the correct space
    for x in range (0, 5):
        if user_guess[x] in key_word:
            block_color[x] = yellow
    #checks if user_guess[x] is the same as key_word[x],
    #which tells the user that the character is in the correct space
        if user_guess[x] == key_word[x]:
            block_color[x] = green
    #creates user_guess into a list
    list(user_guess)
 
    for x in range (0, 5):
        #adding the rendered characters to spacing_list  
        spacing_list[x] = letter_font.render(user_guess[x], True, black)
        #draws the color of block_color to the rectangle where the characters are being displayed
        pygame.draw.rect(window, block_color[x], pygame.Rect(160 + character_spacing, 130 + (user_turns * 80), 50, 50))
        window.blit(spacing_list[x], (170 + character_spacing, 130 + (user_turns * 80)))
        character_spacing += 80

    #if every block becomes green, return True (user won)
    if block_color == [green, green, green, green, green]:
        return True
main()