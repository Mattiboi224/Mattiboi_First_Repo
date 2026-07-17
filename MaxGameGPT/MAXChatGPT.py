# Improvements

# Make it turn based
    # Convert speed to tiles rather than pixels per second
    # Add shots in so 
# Proper Side Menu
    # Stats
    # Mini Map
    # Buttons: Range, Scan
# Remove the option box on the right hand side
# Create a light constructor unit
# Create a screen for construction with unit stats
    # Note this pauses the screen
# Make losing ammo mean finding ammo trucks to resupply
# Change some buildings to 2x2 or 3x3
# Add base defence turrets
# Upgrade AI
# Add more units
# Add Radar/Fog of war
# Add starting units
# Add Amphib units
# Create Buildings you can pass through/under





import os, textwrap, json, math, random, sys, time
import util as m

##code = r'''# grid_rts.py
# A minimal grid-based base-building game prototype in Pygame
#
# Features:
# - Grid map you can edit (toggle terrain/resources) in Map Edit mode (press M)
# - Mouse selection box to select/deselect your units
# - Right-click to move selected units; they'll auto-attack enemies in range
# - Simple base-building: press B to place a building (Barracks), U to train a unit (Worker) at your Base
# - Resources: Workers can harvest resource tiles (right-click resource tile) for money
# - Multiple AIs (tweak NUM_AI) that spawn soldiers and attack you
#
# Controls (Player is Team 0 - blue):
#   Left drag            : selection box (select your units)
#   Left click           : select a single unit / place building (when in build mode)
#   Right click          : move/attack/harvest context command for selected units
#   M                    : toggle Map Edit mode
#   [ / ]                : in Map Edit mode, choose paint tile type (Grass/Wall/Resource)
#   B                    : enter Building Placement mode (Barracks, cost 75) - press ESC to cancel
#   U                    : queue a Worker from your Base (cost 50)
#   S                    : queue a Soldier from a selected Barracks (cost 60)
#   ESC                  : clear selection / cancel building placement
#   F1                   : quick help overlay toggle
#
# Notes:
# - This is a prototype meant for learning and extension. Feel free to tweak constants below.
# - Requires: pygame 2.x
#
# Run: python grid_rts.py

import pygame
import math
import random
import Config as C
import util as UT
from entity import Entity
from units import Unit
from building import Building
from game import Game


