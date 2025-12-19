# Let's create a complete, runnable Pygame prototype for a grid-based base-building RTS with selection,
# simple AI opponents, map editing, and basic building/unit behaviors.

import os, textwrap, json, math, random, sys, time

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
                    if game.build_mode:
                        game.build_mode = False
                    else:
                        for u in game.selected_units: u.selected = False
                        game.selected_units.clear()

                elif event.key == pygame.K_F1:
                    game.help_on = not game.help_on

                elif event.key == pygame.K_m:
                    game.map_edit = not game.map_edit

                elif event.key == pygame.K_LEFTBRACKET:
                    game.paint_tile = C.T_WALL
                elif event.key == pygame.K_RIGHTBRACKET:
                    game.paint_tile = C.T_RESOURCE

                elif event.key == pygame.K_b:
                    # enter build mode (Barracks)
                    if game.money[C.PLAYER_TEAM] >= C.COST_BARRACKS:
                        game.build_mode = True
                        game.build_kind = "barracks"

                elif event.key == pygame.K_w:
                    # enter build mode (Warfactory)
                    if game.money[C.PLAYER_TEAM] >= C.COST_TANK_FACTORY:
                        game.build_mode = True
                        game.build_kind = "tank_factory"

                elif event.key == pygame.K_u:
                    # queue a worker at player's base
                    base = game.player_base
                    if base and game.money[C.PLAYER_TEAM] >= C.COST_WORKER:
                        base.queue.append("worker")
                        if len(base.queue) == 1:
                            base.queue_time = C.BUILD_WORKER_TIME
                        game.money[C.PLAYER_TEAM] -= C.COST_WORKER

                elif event.key == pygame.K_s:
                    # queue a soldier at any selected barracks
                    selected_barracks = [b for b in game.buildings if b.team==C.PLAYER_TEAM and b.kind=="barracks"
                                         and pygame.Rect(0,0,C.TILE,C.TILE).inflate(0,0)]
                    # if player selected a barracks, use that; otherwise first barracks
                    # (for simplicity here we'll just use the first owned barracks)
                    own_barracks = [b for b in game.buildings if b.team==C.PLAYER_TEAM and b.kind=="barracks"]
                    if own_barracks and game.money[C.PLAYER_TEAM] >= C.COST_SOLDIER:
                        bb = own_barracks[0]
                        bb.queue.append("soldier")
                        if len(bb.queue) == 1:
                            bb.queue_time = C.BUILD_SOLDIER_TIME
                        game.money[C.PLAYER_TEAM] -= C.COST_SOLDIER

                elif event.key == pygame.K_t:
                    # queue a tank at any selected warfactory
                    selected_tank_factory = [b for b in game.buildings if b.team==C.PLAYER_TEAM and b.kind=="tank_factory"
                                         and pygame.Rect(0,0,C.TILE,C.TILE).inflate(0,0)]
                    # if player selected a tank factory, use that; otherwise first tank factory
                    # (for simplicity here we'll just use the first owned tank factory)
                    own_tank_factory = [b for b in game.buildings if b.team==C.PLAYER_TEAM and b.kind=="tank_factory"]
                    if own_tank_factory and game.money[C.PLAYER_TEAM] >= C.COST_TANK:
                        bb = own_tank_factory[0]
                        bb.queue.append("tank")
                        if len(bb.queue) == 1:
                            bb.queue_time = C.BUILD_TANK_TIME
                        game.money[C.PLAYER_TEAM] -= C.COST_TANK

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left
                    if game.build_mode and game.build_kind == "barracks":
                        # attempt to place building
                        if game.ghost_valid and game.money[C.PLAYER_TEAM] >= C.COST_BARRACKS:
                            px, py = game.ghost_pos
                            game.spawn_building(C.PLAYER_TEAM, px, py, C.BARRACKS_IMAGE, "barracks")
                            game.money[C.PLAYER_TEAM] -= C.COST_BARRACKS
                            game.build_mode = False
                    elif game.build_mode and game.build_kind == "tank_factory":
                        # attempt to place building
                        if game.ghost_valid and game.money[C.PLAYER_TEAM] >= C.COST_TANK_FACTORY:
                            px, py = game.ghost_pos
                            game.spawn_building(C.PLAYER_TEAM, px, py, C.TANK_FACTORY_IMAGE, "tank_factory")
                            game.money[C.PLAYER_TEAM] -= C.COST_TANK_FACTORY
                            game.build_mode = False
                    elif game.map_edit:
                        tx, ty = UT.to_grid(event.pos)
                        # paint chosen tile (or grass with middle click, but here: toggle between selected and grass with shift)
                        if UT.in_bounds(tx, ty):
                            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                                game.grid.toggle_at(tx, ty, C.T_GRASS)
                            else:
                                game.grid.toggle_at(tx, ty, game.paint_tile)
                    else:
                        # print("starting sel")
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
                                u.target = enemy
                        else:
                            tx, ty = UT.to_grid(event.pos)
                            #print(tx)
                            #print(ty)
                            if UT.in_bounds(tx, ty) and (game.grid.tiles[ty][tx] == C.T_RESOURCE or game.grid.tiles[ty][tx] == C.T_GEMS):
                                                         #and game.selected_units.kind == "worker"):
                                game.order_harvest(game.selected_units, (tx, ty))
                                #print("harvesting")
                            else:
                                game.order_move(game.selected_units, event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and game.select_start:

                    #print("selection ava")
                    # finalize selection
                    if not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                        # clear previous unless holding shift
                        for u in game.selected_units: u.selected = False
                        game.selected_units.clear()
                    rect = game.selection_rect
                    #if rect.width < 5 and rect.height < 5:
                    # treat as click selection
                    u = game.unit_at_point(event.pos, team=C.PLAYER_TEAM)
                    if u:
                        u.selected = True
                        if u not in game.selected_units:
                            game.selected_units.append(u)
                            #print("found unit")
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


            elif event.type == pygame.MOUSEMOTION:
                if game.selection_rect and game.select_start:
                    x0, y0 = game.select_start
                    x1, y1 = event.pos
                    x = min(x0, x1)
                    y = min(y0, y1)
                    w = abs(x1 - x0)
                    h = abs(y1 - y0)
                    game.selection_rect = pygame.Rect(x, y, w, h)

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
