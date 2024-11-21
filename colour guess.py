#Colour Guess
#by Connor McSweeney

#import libraries
from turtle import *
from random import randint

def setup_game():
    colormode(255)
    display = getscreen()
    penup()
    hideturtle()
    display.bgpic('assets/transparent_bg.png')
    rgb_or_hex=0
    session_best_score=0
    return rgb_or_hex, session_best_score

def show_menu():
    print("=================================")
    username = input("Enter Username (3 letters): ").upper().ljust(3, '_')[:3]
    rgb_or_hex=0
    while rgb_or_hex not in ["1", "2"]:
        rgb_or_hex = input("Type '1' for RGB, or '2' for HEX \n(1 or 2) >> ")
    print("=================================")
    print()
    leaderboard_file = "assets/rgb_leaderboard.txt" if rgb_or_hex == "1" else "assets/hex_leaderboard.txt"
    return username, int(rgb_or_hex), leaderboard_file

def gen_random_colours():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r,g,b

def draw_dot(r,g,b,pos):
    goto(75*pos, 0)
    color(r,g,b)
    pendown()
    dot(300)
    penup()

def calculate_average_score(player, leaderboard_file):
    scores = 0
    count = 0
    with open(leaderboard_file, 'r') as f:
        leaderboard = f.readlines()
        for line in leaderboard:
            if player in line:
                score = float(line.rsplit(' ', 1)[0])
                scores += score
                count += 1
        average = scores/count
        return average

def rgb_to_hex(colour):
    return hex(colour).upper()[2:]
        
def add_leaderboard(score, player, leaderboard_file):
    with open(leaderboard_file, 'a') as file:
        file.write(f'{score} ({player})\n')

def show_leaderboard(scores, leaderboard_file):
    place = 0
    score = 0
    prev_score = 0
    try:
        with open(leaderboard_file, 'r') as f:
            leaderboard = f.readlines()
            leaderboard.sort(reverse=True)
            for entry in leaderboard[:scores]:
                try:
                    score = float(entry.split()[0])
                except ValueError:
                    continue  # Skip invalid entries
                if prev_score != score:
                    place += 1
                prev_score = score
                print(str(place) + "# " + entry.strip())
    except FileNotFoundError:
        print(f"Leaderboard file {leaderboard_file} not found.")
            
def get_rgb_colour_guess(colour_name, r, g, b):
    while True:
        guess = input(colour_name + ": ")
        if guess == "T00WHAT?":
            hint_higher_or_lower(colour_name, r, g, b)
            continue
        if not guess.isdigit():
            print("Please enter a valid number")
            continue
        guess = int(guess)
        if guess < 0 or guess > 255:
            print("Value must be between 0 and 255")
        else:
            return guess
        
def get_rgb_colour_guesses(r, g, b):
    r_guess = get_rgb_colour_guess("r", r, g, b)
    g_guess = get_rgb_colour_guess("g", r, g, b)
    b_guess = get_rgb_colour_guess("b", r, g, b)
    print()
    return r_guess, g_guess, b_guess

def get_hex_color_guesses():
    while True:
        hex_guess = input("Hex (#RRGGBB): #")
        if len(hex_guess) != 6:
            print("Invalid Format")
            continue
        try:
            r_guess = int(hex_guess[0:2], 16)
            g_guess = int(hex_guess[2:4], 16)
            b_guess = int(hex_guess[4:6], 16)
            print()
            return r_guess, g_guess, b_guess
        except ValueError:
            print("Invalid HEX value")

def correct_value(correct_colour, mode):
    return rgb_to_hex(correct_colour) if mode == 2 else str(correct_colour)

def print_score(r_score, g_score, b_score, tot_score, r, g, b, mode):
        print("Red Score: " + str(r_score)[:6] + "% (" + correct_value(r, mode) + ")")
        print("Green Score: " + str(g_score)[:6] + "% (" + correct_value(g, mode) + ")")
        print("Blue Score: " + str(b_score)[:6] + "% (" + correct_value(b, mode) + ")")
        print("Total Score: " + str(tot_score) + "%")
        print()