# ------------------ MAIN LOOP ------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT+28))
    pygame.display.set_caption("Grid RTS Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    game = Game()

    def queue_unit(game, kind):
        stats = C.ENTITY_STATS[kind]
        cost = stats["cost"]
        building_kind = stats["builds_from"]
        unit_name = stats["Name"]
        build_time = stats["build_time"]

        # find owned buildings of the correct type
        buildings = [b for b in game.buildings
                    if b.team == C.PLAYER_TEAM and b.kind == building_kind]

        if buildings and game.player_mat[C.PLAYER_TEAM].money >= cost:
            bb = buildings[0]
            bb.queue.append(unit_name)
            if len(bb.queue) == 1:
                bb.queue_time = build_time
            game.player_mat[C.PLAYER_TEAM].money -= cost

    running = True
    while running:
        dt = clock.tick(C.FPS) / 1000.0

        # ------------- INPUT -------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # cancel build mode or clear selection
                    if game.build_mode or game.sell_mode:
                        game.build_mode = False
                        game.sell_mode = False
                    else:
                        for u in game.selected_units: u.selected = False
                        game.selected_units.clear()
                        
                elif event.key == pygame.K_F1:
                    game.help_on = not game.help_on

                elif event.key == pygame.K_m:
                    game.map_edit = not game.map_edit

                elif event.key == pygame.K_r:
                    game.resource_mode = not game.resource_mode

                elif event.key == pygame.K_LEFTBRACKET:
                    game.paint_tile = C.T_WALL
                elif event.key == pygame.K_RIGHTBRACKET:
                    game.paint_tile = C.T_RESOURCE

                elif event.key == pygame.K_b:
                    # enter build mode (Barracks)
                    if game.player_mat[C.PLAYER_TEAM].money >= C.COST_BARRACKS:
                        game.build_mode = True
                        game.build_name = "Barracks"

                elif event.key == pygame.K_c:
                    # enter build mode (Barracks)
                    if game.player_mat[C.PLAYER_TEAM].money >= C.COST_BASE:
                        game.build_mode = True
                        game.build_name = "Base"

                elif event.key == pygame.K_w:
                    # enter build mode (Warfactory)
                    if game.player_mat[C.PLAYER_TEAM].money >= C.COST_TANK_FACTORY:
                        game.build_mode = True
                        game.build_name = "Tank Factory"

                elif event.key == pygame.K_s:
                    queue_unit(game, "Soldier")

                elif event.key == pygame.K_t:
                    queue_unit(game, "Tank")

                elif event.key == pygame.K_a:
                    queue_unit(game, "Ammo Truck")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left

                    for label, rect in game.menu.options_buttons:
                        if not rect.collidepoint(event.pos):
                            continue

                        if rect.collidepoint(event.pos):

                            if label == 'Pause':
                                pass

                            elif label == 'Save':
                                game.save_game("save_game01.json")
                                print("Gave Saved")

                            elif label == 'Load':
                                game.load_game("save_game01.json")
                                print("Game Loaded")

                            elif label == 'Exit':
                                running = False

                    for label, rect in game.menu.buttons: 
                        if not rect.collidepoint(event.pos):
                            continue 
                        
                        if rect.collidepoint(event.pos):

                            if label == "Sell":
                                game.sell_mode = True
                                game.repair_mode = False

                            elif label == "Repair":
                                game.repair_mode = True
                                game.sell_mode = False

                            elif label in C.ENTITY_STATS:
                                stats = C.ENTITY_STATS[label]
                                cost = stats.get("cost")

                                if stats["category"] == "building":
                                    if cost is not None and game.player_mat[C.PLAYER_TEAM].money >= cost:
                                        game.build_mode = True
                                        game.build_name = stats["Name"]

                                elif stats["category"] == "unit":
                                    queue_unit(game, label)


                    # Sell the Building
                    if game.building_at_point(event.pos, team=C.PLAYER_TEAM) is not None and game.sell_mode:
                        b_at_point = game.building_at_point(event.pos, team=C.PLAYER_TEAM)
                        
                        b_at_point.sold = True
                        b_at_point.Tile.occupied = False
                        
                        for name, stats in C.ENTITY_STATS.items():
                            if stats["kind"] == b_at_point.kind:
                                game.player_mat[C.PLAYER_TEAM].money += (stats["cost"] * C.SELL_PERCENTAGE)

                        game.sell_mode = False
                        game.ghost_valid = False

                    # Repair the building
                    elif game.building_at_point(event.pos, team=C.PLAYER_TEAM) is not None and game.repair_mode:
                        b_at_point = game.building_at_point(event.pos, team=C.PLAYER_TEAM)
                            
                        # If missing health
                        if b_at_point.hp < b_at_point.max_hp and game.player_mat[C.PLAYER_TEAM].money > 0:
                            hp_diff = b_at_point.max_hp - b_at_point.hp
                            hp_diff = hp_diff // 2
                            game.player_mat[C.PLAYER_TEAM].money -= hp_diff
                            b_at_point.hp = b_at_point.max_hp
                            
                        game.repair_mode = False
                        game.ghost_valid = False

                    elif game.move_mode:
                        # Move selected units to clicked position
                        tx, ty = UT.to_grid(event.pos)
                        tx -= C.UNIT_MENU_WIDTH // C.TILE
                        game.order_move_grid(game.selected_units, (tx, ty))
                        game.move_mode = False

                    elif game.attack_mode:
                        enemy = game.unit_at_point(event.pos, team=None)
                        if enemy is None:
                            enemy = game.building_at_point(event.pos, team=None)
                            
                        if enemy is not None and enemy.team != C.PLAYER_TEAM:

                            dist = math.inf
                            chosen_point = None

                            for u in game.selected_units:
                                u.target = enemy
                                ava_locs = m.locations_in_range(u.range, enemy)

                                for i in ava_locs:
                                    # If Filled Skip
                                    if i in game.unit_locs:
                                        continue

                                    dist_between = math.dist(i, u.pos_grid())

                                    if dist_between < dist:
                                        dist = dist_between
                                        chosen_point = i

                                game.order_move_grid(game.selected_units, chosen_point)

                                game.attack_mode = False
                        
                        else:
                            game.attack_mode = False

                    elif game.transfer_mode:
                        for u in game.selected_units:
                            if isinstance(u, Unit) and u.carry > 0:

                                if game.unit_at_point(event.pos, team=None) is not None:
                                    target_unit = game.unit_at_point(event.pos, team=None)
                                    if target_unit.team == C.PLAYER_TEAM and target_unit.transfer_unit:
                                        # Transfer resources to the desired_unit with carry
                                        target_unit.carry = min(target_unit.carry_max, target_unit.carry + u.carry)
                                        u.carry = 0
                                        game.transfer_mode = False
                                    elif target_unit.team == C.PLAYER_TEAM and target_unit.ammo < target_unit.max_ammo:
                                        # Transfer resources to the unit
                                        transfer_amount = min(u.carry, target_unit.max_ammo - target_unit.ammo)
                                        target_unit.ammo += transfer_amount
                                        u.carry -= transfer_amount
                                        game.transfer_mode = False
                                    else:
                                        game.transfer_mode = False
                                
                                elif game.building_at_point(event.pos, team=None) is not None:
                                    target_building = game.building_at_point(event.pos, team=None)
                                    if target_building.team == C.PLAYER_TEAM and target_building.storage:
                                        # Transfer resources to the building
                                        #target_building.resources += u.carry
                                        game.player_mat[C.PLAYER_TEAM].money += u.carry
                                        u.carry = 0
                                        game.transfer_mode = False
                                    else:
                                        game.transfer_mode = False
                                
                                else:
                                    game.transfer_mode = False

                            if isinstance(u, Building) and u.storage and game.player_mat[C.PLAYER_TEAM].money > 0:
                                # Transfer resources to nearest unit
                                if game.unit_at_point(event.pos, team=None) is not None:
                                    target_unit = game.unit_at_point(event.pos, team=None)
                                    if target_unit.team == C.PLAYER_TEAM and target_unit.kind == "ammo_truck":
                                        # Transfer resources to the ammo truck
                                        target_unit.carry = min(target_unit.carry_max, target_unit.carry + game.player_mat[C.PLAYER_TEAM].money)
                                        u.carry = 0
                                        game.transfer_mode = False
                                    else:
                                        game.transfer_mode = False
                                else:
                                    game.transfer_mode = False

                    elif game.selected_units and not game.build_mode and not game.sell_mode and not game.repair_mode:
                        for label, rect in game.selected_units[0].local_buttons:
                            if rect.collidepoint(event.pos):
                                if label == "Move":
                                    game.move_mode = True
                                    break

                                elif label == "Attack":
                                    game.attack_mode = True
                                    break

                                elif label == "Stop":
                                    for u in game.selected_units:
                                        u.selected = False
                                    game.selected_units.clear()
                                    break

                                elif label == "Build":
                                    for u in game.selected_units:
                                        u.target = None
                                        u.path = []
                                        u.path_px = []
                                    print("Build")
                                    break

                                elif label == "X-fer":
                                    game.transfer_mode = True
                                    break
                            
                        else:
                            game.select_start = event.pos
                    
                    elif game.build_mode and game.build_name in C.ENTITY_STATS:
                        
                        cost = C.ENTITY_STATS[game.build_name]["cost"]

                        # attempt to place building
                        if game.ghost_valid and game.player_mat[C.PLAYER_TEAM].money >= cost:
                            px, py = game.ghost_pos
                            game.spawn_building(C.PLAYER_TEAM, px, py, game.build_name)
                            game.player_mat[C.PLAYER_TEAM].money -= cost
                            game.build_mode = False
                            game.ghost_valid = False


                    elif game.map_edit:
                        tx, ty = UT.to_grid(event.pos)
                        # paint chosen tile (or grass with middle click, but here: toggle between selected and grass with shift)
                        if UT.in_bounds(tx, ty):
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                game.grid.toggle_at(tx, ty, C.T_GRASS)
                            else:
                                game.grid.toggle_at(tx, ty, game.paint_tile)
                    else:
                        # begin selection
                        game.select_start = event.pos
                        #game.selection_rect = pygame.Rect(event.pos, (0,0))

                elif event.button == 3:  # right
                    if game.map_edit:
                        # right click sets grass
                        tx, ty = UT.to_grid(event.pos)
                        
                        if UT.in_bounds(tx, ty):
                            game.grid.toggle_at(tx, ty, C.T_GRASS)
                    else:
                        # context command: attack/move/harvest
                        # priority: if clicked enemy => attack; if resource tile => harvest; else move
                        enemy = game.unit_at_point(event.pos, team=None)
                        if enemy and enemy.team != C.PLAYER_TEAM:
                            for u in game.selected_units:
                                if u.attacking_unit:
                                    u.target = enemy
                        else:
                            tx, ty = UT.to_grid(event.pos)
                            tx -= C.UNIT_MENU_WIDTH // C.TILE
                            game.order_move_grid(game.selected_units, (tx, ty))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and game.select_start:

                    # finalize selection
                    if not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                        # clear previous unless holding shift
                        for u in game.selected_units: u.selected = False
                        game.selected_units.clear()
                    rect = game.selection_rect
                    #if rect.width < 5 and rect.height < 5:
                    # treat as click selection
                    u = game.unit_at_point(event.pos, team=C.PLAYER_TEAM)
                    b = game.building_at_point(event.pos, team=C.PLAYER_TEAM)
                    if u:
                        u.selected = True
                        if u not in game.selected_units:
                            game.selected_units.append(u)
                    elif b:
                        b.selected = True
                        if b not in game.selected_units:
                            game.selected_units.append(b)
                    else:
                        # clicked empty space: clear selection (if not shift)
                        if not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                            for u in game.selected_units: u.selected = False
                            game.selected_units.clear()
                    '''
                    ##else:
                        # box selection
                        for u in game.units:
                            if u.team != PLAYER_TEAM or u.dead: continue
                            if rect.collidepoint(u.x, u.y):
                                u.selected = True
                                if u not in game.selected_units:
                                    game.selected_units.append(u)

                                    '''
                    game.selection_rect = None
                    game.select_start = None


            # elif event.type == pygame.MOUSEMOTION:
            #     if game.selection_rect and game.select_start:
            #         x0, y0 = game.select_start
            #         x1, y1 = event.pos
            #         x = min(x0, x1)
            #         y = min(y0, y1)
            #         w = abs(x1 - x0)
            #         h = abs(y1 - y0)
            #         game.selection_rect = pygame.Rect(x, y, w, h)

        # Get pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.camera_x = max(game.camera_x - game.camera_speed, 0)
        if keys[pygame.K_RIGHT]:
            game.camera_x = min(game.camera_x + game.camera_speed, C.MAP_WIDTH * C.TILE - C.SCREEN_WIDTH)
        if keys[pygame.K_UP]:
            game.camera_y = max(game.camera_y - game.camera_speed, 0)
        if keys[pygame.K_DOWN]:
            game.camera_y = min(game.camera_y + game.camera_speed, game.grid.h * C.TILE - C.HEIGHT)

        # ------------- UPDATE -------------
        game.update(dt)

        # ------------- DRAW -------------
        screen.fill((30, 30, 30))
        game.draw(screen, font)
        pygame.display.flip()

        # End Game conditions

        final_teams = []
        for b in game.buildings:
            if not b.dead and not b.sold:
                final_teams.append(b.team)
        
        unique_final_teams = list(set(final_teams))

        if len(unique_final_teams) == 1 or C.PLAYER_TEAM not in unique_final_teams:
            running = False
            print("Game Over")

            b_built = 0
            b_lost = 0
            b_destroyed = 0

            u_built = 0
            u_lost = 0
            u_destroyed = 0

            eb_built = 0
            eu_built = 0
            

            for b in game.total_buildings:
                if b.team == 0: # If Player Buildings
                    b_built += 1
                    if b.dead == True:
                        b_lost += 1
                else:
                    if b.dead == True or b.sold == True:
                        b_destroyed += 1
                    eb_built += 1
                    
            for u in game.total_units:
                if u.team == 0: # If Player Units
                    u_built += 1
                    if u.dead == True:
                        u_lost += 1
                else:
                    if u.dead == True:
                        u_destroyed += 1
                    eu_built += 1

            print('End Game Stats')
            print('Buildings Built: ', b_built)
            print('Buildings Lost: ', b_lost)
            print('Buildings Destroyed: ', b_destroyed)
            print('Units Built: ', u_built)
            print('Units Lost: ', u_lost)
            print('Units Destroyed: ', u_destroyed)
            print('Enemy Buildings Built: ', eb_built)
            print('Enemy Units Built: ', eu_built)

    

    pygame.quit()

if __name__ == "__main__":
    main()
