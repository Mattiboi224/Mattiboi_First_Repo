# Catan Game

# Improvements
# Adjust colouring of board i.e. have a board around the tiles to make it clearer -- Done
# Change the colours of the player
# Make a function to split mid game clicks vs start game -- Done
# Adjust early game clicks to have settlements and roads only in correct order -- Done
# Adjust the number of pieces played by the player to stop breaking rules -- In Prog
# Add Mid Game Placement rules and function -- Done
    # Options for player to select different things to do
    # Getting Development Cards -- Done
    # Add Playing Cards
    # Building
    # Add Trading
# Add Title for who's turn it is
# Display what resources each player has
# Add Non-Human Player
# Limit piece players can build
# Robber doesn't remove more than 7 resources
# Information to tell you what you do


# Bugs
# Fix the 13 vs 12 early game placement
# Fix drawing for the first settlement placement  -- Done
# Clear and rebuild for Cities
# Fix City Rebuild to update
# Robber Breaks game via while loop
# Robber Removes Numbers


import turtle
import Config as C
import random
from game import Game
from player import Player as P
import util as m

# Create Teams
TEAM_1 = P(C.TEAM_1_COLOUR, 'TEAM_1', 1)
TEAM_2 = P(C.TEAM_2_COLOUR, 'TEAM_2', 1)
TEAM_3 = P(C.TEAM_3_COLOUR, 'TEAM_3', 1)

team_mat = []

# Team LIST
team_mat.append(TEAM_1)
team_mat.append(TEAM_2)
team_mat.append(TEAM_3)

game = Game(team_mat)

random.shuffle(C.DEVELOPMENT_CARD_DECK)

# Select Positions
for pre_turn in range(4 * len(team_mat)):

    # First 2 are Settlements
    # Second 2 are Roads

    # Team 1
    if pre_turn in [0, 5, 6, 11]:

        C.selecting_on_screen = False
        if pre_turn in [0, 5]:
            C.selecting_type = 'Settlement'
        else:
            C.selecting_type = 'Road'
        C.selected_team = team_mat[0]
        turtle.onscreenclick(game.unit_at_point)

        while not C.selecting_on_screen:
            C.wn.update()

        turtle.onscreenclick(None)

    # Team 2
    elif pre_turn in [1, 4, 7, 10]:
        
        C.selecting_on_screen = False
        if pre_turn in [1, 4]:
            C.selecting_type = 'Settlement'
        else:
            C.selecting_type = 'Road'
        C.selected_team = team_mat[1]
        turtle.onscreenclick(game.unit_at_point)
        
        while not C.selecting_on_screen:
            C.wn.update()

        turtle.onscreenclick(None)

    # Team 2
    elif pre_turn in [2, 3, 8, 9]:

        C.selecting_on_screen = False  
        if pre_turn in [2, 3]:
            C.selecting_type = 'Settlement'
        else:
            C.selecting_type = 'Road'
        C.selected_team = team_mat[2]
        turtle.onscreenclick(game.unit_at_point)
        while not C.selecting_on_screen:
            C.wn.update()

        turtle.onscreenclick(None)

C.selecting_type = None
    

