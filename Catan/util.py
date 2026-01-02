import turtle
import math
from collections import deque
import random
import Config as C


# Draw a hexagon
def hexagon_shape(position_x, position_y, sel_turtle, colour, side_length, fill_on_off, big_hex):

    if sel_turtle == 'Main':
        turtle.tracer(False)
        # Start Location to Start of Hexagon
        C.main_turtle.color(colour)
        C.main_turtle.goto(position_x, position_y)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.up()
        C.main_turtle.left(C.angle * 2)
        C.main_turtle.forward(side_length)
        #main_turtle.right(angle * 2)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.down()

        # Draw Hexagon
        for i in range(C.num_sides):
            C.main_turtle.forward(side_length)
            C.main_turtle.right(C.angle)

        # Back to Start Location
        C.main_turtle.up()
        C.main_turtle.right(C.angle)
        C.main_turtle.forward(side_length)
        C.main_turtle.left(C.angle)

        C.main_turtle.goto(position_x, position_y)
        C.main_turtle.right(C.main_turtle.heading())
        turtle.tracer(True)

    if sel_turtle == 'Board':
        turtle.tracer(False)
        # Start Location to Start of Hexagon

        C.board_turtle.pencolor('Black')
        C.board_turtle.fillcolor(colour)
        C.board_turtle.goto(position_x, position_y)
        C.board_turtle.right(C.board_turtle.heading())
        C.board_turtle.up()

        if big_hex == 'No':
            C.board_turtle.left(C.angle * 2)

        if big_hex == 'Yes':
            C.board_turtle.left(90)

        C.board_turtle.forward(side_length)
        #main_turtle.right(angle * 2)
        C.board_turtle.right(C.board_turtle.heading())
        
        if big_hex == 'Yes':
            C.board_turtle.right(30)

        C.board_turtle.down()

        # Draw Hexagon

        if fill_on_off == 'On':
            C.board_turtle.begin_fill()

        for i in range(C.num_sides):
            C.board_turtle.forward(side_length)
            C.board_turtle.right(C.angle)

        if fill_on_off == 'On':
            C.board_turtle.end_fill()

        # Back to Start Location
        C.board_turtle.up()
        C.board_turtle.right(C.angle)
        C.board_turtle.forward(side_length)
        C.board_turtle.left(C.angle)

        C.board_turtle.goto(position_x, position_y)
        C.board_turtle.right(C.board_turtle.heading())
        turtle.tracer(True)



def getlocations(posx, posy):
    avaliable_position = []
    
    for i in range(6):
        turtle.tracer(False)
        C.main_turtle.goto(posx, posy)
        C.main_turtle.setheading(0)
        C.main_turtle.up()
        C.main_turtle.left(150 - 60 * i)
        C.main_turtle.forward(C.side_length * math.sqrt(3))
        C.main_turtle.right(150)
        C.main_turtle.setheading(0)
        xpos = C.main_turtle.xcor()
        ypos = C.main_turtle.ycor()
        avaliable_position.append([round(xpos,3), round(ypos,3)])
        turtle.tracer(True)
    
    return avaliable_position

def get_corners(posx, posy, sel_turtle):
    if sel_turtle == 'Main':
        turtle.tracer(False)
        # Start Location to Start of Hexagon
        C.main_turtle.color('Black')
        C.main_turtle.goto(posx, posy)
        C.main_turtle.right(C.main_turtle.heading())
        C.main_turtle.up()
        C.main_turtle.left(C.angle * 2)
        C.main_turtle.forward(C.side_length)
        #main_turtle.right(angle * 2)
        C.main_turtle.right(C.main_turtle.heading())
        #C.main_turtle.down()

        corner_mat = []

        # Draw Hexagon
        #C.main_turtle.begin_fill()
        for i in range(C.num_sides):
            xpos = C.main_turtle.xcor()
            ypos = C.main_turtle.ycor()
            corner_mat.append([round(xpos,3), round(ypos,3)])
            C.main_turtle.forward(C.side_length)
            C.main_turtle.right(C.angle)

        #C.main_turtle.end_fill()

        return corner_mat


