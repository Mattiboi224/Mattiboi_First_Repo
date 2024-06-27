import random
from turtle import *
screen = Screen()
screen.screensize(430,430)

writer = Turtle()
writer.hideturtle()
writer.up()

def main():
    [player_position_list, ladder_list, ladder_up_list \
           , snake_list, snake_down_list, final_value] = starting_conditions()

    [size_of_screen, map_square_size] = setupmapscreen()
    #writer.showturtle()
    #writer.setposition(270,270)
    [number_list, number_loc] = placing_numbers(size_of_screen, map_square_size, final_value)
    
    main_game(player_position_list, ladder_list, ladder_up_list \
           , snake_list, snake_down_list, final_value)

    
def starting_conditions():
    player_position_list = []

    ladder_list = [5, 7, 18, 21, 55, 71, 87]
    ladder_up_list = [15, 12, 25, 38, 65, 82, 93]
    snake_list = [19, 99, 53, 30, 97, 92, 78, 83]
    snake_down_list = [3, 51, 47, 18, 76, 86, 62, 79]

    final_value = 100

    return player_position_list, ladder_list, ladder_up_list \
           , snake_list, snake_down_list, final_value


def main_game(player_position_list, ladder_list, ladder_up_list \
           , snake_list, snake_down_list, final_value):
    
    #print(dice_roll)
    while True:
        try:
            number_players_str = textinput("How many people are playing?", "A number > 0")
            number_players = int(number_players_str)
            break
        except:
            print("Not a Number")



    #print(number_players)

    for i in range(0,number_players):
        player_position_list.append(0)
    i = 0
    while True:
        i += 1
        for j in range(0,number_players):
            dice_roll = random.randint(1,6)
            player_position_list[j] += dice_roll
            #if i == 0:
            #    print(player_position_list[j])
            #    print(ladder_list)
            #    print(player_position_list)
            #    print(player_position_list[j] in ladder_list)
            #print(i)
            #print(player_position_list)
            #print(i)
            #print(player_position_list[j])
            if player_position_list[j] > final_value:
                print(player_position_list[j])
                missed_final = player_position_list[j] - final_value
                player_position_list[j] = final_value - missed_final
                #player_position_list[j] = 100
            while player_position_list[j] in ladder_list or player_position_list[j] in snake_list:
                # Up Ladders
                if player_position_list[j] in ladder_list:
                    print("Up Ladder")
                    ladder_loc = ladder_list.index(player_position_list[j])
                    player_position_list[j] = ladder_up_list[ladder_loc]
                    print("Player " + str(j + 1) + " went up " + str(ladder_up_list[ladder_loc] - ladder_list[ladder_loc]) + ' places')

                # Down Snakes
                if player_position_list[j] in snake_list:
                    print("Down Snake")
                    snake_loc = snake_list.index(player_position_list[j])
                    player_position_list[j] = snake_down_list[snake_loc]
                    print("Player " + str(j + 1) + " went down " + str(abs(snake_down_list[snake_loc] - snake_list[snake_loc])) + ' places')
            
            #Game Over
            if max(player_position_list) == final_value:
                break
        #Game Over
        if max(player_position_list) == final_value:
            break

    print(i)
    print(player_position_list)

def setupmapscreen():
    size_of_screen = 270
    map_square_size = 54
    repeats = size_of_screen * 2 / map_square_size + 1
    repeats = int(repeats)
    tracer(False)
    for i in range(repeats):
        location_spot = -size_of_screen + map_square_size * i
        writer.setposition(location_spot, size_of_screen)
        writer.down()
        writer.setposition(location_spot, -size_of_screen)
        writer.up()
        writer.setposition(-size_of_screen, location_spot)
        writer.down()
        writer.setposition(size_of_screen, location_spot)
        writer.up()
    tracer(True)
    return size_of_screen, map_square_size

def placing_numbers(size_of_screen, map_square_size, final_value):
    number_list = []
    number_loc = []
    tracer(False)
    i = 0
    for j in range(0,10):
        for k in range(0,10):
            i += 1
            if j % 2 != 1: 
                write_location_x = -size_of_screen + map_square_size/2 + map_square_size * k
            else:
                write_location_x = size_of_screen - map_square_size/2 - map_square_size * k
            write_location_y = -size_of_screen + map_square_size/2 + map_square_size * j
            writer.setposition(write_location_x, write_location_y - map_square_size / 8)
            writer.write(i, False, align="center", font=("Arial", round(map_square_size / 4), "normal"))
            number_list.append(i)
            number_loc.append([write_location_x, write_location_y])
    tracer(True)
    #print(number_list)
    #print(number_loc)
    return number_list, number_loc
main()
