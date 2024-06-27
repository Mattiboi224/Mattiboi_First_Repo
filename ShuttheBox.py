import random
import turtle
import itertools


playscreen = turtle.Screen()
mt = turtle.Turtle()
dt = turtle.Turtle()
dt.hideturtle()
mt.hideturtle()

def dice_roll():
    return random.randint(1,6)


def draw_square(x,y):
    turtle.tracer(False)
    mt.up()
    mt.goto(x,y)
    mt.down()
    for i in range(4):
        mt.forward(100)
        mt.left(90)
    mt.up()
    turtle.tracer(True)

def draw_dot(x, y):
    dt.up()
    dt.goto(x,y)
    dt.down()
    dt.fillcolor("black")
    dt.begin_fill()
    dt.circle(10)
    dt.end_fill()
    dt.up()

def draw_dice_roll(dr,x,y):
    draw_square(x,y)
    turtle.tracer(False)
    dt.up()

    if dr == 1:
        draw_dot(x+50,y+40)

    if dr == 2:
        draw_dot(x+20,y+10)
        draw_dot(x+80,y+70)

    if dr == 3:
        draw_dot(x+20,y+10)
        draw_dot(x+80,y+70)
        draw_dot(x+50,y+40)

    if dr == 4:
        draw_dot(x+20,y+10)
        draw_dot(x+80,y+70)
        draw_dot(x+20,y+70)
        draw_dot(x+80,y+10)

    if dr == 5:
        draw_dot(x+20,y+10)
        draw_dot(x+80,y+70)
        draw_dot(x+20,y+70)
        draw_dot(x+80,y+10)
        draw_dot(x+50,y+40)

    if dr == 6:
        draw_dot(x+20,y+10)
        draw_dot(x+80,y+70)
        draw_dot(x+20,y+70)
        draw_dot(x+80,y+10)
        draw_dot(x+20,y+40)
        draw_dot(x+80,y+40)
        
    turtle.tracer(True)

def draw_rectangle(x,y):
    turtle.tracer(False)
    mt.up()
    mt.goto(x,y)
    mt.down()
    mt.forward(50)
    mt.left(90)
    mt.forward(100)
    mt.left(90)
    mt.forward(50)
    mt.left(90)
    mt.forward(100)
    mt.left(90)
    mt.up()
    turtle.tracer(True)    

def draw_x(x,y):
    turtle.tracer(False)
    mt.up()
    mt.goto(x,y)
    mt.down()    
    mt.goto(x+50, y+100)
    mt.up()
    mt.goto(x,y+100)
    mt.down()
    mt.goto(x+50,y)
    mt.up()

box_loc = []
for i in range(9):
    draw_rectangle(-265 + 60 * i ,0)
    box_loc.append([-265 + 60 * i,0])
    turtle.tracer(False)
    mt.goto(-265 + 60 * i + 25, 45)
    mt.write(i + 1)
    turtle.tracer(True)    

number_left = [1,2,3,4,5,6,7,8,9]

def main():
    
    while sum(number_left) > 0:
        dt.clear()
        d1 = dice_roll()
        draw_dice_roll(d1,150,150)

        d2 = dice_roll()
        draw_dice_roll(d2,-250,150)

        target = d1 + d2
        #print(number_left)
        if target not in number_left:
            found_combination = False
            for numbers in itertools.combinations(range(len(number_left)), 2):
                if number_left[numbers[0]] + number_left[numbers[1]] == target:
                    #print([numbers[0], numbers[1]])  # Print the indices of the numbers
                    found_combination = True
                    break

            if not found_combination:
                #print("No valid combination")
                break

        number_selection = None
        
        def selecting_number(x,y):
            nonlocal number_selection
            #nonlocal number_2
            mt.goto(x,y)

            if x >= -265 and x <= -215 and y >=0 and y <= 100:
                number_selection = 1

            if x >= -205 and x <= -155 and y >=0 and y <= 100:
                number_selection = 2        
            
            if x >= -145 and x <= -95 and y >=0 and y <= 100:
                number_selection = 3
                
            if x >= -85 and x <= -35 and y >=0 and y <= 100:
                number_selection = 4    

            if x >= -25 and x <= 25 and y >=0 and y <= 100:
                number_selection = 5

            if x >= 45 and x <= 95 and y >=0 and y <= 100:
                number_selection = 6        
            
            if x >= 105 and x <= 155 and y >=0 and y <= 100:
                number_selection = 7
                
            if x >= 165 and x <= 215 and y >=0 and y <= 100:
                number_selection = 8    

            if x >= 225 and x <= 275 and y >=0 and y <= 100:
                number_selection = 9


        playscreen.onclick(selecting_number)
        number1 = 0
        while number_selection != -1:
            #print(number_selection)
            while number_selection is None:
                playscreen.update()
                        
            if number_selection == d1 + d2:
                draw_x(box_loc[number_selection-1][0],box_loc[number_selection-1][1])
                number_left[number_selection-1] = 0
                break

            if number_selection < d1 + d2:
                if number1 == 0:
                    number1 = number_selection
                else:
                    number2 = number_selection
                    if number1 + number2 == d1 + d2:
                        draw_x(box_loc[number1-1][0],box_loc[number1-1][1])
                        draw_x(box_loc[number2-1][0],box_loc[number2-1][1])
                        number_left[number1-1] = 0
                        number_left[number2-1] = 0
                        break
                    else:
                        number_selection = None
                        number1 = 0
                        continue
            
            if number_selection > d1 + d2 or number_selection != number_left[number_selection - 1]:
                number_selection = None
                continue
            
            number_selection = None

        #print(number_left)



    if sum(number_left) == 0:
        print("You win")
    else:
        print("You lose")

main()
turtle.tracer(True)
playscreen.exitonclick()