def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])


def rectangle_shape(x, y, w, h, sel_turtle, fill='No', colour ='black'):
    if sel_turtle == 'Selection':
    
        turtle.tracer(False)
        
        if colour == 'Red':
            C.selection_turtle.fillcolor('red')
            C.selection_turtle.pencolor('red')

        C.selection_turtle.up()
        C.selection_turtle.goto(x, y)
        C.selection_turtle.right(C.selection_turtle.heading())
        C.selection_turtle.down()

        if fill != 'No':
            C.selection_turtle.begin_fill()
        for _ in range(2):
            C.selection_turtle.forward(w)
            C.selection_turtle.right(90)
            C.selection_turtle.forward(h)
            C.selection_turtle.right(90)
        
        if fill != 'No':
            C.selection_turtle.end_fill()

        if colour == 'Red':
            C.selection_turtle.fillcolor('black')
            C.selection_turtle.pencolor('black')

        C.selection_turtle.up()
        
        turtle.tracer(True)

def write_text(label, x, y, w, h, width):
    turtle.tracer(False)
    for a in range(len(label)):
        C.selection_turtle.goto(x + w/2, y - width + a * - 40)
        C.selection_turtle.write(label[a], False, align="center", font=("Arial", 20, "normal"))
    turtle.tracer(True)    


def selection(x, y):
    
    # Road
    if x >= 290 and x <= 460 and y <= 400 and y >= 400 - 115 and C.road_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Road'

    # Settlement
    elif x >= 290 and x <= 460 and y <= 260 and y >= 260 - 115 and C.settlement_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Settlement'

    # City
    elif x >= 290 and x <= 460 and y <= 120 and y >= 120 - 115 and C.city_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'City'

    # Development Card
    elif x >= 290 and x <= 460 and y <= -20 and y >= -20 - 115 and C.development_card_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Development Card'

    # Development Card
    elif x >= 290 and x <= 460 and y <= -160 and y >= -160 - 115 and C.card_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Play Card'

    # Development Card
    elif x >= 290 and x <= 460 and y <= -300 and y >= -300 - 115 and C.trade_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Trade'

    # End Turn
    elif x >= -450 and x <= -450 + 170 and y <= -250 and y >= -250 - 125:
        C.selecting_on_screen = True
        C.selecting_type = 'End Turn'

    else:
        print('Invalid Click')
        C.selecting_on_screen = False

def card_selection(x, y):
    
    # Knight
    if x >= -230 and x <= -230 + 100 and y <= -250 and y >= -250 - 125 and C.knight_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Knight'

    # Monopoly
    elif x >= -105 and x <= -105 + 100 and y <= -250 and y >= -250 - 125 and C.monopoly_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Monopoly'

    # Road Building
    elif x >= 20 and x <= 20 + 100 and y <= -250 and y >= -250 - 125 and C.road_building_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Road Building'

    # Year of Plenty
    elif x >= 145 and x <= 145 + 100 and y <= -250 and y >= -250 - 125 and C.year_of_plenty_check == 1:
        C.selecting_on_screen = True
        C.selecting_type = 'Year of Plenty'

    # End Turn
    elif x >= -450 and x <= -450 + 170 and y <= -250 and y >= -250 - 125:
        C.selecting_on_screen = True
        C.selecting_type = 'End Turn'

    else:
        print('Invalid Click')
        C.selecting_on_screen = False

def resource_selection(x, y):
    
    # Wood
    if x >= -400 and x <= -400 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Wood'

    # Brick
    elif x >= -275 and x <= -275 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Brick'

    # Wheat
    elif x >= -150 and x <= -150 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Wheat'

    # Sheep
    elif x >= -25 and x <= -25 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Sheep'

    # Stone
    elif x >= 100 and x <= 100 + 100 and y <= 350 and y >= 350 - 50:
        C.selecting_on_screen = True
        C.selecting_type = 'Stone'

    # End Turn
    elif x >= -450 and x <= -450 + 170 and y <= -250 and y >= -250 - 125:
        C.selecting_on_screen = True
        C.selecting_type = 'End Turn'

    else:
        print('Invalid Click')
        C.selecting_on_screen = False


