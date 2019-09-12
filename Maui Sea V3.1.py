# Maui_Sea_V3.1.py

chunks = [' _- _- ', ' _   -_', '-  - _-', '-  _   ']
fish   = ['-_- -_-', '_  ⤬  _', '-__-__ ']
boat   = ['   \O, ', '\__/\)/', '  -_ \-']
bottle = ['  -  - ', '   !  _', '  ͖   -_']
big_fish = ['  !  ! ', ' ! ! ! ! ', '   ! ! ']

import random
import time

def clearscreen():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

# board printer function
def board(chunks, fish, world, bottle, big_fish):
    # rows of board
    for board_row in range(0, 35, 6):
        # rows in a board row
        for row_section in range(3):
            row = ''
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
    print("\nYou found a bottle with a piece of story in it.\n------------------------------------------------\n")
    for i in range(paragraph_count*5, paragraph_count*5+5):
        print(story.readline())
    print('------------------------------------------------')
    
def hud(food, move_count, world, alive, paragraph_count, read_paragraph, story, mode):
    # define variables
    moves = {'a':-1, 'w':-6, 's':6, 'd':1}
    direction = 0

    # print hunger
    print("\nFood: {}".format(' ><_> ' * food))
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
        direction = input('\nWhich way shall Maui move? (W,A,S,D): ').lower().strip()
        if direction in moves:
            ask_again = False
        else:
            print("Please press 'W' (Up), 'A' (Left), 'S' (Down), 'D' (Right).")
    
    # repeat for each movement direction
    for i in moves:
        if direction == i:
            # making sure the boat does not leave the boundaries and skip turn if so
            if (direction == 'a' and boat_pos %6 == 0) or (direction == 'd' and (boat_pos %6) -5 == 0) or (direction == 'w' and boat_pos < 6) or (direction == 's' and boat_pos >= 30):
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
                    if move_count >= 1:
                        food -= 1
                        move_count = 0
                    else:
                        move_count += 1
                    
                    if world[boat_pos + moves[i]] == '3' or world[boat_pos + moves[i]] == '4': # story bottle
                        read_paragraph = True
                # place boat in new position
                world[boat_pos + moves[i]] = '2'          
    # turn list back into string and return to main function
    return(food, move_count, world, alive, paragraph_count, read_paragraph, story, mode)

def main():
    default_world = '100100030000010100000200000100010001'
    food = 3
    move_count = 0
    paragraph_count = 0
    alive = True
    mode = 'main'
    read_paragraph = False
    story = open("storyboard.txt", 'r')
    # introduce game
    print('------------------------------------------------\n\n\n\n\n\n')
    print("\nWelcome to Maui's story board game.\n\n\nYou will play on a 6x6 board where you must\nstay alive by moving around and collecting fish\non the board. To move, use the WASD keys and press enter.\nOn your trip you will uncover the story of Maui\nand Aotearoa, Good luck!\n\n\nPlease shorten the window so the top and bottom lines are just visible\nand the press start line can be seen.\n")
    print("Press enter to start the game.")
    print('\n\n\n\n\n------------------------------------------------')
    input("")
    # shuffle default world tiles and turn into editable list
    world = list(''.join(random.sample(default_world,len(default_world))))
    # loop game function
    while alive == True:
        clearscreen()
        board(chunks, fish, world, bottle, big_fish)
        food, move_count, world, alive, paragraph_count, read_paragraph, story, mode = hud(food, move_count, world, alive, paragraph_count, read_paragraph, story, mode)
    # end of game scene
    if mode == 'endgame':
        import scene
        printstory(paragraph_count, story)
        time.sleep(10)
        print("Game 100% complete.")
    else:
        # print death screen
        print("\nOh no, Maui ran out of food! Please try again.")
main()
