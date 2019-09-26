# Māui_Sea_V3.7.2.py
# Maui tile based board game where the user can read the legend of Maui and the big fish

# created by: Declan Cross
# modified on: 27/09/2019


# import functions
import random
import time
import sys # import colour
try:
    color = sys.stdout.shell
except AttributeError:
    raise RuntimeError("Use IDLE")

# function to clear the screen
def clearscreen():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
# function to create a break point
def breakline():
    color.write('--------------------------------------------------\n\n', 'SYNC')

# disclaimer for the user to optionally read.
def printdisclaimer():
    time.sleep(0.5)
    color.write("""
There is no recorded data in the game, meaning
that there is no personal data captured. There
is also no input of personal information.

The only files that this program has access to
is the scene.py (animation) and the story.txt
which is located in the same folder. No external
access is needed or used.

While Māui has an accent mark on his name in the
UI, he does not have it in the story because it
causes it to crash unfortunately.

The content used from the story requires
permission from Wiremu Grace before being shared
anywhere else apart from this program.

""", 'SYNC')
    time.sleep(2.5)
    
# tutorial function that user can read
def tutorial():
    breakline()
    time.sleep(0.5)
    print("""Your character is this boat.     \O,
                              \__/\)/
    'Kia Ora! Hello.'           -_ \-
""")
    time.sleep(0.5)
    print("""
Use the 'W', 'A', 'S', 'D' keys to
move around the board. Remember, each second
move uses up food.
""")
    color.write('>> Press enter to learn [Food]. ', 'BUILTIN')
    input()
    time.sleep(0.3)
    print("""
You're going to get hungry so we need
to collect food on the way. This      -_- -_-
is what a fish tile looks like  -->   _  ⤬  _
Just move to the tile to collect it!   -__-__ 
""")
    color.write('>> Press enter to learn [Progression]. ', 'BUILTIN')
    input()
    time.sleep(0.3)
    print("""
Help Maui throughout the story by
collecting story bottles. These look like this:
  -  -
_  !  _    <-- Collect me and read the story!
  ͖   -_
""")
    color.write('>> Press enter to learn [Definitions]. ', 'BUILTIN')
    input()
    time.sleep(0.7)
    print("""
Terms used in the game:
 Aotearoa - This is New Zealand.
 Karakia - These are Māori incantations & prayers.
 Muri-ranga-whenua - Māui's grandmother.
 Hawaiki - The traditional Māori place of origin.
 Tangaroa - The great god of the sea.
""")
    color.write('>> Press enter to exit tutorial. ', 'BUILTIN')
    input()
    time.sleep(0.7)
    breakline()

# board printer function
def board(world):
    # define board pieces
    chunks   = [' _  _- ', ' _   -_', '-  - _ ', '-   _  ']
    fish     = ['-_  -_ ', '_  ⤬  _', '-  - _ ']
    boat     = ['   \O, ', '\__/\)/', '  -_ \-']
    bottle   = ['  -  - ', ' - !  _', '- ͖   -_']
    rock     = ['   . , ', ' ` ⋀^ ,', '  ^_`- ']
    big_fish = ['  !  ! ', '! ! ! !', '  ͖ ! ! ']
    # rows of board
    for board_row in range(0, 35, 6):
        # rows in a board row
        for row_section in range(3):
            row = '  '
            # columns in a row
            for row_column in range(6):
                # check if square is 0 (Water), 1 (Fish) or 2 (Boat) or 3 (bottle) or 4 big fish
                if world[row_column + board_row] == '0':
                    row += chunks[random.randint(0, len(chunks)-1)]
                elif world[row_column + board_row] == '1':
                    row += fish[row_section]
                elif world[row_column + board_row] == '3':
                    row += bottle[row_section]
                elif world[row_column + board_row] == '4':
                    row += big_fish[row_section]
                elif world[row_column + board_row] == '5':
                    row += rock[row_section]
                else:
                    row += boat[row_section]
            # print section of that row
            print(row)

# function to print out next section of story when called 
def printstory(paragraph_count, story, world, mode):
    color.write('\nYou found a bottle with a piece of story in it.\n\n--------------------------------------------------\n\n', 'STRING')
    for i in range(paragraph_count*5, paragraph_count*5+5):
        color.write(story.readline(), 'SYNC')
        print()
    color.write('\n--------------------------------------------------\n', 'STRING')
    # redisplay map after reading if not in end game
    if mode == 'main':
        color.write('>> Press enter to continue. ', 'BUILTIN')
        input()
        time.sleep(0.25)
        board(world)
    

