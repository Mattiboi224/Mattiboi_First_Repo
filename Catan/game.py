from board import Board
import Config as C
import util as m
from corner import Corner as Co
from road import Road as R
import random
import turtle

class Game:
    def __init__(self, team_mat):
        self.board = Board()
        self.objects = []
        self.team_mat = team_mat

        for i in self.board.road_mat_class:
            self.objects.append(i)

        for i in self.board.corner_mat_class:
            self.objects.append(i)


    def unit_at_point(self, x, y):

        team_class = C.selected_team
        team = team_class.team
        colour = team_class.colour
        #print(colour)

        breaker = 0
        works = 0

        #print(x, y)
        #print(self.objects)

        # End Turn
        if x >= -450 and x <= -450 + 170 and y <= -250 and y >= -250 - 125:
            C.selecting_on_screen = True
            C.selecting_type = 'End Turn'
            return
        

        # Search all the roads and corners
        for u in self.objects:

            if isinstance(u, Co) and C.selecting_type == 'Road':
                continue

            if isinstance(u, R) and (C.selecting_type == 'Settlement' and C.selecting_type == 'City'):
                continue

            if m.dist([x, y], u.pos()) <= u.radius:

                # If the one selected is empty build something
                if u.team is None:

                    #print('Team is None')

                    # Check if it's a valid space i.e. not next to occupied corners
                    if isinstance(u, Co):
                        for i in u.nearby_corners_mat_class:
                            if i.is_occupied == 1:
                                breaker = 1
                                break

                    if isinstance(u, R):
                        # Check for nearby roads and if it's yours you can extend
                        for i in u.nearby_roads_mat_class:

                            if i.is_occupied == 1 and i.team == team:
                                works = 1
                                
                                break
                        
                        # Check for nearby settlements if yours you can continue
                        for i in u.nearby_corners_mat_class:
                            if i.is_occupied == 1 and team == i.team:
                                works = 1
                                break
                        


                    if breaker == 1 and isinstance(u, Co):
                        continue

                    if works == 0 and isinstance(u, R):
                        continue

                    # Add your team to selected object
                    u.team = team
                    u.is_occupied = 1

                    # If it's a corner add a settlement
                    if isinstance(u, Co):
                        u.building = 'Settlement'
                        C.built = 'Settlement'

                    else:
                        C.built = 'Road'
                    
                    u.draw(colour)
                    C.selecting_on_screen = True
                    return
                
                # Upgrade to City
                elif u.team is not None and u.team == team:
                    if isinstance(u, Co):
                        u.building = 'City'

                        C.selecting_on_screen = True

                        C.built = 'City'

                        #print('Passed')
                        return

                    

        print('Invalid Click')
        C.selecting_on_screen = False


    def update_stats(self, curr_team):

        turtle.tracer(False)
                
        original_x = -500
        original_y = 300

        curr_team = self.team_mat[curr_team]

        C.announcer_turtle.clear()

        C.announcer_turtle.color('Black')
        C.announcer_turtle.goto(original_x, original_y)
        C.announcer_turtle.write('Statistics', False, align="left", font=("Arial", 20, "bold"))

        C.announcer_turtle.goto(original_x, original_y - 20)
        C.announcer_turtle.write('Victory Points', False, align="left", font=("Arial", 15, "bold"))

        count = original_y  - 40
        for i in self.team_mat:
            label = str(i.team) + ' = ' + str(i.current_points)

            C.announcer_turtle.color(i.colour)
            C.announcer_turtle.goto(original_x, count)
            C.announcer_turtle.write(label, False, align="left", font=("Arial", 10, "normal"))
            count -= 20

        C.announcer_turtle.color('Black')
        C.announcer_turtle.goto(original_x, original_y - 120)
        C.announcer_turtle.write('Cards in Deck: ' + str(len(C.DEVELOPMENT_CARD_DECK)), False, align="left", font=("Arial", 15, "bold"))


        C.announcer_turtle.color('Black')
        C.announcer_turtle.goto(original_x, original_y - 150)
        C.announcer_turtle.write('Avaliable Pieces', False, align="left", font=("Arial", 15, "bold"))

        C.announcer_turtle.color(curr_team.colour)
        C.announcer_turtle.goto(original_x, original_y - 165)
        C.announcer_turtle.write('Roads: ' + str(curr_team.avaliable_road_pieces), False, align="left", font=("Arial", 10, "normal"))

        C.announcer_turtle.goto(original_x, original_y - 180)
        C.announcer_turtle.write('Settlements: ' + str(curr_team.avaliable_settlement_pieces), False, align="left", font=("Arial", 10, "normal"))

        C.announcer_turtle.goto(original_x, original_y - 195)
        C.announcer_turtle.write('Cities: ' + str(curr_team.avaliable_city_pieces), False, align="left", font=("Arial", 10, "normal"))


        C.announcer_turtle.color('Black')
        C.announcer_turtle.goto(original_x, original_y - 220)
        C.announcer_turtle.write('Resources in Hand: ' + str(len(curr_team.resources)), False, align="left", font=("Arial", 15, "bold"))

        C.announcer_turtle.color(curr_team.colour)
        C.announcer_turtle.goto(original_x, original_y - 235)
        C.announcer_turtle.write('Wood: ' + str(curr_team.resources.count('Wood')), False, align="left", font=("Arial", 10, "normal"))

        C.announcer_turtle.goto(original_x, original_y - 250)
        C.announcer_turtle.write('Brick: ' + str(curr_team.resources.count('Brick')), False, align="left", font=("Arial", 10, "normal"))

        C.announcer_turtle.goto(original_x, original_y - 265)
        C.announcer_turtle.write('Wheat: ' + str(curr_team.resources.count('Wheat')), False, align="left", font=("Arial", 10, "normal"))

        C.announcer_turtle.goto(original_x, original_y - 280)
        C.announcer_turtle.write('Sheep: ' + str(curr_team.resources.count('Sheep')), False, align="left", font=("Arial", 10, "normal"))

        C.announcer_turtle.goto(original_x, original_y - 295)
        C.announcer_turtle.write('Stone: ' + str(curr_team.resources.count('Stone')), False, align="left", font=("Arial", 10, "normal"))



        if len(curr_team.cards) > 0:
            C.announcer_turtle.color('Black')
            C.announcer_turtle.goto(original_x, original_y - 325)
            C.announcer_turtle.write('Cards in Hand', False, align="left", font=("Arial", 15, "bold"))

            C.announcer_turtle.color(curr_team.colour)
            if curr_team.cards.count('Knight') > 0:
                C.announcer_turtle.goto(original_x, original_y - 340)
                C.announcer_turtle.write('Knight: ' + str(curr_team.cards.count('Knight')), False, align="left", font=("Arial", 10, "normal"))

            if curr_team.cards.count('VP') > 0:
                C.announcer_turtle.goto(original_x, original_y - 355)
                C.announcer_turtle.write('VP: ' + str(curr_team.cards.count('VP')), False, align="left", font=("Arial", 10, "normal"))

            if curr_team.cards.count('Monopoly') > 0:
                C.announcer_turtle.goto(original_x, original_y - 370)
                C.announcer_turtle.write('Monopoly: ' + str(curr_team.cards.count('Monopoly')), False, align="left", font=("Arial", 10, "normal"))

            if curr_team.cards.count('Road Building') > 0:
                C.announcer_turtle.goto(original_x, original_y - 385)
                C.announcer_turtle.write('Road Building: ' + str(curr_team.cards.count('Road Building')), False, align="left", font=("Arial", 10, "normal"))

            if curr_team.cards.count('Year of Plenty') > 0:
                C.announcer_turtle.goto(original_x, original_y - 400)
                C.announcer_turtle.write('Year of Plenty: ' + str(curr_team.cards.count('Year of Plenty')), False, align="left", font=("Arial", 10, "normal"))

        turtle.tracer(True)

    def robber_switch(self, x, y):

        team_class = self.team_mat[C.built % C.NO_OF_PLAYER]
        team = team_class.team

        # # Find the current robber and turn it to 0
        # for r in self.board.Tiles_Mat:
        #     if r.is_robber == 1:
        #         r.is_robber = 0
        #         break

        # Search the tiles
        for u in self.board.Tiles_Mat:


            # Find the Tile selected
            if m.dist([x, y], u.pos()) <= u.radius:

                for r in self.board.Tiles_Mat:
                    if r.is_robber == 1:
                        r.is_robber = 0
                        break

                u.is_robber = 1

                r.number = u.number
                u.number = 0

                # Steal Resource

                stealable_teams = []
                for i in u.corner_mat_class:
                    if i.is_occupied == 1 and i.team != team:

                        if i.team not in stealable_teams:
                            stealable_teams.append(i.team)

                stolen = 0

                while len(stealable_teams) != 0:

                    team_to_be_stolen = random.randint(0, len(stealable_teams)-1)

                    #print(team_to_be_stolen)
                    #print(stealable_teams)
                    #print(C.selected_team)

                    # Find the chosen team
                    for i in C.selected_team:
                        
                        #print(stealable_teams)

                        if i.team == stealable_teams[team_to_be_stolen]:

                            #print(i.team)

                            if len(i.resources) > 0:
                                chosen_resource_idx = random.randint(0, len(i.resources) - 1)
                                chosen_resource = i.resources[chosen_resource_idx]
                                
                                # Remove it from player
                                i.resources.pop(chosen_resource_idx)
                                
                                # Give it to other player
                                C.selected_team[C.built % C.NO_OF_PLAYER].resources.append(chosen_resource)

                                stealable_teams.pop(0)
                                stolen = 1
                                break
                                
                            
                            # If they have no resources remove them
                            else:
                                stealable_teams.pop(0)
                    
                    if stolen == 1:
                        break

                # Update Drawing
                C.number_turtle.clear()
                
                for t in self.board.Tiles_Mat:
                    t.draw_number()

                C.selecting_on_screen = True

                return


        print('Invalid Click')
        C.selecting_on_screen = False

    def intial_ai_build(self, TEAM):

        if C.selecting_type == 'Settlement':
            self.ai_find_settlement(TEAM, initial=1)

        elif C.selecting_type == 'Road':
            self.ai_find_road(TEAM)


    def ai_find_settlement(self, TEAM, initial=0):

        colour = TEAM.colour
        team_name = TEAM.team
        if C.selecting_type == 'Settlement':
            if initial == 1:
                while 1 == 1:
                    a = 0
                    corner_selection = random.randint(0, len(self.board.corner_mat_class) - 1)
                    
                    # Remove Occupied Ones
                    if self.board.corner_mat_class[corner_selection].is_occupied == 1:
                        continue
                    
                    occupied_corners = []

                    # Remove Corners next to a current spot
                    for i in self.board.corner_mat_class:
                        if i.is_occupied == 1:
                            if self.board.corner_mat_class[corner_selection] in i.nearby_corners_mat_class:
                                a = 1
                            for j in i.nearby_corners_mat_class:
                                occupied_corners.append(j)
                            
                    # Valid
                    if a == 0:
                        break

                self.board.corner_mat_class[corner_selection].is_occupied = 1
                self.board.corner_mat_class[corner_selection].team = team_name
                self.board.corner_mat_class[corner_selection].building = 'Settlement'
                self.board.corner_mat_class[corner_selection].draw(colour)

                return

            elif initial == 0:

                occupied_corners = []
                available_corners = []

                # Remove Corners next to a current spot
                for i in self.board.corner_mat_class:
                    if i.is_occupied == 1:
                        for j in i.nearby_corners_mat_class:
                            occupied_corners.append(j)

                # Search all the roads
                for i in self.board.road_mat_class:
                    # Find the ones you own
                    if i.is_occupied == 1 and i.team == team_name:

                        # If either end if occupied Skip
                        if i.nearby_corners_mat_class[0].is_occupied == 1 or i.nearby_corners_mat_class[1].is_occupied == 1:
                            pass
                        else:
                            if i.nearby_corner_mat_class[0] not in occupied_corners and \
                                i.nearby_corner_mat_class[0] not in available_corners:
                                available_corners.append(i.nearby_corner_mat_class[0])
                            if i.nearby_corner_mat_class[1] not in occupied_corners and \
                                i.nearby_corner_mat_class[1] not in available_corners:
                                available_corners.append(i.nearby_corner_mat_class[1])
                        
                if len(available_corners) > 0:
                    corner_selection = random.randint(0, len(available_corners)-1)
                    self.board.corner_mat_class[corner_selection].is_occupied = 1
                    self.board.corner_mat_class[corner_selection].team = team_name
                    self.board.corner_mat_class[corner_selection].building = 'Settlement'
                    self.board.corner_mat_class[corner_selection].draw(colour)

                    return True

                else:
                    return False 

    def ai_find_road(self, TEAM):
        
        colour = TEAM.colour
        team_name = TEAM.team 
        if C.selecting_type == 'Road':

            # Find Roads around current spot
            avaliable_roads = []
            for i in self.board.corner_mat_class:
                if i.is_occupied == 1 and i.team == team_name:
                    for j in i.nearby_roads_mat:
                        if j not in avaliable_roads:
                            avaliable_roads.append(j)

            for i in self.board.road_mat_class:
                if i.is_occupied == 1 and i.team == team_name:
                    for j in i.nearby_road_mat_class:
                        if [j.p1, j.p2] not in avaliable_roads and [j.p2, j.p1] not in avaliable_roads:
                            avaliable_roads.append([j.p1, j.p2])

            if len(avaliable_roads) > 0:
                road_selection = random.randint(0, len(avaliable_roads) - 1)

                for i in self.board.road_mat_class:
                    if i.p1 == avaliable_roads[road_selection][0] and i.p2 == avaliable_roads[road_selection][1] or \
                        i.p2 == avaliable_roads[road_selection][0] and i.p1 == avaliable_roads[road_selection][1]:
                        
                        i.occupied = 1
                        i.team = team_name
                        i.draw(colour)
                        return True
            else:
                return False


    def ai_robber(self, TEAM):

        team = TEAM.team

        chosen_tile = random.randint(0, len(self.board.Tiles_Mat)-1)
        
        # Search the tiles
        u = self.board.Tiles_Mat[chosen_tile]

        for r in self.board.Tiles_Mat:
            if r.is_robber == 1:
                r.is_robber = 0
                break

        u.is_robber = 1

        r.number = u.number
        u.number = 0

        # Steal Resource

        stealable_teams = []
        for i in u.corner_mat_class:
            if i.is_occupied == 1 and i.team != team:

                if i.team not in stealable_teams:
                    stealable_teams.append(i.team)

        stolen = 0

        while len(stealable_teams) != 0:

            team_to_be_stolen = random.randint(0, len(stealable_teams)-1)

            #print(team_to_be_stolen)
            #print(stealable_teams)
            #print(C.selected_team)

            # Find the chosen team
            for i in C.selected_team:
                
                #print(stealable_teams)

                if i.team == stealable_teams[team_to_be_stolen]:

                    #print(i.team)

                    if len(i.resources) > 0:
                        chosen_resource_idx = random.randint(0, len(i.resources) - 1)
                        chosen_resource = i.resources[chosen_resource_idx]
                        
                        # Remove it from player
                        i.resources.pop(chosen_resource_idx)
                        
                        # Give it to other player
                        C.selected_team[C.built % C.NO_OF_PLAYER].resources.append(chosen_resource)

                        stealable_teams.pop(0)
                        stolen = 1
                        break
                        
                    
                    # If they have no resources remove them
                    else:
                        stealable_teams.pop(0)
            
            if stolen == 1:
                break

        # Update Drawing
        C.number_turtle.clear()
        
        for t in self.board.Tiles_Mat:
            t.draw_number()

        C.selecting_on_screen = True

    def ai_build_city(self, TEAM):

        team_class = TEAM
        team = team_class.team
        
        # Find all the options
        avaliable_buildings = []
        for i in self.board.corner_mat_class:
            if i.is_occupied == 1 and i.team == team and i.building == 'Settlement':
                avaliable_buildings.append(i)
        
        if len(avaliable_buildings) == 0:
            return False

        else:
            choice = random.randint(0, len(avaliable_buildings)- 1)
            avaliable_buildings[choice].building = 'City'
            C.built = 'City'

        return True