def draw_square(x,y):
    turtle.tracer(False)
    C.dice_turtle.up()
    C.dice_turtle.goto(x,y)
    C.dice_turtle.down()
    for i in range(4):
        C.dice_turtle.forward(100)
        C.dice_turtle.left(90)
    C.dice_turtle.up()
    turtle.tracer(True)

def draw_dot(x, y):
    C.dice_turtle.up()
    C.dice_turtle.goto(x,y)
    C.dice_turtle.down()
    C.dice_turtle.fillcolor("black")
    C.dice_turtle.begin_fill()
    C.dice_turtle.circle(10)
    C.dice_turtle.end_fill()
    C.dice_turtle.up()

def draw_dice_roll(dr,x,y):
    draw_square(x,y)
    turtle.tracer(False)
    C.dice_turtle.up()

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

def goto(x, y):
    C.board_turtle.penup()
    C.board_turtle.goto(x, y)
    C.board_turtle.pendown()

def poly(points, fill=None, outline=None, pensize=1):
    if outline is None:
        C.board_turtle.pencolor(fill if fill else "black")
    else:
        C.board_turtle.pencolor(outline)
    C.board_turtle.pensize(pensize)
    if fill:
        C.board_turtle.fillcolor(fill)
        C.board_turtle.begin_fill()
    goto(points[0][0], points[0][1])
    for x, y in points[1:]:
        C.board_turtle.goto(x, y)
    C.board_turtle.goto(points[0][0], points[0][1])
    if fill:
        C.board_turtle.end_fill()

    C.board_turtle.penup()

def diamond(cx, cy, r, fill, outline=None, pensize=1):
    pts = [(cx, cy + r), (cx + r, cy), (cx, cy - r), (cx - r, cy)]
    poly(pts, fill=fill, outline=outline, pensize=pensize)

def circle_at(x, y, r, fill=None, outline=None, pensize=1):
    C.board_turtle.pensize(pensize)
    if outline is None:
        C.board_turtle.pencolor(fill if fill else "black")
    else:
        C.board_turtle.pencolor(outline)
    if fill:
        C.board_turtle.fillcolor(fill)
        C.board_turtle.begin_fill()
    C.board_turtle.penup()
    C.board_turtle.goto(x, y - r)
    C.board_turtle.setheading(0)
    C.board_turtle.pendown()
    C.board_turtle.circle(r)
    if fill:
        C.board_turtle.end_fill()

    C.board_turtle.penup()