def hint_higher_or_lower(colour_name, r, g, b):
    #get correct colour value
    if colour_name == "r":
        current_colour = r
    elif colour_name == "g":
        current_colour = g
    else:
        current_colour = b
    #get valid user input
    while True:
        guess = input(colour_name + " guess: ")
        if not guess.isdigit():
            print("Please enter a valid number")
            continue
        guess = int(guess)
        if guess < 0 or guess > 255:
            print("Value must be between 0 and 255")
        else:
            break
    #print whether the user's guess is greater, less than or the same as the correct value
    if guess > current_colour:
        print("Too High")
    elif guess < current_colour:
        print("Too Low")
    else:
        print("Perfecto")
    
def calc_scores(r, g, b, r_guess, g_guess, b_guess):
    r_score, g_score, b_score = (256-abs(r - r_guess))/2.56, (256-abs(g - g_guess))/2.56, (256-abs(b - b_guess))/2.56
    tot_score=round((r_score+g_score+b_score)/3,3)
    return r_score, g_score, b_score, tot_score

def update_leaderboard_and_highscores(tot_score, username, leaderboard_file, session_best_score):
    if username != "NUL":  # For me to test without affecting leaderboard
        add_leaderboard(tot_score, username, leaderboard_file)
        if tot_score > session_best_score:
            session_best_score = tot_score
            print(f"NEW SESSION BEST SCORE ({username}, {tot_score}%)")
    if session_best_score != 0:
        print(f"Best Score: {str(session_best_score)[:6]}%")
        print()
    return session_best_score

def prompt_view_leaderboard(leaderboard_file):
    show_leaderboard_prompt = input("Do you want to see the all-time leaderboard (y/n): ").lower()[0]
    if show_leaderboard_prompt == "y":
        while True:
            try:
                scores = int(input("How many scores: "))
                break
            except ValueError:
                print('You entered a non-integer value, try again.')
                continue
        print()
        print("**LEADERBOARD**")
        show_leaderboard(scores, leaderboard_file)
    print()

def view_average_score(username, leaderboard_file):
    if username != "NUL":
        show_average = input("Do you want to see the average score for this user (y/n): ").lower()
        if show_average == 'y':
            avg_score = float(calculate_average_score(username, leaderboard_file))
            print(f"The average score for {username} is: {str(round(avg_score, 3))}%")
        print()
        
def round_break():
    print()
    print("---------------------------------")
    print()

def ask_to_go_to_menu():
    while True:
        go_to_menu = input("Do you want to go back to the menu (y/n): ").lower()[0]
        if go_to_menu == "y":
            return True
        elif go_to_menu == "n":
            round_break()
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def play_round(username, rgb_or_hex, leaderboard_file, session_best_score):
    #reset display to play again
    clear()
    
    #generate and display the original colour
    r, g, b = gen_random_colours()
    draw_dot(r, g, b, -1)
    
    #get user's guess for the colour:
    if rgb_or_hex == 1:
        r_guess, g_guess, b_guess = get_rgb_colour_guesses(r, g, b)
    else:
        r_guess, g_guess, b_guess = get_hex_color_guesses()
        
    #display the colour that the user guessed
    draw_dot(r_guess, g_guess, b_guess, 1)
    
    #calculate user's score
    r_score, g_score, b_score, tot_score = calc_scores(r, g, b, r_guess, g_guess, b_guess)
    
    #print user's score
    print_score(r_score, g_score, b_score, tot_score, r, g, b, rgb_or_hex)
    
    #update leaderboard and session highscores
    session_best_score = update_leaderboard_and_highscores(tot_score, username, leaderboard_file, session_best_score)
        
    #allow user to see leaderboard
    prompt_view_leaderboard(leaderboard_file)
    
    #allow user to see their personal average score (using their username)
    view_average_score(username, leaderboard_file)
    
    #return session_best_score after the round is complete
    return session_best_score

# play_game function handles the overall flow of the game
def play_game(rgb_or_hex, session_best_score):
    while True:
        #menu (username and colour mode)
        username, rgb_or_hex, leaderboard_file = show_menu()
        
        #one round cycle
        while True:
            # play one round and update session_best_score
            session_best_score = play_round(username, rgb_or_hex, leaderboard_file, session_best_score)
            
            #allow user to play again or go back to the menu
            if ask_to_go_to_menu():
                break
        
if __name__ == "__main__":
    rgb_or_hex, session_best_score = setup_game()
    play_game(rgb_or_hex, session_best_score)
