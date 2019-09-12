# Maui_Sea_V3.2.py

chunks = [' _- _- ', ' _   -_', '-  - _-', '-  _   ']
fish   = ['-_- -_-', '_  ⤬  _', '-__-__ ']
boat   = ['   \O, ', '\__/\)/', '  -_ \-']
bottle = ['  -  - ', '   !  _', '  ͖   -_']
big_fish = ['  !  ! ', ' ! ! ! ! ', '   ! ! ']

import random
import time

def clearscreen():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

def breakline():
    print('--------------------------------------------------\n')

def tutorial():
    breakline()
    time.sleep(0.7)
    print("""Your character is this boat.     \O,
                              \__/\)/
        'Hello!'                -_ \-
""")
    time.sleep(0.5)
    print("""
Use the 'W', 'A', 'S', 'D' keys to
move around the board. Remember, each second
move uses up food.
""")
    input(">> Press enter to continue.")
    time.sleep(0.3)
    print("""
You're going to get hungry so we need
to collect food on the way. This      -_- -_-
is what a fish tile looks like  -->   _  ⤬  _
Just move to the tile to collect it!   -__-__ 
""")
    input(">> Press enter to continue.")
    time.sleep(0.3)
    print("""
Help Maui throughout the story by
collecting story bottles. These look like this:
  -  -
_  ⤬  _    <-- Collect me and read the story!
  ͖   -_
""")
    input(">> Press enter to start game.")
    time.sleep(0.7)
    breakline()

# board printer function
def board(chunks, fish, world, bottle, big_fish):
    # rows of board
    for board_row in range(0, 35, 6):
        # rows in a board row
        for row_section in range(3):
            row = '    '
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
                else:
                    row += boat[row_section]
            # print section of that row
            print(row)
            
def printstory(paragraph_count, story):
    print("\nYou found a bottle with a piece of story in it.\n--------------------------------------------------\n")
    for i in range(paragraph_count*5, paragraph_count*5+5):
        print(story.readline())
    print('--------------------------------------------------')
    
def hud(food, move_count, world, alive, paragraph_count, read_paragraph, story, mode):
    # define variables
    moves = {'a':-1, 'w':-6, 's':6, 'd':1}
    direction = 0

    # print hunger
    print("\nFood: {}".format('><> ' * food))
    if food < 0:
        alive = False
        
    # print story piece previous move requested it
    if read_paragraph == True:
        if paragraph_count <= 8:
            printstory(paragraph_count, story)
            # add new bottle to board
            add_bottle = True
            while add_bottle:
                temp_bottle_location = random.randint(0, 35)
                if world[temp_bottle_location] == '0':
                    world[temp_bottle_location] = '3'
                    add_bottle = False
        elif mode == 'endgame':
            print("The line tugs...")
            alive = False
        else:
            mode = 'endgame'
            printstory(paragraph_count, story)
            if not world[7] == '2':
                world[7] = '4'
            else:
                world[28] = '4'
        paragraph_count += 1
        read_paragraph = False
            
    # find boat position and turn world into editable list
    boat_pos = world.index('2')
    
    ask_again = True
    while ask_again and alive == True:
        # ask for boat direction input and loop if invalid
        direction = input('\nWhich way shall Maui move? (W,A,S,D): ').lower().strip() or ' '
        if direction[-1] in moves:
            ask_again = False
            direction = direction[-1]
        else:
            print("Please press 'W' (Up), 'A' (Left), 'S' (Down), 'D' (Right).")
    
    # repeat for each movement direction
    for i in moves:
        if direction == i:
            # making sure the boat does not leave the boundaries and skip turn if so
            if (direction == 'a' and boat_pos % 6 == 0) or (direction == 'd' and (boat_pos % 6) -5 == 0) or (direction == 'w' and boat_pos < 6) or (direction == 's' and boat_pos >= 30):
                print("Cannot move in that direction")
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
                    if world[boat_pos + moves[i]] == '3' or world[boat_pos + moves[i]] == '4': # story bottle
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

def main():
    # initial variables
    default_world = '111123000000000000000000000000000000'
    food = 3
    move_count = 0
    paragraph_count = 0
    alive = True
    mode = 'main'
    read_paragraph = False
    story = open("storyboard.txt", 'r')
    # introduce game
    breakline()
    print("\n\n\n\n\n\nWelcome to Maui's story board game.\n\n\nYou will play on a 6x6 board where you must\nstay alive by moving around and collecting fish\non the board.\nOn your trip you will uncover the story of Maui\nand Aotearoa, Good luck!\n\n\nPlease resize the window width so the breakline above is a single line.")
    input("\nPress enter to start the tutorial.\n\n\n\n\n\n")
    tutorial()
    # shuffle default world tiles and turn into editable list
    world = list(''.join(random.sample(default_world,len(default_world))))
    # loop game function
    while alive == True:
        clearscreen()
        board(chunks, fish, world, bottle, big_fish)
        food, move_count, world, alive, paragraph_count, read_paragraph, story, mode = hud(food, move_count, world, alive, paragraph_count, read_paragraph, story, mode)
    # end of game scene
    if mode == 'endgame':
        # play animation
        import scene
        printstory(paragraph_count, story)
        time.sleep(10)
        print("Game 100% complete.")
    else:
        # print death screen
        print("""
                      /"*._         _
                  .-*'`    `*-.._.-'/
                < X ))     ,       ( 
                  `*-._`._(__.--*"`.\


  Oh no, Maui ran out of food! Please try again.
""")

# start main function
main()