# main function that prints out UI
def hud(food, move_count, world, alive, paragraph_count, read_paragraph, story, mode):
    # define variables
    moves = {'a':-1, 'w':-6, 's':6, 'd':1}
    direction = 0
    # print hunger
    color.write('\nFood: ', 'console')
    color.write("{}\n".format('><> ' * food), 'KEYWORD')
    if food < 0:
        alive = False
    # print story piece if previous move requested it
    if read_paragraph == True:
        if paragraph_count <= 8:
            # add new bottle to board if the spot is free
            add_bottle = True
            while add_bottle:
                temp_bottle_location = random.randint(0, 35)
                if world[temp_bottle_location] == '0':
                    world[temp_bottle_location] = '3'
                    add_bottle = False
            # call story printing function
            printstory(paragraph_count, story, world, mode)
        elif mode == 'endgame':
            print("The line tugs...")
            alive = False
        else:
            # create end game fish ile
            if not world[7] == '2':
                world[7] = '4'
            else:
                world[28] = '4'
            # call story printing function and set mode to end game
            printstory(paragraph_count, story, world, mode)
            mode = 'endgame'
        paragraph_count += 1
        read_paragraph = False
    # find boat position and turn world into editable list
    boat_pos = world.index('2')
    ask_again = True
    while ask_again and alive == True:
        # ask for boat direction input and loop if invalid
        direction = input('\nWhich way shall Māui move? (W,A,S,D): ').lower().strip() or ' '
        if direction[-1] in moves:
            ask_again = False
            direction = direction[-1]
        else:
            color.write("Please press 'W' (Up), 'A' (Left), 'S' (Down), 'D' (Right).\n", 'stderr')
    # repeat for each movement direction
    for i in moves:
        if direction == i:
            # making sure the boat does not leave the boundaries and redo turn if so
            if (direction == 'a' and boat_pos % 6 == 0) or (direction == 'd' and (boat_pos % 6) -5 == 0) or (direction == 'w' and boat_pos < 6) or (direction == 's' and boat_pos >= 30):
                color.write("There is a storm in that direction! Please move another way.\n", 'stderr')
                time.sleep(1.5)
            elif world[boat_pos + moves[i]] == '5':
                color.write("There is a rock in that direction.\n", 'stderr')
                time.sleep(1.5)
            else:
                # delete boat and move boat to new position using dictionary above
                world[boat_pos] = '0'
                # if landed on fish block, gain a fish and reset the counter
                if world[boat_pos + moves[i]] == '1':
                    food += 1
                    move_count = 0
                    # add random fish
                    add_fish = True
                    while add_fish:
                        temp_fish_location = random.randint(0, 35)
                        if world[temp_fish_location] == '0':
                            world[temp_fish_location] = '1'
                            add_fish = False
                else:
                    if world[boat_pos + moves[i]] == '3' or world[boat_pos + moves[i]] == '4': # story bottle and end story bottle
                        read_paragraph = True
                    # add move to counter and reduce food by one if it has reached two
                    if move_count >= 1:
                        food -= 1
                        move_count = 0
                    else:
                        move_count += 1  
                # place boat in new position
                world[boat_pos + moves[i]] = '2'          
    # return variables to main function
    return(food, move_count, world, alive, paragraph_count, read_paragraph, story, mode)

# initial function to generate world and loop game until death or success.
def main():
    # initial variables
    default_world = '111123555000000000000000000000000000'
    food = 3
    move_count = 0
    paragraph_count = 0
    alive = True
    mode = 'main'
    read_paragraph = False
    story = open("storyboard.txt", 'r')
    # introduce game and call tutorial
    breakline()
    print("""
 ___  ___            _  _      _____            
 |  \/  |  __       (_|| )    /  ___|           
 | .  . | __ _ _   _ _ |/___  \ `--.  ___  __ _ 
 | |\/| |/ _` | | | | | / __|  `--. \/ _ \/ _` |
 | |  | | (_| | |_| | | \__ \ /\__/ /  __/ (_| |
 \_|  |_/\__,_|\__,_|_| |___/ \____/ \___|\__,_|

 """)
    print("""
 Welcome to Māui's story board game.

 You will play on a 6x6 board where you must
 stay alive by moving around and collecting fish
 on the board.

 On your trip you will uncover the story of Maui
 and Aotearoa, Good luck!


(!) Please resize the window width so the
    breakline above is just a single line.

""")
    # ask user if they would want to read the disclaimers and loop if answer is not recognised
    ask_again = True
    while ask_again:
        user_answer = input('Would you like to read the disclaimer? (Y/N): ').strip().lower()
        if user_answer == 'y':
            printdisclaimer()
            ask_again = False
        elif user_answer == 'n':
            ask_again = False
        else:
            color.write('Please reply with Y or N.\n\n', 'stderr')
            time.sleep(0.5)
    time.sleep(0.5)
    color.write('\n>> Press enter to start the tutorial.\n\n\n\n\n\n\n', 'BUILTIN')
    input()
    tutorial()
    # shuffle default world tiles and turn into editable list
    world = list(''.join(random.sample(default_world, len(default_world))))
    # loop game function
    while alive == True:
        clearscreen()
        board(world)
        food, move_count, world, alive, paragraph_count, read_paragraph, story, mode = hud(food, move_count, world, alive, paragraph_count, read_paragraph, story, mode)
    # end of game scene
    if mode == 'endgame':
        # play animation
        import scene
        printstory(paragraph_count, story, world, mode)
        time.sleep(10)
        print("Game 100% complete. Well done!")
    else:
        # print end screen
        print("""
                      /"*._         _
                  .-*'`    `*-.._.-'/
                < X ))     ,       ( 
                  `*-._`._(__.--*"`.\
\n
Oh no, Māui and his brothers see a storm coming!
With little food left in the boat, they return
home. Please try again!
""")

# start main function
main()