# ---------- draw ----------
def draw_icon(cx=0, cy=0, s=2):
    # Color picks to roughly match the tiny reference
    CREAM = "#E8DDCF"
    CREAM_SHADOW = "#D3C6B8"

    BROWN = "#9A7B53"
    BROWN_DARK = "#7A5E3D"

    # cat face (simple rounded circle + slight shadow)
    circle_at(cx - 0*s, cy + 0*s, 6.2*s, fill=CREAM, outline=CREAM_SHADOW, pensize=max(1, s//6))

    # right "fur/ear" brown wedge
    wedge = [
        (cx + 0.0*s, cy - 3.5*s),
        (cx + 6.5*s, cy - 2.5*s),
        (cx + 5.0*s, cy - 6.5*s),
        (cx - 5.0*s, cy - 6.5*s),
        (cx - 6.5*s, cy - 2.5*s),
    ]
    poly(wedge, fill=BROWN, outline=BROWN_DARK, pensize=max(1, s//6))


    #C.board_turtle.goto(cx + 2.5*s, cy + 1.0*s)
    #C.board_turtle.dot(20)


def rect(cx, cy, w, h, fill, outline="black", pen=1):
    C.board_turtle.pensize(pen)
    C.board_turtle.pencolor(outline)
    C.board_turtle.fillcolor(fill)
    C.board_turtle.penup()
    C.board_turtle.goto(cx - w/2, cy - h/2)
    C.board_turtle.pendown()
    C.board_turtle.begin_fill()
    for _ in range(2):
        C.board_turtle.forward(w); C.board_turtle.left(90)
        C.board_turtle.forward(h); C.board_turtle.left(90)
    C.board_turtle.end_fill()

def circle(cx, cy, r, fill, outline="black", pen=1):
    C.board_turtle.pensize(pen)
    C.board_turtle.pencolor(outline)
    C.board_turtle.fillcolor(fill)
    C.board_turtle.penup()
    C.board_turtle.goto(cx, cy - r)
    C.board_turtle.pendown()
    C.board_turtle.begin_fill()
    C.board_turtle.circle(r)
    C.board_turtle.end_fill()

def log(cx, cy, w, h, fill="#A46A3A", outline="#6B3E1E", pen=1):
    r = h / 2
    # body + rounded ends
    rect(cx, cy, w, h, fill=fill, outline=outline, pen=pen)
    circle(cx - w/2, cy, r, fill=fill, outline=outline, pen=pen)
    circle(cx + w/2, cy, r, fill=fill, outline=outline, pen=pen)

    # end-grain rings (left end)
    C.board_turtle.pencolor(outline)
    C.board_turtle.pensize(max(1, int(pen)))
    for rr in (r * 0.65, r * 0.35):
        C.board_turtle.penup()
        C.board_turtle.goto(cx - w/2, cy - rr)
        C.board_turtle.pendown()
        C.board_turtle.circle(rr)

def draw_wood_stack(x=0, y=0, size=20, logs=3):
    """
    Draw a stack of logs inside a ~size x size box (roughly).
    x,y = center of the icon
    size = overall scale (20 gives ~20x20)
    logs = number of logs stacked (default 3)
    """
    # Proportions (tuned so total height fits within `size`)
    w = size                      # log width ~ overall size
    h = size * 0.30               # log height
    overlap = size * 0.05         # how much logs overlap vertically

    # Total stacked height:
    total_h = logs * h - (logs - 1) * overlap

    # Outline thickness scales with size (clamped)
    pen = max(1, int(size / 20))

    # Start from bottom log and stack upward
    bottom_cy = y - total_h / 2 + h / 2
    for i in range(logs):
        cy = bottom_cy + i * (h - overlap)
        log(x, cy, w=w, h=h, pen=pen)

def draw_brick_stack(x=0, y=0, box=5, bricks=3,
                     mortar_ratio=0.00, brick_ratio=1):
    """
    Draws `bricks` bricks stacked vertically inside a box x box.
    Scales with `box`.
    - mortar_ratio: thickness of mortar relative to box
    - brick_ratio: brick height relative to (usable height per brick)
    """

    # Dimensions
    mortar = box * mortar_ratio
    usable_h = box - mortar * (bricks + 1)  # top+bottom + between bricks
    per_slot = usable_h / bricks            # height available per brick (excluding mortar lines)
    brick_h = per_slot * brick_ratio
    gap_inside_slot = per_slot - brick_h

    # Brick width: leave a little inset from the box
    inset = max(mortar, box * 0.05)
    brick_w = (box - 2 * inset) * 1.7

    # Start from bottom-left of the overall box
    left = x - box / 2 - 4
    bottom = y - box / 2 

    def rect(px, py, w, h, fill=None, outline="black"):
        C.board_turtle.goto(px, py)
        C.board_turtle.setheading(0)
        C.board_turtle.pendown()
        C.board_turtle.pencolor(outline)
        if fill is not None:
            C.board_turtle.fillcolor(fill)
            C.board_turtle.begin_fill()
        for _ in range(2):
            C.board_turtle.forward(w); C.board_turtle.left(90)
            C.board_turtle.forward(h); C.board_turtle.left(90)
        if fill is not None:
            C.board_turtle.end_fill()
        C.board_turtle.penup()

    # Draw stacked bricks
    curr_y = bottom + mortar
    colors = ["#b55239", "#c15a3a", "#a94a35"]  # slight variation

    for i in range(bricks):
        # Center brick horizontally with inset
        bx = left + inset
        by = curr_y + gap_inside_slot / 2

        rect(bx, by, brick_w, brick_h, fill=colors[i % len(colors)], outline="black")

        # Move up to next slot (brick + inside gap + mortar line)
        curr_y += brick_h + gap_inside_slot + mortar


def bushel_of_wheat(x=0, y=0, box=20, stalks=9):
    """
    Draw a simple bushel of wheat (bundle of stalks + heads + tie)
    that fits roughly inside a box x box area and scales with `box`.
    """


    # Helpers
    def lerp(a, b, u): return a + (b - a) * u

    def goto(px, py):
        C.board_turtle.penup()
        C.board_turtle.goto(px, py)

    def line(x1, y1, x2, y2, width=1):
        C.board_turtle.pensize(width)
        C.board_turtle.goto(x1, y1)
        C.board_turtle.pendown()
        C.board_turtle.goto(x2, y2)
        C.board_turtle.penup()

    def oval(cx, cy, w, h, angle_deg, fill=None, outline="black", width=1):
        # Draw a small rotated oval using many short segments
        steps = 18
        rad = math.radians(angle_deg)
        C.board_turtle.pensize(width)
        C.board_turtle.pencolor(outline)
        if fill is not None:
            C.board_turtle.fillcolor(fill)
            C.board_turtle.begin_fill()
        pts = []
        for i in range(steps + 1):
            th = 2 * math.pi * i / steps
            px = (w / 2) * math.cos(th)
            py = (h / 2) * math.sin(th)
            rx = px * math.cos(rad) - py * math.sin(rad)
            ry = px * math.sin(rad) + py * math.cos(rad)
            pts.append((cx + rx, cy + ry))
        goto(pts[0][0], pts[0][1])
        C.board_turtle.pendown()
        for p in pts[1:]:
            C.board_turtle.goto(p[0], p[1])
        C.board_turtle.penup()
        if fill is not None:
            C.board_turtle.end_fill()

    # Scale constants
    s = box / 20.0
    stalk_w = 2 #max(1, int(round(2 * s)))

    # Bounding box corners (for positioning)
    bottom = y - box / 2

    # Colors
    stalk_color = "#c8a23a"
    outline = "black"

    C.board_turtle.pencolor(outline)

    # Bundle geometry: stems converge near the tie
    tie_y = bottom + box * 0.30
    base_y = bottom + box * 0.06
    head_y = bottom + box * 0.80

    center_x = x
    spread_top = box * 0.34
    spread_bottom = box * 0.12

    # Draw stalks
    for i in range(stalks):
        u = i / (stalks - 1) if stalks > 1 else 0.5
        # Top x spreads wider, bottom x is narrower
        top_x = center_x + lerp(-spread_top, spread_top, u) + (math.sin(i * 1.7) * box * 0.01)
        bot_x = center_x + lerp(-spread_bottom, spread_bottom, u)

        # Slight curve by splitting into 2 segments
        mid_x = (top_x + bot_x) / 2 + (top_x - bot_x) * 0.15
        mid_y = (head_y + base_y) / 2

        C.board_turtle.pencolor(stalk_color)
        line(bot_x, base_y, mid_x, mid_y, width=stalk_w)
        line(mid_x, mid_y, top_x, head_y, width=stalk_w)

        # A couple of side "awns" (little whiskers)
        C.board_turtle.pencolor(outline)
        awn_len = 4.5 * s
        for sign in (-1, 1):
            ax1, ay1 = top_x, head_y - 1.2 * s
            ax2 = ax1 + sign * awn_len * 0.75
            ay2 = ay1 + awn_len * 0.35
            line(ax1, ay1, ax2, ay2, width=max(1, int(round(1 * s))))

    # Little knot lines
    C.board_turtle.pencolor(outline)
    line(center_x - 1.5 * s, tie_y, center_x + 1.5 * s, tie_y, width=max(1, int(round(2 * s))))
    line(center_x, tie_y, center_x + 2.8 * s, tie_y - 2.2 * s, width=max(1, int(round(1 * s))))


def draw_sheep(x=0, y=0, box=20):
    """
    Cute pixel-ish sheep that fits roughly in a box x box area.
    Scales with `box`.
    """
    s = box / 20.0
    outline_w = max(1, int(round(1 * s)))

    def rect(px, py, w, h, fill, outline="black", pw=outline_w):
        C.board_turtle.pensize(pw)
        C.board_turtle.pencolor(outline)
        C.board_turtle.fillcolor(fill)
        C.board_turtle.goto(px, py)
        C.board_turtle.setheading(0)
        C.board_turtle.pendown()
        C.board_turtle.begin_fill()
        for _ in range(2):
            C.board_turtle.forward(w); C.board_turtle.left(90)
            C.board_turtle.forward(h); C.board_turtle.left(90)
        C.board_turtle.end_fill()
        C.board_turtle.penup()

    def circle_fill(cx, cy, r, fill, outline="black", pw=outline_w):
        C.board_turtle.pensize(pw)
        C.board_turtle.pencolor(outline)
        C.board_turtle.fillcolor(fill)
        C.board_turtle.goto(cx, cy - r)
        C.board_turtle.setheading(0)
        C.board_turtle.pendown()
        C.board_turtle.begin_fill()
        C.board_turtle.circle(r)
        C.board_turtle.end_fill()
        C.board_turtle.penup()

    # Colors
    wool = "#f2f2f2"
    face = "#444444"
    leg  = "#333333"
    ear  = "#3a3a3a"
    eye  = "black"

    # Layout inside the box (all relative)
    body_cx = x - 0.5 * s
    body_cy = y + 0.5 * s
    body_r  = 6.0 * s

    # Wool "puffs" around body (small circles)
    puff_r = 2.1 * s
    puffs = [
        (-6,  0), (-3,  4), (1,  5), (5,  3),
        (6,  0), (5, -3), (1, -5), (-3, -4),
        (-6, -1)
    ]
    for dx, dy in puffs:
        circle_fill(body_cx + dx*s, body_cy + dy*s, puff_r, wool, outline="black", pw=outline_w)

    # Main body (slightly smaller so puffs show)
    circle_fill(body_cx, body_cy, body_r, wool, outline="black", pw=outline_w)

    # Head (right side)
    head_w = 6.0 * s
    head_h = 5.0 * s
    head_x = x + 4.5 * s
    head_y = y - 0.5 * s
    rect(head_x - head_w/2, head_y - head_h/2, head_w, head_h, face, outline="black", pw=outline_w)

    # Ears
    ear_w = 2.2 * s
    ear_h = 2.4 * s
    rect(head_x - head_w/2 - ear_w*0.9, head_y + ear_h*0.3, ear_w, ear_h, ear, outline="black", pw=outline_w)
    rect(head_x + head_w/2 - ear_w*0.1, head_y + ear_h*0.3, ear_w, ear_h, ear, outline="black", pw=outline_w)

    # Legs (4 little rectangles)
    leg_w = 2.0 * s
    leg_h = 4.0 * s
    leg_y = y - 8.0 * s
    legs_x = [x - 5.0*s, x - 1.5*s, x + 1.5*s, x + 4.8*s]
    for lx in legs_x:
        rect(lx - leg_w/2, leg_y, leg_w, leg_h, leg, outline="black", pw=outline_w)

    # Eyes (two small filled circles)
    eye_r = 0.7 * s
    circle_fill(head_x - 1.4*s, head_y + 0.8*s, eye_r, eye, outline=eye, pw=max(1, int(round(1*s))))
    circle_fill(head_x + 1.4*s, head_y + 0.8*s, eye_r, eye, outline=eye, pw=max(1, int(round(1*s))))

    # Snout / nose (tiny lighter patch + nostrils)
    snout_w = 3.2 * s
    snout_h = 2.0 * s
    rect(head_x - snout_w/2, head_y - 2.0*s, snout_w, snout_h, "#666666", outline="black", pw=max(1, int(round(1*s))))
    circle_fill(head_x - 0.7*s, head_y - 1.3*s, 0.25*s, "black", outline="black", pw=1)
    circle_fill(head_x + 0.7*s, head_y - 1.3*s, 0.25*s, "black", outline="black", pw=1)

def draw_3_stones_triangle(x=0, y=0, box=20, stone_ratio=0.28, jitter=0.10):
    """
    Draw 3 stones arranged in a triangle formation, scaled to fit roughly in box x box.

    x, y          : center of the formation
    box           : overall size (20 by default)
    stone_ratio   : stone radius relative to box (0.28 works well for 3 stones)
    jitter        : how "rocky" the outline is (0 = perfect circle)
    """
    s = box / 20.0
    outline_w = max(1, int(round(1 * s)))

    def rocky_circle(cx, cy, r, fill="#9b9b9b", outline="black", width=outline_w, rough=jitter):
        steps = 24
        C.board_turtle.pensize(width)
        C.board_turtle.pencolor(outline)
        C.board_turtle.fillcolor(fill)

        # deterministic "jitter" based on step index (no random module needed)
        pts = []
        for i in range(steps + 1):
            ang = 2 * math.pi * i / steps
            wobble = 1.0 + rough * math.sin(i * 1.9) * 0.6 + rough * math.cos(i * 2.7) * 0.4
            rr = r * wobble
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))

        C.board_turtle.goto(pts[0]); C.board_turtle.pendown()
        C.board_turtle.begin_fill()
        for p in pts[1:]:
            C.board_turtle.goto(p)
        C.board_turtle.end_fill()
        C.board_turtle.penup()

        # small highlight
        C.board_turtle.pensize(max(1, int(round(1 * s))))
        C.board_turtle.pencolor("white")
        C.board_turtle.goto(cx - r*0.25, cy + r*0.15)
        C.board_turtle.setheading(20)
        C.board_turtle.pendown()
        C.board_turtle.forward(r * 0.7)
        C.board_turtle.penup()

    # Geometry for triangle (equilateral-ish)
    r = box * stone_ratio
    side = r * 2.2  # spacing between stone centers
    tri_h = side * math.sqrt(3) / 2

    # Centers (top, bottom-left, bottom-right)
    c_top = (x, y + tri_h/3)
    c_bl  = (x - side/2, y - tri_h*2/3)
    c_br  = (x + side/2, y - tri_h*2/3)

    # Draw (slightly varied fills)
    rocky_circle(*c_top, r, fill="#9e9e9e")
    rocky_circle(*c_bl,  r*0.98, fill="#8f8f8f")
    rocky_circle(*c_br,  r*1.02, fill="#a7a7a7")



def draw_shipping(x,y,number,tile_type):
    
    draw_icon(x, y, s=3)

    C.board_turtle.goto(x, y-10)
    C.board_turtle.write(str(-number)+ ':1', False, align="center", font=("Arial", 7, "normal"))

    if number == -3:
        C.board_turtle.goto(x, y+2)
        C.board_turtle.write('?', False, align="center", font=("Arial", 7, "normal"))
    elif number == -2:
        if tile_type == 'Wood':
            draw_wood_stack(x, y+8, size=11, logs=3)
        elif tile_type == 'Brick':
            draw_brick_stack(x, y+8, box=9, bricks=3)
        elif tile_type == 'Wheat':
            bushel_of_wheat(x, y+8, box=12, stalks=3)
        elif tile_type == 'Sheep':
            draw_sheep(x, y+8, box=14)
        elif tile_type == 'Stone':
            draw_3_stones_triangle(x, y+9, box=10)

def announce_text(text):
    C.text_announcer_turtle.clear()
    C.text_announcer_turtle.goto(0, 400)
    C.text_announcer_turtle.write(text, False, align="center", font=("Arial", 10, "normal"))