# Catan Game

# Improvements
# Adjust colouring of board i.e. have a board around the tiles to make it clearer -- Done
# Change the colours of the player -- Done
# Make a function to split mid game clicks vs start game -- Done
# Adjust early game clicks to have settlements and roads only in correct order -- Done
# Adjust the number of pieces played by the player to stop breaking rules -- Done
# Add Mid Game Placement rules and function -- Done
    # Options for player to select different things to do -- Done
    # Getting Development Cards -- Done
    # Add Playing Cards -- Done
    # Building -- Done
    # Add Trading To Docks -- Done
    # Add Trading to Players

# Add Title for who's turn it is
# Display what resources each player has -- Done
# Add Non-Human Player
# Limit piece players can build -- Done
# Robber doesn't remove more than 7 resources
# Information to tell you what you do -- MORE IMPORTANT -- Done
# Add Indictator to corner that it can trade via seaport -- IN BOARD -- Done
# Add map icon to determine which corner can trade -- In GAME
# Create the requirements for a button to show, i.e. Tradeable items and next to seaport -- Done
# Create a button to the right to allow a trade -- In UTIL -- Done
# Click the seaport to know which seaport is trading -- In GAME
# Select the resource of what you want if 2x1 and what resources to and from for a 3x1 -- IN MAIN -- 1/2 Done
# Complete the trade -- IN MAIN -- Done
# Remove resources based tradable resource I have
# Add Longest Road
# Add Largest Army


# Bugs
# Fix the 13 vs 12 early game placement -- Done
# Fix drawing for the first settlement placement  -- Done
# Clear and rebuild for Cities -- Done
# Fix City Rebuild to update -- Done
# Robber Breaks game via while loop -- Done
# Robber Removes Numbers -- Done
# Check Victory Point Logic when building settlements


import turtle
import Config as C
import random
from collections import Counter
from game import Game
from player import Player as P
from corner import Corner as Co
from road import Road as R
import util as m

# Create Teams
TEAM_1 = P(C.TEAM_1_COLOUR, 'TEAM_1', 1)
TEAM_2 = P(C.TEAM_2_COLOUR, 'TEAM_2', 0)
TEAM_3 = P(C.TEAM_3_COLOUR, 'TEAM_3', 0)

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
            m.announce_text('Select a settlement')
        else:
            C.selecting_type = 'Road'
            m.announce_text('Select a road')
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
            m.announce_text('Select a settlement')
        else:
            C.selecting_type = 'Road'
            m.announce_text('Select a road')

        C.selected_team = team_mat[1]

        if team_mat[1].is_human == 0:

            game.intial_ai_build(team_mat[1])
        
        else:
            turtle.onscreenclick(game.unit_at_point)
            
            while not C.selecting_on_screen:
                C.wn.update()

            turtle.onscreenclick(None)

    # Team 2
    elif pre_turn in [2, 3, 8, 9]:

        C.selecting_on_screen = False  
        if pre_turn in [2, 3]:
            C.selecting_type = 'Settlement'
            m.announce_text('Select a settlement')
        else:
            C.selecting_type = 'Road'
            m.announce_text('Select a road')

        C.selected_team = team_mat[2]

        if team_mat[2].is_human == 0:

            game.intial_ai_build(team_mat[2])
        
        else:
            turtle.onscreenclick(game.unit_at_point)
            
            while not C.selecting_on_screen:
                C.wn.update()

            turtle.onscreenclick(None)

# Give resources to player for intial starting placement
C.text_announcer_turtle.clear()

for i in game.objects:
    
    # If Road Skip or not occupied
    if isinstance(i, R) or i.is_occupied == 0:
        continue

    # Check the teams
    for k in team_mat:

        # If the team matches the object continue
        if i.team == k.team:

            # Find the Tiles surrounding it
            for j in i.nearby_tiles:

                # Append the resource
                k.resources.append(j.tile_type)



C.selecting_type = None
    

#for turn in range(50):
win_con = 0
for i in team_mat:
    if i.current_points > win_con:
        win_con = i.current_points


turn = 0

