# Maui_Sea_V2.py

chunks = [' _- _- ', ' _   -_', '-  - _-', '-  _   ']
fish  = ['-_-_-_-', '__-_-__', '-__-__-', '_-_-__-']
boat  = ['   \O, ', '\__/\)/', '  -_ \-']
bottle = ['  -   ', '  ͖  -_', ' _   -_']

import random

def clearscreen():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

# board printer function
def board(chunks, fish, world, bottle):
    # rows of board
    for board_row in range(0, 36, 6):
        # rows in a board row
        for row_section in range(3):
            row = ''
            # columns in a row
            for row_column in range(6):
                # check if square is 0 (Water), 1 (Fish) or 2 (Boat)
                if world[row_column + board_row] == '0':
                    row += chunks[random.randint(0, len(chunks)-1)]
                elif world[row_column + board_row] == '1':
                    row += fish[random.randint(0, len(fish)-1)]
                elif world[row_column + board_row] == '3':
                    row += bottle[row_section]
                else:
                    row += boat[row_section]
            # print section of that row
            print(row)

def hud(food, move_count, world, alive, paragraph_count, read_paragraph, story):
    # define variables
    moves = {'a':-1, 'w':-6, 's':6, 'd':1}
    direction = 0

    # print hunger
    print("\nFood: {}".format(' ><_> ' * food))

    # print story piece if true
    if read_paragraph == True:
        print("\nYou found a bottle with a piece of story in it.\n------------------------------------------------\n")
        for i in range(paragraph_count*5, paragraph_count*5+5):
            print(story.readline())
        print('------------------------------------------------')
        paragraph_count += 1
        read_paragraph = False
        
    # find boat position and turn world into editable list
    boat_pos = world.index('2')
    
    if food < 0:
        alive = False
        
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
                else:
                    if move_count >= 1:
                        food -= 1
                        move_count = 0
                    else:
                        move_count += 1
                    
                    if world[boat_pos + moves[i]] == '3': # story bottle
                        # randomly select place on board to make new bottle.
                        read_paragraph = True
                # place boat in new position
                world[boat_pos + moves[i]] = '2'          
    # turn list back into string and return to main function
    return(food, move_count, world, alive, paragraph_count, read_paragraph, story)

def main():
    default_world = '100100030000010010000213301000100001'
    food = 3
    move_count = 0
    paragraph_count = 0
    alive = True
    read_paragraph = False
    story = open("storyboard.txt", 'r')

    world = ''
    global world

    # introduce game
    print('------------------------------------------------\n\n\n\n\n\n')
    print("\nWelcome to Maui's story board game.\n\n\nYou will play on a 6x6 board where you must\nstay alive by moving around and collecting fish\non the board. To move, use the WASD keys and press enter.\nOn your trip you will uncover the story of Maui\nand Aotearoa, Good luck!\n\n\nPlease shorten the window so the top and bottom lines are just visible\nand the press start line can be seen.\n")
    print("Press enter to start the game.")
    print('\n\n\n\n\n------------------------------------------------')
    input("")

    # shuffle default world tiles and turn into editable list
    world = list(''.join(random.sample(default_world,len(default_world))))
    
    # loop game function
    while alive:
        clearscreen()
        board(chunks, fish, world, bottle)
        food, move_count, world, alive, paragraph_count, read_paragraph, story = hud(food, move_count, world, alive, paragraph_count, read_paragraph, story)

    # print end screen
    print("\nOh no, Maui ran out of food! Please try again.")

main()
