#Colour Guess
#by Connor McSweeney

#setup
from turtle import *
from random import randint
colormode(255)
display = getscreen()
penup()
hideturtle()
display.bgpic('assets/transparent_bg.png')
clear()
rgb_or_hex=0

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

def rgb_to_hex(r, g, b):
    return ('{:02X}' * 3).format(r, g, b)
        
def add_leaderboard(score, player):
    with open(leaderboard_file, 'a') as file:
        file.write(f'{score} ({player})\n')

def show_leaderboard(scores):
    place = 0
    score = 0
    prev_score = 0
    with open(leaderboard_file, 'r') as f:
        leaderboard = f.readlines()
        leaderboard.sort(reverse=True)
        for entry in leaderboard[:scores]:
            score = float(entry.split()[0])
            if prev_score != score:
                place += 1
            prev_score = score
            print(str(place) + "# " + entry.strip())
            
def get_rgb_colour_guess(colour_name):
    while True:
        guess = input(colour_name + ": ")
        if guess == "T00WHAT?":
            hint_higher_or_lower(colour_name)
            continue
        if not guess.isdigit():
            print("Please enter a valid number")
            continue
        guess = int(guess)
        if guess < 0 or guess > 255:
            print("Value must be between 0 and 255")
        else:
            return guess
        
def get_rgb_colour_guesses():
    r_guess = get_rgb_colour_guess("r")
    g_guess = get_rgb_colour_guess("g")
    b_guess = get_rgb_colour_guess("b")
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
            return r_guess, g_guess, b_guess
        except ValueError:
            print("Invalid HEX value")
            
def hint_higher_or_lower(colour_name):
    #get correct colour value
    if colour_name == "r":
        current_colour = r
    elif colour_name == "b":
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

while True:
    #setup
    session_best_score=0
    play_again = "y"
    
    #menu (username and colour mode)
    print("=================================")
    print()
    username = input("Enter Username (3 letters): ").upper()[:3]
    print("RGB or HEX: ")
    while rgb_or_hex != "1" and rgb_or_hex != "2":
        rgb_or_hex = input("Type '1' for RGB, or '2' for HEX \n(1 or 2) >> ")
    rgb_or_hex = int(rgb_or_hex)
    if rgb_or_hex == 1:
        leaderboard_file="assets/rgb_leaderboard.txt"
    elif rgb_or_hex == 2:
        leaderboard_file="assets/hex_leaderboard.txt"
    print()
    print("=================================")
    print()
    
    #one round cycle
    while play_again == "y":
        #reset to play again
        clear()
        r_guess="null"
        g_guess="null"
        b_guess="null"
        
        #generate and display the original colour
        r,b,g = gen_random_colours()
        draw_dot(r,g,b,-1)
        
        #get user's guess for the colour:
        if rgb_or_hex == 1:
            r_guess, g_guess, b_guess = get_rgb_colour_guesses()
        elif rgb_or_hex == 2:
            r_guess, g_guess, b_guess = get_hex_color_guesses()
            
        #display the colour that the user guessed
        draw_dot(r,g,b,1)
        
        #calculate user's score
        r_diff=abs(r-r_guess)
        g_diff=abs(g-g_guess)
        b_diff=abs(b-b_guess)
        tot_diff=r_diff+g_diff+b_diff
        r_score=256-r_diff
        g_score=256-g_diff
        b_score=256-b_diff
        tot_score=765-tot_diff
        #turn to % accuracy
        r_score/=2.56
        g_score/=2.56
        b_score/=2.56
        colour_scores=(r_score,g_score,b_score)
        tot_score=sum(colour_scores)/3
        tot_score=round(tot_score,3)
        
        #print user's score
        print()
        print("Red Score: " + str(r_score)[:6] + "% (" + str(r) + ")")
        print("Green Score: " + str(g_score)[:6] + "% (" + str(g) + ")")
        print("Blue Score: " + str(b_score)[:6] + "% (" + str(b) + ")")
        print("Total Score: " + str(tot_score) + "%")
        print()
        
        #update leaderboard a session highscores
        if username != "NUL": #for me to test with without affecting the leaderboard
            add_leaderboard(tot_score, username)
            print()
            if tot_score > session_best_score:
                session_best_score = tot_score
                print("NEW SESSION BEST SCORE ("+ username +")")
            print("Best Score: " + str(session_best_score)[:6] + "%")
            print()
            
        #allow user to see leaderboard
        show_leaderboard_prompt = input("do you want to see the all time leaderboard (y/n): ").lower()[0]
        if show_leaderboard_prompt == "y":
            while True:
                try:
                    scores = int(input("how many scores: "))
                    break
                except ValueError:
                    print('You entered a non integer value, try again.')
                    continue
            print()
            print("**LEADERBOARD**")
            show_leaderboard(scores)
        print()
        
        #allow user to see their personal average score (using their username)
        if username != "NUL":
            show_average = input("do you want to see the average score for this user (y/n): ").lower()
            if show_average == 'y':
                avg_score = float(calculate_average_score(username, leaderboard_file))
                print(f"The average score for {username} is: {string(avg_score.round[3])}%")
        print()
        
        #allow user to play again
        play_again=input("do you want to play again (y/n): ").lower()[0]
        print()
        print("---------------------------------")
        print() 