while win_con <= C.NO_OF_VICTORY_WINNING_POINTS:

    game.update_stats(turn % C.NO_OF_PLAYER)

    # Roll the dice
    dice_roll_1 = random.randint(1,6)
    dice_roll_2 = random.randint(1,6)

    m.draw_dice_roll(dice_roll_1, 150, 150)
    m.draw_dice_roll(dice_roll_2, -250, 150)

    dice_roll = dice_roll_1 + dice_roll_2

    # Find which Tile has been triggered
    for i in game.board.Tiles_Mat:
        if i.number == dice_roll and i.tile_type != 'Sand':

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
        
            

#if team_mat[turn % C.NO_OF_PLAYER].is_human == 1:

    game.update_stats(turn % C.NO_OF_PLAYER)

    C.selecting_type = None
    
    # Robber Activates
    if dice_roll == 7:

        C.selecting_on_screen = False
        C.selected_team = team_mat
        C.built = turn

        m.announce_text('Move the Robber')

        if team_mat[turn % C.NO_OF_PLAYER].is_human == 1:

            turtle.onscreenclick(game.robber_switch)

            while not C.selecting_on_screen:
                C.wn.update()

            turtle.onscreenclick(None)
            C.selecting_on_screen = False

            game.update_stats(turn % C.NO_OF_PLAYER)
        
        else:
            game.ai_robber(team_mat[turn % C.NO_OF_PLAYER])

    possible_road = 1
    possible_settlement = 1
    possible_city = 1
    possible_development_card = 1
    possible_play_card = 1


    while C.selecting_type != 'End Turn':

        # See if they can do anything
        ava_resources = team_mat[turn % C.NO_OF_PLAYER].resources

        #print(ava_resources)

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
        C.trade_check = 0


        # Road Check
        if count_wood >= C.BUILD_ROAD_REQ_WOOD and count_brick >= C.BUILD_ROAD_REQ_BRICK and \
            team_mat[turn % C.NO_OF_PLAYER].avaliable_road_pieces > 0 and possible_road == 1:

            # Draw Check
            C.road_check = 1


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
                    team_mat[turn % C.NO_OF_PLAYER].avaliable_settlement_pieces > 0 and \
                        possible_settlement == 1:
            
            C.settlement_check = 1


            
            # turtle.tracer(False)
            # C.selection_turtle.goto(290 + 85, 175 - 60)
            # C.selection_turtle.write('Build', False, align="center", font=("Arial", 20, "normal"))
            # C.selection_turtle.goto(290 + 85, 175 - 100)
            # C.selection_turtle.write('Settlement', False, align="center", font=("Arial", 20, "normal"))
            # turtle.tracer(True)

                    
        # City Check
        if count_wheat >= C.BUILD_CITY_REQ_WHEAT and count_stone >= C.BUILD_CITY_REQ_STONE and \
            team_mat[turn % C.NO_OF_PLAYER].avaliable_city_pieces > 0 and possible_city == 1:
            
            C.city_check = 1


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
                    len(C.DEVELOPMENT_CARD_DECK) > 0 and \
                        possible_development_card == 1:
            
            C.development_card_check = 1

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
        if len(team_mat[turn % C.NO_OF_PLAYER].cards) > team_mat[turn % C.NO_OF_PLAYER].cards.count('VP') and possible_play_card == 1:
            
            C.card_check = 1


        game_trade_check = 0
        # Trade with Game
        counts = Counter(team_mat[turn % C.NO_OF_PLAYER].resources)
        if len(team_mat[turn % C.NO_OF_PLAYER].resources) > 1:
            most_common_item, occurrences = counts.most_common(1)[0]
        if occurrences >= 4:
            game_trade_check = 1
        
        seaport_trade_check = 0
        resource_seaport_trade_check = 0
        # Trade with Seaport
        # Check if they own a seaport that has trading
        for i in game.board.seaports_class:
            for j in i.corner_mat_class:
                if j.is_occupied == 1 and j.team == team_mat[turn % C.NO_OF_PLAYER].team and j.seaport_trade == 1:
                    if i.number == -3:
                        if occurrences >= 3:
                            seaport_trade_check = 1
                    elif i.number == -2:
                        counts = team_mat[turn % C.NO_OF_PLAYER].resources.count(i.tile_type)
                        if counts > 2:
                            resource_seaport_trade_check = 1
                            original_resource = i.tile_type
        
        if team_mat[turn % C.NO_OF_PLAYER].is_human == 1:
            if C.road_check == 1:
                # Draw Road Selection Box
                m.rectangle_shape(290, 400, 170, 115, 'Selection')
                m.write_text(['Build', 'Road'], 290, 400, 170, 125, 50)

            if C.settlement_check == 1:
                # Draw Settlement Selection Box
                m.rectangle_shape(290, 260, 170, 115, 'Selection')
                m.write_text(['Build', 'Settlement'], 290, 260, 170, 125, 50)

            if C.city_check == 1:
                # Draw City Selection Box
                m.rectangle_shape(290, 120, 170, 115, 'Selection')
                m.write_text(['Build', 'City'], 290, 120, 170, 125, 50)

            if C.development_card_check == 1:
                # Draw Development Card Box
                m.rectangle_shape(290, -20, 170, 115, 'Selection')
                m.write_text(['Buy', 'Development', 'Card'], 290, -20, 170, 125, 30)

            if C.card_check == 1:
                # Draw Available Cards
                m.rectangle_shape(290, -160, 170, 115, 'Selection')
                m.write_text(['Play', 'Card'], 290, -160, 170, 125, 50)

            if seaport_trade_check == 1 or game_trade_check == 1 or resource_seaport_trade_check == 1:
                C.trade_check = 1
                # Draw Available Cards
                m.rectangle_shape(290, -300, 170, 115, 'Selection')
                m.write_text(['Trade'], 290, -300, 170, 125, 50)


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

            m.announce_text('Select what to do')
            
            turtle.onscreenclick(m.selection)

            while not C.selecting_on_screen:
                C.wn.update()

            turtle.onscreenclick(None)

        else:
            avaliable_options = []

            if C.road_check == 1:
                avaliable_options.append('Road')

            if C.settlement_check == 1:
                avaliable_options.append('Settlement')

            if C.city_check == 1:
                avaliable_options.append('City')

            if C.development_card_check == 1:
                avaliable_options.append('Development Card')

            if C.card_check == 1:
                avaliable_options.append('Play Card')

            if len(avaliable_options) > 0:
                option_selected = random.randint(0, len(avaliable_options) - 1)

                C.selecting_type = avaliable_options[option_selected]

            else:
                C.selecting_type = 'End Turn'

            # Ignoring Trade

        # Do the option selected
        if C.selecting_type in ('Settlement', 'Road', 'City'):

            if team_mat[turn % C.NO_OF_PLAYER].is_human == 1:
                C.selecting_on_screen = False
                C.selected_team = team_mat[turn % C.NO_OF_PLAYER]

                if C.selecting_type == 'Settlement':
                    m.announce_text('Select a Settlement')

                if C.selecting_type == 'Road':
                    m.announce_text('Build a Road')

                if C.selecting_type == 'City':
                    m.announce_text('Build a City')

                turtle.onscreenclick(game.unit_at_point)

                while not C.selecting_on_screen:
                    C.wn.update()

                turtle.onscreenclick(None)
                C.selecting_on_screen = False
            
            else:
                if C.selecting_type == 'Settlement':
                    if game.ai_find_settlement(team_mat[turn % C.NO_OF_PLAYER]):
                        C.built = 'Settlement'
                    else:
                        possible_settlement = 0

                elif C.selecting_type == 'Road':
                    if game.ai_find_road(team_mat[turn % C.NO_OF_PLAYER]):
                        C.built = 'Road'
                    else:
                        possible_road = 0

                elif C.selecting_type == 'City':
                    if game.ai_build_city(team_mat[turn % C.NO_OF_PLAYER]):
                        C.built = 'City'
                    else:
                        possible_city = 0


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
                team_mat[turn % C.NO_OF_PLAYER].current_points += 1
                team_mat[turn % C.NO_OF_PLAYER].avaliable_city_pieces -= 1
                team_mat[turn % C.NO_OF_PLAYER].avaliable_settlement_pieces += 1

                # Remove Resources
                for _ in range(C.BUILD_CITY_REQ_WHEAT):
                    team_mat[turn % C.NO_OF_PLAYER].resources.remove('Wheat')

                for _ in range(C.BUILD_CITY_REQ_STONE):
                    team_mat[turn % C.NO_OF_PLAYER].resources.remove('Stone')

                C.main_turtle.clear()
                game.board.draw_current_board(team_mat)

            elif C.built == 'Road':

                team_mat[turn % C.NO_OF_PLAYER].avaliable_road_pieces -= 1

                # Remove Resources
                for _ in range(C.BUILD_ROAD_REQ_WOOD):
                    team_mat[turn % C.NO_OF_PLAYER].resources.remove('Wood')

                for _ in range(C.BUILD_ROAD_REQ_BRICK):
                    team_mat[turn % C.NO_OF_PLAYER].resources.remove('Brick')

            C.selecting_type = None

            game.update_stats(turn % C.NO_OF_PLAYER)

        elif C.selecting_type == 'Development Card':

            if C.DEVELOPMENT_CARD_DECK[0] == 'VP':
                team_mat[turn % C.NO_OF_PLAYER].current_points += 1

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

            game.update_stats(turn % C.NO_OF_PLAYER)

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

            if team_mat[turn % C.NO_OF_PLAYER].is_human == 1:
                C.selecting_on_screen = False
                m.announce_text('Select a card to play')

                turtle.onscreenclick(m.card_selection)

                while not C.selecting_on_screen:
                    C.wn.update()

                turtle.onscreenclick(None)
                C.selecting_on_screen = False

            else:
                avaliable_card = []
                if C.knight_check == 1:
                    avaliable_card.append('Knight')
                
                if C.monopoly_check == 1:
                    avaliable_card.append('Monopoly')
                
                if C.road_building_check == 1:
                    avaliable_card.append('Road Building')

                if C.year_of_plenty_check == 1:
                    avaliable_card.append('Year of Plenty')

                if len(avaliable_card) > 0:
                    option_selected = random.randint(0, len(avaliable_card) - 1)

                    C.selecting_type = avaliable_card[option_selected]

                else:
                    C.selecting_type = 'End Turn'

            if C.selecting_type == 'Knight':
                # Move the Robber. Steal 1 resource from the owner of the settlement or city
                # adjacent to the robber's new hex

                C.selecting_on_screen = False
                C.selected_team = team_mat
                C.built = turn

                if team_mat[turn % C.NO_OF_PLAYER].is_human == 1:

                    turtle.onscreenclick(game.robber_switch)

                    while not C.selecting_on_screen:
                        C.wn.update()

                    turtle.onscreenclick(None)
                    C.selecting_on_screen = False

                    team_mat[turn % C.NO_OF_PLAYER].cards.remove('Knight')

                    team_mat[turn % C.NO_OF_PLAYER].played_knights += 1

                    game.update_stats(turn % C.NO_OF_PLAYER)

                else:
                    game.ai_robber(team_mat[turn % C.NO_OF_PLAYER])


            elif C.selecting_type == 'Monopoly':
                # When you play this card, announce 1 type of resource. All other players must
                # give you all of their resources of that type

                a = ['Wood', 'Brick', 'Wheat', 'Sheep', 'Stone']
                for i in range(len(a)):
                    label = [a[i]]
                    #print(label)
                    m.rectangle_shape(-400 + i * 125, 350, 100, 50, 'Selection')
                    m.write_text(label, -400 + i * 125, 320, 100, 125, 10)

                C.selecting_on_screen = False
                m.announce_text('Select a resource to take off all players')
            
                turtle.onscreenclick(m.resource_selection)

                while not C.selecting_on_screen:
                    C.wn.update()

                turtle.onscreenclick(None)
                C.selecting_on_screen = False
                
                if C.selecting_type != 'End Turn':

                    for i in team_mat:

                        # Skip Itself
                        if i == team_mat[turn % C.NO_OF_PLAYER]:
                            continue

                        if C.selecting_type in i.resources:
                            
                            occurrence = i.resources.count(C.selecting_type)
                            
                            # Add to player
                            team_mat[turn % C.NO_OF_PLAYER].resources.extend([C.selecting_type] * occurrence)

                            for _ in range(i.resources.count(C.selecting_type)):
                                i.resources.remove(C.selecting_type)

                    team_mat[turn % C.NO_OF_PLAYER].cards.remove('Monopoly')

                    game.update_stats(turn % C.NO_OF_PLAYER)


            elif C.selecting_type == 'Road Building':
                # Place 2 new roads as if you just built them
                C.selected_team = team_mat[turn % C.NO_OF_PLAYER]

                for i in range(2):
                    C.selecting_on_screen = False

                    if i == 0:
                        text = 'First'
                    elif i == 1:
                        text = 'Second'
                    m.announce_text('Build ' + text + ' Road')
                
                    turtle.onscreenclick(game.unit_at_point)

                    while not C.selecting_on_screen:
                        C.wn.update()

                    turtle.onscreenclick(None)
                    C.selecting_on_screen = False

                    game.update_stats(turn % C.NO_OF_PLAYER)

                if C.selecting_type != 'End Turn':
                    team_mat[turn % C.NO_OF_PLAYER].cards.remove('Road Building')

                    game.update_stats(turn % C.NO_OF_PLAYER)

            elif C.selecting_type == 'Year of Plenty':
                # Take any 2 resources from the bank. Add them to your hand. They can be 2 of
                # the same resouces or 2 different resources

                a = ['Wood', 'Brick', 'Wheat', 'Sheep', 'Stone']
                for i in range(len(a)):
                    label = [a[i]]
                    #print(label)
                    m.rectangle_shape(-400 + i * 125, 350, 100, 50, 'Selection')
                    m.write_text(label, -400 + i * 125, 320, 100, 125, 10)

                for i in range(2):
                    C.selecting_on_screen = False
                    
                    if i == 0:
                        text = 'First'
                    elif i == 1:
                        text = 'Second'

                    m.announce_text('Take ' + text + ' Resource')
                
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

                game.update_stats(turn % C.NO_OF_PLAYER)

            C.selecting_type = None


        elif C.selecting_type == 'Trade':

            a = ['Wood', 'Brick', 'Wheat', 'Sheep', 'Stone']
            for i in range(len(a)):
                label = [a[i]]
                #print(label)
                m.rectangle_shape(-400 + i * 125, 350, 100, 50, 'Selection')
                m.write_text(label, -400 + i * 125, 320, 100, 125, 10)

            if (game_trade_check == 1 or seaport_trade_check == 1):

                m.announce_text('Pick the resource to trade')

                # Select the original trading object
                C.selecting_on_screen = False
            
                turtle.onscreenclick(m.resource_selection)

                while not C.selecting_on_screen:
                    C.wn.update()

                turtle.onscreenclick(None)

                original_resource = C.selecting_type

            # Announce what to do
            m.announce_text('Pick the resource you want')

            C.selecting_on_screen = False
        
            turtle.onscreenclick(m.resource_selection)

            while not C.selecting_on_screen:
                C.wn.update()

            turtle.onscreenclick(None)

            new_resource = C.selecting_type

            if seaport_trade_check != 1 and game_trade_check == 1 and resource_seaport_trade_check == 0:
                number_of_trades = 4

            if seaport_trade_check == 1 and game_trade_check == 1 and resource_seaport_trade_check == 0:
                number_of_trades = 3
            
            if resource_seaport_trade_check == 1:
                number_of_trades = 2
            
            for _ in range(number_of_trades):
                team_mat[turn % C.NO_OF_PLAYER].resources.remove(original_resource)

            team_mat[turn % C.NO_OF_PLAYER].resources.append(new_resource)

            game.update_stats(turn % C.NO_OF_PLAYER)

            # Trade with another player

        # Once selected
        C.selection_turtle.clear()
        C.text_announcer_turtle.clear()

    
    for i in team_mat:
        if i.current_points > win_con:
            win_con = i.current_points
    turn += 1
    C.dice_turtle.clear()
        



for i in team_mat:
    print(i.resources)

print('Ended Game')

C.wn.exitonclick()