for turn in range(50):

    # Roll the dice
    dice_roll = random.randint(1,12)

    # Find which Tile has been triggered
    for i in game.board.Tiles_Mat:
        if i.number == dice_roll:

            # Find which corners are occupied
            for j in i.corner_mat_class:
                if j.is_occupied == 1:

                    # Check who's occupied by
                    for k in team_mat:
                        if k.team == j.team:

                            # Give Resources
                            if j.building == 'Settlement':
                                k.resources.append(i.tile_type)
                            elif j.building == 'City':
                                k.resources.append(i.tile_type)
                                k.resources.append(i.tile_type)
        
            

    if turn % C.NO_OF_PLAYER == 0:

        game.update_stats(turn % C.NO_OF_PLAYER)

        C.selecting_type = None
        
        # Robber Activates
        if dice_roll == 7:

            C.selecting_on_screen = False
            C.selected_team = team_mat
            C.built = turn

            turtle.onscreenclick(game.robber_switch)

            while not C.selecting_on_screen:
                C.wn.update()

            turtle.onscreenclick(None)
            C.selecting_on_screen = False

            game.update_stats(turn % C.NO_OF_PLAYER)
        

        while C.selecting_type != 'End Turn':

            # See if they can do anything
            ava_resources = team_mat[turn % C.NO_OF_PLAYER].resources

            print(ava_resources)

            count_wood = 0
            count_brick = 0
            count_wheat = 0
            count_stone = 0
            count_sheep = 0

            for i in range(len(ava_resources)):

                if ava_resources[i] == 'Wood':
                    count_wood += 1
                elif ava_resources[i] == 'Brick':
                    count_brick += 1
                elif ava_resources[i] == 'Wheat':
                    count_wheat += 1
                elif ava_resources[i] == 'Stone':
                    count_stone += 1
                elif ava_resources[i] == 'Sheep':
                    count_sheep += 1

            # Put all the options of stuff they can do on the screen if they can do them with a skip

            C.road_check = 0
            C.settlement_check = 0
            C.city_check = 0
            C.development_card_check = 0
            C.end_turn_check = 0
            C.card_check = 0
            C.knight_check = 0
            C.monopoly_check = 0
            C.road_building_check = 0
            C.year_of_plenty_check = 0


            # Road Check
            if count_wood >= C.BUILD_ROAD_REQ_WOOD and count_brick >= C.BUILD_ROAD_REQ_BRICK and \
                team_mat[turn % C.NO_OF_PLAYER].avaliable_road_pieces > 0:

                # Draw Check
                C.road_check = 1

                # Draw Road Selection Box
                m.rectangle_shape(290, 350, 170, 115, 'Selection')
                m.write_text(['Build', 'Road'], 290, 350, 170, 125, 50)
                # turtle.tracer(False)
                # C.selection_turtle.goto(290 + 85, 350 - 60)
                # C.selection_turtle.write('Build', False, align="center", font=("Arial", 20, "normal"))
                # C.selection_turtle.goto(290 + 85, 350 - 100)
                # C.selection_turtle.write('Road', False, align="center", font=("Arial", 20, "normal"))
                # turtle.tracer(True)
            
            # Settlement check
            if count_wood >= C.BUILD_SETTLEMENT_REQ_WOOD and \
                count_brick >= C.BUILD_SETTLEMENT_REQ_BRICK and \
                count_wheat >= C.BUILD_SETTLEMENT_REQ_WHEAT and \
                    count_sheep >= C.BUILD_SETTLEMENT_REQ_SHEEP and \
                        team_mat[turn % C.NO_OF_PLAYER].avaliable_settlement_pieces > 0:
                
                C.settlement_check = 1

                # Draw Settlement Selection Box
                m.rectangle_shape(290, 210, 170, 115, 'Selection')
                m.write_text(['Build', 'Settlement'], 290, 210, 170, 125, 50)
                
                # turtle.tracer(False)
                # C.selection_turtle.goto(290 + 85, 175 - 60)
                # C.selection_turtle.write('Build', False, align="center", font=("Arial", 20, "normal"))
                # C.selection_turtle.goto(290 + 85, 175 - 100)
                # C.selection_turtle.write('Settlement', False, align="center", font=("Arial", 20, "normal"))
                # turtle.tracer(True)

                        
            # City Check
            if count_wheat >= C.BUILD_CITY_REQ_WHEAT and count_stone >= C.BUILD_CITY_REQ_STONE and \
                team_mat[turn % C.NO_OF_PLAYER].avaliable_city_pieces > 0:
                
                C.city_check = 1

                # Draw City Selection Box
                m.rectangle_shape(290, 70, 170, 115, 'Selection')
                m.write_text(['Build', 'City'], 290, 70, 170, 125, 50)

                # turtle.tracer(False)
                # C.selection_turtle.goto(290 + 85, 0 - 60)
                # C.selection_turtle.write('Build', False, align="center", font=("Arial", 20, "normal"))
                # C.selection_turtle.goto(290 + 85, 0 - 100)
                # C.selection_turtle.write('City', False, align="center", font=("Arial", 20, "normal"))
                # turtle.tracer(True)


            # Development Card Check
            if count_wheat >= C.BUILD_DEVELOPMENT_CARD_REQ_WHEAT and \
                count_stone >= C.BUILD_DEVELOPMENT_CARD_REQ_STONE and \
                    count_sheep >= C.BUILD_DEVELOPMENT_CARD_REQ_SHEEP and \
                        len(C.DEVELOPMENT_CARD_DECK) > 0:
                
                C.development_card_check = 1

                # Draw Development Card Box
                m.rectangle_shape(290, -70, 170, 115, 'Selection')
                m.write_text(['Buy', 'Development', 'Card'], 290, -70, 170, 125, 30)

                # turtle.tracer(False)
                # C.selection_turtle.goto(290 + 85, -175 - 40)
                # C.selection_turtle.write('Buy', False, align="center", font=("Arial", 20, "normal"))
                # C.selection_turtle.goto(290 + 85, -175 - 80)
                # C.selection_turtle.write('Development', False, align="center", font=("Arial", 20, "normal"))
                # C.selection_turtle.goto(290 + 85, -175 - 120)
                # C.selection_turtle.write('Card', False, align="center", font=("Arial", 20, "normal"))
                # turtle.tracer(True)


            # Play Development cards Check
            # Check if they have a card to play that's not a Victory Point Card
            if len(team_mat[turn % C.NO_OF_PLAYER].cards) > team_mat[turn % C.NO_OF_PLAYER].cards.count('VP'):
                
                C.card_check = 1

                # Draw Available Cards
                m.rectangle_shape(290, -210, 170, 115, 'Selection')
                m.write_text(['Play', 'Card'], 290, -210, 170, 125, 50)


            # End Turn Box creation
            m.rectangle_shape(-450, -250, 170, 125, 'Selection', fill='Yes', colour='Red')
            turtle.tracer(False)
            C.selection_turtle.pencolor('Black')
            C.selection_turtle.goto(-450 + 85, -250 - 60)
            C.selection_turtle.write('End', False, align="center", font=("Arial", 20, "normal"))
            C.selection_turtle.goto(-450 + 85, -250 - 100)
            C.selection_turtle.write('Turn', False, align="center", font=("Arial", 20, "normal"))
            turtle.tracer(True)

            C.selecting_on_screen = False

            # Set Click Boxes and Make sure exit box exists


            
            turtle.onscreenclick(m.selection)

            while not C.selecting_on_screen:
                C.wn.update()

            turtle.onscreenclick(None)

            # Do the option selected
            if C.selecting_type in ('Settlement', 'Road', 'City'):
                C.selecting_on_screen = False
                C.selected_team = team_mat[turn % C.NO_OF_PLAYER]

                turtle.onscreenclick(game.unit_at_point)

                while not C.selecting_on_screen:
                    C.wn.update()

                turtle.onscreenclick(None)
                C.selecting_on_screen = False

                if C.built == 'Settlement':
                    team_mat[turn % C.NO_OF_PLAYER].current_points += 1
                    team_mat[turn % C.NO_OF_PLAYER].avaliable_settlement_pieces -= 1
                    
                    # Remove Resources
                    for _ in range(C.BUILD_SETTLEMENT_REQ_WOOD):
                        team_mat[turn % C.NO_OF_PLAYER].resources.remove('Wood')

                    for _ in range(C.BUILD_SETTLEMENT_REQ_BRICK):
                        team_mat[turn % C.NO_OF_PLAYER].resources.remove('Brick')

                    for _ in range(C.BUILD_SETTLEMENT_REQ_WHEAT):
                        team_mat[turn % C.NO_OF_PLAYER].resources.remove('Wheat')

                    for _ in range(C.BUILD_SETTLEMENT_REQ_SHEEP):
                        team_mat[turn % C.NO_OF_PLAYER].resources.remove('Sheep')

                elif C.built == 'City':
                    team_mat[turn % C.NO_OF_PLAYER].current_points += 2
                    team_mat[turn % C.NO_OF_PLAYER].avaliable_city_pieces -= 1

                    # Remove Resources
                    for _ in range(C.BUILD_CITY_REQ_WHEAT):
                        team_mat[turn % C.NO_OF_PLAYER].resources.remove('Wheat')

                    for _ in range(C.BUILD_CITY_REQ_STONE):
                        team_mat[turn % C.NO_OF_PLAYER].resources.remove('Stone')

                    C.main_turtle.clear()
                    game.board.draw_current_board(team_mat)

                elif C.built == 'Road':

                    # Remove Resources
                    for _ in range(C.BUILD_ROAD_REQ_WOOD):
                        team_mat[turn % C.NO_OF_PLAYER].resources.remove('Wood')

                    for _ in range(C.BUILD_ROAD_REQ_BRICK):
                        team_mat[turn % C.NO_OF_PLAYER].resources.remove('Brick')

                C.selecting_type = None

            elif C.selecting_type == 'Development Card':

                # Give the card to the player
                team_mat[turn % C.NO_OF_PLAYER].cards.append(C.DEVELOPMENT_CARD_DECK[0])
                C.DEVELOPMENT_CARD_DECK.pop(0)

                # Remove Resources
                for _ in range(C.BUILD_DEVELOPMENT_CARD_REQ_SHEEP):
                    team_mat[turn % C.NO_OF_PLAYER].resources.remove('Sheep')

                for _ in range(C.BUILD_DEVELOPMENT_CARD_REQ_STONE):
                    team_mat[turn % C.NO_OF_PLAYER].resources.remove('Stone')

                for _ in range(C.BUILD_DEVELOPMENT_CARD_REQ_WHEAT):
                    team_mat[turn % C.NO_OF_PLAYER].resources.remove('Wheat')

                C.selecting_type = None

            elif C.selecting_type == 'Play Card':
                
                if 'Knight' in team_mat[turn % C.NO_OF_PLAYER].cards:
                    m.rectangle_shape(-230, -250, 100, 125, 'Selection')
                    m.write_text(['Knight'], -230, -250, 100, 125, 50)
                    C.knight_check = 1

                if 'Monopoly' in team_mat[turn % C.NO_OF_PLAYER].cards:
                    m.rectangle_shape(-105, -250, 100, 125, 'Selection')
                    m.write_text(['Monopoly'], -105, -250, 100, 125, 50)
                    C.monopoly_check = 1

                if 'Road Building' in team_mat[turn % C.NO_OF_PLAYER].cards:
                    m.rectangle_shape(20, -250, 100, 125, 'Selection')
                    m.write_text(['Road', 'Building'] , 20, -250, 100, 125, 50)
                    C.road_building_check = 1

                if 'Year of Plenty' in team_mat[turn % C.NO_OF_PLAYER].cards:
                    m.rectangle_shape(145, -250, 100, 125, 'Selection')
                    m.write_text(['Year', 'of', 'Plenty'], 145, -250, 100, 125, 50)
                    C.year_of_plenty_check = 1


                C.selecting_on_screen = False

                turtle.onscreenclick(m.card_selection)

                while not C.selecting_on_screen:
                    C.wn.update()

                turtle.onscreenclick(None)
                C.selecting_on_screen = False

                if C.selecting_type == 'Knight':
                    # Move the Robber. Steal 1 resource from the owner of the settlement or city
                    # adjacent to the robber's new hex

                    pass
                elif C.selecting_type == 'Monopoly':
                    # When you play this card, announce 1 type of resource. All other players must
                    # give you all of their resources of that type

                    C.selecting_on_screen = False
                
                    turtle.onscreenclick(m.resource_selection)

                    while not C.selecting_on_screen:
                        C.wn.update()

                    turtle.onscreenclick(None)
                    C.selecting_on_screen = False
                    
                    if C.selecting_type != 'End Turn':

                        for i in team_mat:

                            # Skip Itself
                            if i == team_mat[turn % C.NO_OF_PLAYER]:
                                print(turn % C.NO_OF_PLAYER)
                                continue

                            if C.selecting_type in i.resources:
                                print('Check')
                                
                                occurrence = i.resources.count(C.selecting_type)
                                
                                # Add to player
                                team_mat[turn % C.NO_OF_PLAYER].resources.extend([C.selecting_type] * occurrence)

                                for _ in range(i.resources.count(C.selecting_type)):
                                    i.resources.remove(C.selecting_type)

                        team_mat[turn % C.NO_OF_PLAYER].cards.remove('Monopoly')


                elif C.selecting_type == 'Road Building':
                    # Place 2 new roads as if you just built them
                    C.selected_team = team_mat[turn % C.NO_OF_PLAYER]

                    for _ in range(2):
                        C.selecting_on_screen = False
                    
                        turtle.onscreenclick(game.unit_at_point)

                        while not C.selecting_on_screen:
                            C.wn.update()

                        turtle.onscreenclick(None)
                        C.selecting_on_screen = False

                        game.update_stats(turn % C.NO_OF_PLAYER)

                    if C.selecting_type != 'End Turn':
                        team_mat[turn % C.NO_OF_PLAYER].cards.remove('Road Building')

                elif C.selecting_type == 'Year of Plenty':
                    # Take any 2 resources from the bank. Add them to your hand. They can be 2 of
                    # the same resouces or 2 different resources

                    a = ['Wood', 'Brick', 'Wheat', 'Sheep', 'Stone']
                    for i in range(len(a)):
                        label = [a[i]]
                        #print(label)
                        m.rectangle_shape(-400 + i * 125, 350, 100, 50, 'Selection')
                        m.write_text(label, -400 + i * 125, 320, 100, 125, 10)

                    for _ in range(2):
                        C.selecting_on_screen = False
                    
                        turtle.onscreenclick(m.resource_selection)

                        while not C.selecting_on_screen:
                            C.wn.update()

                        turtle.onscreenclick(None)
                        C.selecting_on_screen = False

                        if C.selecting_type != 'End Turn':
                            team_mat[turn % C.NO_OF_PLAYER].resources.append(C.selecting_type)

                        else:
                            break

                        game.update_stats(turn % C.NO_OF_PLAYER)

                        team_mat[turn % C.NO_OF_PLAYER].cards.remove('Year of Plenty')

                C.selecting_type = None


            elif C.selecting_type == 'Trade':
                
                pass
                # Trade with another player

            # Once selected
            C.selection_turtle.clear()
        



for i in team_mat:
    print(i.resources)

print('Ended Game')

C.wn.exitonclick()