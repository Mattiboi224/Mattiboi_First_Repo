import math
import random
from turtle import *
## Set Up Turtles
screen = Screen()

writer = Turtle()
writer.hideturtle()
writer.up()

updater = Turtle()
updater.hideturtle()
updater.up()

player_map = Turtle()
player_map.up()
player_map.shape("square")
player_map.hideturtle()

player1 = Turtle()
player1.up()
player1.shape("square")
player1.hideturtle()

player2 = Turtle()
player2.up()
player2.shape("circle")
player2.hideturtle()

player_updater = Turtle()
player_updater.hideturtle()
player_updater.up()

monster_updater = Turtle()
monster_updater.hideturtle()
monster_updater.up()

announcer = Turtle()
announcer.hideturtle()

display = Turtle()
display.up()
display.hideturtle()

boxturtle = Turtle()
boxturtle.up()
boxturtle.hideturtle()

protectionturtle = Turtle()
protectionturtle.up()
protectionturtle.hideturtle()

title('Tic Tac Toe Fighter')

#map_movement_counter = 0

def main():
    counter = 0
    locations = []
    player_health_list = []
    boss = 0
#    player1movement()
#    player2movement()
    ## Starting Conditions
    [battle_count, player_level,  player_bonus, current_exp, remaining_exp,
        starting_remaining_exp, starting_player_health, player_health,
        monster_level, monster_health,
        starting_monster_health, armour, boss, health_pot, item_count] = starting_conditions()
    protection = 0
    boss_count = 0
    bonus_weapon = 0
    boss_chance_redo = 0
    announcer.up()
    announcer.home()
    announcer.write("Game Start", False, align="center", font=("Arial", 15, "normal"))
    displayturtle()
    
    # Adding Handicap
    handicap_counter = 0
    handicap_counter_q2 = 0
    while handicap_counter != 1:
        handicap_q = textinput("Would You Like A Handicap?", "Answer Y or N")
        if handicap_q == "Y":
            while handicap_counter_q2 != 1:
                handicap_q2 = textinput("How Much?", "Pick a Number Greater than 0")
                handicap_q2 = int(handicap_q2)
                if handicap_q2 > 0:
                    handicap = handicap_q2
                    handicap_counter_q2 = 1
                    handicap_counter = 1
        elif handicap_q == "N":
            handicap = 1
            handicap_counter = 1
    
    clearturtle()
    
    # Setup Grid
    [size_of_screen, map_square_size] = setupmapscreen()
    
    # Place X's and O's
    [counter, locations] = placexs(counter, locations, player_health_list, map_square_size)            
    
    games_played = 0
    dead_counter = 0
    while games_played <= 24:
        games_played = games_played + 1
        
        # Move Around the Map
        locations = mapmovement(size_of_screen, map_square_size, locations, player_health_list)           
        
        # Clear the Map
        clearturtle()
        
        # Check if passed the first battle
        if games_played >= 2:
            
            # Reset Boss and Test for Random Boss 
            [boss, boss_chance_redo] = boss_chance_method(boss, boss_chance_redo)
            
            # If dead reset everyone
            if player_health <= 0:
                [battle_count, player_level,  player_bonus, current_exp, remaining_exp,
                    starting_remaining_exp, starting_player_health, player_health,
                    monster_level, monster_health,
                    starting_monster_health, armour, boss, health_pot, item_count] = starting_conditions()
                dead_counter = 1
                monster_level -= 1
                starting_monster_health -= 5
            
            # Check if Going to win and change to winning boss
            [boss, boss_chance_redo] = superboss(boss, locations, map_square_size, player_health_list, dead_counter, boss_chance_redo)

            # Give the boss characteristics
            [boss, starting_monster_health, monster_level, monster_health] = boss_characteristics(boss,
                                                starting_monster_health, monster_level, monster_health)
        
        if locations.count(locations[-1]) > 1:
            player_index = locations.index(locations[-1])
            #Player and Monster Alive Play the Square
            if player_health > 0 and player_health_list[player_index][1] > 0: 
                monster_health = player_health_list[player_index][1]
                starting_monster_health = player_health_list[player_index][2]
                monster_level = player_health_list[player_index][3]
                boss = player_health_list[player_index][4]
            
            ## If Saved the Game reset the stats
            #if monster_health >= 0 and player_health > 0:
            #    if boss == 1:
            #        monster_level -= 7
            #        starting_monster_health -= 7                            
            #    if boss == 2 or boss == 3:
            #        monster_level -= 14
            #        starting_monster_health -= 14  
        
        #Setup the Screen
        setupbattlescreen(battle_count, player_level,  player_bonus, armour, remaining_exp,
                    starting_remaining_exp, starting_player_health, player_health,
                    monster_level, monster_health, starting_monster_health, protection)
        
        # Play the Game
        [boss, battle_count, player_level, player_bonus, armour, current_exp, remaining_exp, 
        starting_remaining_exp, starting_player_health, player_health, 
        monster_level, monster_health, starting_monster_health, health_pot, item_count, protection, boss_count, bonus_weapon] = play_game(boss, battle_count, 
                        player_level, player_bonus, armour, current_exp, remaining_exp, 
                          starting_remaining_exp, starting_player_health, player_health, 
                          monster_level, monster_health, starting_monster_health, health_pot, item_count, protection, boss_count, bonus_weapon)

        dead_counter = 0
        
        # Append Health to a list
        player_health_list.append([player_health, monster_health, starting_monster_health, monster_level, boss])
        
        #Saved Game Reset Back to before save
        if player_health > 0 and monster_health > 0:
            if boss == 1:
                monster_level -= 7
                starting_monster_health -= 7                            
            if boss == 2 or boss == 3:
                monster_level -= 14
                starting_monster_health -= 14          
        
        # Clear Screen
        clearturtle()

        # Setup Grid
        [size_of_screen, map_square_size] = setupmapscreen()
        
        # Place X's and O's
        [counter, locations] = placexs(counter, locations, player_health_list, map_square_size)
        
#        # Check if won!
#        if len(locations) >= 3:
            
        
        
    screen.mainloop()



def play_game(boss, battle_count, player_level, player_bonus, armour, \
            current_exp, remaining_exp, starting_remaining_exp, \
            starting_player_health, player_health, monster_level, monster_health, \
            starting_monster_health, health_pot, item_count, protection, boss_count, bonus_weapon):
    player1.showturtle()
    player2.showturtle()
    player1.setposition(-200, -200)
    player2.setposition(200,-200)
    
    # Saying Oh No Boss!
    if boss == 2 or boss == 3:
        announcer.undo()
        announcer.home()
        announcer.write("""HOW DARE YOU TRY 
        AND DEFEAT ME!!!!""", False, align="center", font=("Arial", 40, "normal"))
        displayturtle()    
    
    elif boss == 1:
        announcer.undo()
        announcer.home()
        announcer.write('Oh no boss!', False, align="center", font=("Arial", 15, "normal"))
        displayturtle()

    attack_boxes()
    
    miss_counter = 0
    attack_count = 0
    bonus_damage_weapon = 0
    protection_drawing = 0
    while monster_health > 0:
        
        if player_health > 0:
            rand_monster = random.random()
            announcer.undo()
            announcer.home()
            announcer.write('New Battle! Battle No.' + str(battle_count), False, align="center", font=("Arial", 15, "normal"))

            # If Only Boss Reload
            
            
            # Ask if want to save
            if boss in [1, 2, 3]:
                save_counter = 0
                while save_counter != 1:
                    save_usage = textinput("Run and Fight another battle?", "Would you like to run? Y/N")
                    if save_usage == "Y":
                        return boss, battle_count, player_level, player_bonus, armour, \
                        current_exp, remaining_exp, starting_remaining_exp, \
                        starting_player_health, player_health, monster_level, \
                        monster_health, starting_monster_health, health_pot, \
                        item_count, protection, boss_count, bonus_weapon
                    elif save_usage == "N":
                        break

            # Using Health Pot
            health_pot_counter = 0
            if player_health < starting_player_health:
                if health_pot > 0:
                    while health_pot_counter != 1:
                        health_pot_usage = textinput("Use Health Pot", "Would you like to use a health pot? Y/N")
                        if health_pot_usage == "Y":
                            health_pot -= 1
                            player_health = starting_player_health
                            break
                        elif health_pot_usage == "N":
                            break
            

            ##### Attacking #####
            ## Player Attacks ##
            if bonus_weapon == 3:
                bonus_damage_weapon += 1
            
            attack_count += 1
            high_low_counter = 0
            high_low = None
            list_repeater = []
            if bonus_weapon == 1 and attack_count % 3 == 0:
                repeater_count = 2 
            else:
                repeater_count = 1

            #Using Protections
            protection_counter = 0
            protection_active = 0
            protection_usage = None

##            def click_handler(x,y):
##                nonlocal protection_usage, high_low, protection_active, protection_counter, protection_drawing, protection
##
##                if protection > 0 and protection_drawing == 0:
##                    perks_boxes()
##                    protection_drawing = 1
##
##                if protection > 0:
##                    if x >= -350 and x <= -300 and y <= 60 and y >= 10:
##                        protection_usage = "Y"
##                    elif x >= -350 and x <= -300 and y <= 0 and y >= -50:
##                        protection_usage = "N"
##                    elif x >= -220 and x <= -80 and y >= -300 and y <= -250:
##                        high_low = "H"
##                    elif x >= -70 and x <= 70 and y >= -300 and y <= -250:
##                        high_low = "N"
##                    elif x >= 80 and x <= 220 and y >= -300 and y <= -250:
##                        high_low = "L"
##                else:
##                    if x >= -220 and x <= -80 and y >= -300 and y <= -250:
##                        high_low = "H"
##                    elif x >= -70 and x <= 70 and y >= -300 and y <= -250:
##                        high_low = "N"
##                    elif x >= 80 and x <= 220 and y >= -300 and y <= -250:
##                        high_low = "L"
##            
            if protection > 0 and protection_drawing == 0:
                perks_boxes()
                protection_drawing = 1
                
            if protection > 0:
                def protection_position(x,y):
                    nonlocal protection_usage, high_low
                    if x >= -350 and x <= -300 and y <= 60 and y >= 10:
                        protection_usage = "Y"
                    elif x >= -350 and x <= -300 and y <= 0 and y >= -50:
                        protection_usage = "N"
                    elif x >= -220 and x <= -80 and y >= -300 and y <= -250:
                        high_low = "H"
                    elif  x >= -70 and x <= 70  and y >= -300 and y <= -250:
                        high_low = "N"
                    elif   x >= 80 and x <= 220 and y >= -300 and y <= -250:
                        high_low = "L"

                screen.onclick(protection_position)
                
                while protection_counter != 1:
                    #protection_usage = textinput("Protecting 1/2 Enemies Damage", "Would you like to you a protection? Y/N")

                    while high_low is None and protection_usage is None:
                        screen.update()

                    while high_low is None and protection_usage is not None:
                        screen.update()

                    if protection_usage == "Y" and high_low is None:
                        protection -= 1
                        protection_active = 1
                        #break
                        protection_counter = 0
                        protection_usage = None
                        announcer.clear()
                        announcer.home()
                        announcer.write('Protection Used', False, align="center", font=("Arial", 15, "normal"))
                        protectionturtle.clear()
                        continue
                    elif protection_usage == "N":
                        protectionturtle.clear()
                        protection_drawing = 0
                        continue
                    elif high_low is not None:
                        break

            else:
                def attack_position(x,y):
                    nonlocal high_low
                    if x >= -220 and x <= -80 and y >= -300 and y <= -250:
                        high_low = "H"
                    elif x >= -70 and x <= 70 and y >= -300 and y <= -250:
                        high_low = "N"
                    elif x >= 80 and x <= 220 and y >= -300 and y <= -250:
                        high_low = "L"

                screen.onclick(attack_position)
        
                while high_low_counter != 1:
                    #high_low = textinput("High or Low Attack", "Press 'H' for High or 'L' for Low or 'N' for Normal")

                    while high_low is None:
                        screen.update()

                    break

            [miss_counter, player_damage_dealt] = damage_calculation(high_low, attack_count, bonus_weapon, player_bonus, bonus_damage_weapon, repeater_count, player_level, list_repeater, miss_counter)
                    
            ### Monster ###
            max_attack_damage = monster_level * 1.5;
            max_attack_damage = math.ceil(max_attack_damage);               
            damage_dealt = max_attack_damage * rand_monster;
            monster_damage_dealt = round(damage_dealt) - armour;
            
            # If Protection is used monster deals half damage
            if protection_active == 1:
                monster_damage_dealt = math.floor(monster_damage_dealt / 2)
                
            # Stop Being One Shot (100 -> 0)
            if monster_damage_dealt >= starting_player_health:
                monster_damage_dealt = starting_player_health - 1
            
            # If no damage don't move
            if monster_damage_dealt != 0:
                player2movement()
            
            # Display what happened
            if monster_damage_dealt == 0 and player_damage_dealt == 0:
                announcer.undo()
                announcer.home()
                announcer.write('Everybody Misses!', False, align="center", font=("Arial", 15, "normal"))
                displayturtle()
                continue
            elif monster_damage_dealt < 0:
                announcer.undo()
                announcer.home()
                announcer.write('Player dealt ' + str(player_damage_dealt) + ' damage! and Monster healed Player for ' + \
                                str(-monster_damage_dealt), False, align="center", font=("Arial", 15, "normal"))
                displayturtle()                
            else:
                announcer.undo()
                announcer.home()
                announcer.write('Player dealt ' + str(player_damage_dealt) + ' damage! and Monster dealt ' + \
                                str(monster_damage_dealt) + ' damage!', False, align="center", font=("Arial", 15, "normal"))
                displayturtle()

            if protection == 0:
                if protection_drawing == 1:
                    protectionturtle.clear()
                protection_drawing = 0
            
            ### Reduction in health ###
            monster_health = monster_health - player_damage_dealt;
            player_health = player_health - monster_damage_dealt;

            ### Exp Gained ###
            exp_gained = player_damage_dealt * 4;
            current_exp = exp_gained + current_exp;
            remaining_exp = remaining_exp - exp_gained;
            
            midbattleupdate(player_level, player_health, starting_player_health, remaining_exp, \
                            starting_remaining_exp, monster_level, monster_health, starting_monster_health, protection)
   
            ### Level Up ###
            while remaining_exp <= 0 and player_health > 0:
                if remaining_exp == 0:
                    player_level = player_level + 1;
                    starting_remaining_exp = math.ceil(starting_remaining_exp * 1.1);
                    remaining_exp = starting_remaining_exp;
                    starting_player_health = starting_player_health + 1;
                    #If Overhealed Keep Overheal
                    if player_health + 1 > starting_player_health:
                        player_health += 1
                    else: #Refill health
                        player_health = starting_player_health;
                    #Add one protection
                    if player_level % 3 == 0:
                        protection += 1
                    protection += 1
                    announcer.undo()
                    announcer.home()
                    announcer.write("Level Up", False, align="center", font=("Arial", 15, "normal"))
                    displayturtle()
                    levelupdate(player_level, player_health, starting_player_health, remaining_exp, starting_remaining_exp, protection)

                    continue
                # Reset Exp and put negative exp to next level
                elif remaining_exp < 0 and player_health > 0:
                    transition = -(remaining_exp)
                    player_level = player_level + 1;
                    starting_remaining_exp = math.ceil(starting_remaining_exp * 1.1);
                    remaining_exp = starting_remaining_exp - transition;
                    starting_player_health = starting_player_health + 1;
                    #If Overhealed Keep Overheal
                    if player_health + 1 > starting_player_health:
                        player_health += 1
                    else: #Refill health
                        player_health = starting_player_health;
                    #Add 1 protection
                    if player_level % 3 == 0:
                        protection += 1
                    announcer.undo()
                    announcer.home()
                    announcer.write("Level Up", False, align="center", font=("Arial", 15, "normal"))
                    displayturtle()
                    levelupdate(player_level, player_health, starting_player_health, remaining_exp, starting_remaining_exp, protection)                
                
                    continue   
        
        # Player Dies
        else:
            announcer.undo()
            announcer.home()
            announcer.write('Monster Wins', False, align="center", font=("Arial", 15, "normal"))
            displayturtle()
            
            return boss, battle_count, player_level, player_bonus, armour, \
            current_exp, remaining_exp, starting_remaining_exp, \
            starting_player_health, player_health, monster_level, \
            monster_health, starting_monster_health, health_pot, item_count, protection, boss_count, bonus_weapon
    
    
    # Monster Dies
    battle_count = battle_count + 1;
    ### Items ###
    x = random.random();
    # If Boss Died as you died chance to resurrect!
    if player_health < 0:
        resurrection_chance = random.random()
        if boss == 2 or boss == 3:
            if resurrection_chance > 0.3:    # 70% Chance
                player_health = starting_player_health
                announcer.undo()
                announcer.home()
                announcer.write('Player comes back from the dead!', False, align="center", font=("Arial", 15, "normal"))
                displayturtle()
        elif boss == 1:
            if resurrection_chance > 0.5:    # 50% Chance
                player_health = starting_player_health
                announcer.undo()
                announcer.home()
                announcer.write('Player comes back from the dead!', False, align="center", font=("Arial", 15, "normal"))
                displayturtle()
        elif boss == 0:
            if resurrection_chance > 0.7:    # 30% Chance
                player_health = starting_player_health
                announcer.undo()
                announcer.home()
                announcer.write('Player comes back from the dead!', False, align="center", font=("Arial", 15, "normal"))
                displayturtle()
    else:
        ## IF KILLED BOSS HIGHER CHANCE
        if boss == 2 or boss == 3:
            boss_count += 1
            monster_level -= 14
            starting_monster_health -= 14
            if 0.5 > x and x >= 0.45: ### 5%
    #            # Health
    #            [player_health, starting_player_health] = health(player_health, starting_player_health, 20)
                # Health Pot
                health_pot = health_pot_gained(health_pot, 4)
                item_count = 0
                
            elif x <= 0.3: ### 30%:
                # Damage
                player_bonus = damage(player_bonus, 4)
                item_count = 0
                
            elif 0.55 > x and x >= 0.5: ### 5%
                # Max Health
                [player_health, starting_player_health] = max_health(player_health, starting_player_health, 15)
                item_count = 0
            
            elif x >= 0.75: ### 25%
                # Bonus Level
                [player_level, player_health, starting_player_health] = bonus_level(player_level, player_health, starting_player_health)
                item_count = 0
                
            elif 0.45 > x and x > 0.3: ### 15%
                # Starting Health Increase
                starting_player_health = starting_health_increase(starting_player_health, 15)
                item_count = 0

            elif 0.75 > x and x > 0.55: ### 20%
                # Armour
                armour = armour_increase(armour, 4)
                item_count = 0
            else:
                item_count += 1

        elif boss == 1:
            boss_count += 1
            # Reroll if you've missed an item the times before
            if item_count > 0:
                for i in range(item_count):
                    if x <= 0.5 and x > 0.4:
                        x = random.random()
                    else:
                        break
            monster_level -= 7
            starting_monster_health -= 7
            if x >= 0.8: ### 20%
    #            # Health
    #            [player_health, starting_player_health] = health(player_health, starting_player_health, 10)
                # Health Pot
                health_pot = health_pot_gained(health_pot, 2)
                item_count = 0
                
            elif x <= 0.3: ### 30%:
                # Damage
                player_bonus = damage(player_bonus, 2)
                item_count = 0
                
            elif 0.8 > x and x >= 0.7: ### 10%
                # Max Health
                [player_health, starting_player_health] = max_health(player_health, starting_player_health, 10)
                item_count = 0
            
            elif 0.4 >= x and x > 0.35: ### 5%
                # Bonus Level
                [player_level, player_health, starting_player_health] = bonus_level(player_level, player_health, starting_player_health)
                item_count = 0
                
            elif 0.35 >= x and x > 0.3: ### 5%
                # Starting Health Increase
                starting_player_health = starting_health_increase(starting_player_health, 10)
                item_count = 0
                
            elif 0.7 > x and x < 0.5: ### 20%
                # Armour
                armour = armour_increase(armour, 2)
                item_count = 0
            else:
                item_count += 1
                
        else:
            # Reroll if you've missed an item the times before
            if item_count > 0:
                for i in range(item_count):
                    if x > 0.24 and x < 0.75:
                        x = random.random()
                    else:
                        break
                        
            if x >= 0.9: ### 10%
    #            # Health
    #            [player_health, starting_player_health] = health(player_health, starting_player_health, 5)
                # Health Pot
                health_pot = health_pot_gained(health_pot, 1)
                item_count = 0
                
            elif x <= 0.2: ### 20%:
                # Damage
                player_bonus = damage(player_bonus, 1)
                item_count = 0
                
            elif 0.8 > x and x >= 0.75: ### 5%
                # Max Health
                [player_health, starting_player_health] = max_health(player_health, starting_player_health, 5)
                item_count = 0

            elif 0.24 >= x and x > 0.22: ### 2%
                # Bonus Level
                [player_level, player_health, starting_player_health] = bonus_level(player_level, player_health, starting_player_health)
                item_count = 0
                
            elif 0.22 >= x and x > 0.2: ### 2%
                # Starting Health Increase
                starting_player_health = starting_health_increase(starting_player_health, 5)
                item_count = 0
                
            elif 0.9 > x and x >= 0.8: ### 10%
                # Armour
                armour = armour_increase(armour, 1)
                item_count = 0
            
            else:
                item_count += 1
    #Get a Weapon
    if boss_count == 3:
        weapon_counter = 0
        while weapon_counter != 1:
            weapon_usage = textinput("Choose Your Weapon", """Which weapon would you like?
                                    A) Double Attack Every 3rd Turn within a battle 
                                    B) Critical Attack Every 3rd Turn within battle or
                                    C) Constant Bonus Attack Damage Increase of 1 Every Turn within a battle""")
            if weapon_usage == 'A' or weapon_usage == 'a':
                bonus_weapon = 1
                weapon_counter = 1
            elif weapon_usage == 'B' or weapon_usage == 'b':
                bonus_weapon = 2
                weapon_counter = 1
            elif weapon_usage == 'C' or weapon_usage == 'c':
                bonus_weapon = 3
                weapon_counter = 1
       
    
    return boss, battle_count, player_level, player_bonus, armour, \
            current_exp, remaining_exp, starting_remaining_exp, \
            starting_player_health, player_health, monster_level, \
            monster_health, starting_monster_health, health_pot, item_count, protection, boss_count, bonus_weapon
    
# Boss Chance
def boss_chance_method(boss, boss_chance_redo):
    boss = 0
    if boss != 2 and boss != 3:
        boss_chance = random.random()
        for i in range(boss_chance_redo):
            if boss_chance >= 0.3438:
                boss_chance = random.random()
            else:
                break
        if boss_chance <= 0.2738:
            boss = 1
            boss_chance_redo = 0
        else:
            boss = 0
            boss_chance_redo += 1
    return boss, boss_chance_redo

# Boss Characteristics
def boss_characteristics(boss, starting_monster_health, monster_level, monster_health):
    
    # Boss Characteristics
    # Super Boss while alive
    if boss == 3:
        starting_monster_health = starting_monster_health + 15;
        monster_level += 15
    
    # Super Boss after Death
    elif boss == 2:
        starting_monster_health = starting_monster_health + 10
        monster_level += 10

    # Normal Boss
    elif boss == 1:
        starting_monster_health = starting_monster_health + 10;
        monster_level += 8
        
    ### Normal
    else:
        starting_monster_health = starting_monster_health + 5;
        monster_level = monster_level + 1;
        
    monster_health = starting_monster_health;
    return boss, starting_monster_health, monster_level, monster_health

def damage_calculation(high_low, attack_count, bonus_weapon, player_bonus, bonus_damage_weapon, repeater_count, player_level, list_repeater, miss_counter):
    if high_low == "H":
        announcer.clear()
        protection_counter = 1
        for i in range(repeater_count):
            if attack_count % 3 == 0 and bonus_weapon == 2:
                accuracy = 1
            else:
                accuracy = random.random()
            #Miss
            if accuracy < 0.8:
                player_damage_dealt_num = 0
                miss_counter += 1
                #Sympathy Hit
                if miss_counter >= 3:
                    max_attack_damage = player_level * 2.5 + player_bonus + bonus_damage_weapon;
                    max_attack_damage = math.ceil(max_attack_damage);
                    damage_dealt = max_attack_damage * accuracy;
                    player_damage_dealt_num = round(damage_dealt);
                    if player_damage_dealt_num == 0:
                        player_damage_dealt_num = 1
                    miss_counter = 0
                    player1movement()
            ### Critical Hit
            elif accuracy > 0.95:
                miss_counter = 0
                announcer.undo()
                announcer.home()
                announcer.write('Critical Hit!', False, align="center", font=("Arial", 15, "normal"))
                player1movement()
                max_attack_damage = (player_level * 2.5 + player_bonus) * 1.3 + bonus_damage_weapon;
                player_damage_dealt_num = math.ceil(max_attack_damage)
            #Hit
            else:
                miss_counter = 0
                max_attack_damage = player_level * 2.5 + player_bonus + bonus_damage_weapon;
                max_attack_damage = math.ceil(max_attack_damage);
                damage_dealt = max_attack_damage * accuracy;
                player_damage_dealt_num = round(damage_dealt);
                player1movement()
            list_repeater.append(player_damage_dealt_num)
        player_damage_dealt = sum(list_repeater)
    elif high_low == "L":
        protection_counter = 1
        announcer.clear()
        for i in range(repeater_count):
            if attack_count % 3 == 0 and bonus_weapon == 2:
                accuracy = 1
            else:
                accuracy = random.random()
            #Miss
            if accuracy < 0.1:
                miss_counter += 1
                player_damage_dealt_num = 0
                #Sympathy Hit
                if miss_counter >= 3:
                    max_attack_damage = player_level * 1.1 + player_bonus + bonus_damage_weapon;
                    max_attack_damage = math.ceil(max_attack_damage);
                    damage_dealt = max_attack_damage * accuracy;
                    player_damage_dealt_num = round(damage_dealt);
                    miss_counter = 0
                    player1movement()
                    if player_damage_dealt_num == 0:
                        player_damage_dealt_num = 1
            #Critical Hit
            elif accuracy > 0.95:
                miss_counter = 0
                announcer.undo()
                announcer.home()
                announcer.write('Critical Hit!', False, align="center", font=("Arial", 15, "normal"))
                player1movement()
                max_attack_damage = (player_level * 1.1 + player_bonus) * 1.3 + bonus_damage_weapon;
                player_damage_dealt_num = math.ceil(max_attack_damage)                        
            #Hit
            else:
                miss_counter = 0
                max_attack_damage = player_level * 1.1 + player_bonus + bonus_damage_weapon;
                max_attack_damage = math.ceil(max_attack_damage);
                damage_dealt = max_attack_damage * accuracy;
                if damage_dealt < 0.51:
                    damage_dealt = 0.51
                player_damage_dealt_num = round(damage_dealt);
                player1movement()
            list_repeater.append(player_damage_dealt_num)
        player_damage_dealt = sum(list_repeater)
        
    elif high_low == "N":
        protection_counter = 1
        announcer.clear()
        for i in range(repeater_count):
            if attack_count % 3 == 0 and bonus_weapon == 2:
                accuracy = 1
            else:
                accuracy = random.random()
            #Miss
            if accuracy < 0.5:
                miss_counter += 1
                player_damage_dealt_num = 0
                #Sympathy Hit
                if miss_counter >= 3:
                    max_attack_damage = player_level * 1.5 + player_bonus + bonus_damage_weapon;
                    max_attack_damage = math.ceil(max_attack_damage);
                    damage_dealt = max_attack_damage * accuracy;
                    player_damage_dealt_num = round(damage_dealt);
                    player1movement()
                    miss_counter = 0
                    if player_damage_dealt_num == 0:
                        player_damage_dealt_num = 1                            
            #Critical Hit
            elif accuracy > 0.95:
                miss_counter = 0
                announcer.undo()
                announcer.home()
                announcer.write('Critical Hit!', False, align="center", font=("Arial", 15, "normal"))
                player1movement()
                max_attack_damage = (player_level * 1.5 + player_bonus) * 1.3 + bonus_damage_weapon;
                player_damage_dealt_num = math.ceil(max_attack_damage)   
            #Hit
            else:                    
                miss_counter = 0
                max_attack_damage = player_level * 1.5 + player_bonus + bonus_damage_weapon;
                max_attack_damage = math.ceil(max_attack_damage);
                damage_dealt = max_attack_damage * accuracy;
                player_damage_dealt_num = round(damage_dealt);
                player1movement()
            list_repeater.append(player_damage_dealt_num)
        player_damage_dealt = sum(list_repeater)

    return miss_counter, player_damage_dealt
# Check for Super Boss
def superboss(boss, locations, map_square_size, player_health_list, dead_counter, boss_chance_redo):
    
    [x, y] = player_map.pos()
    current_pos = [x, y]
    # If Chance for 3 in a Row
    if len(locations) >= 3:
        
        ## Up
        # One Square Above
        if [x, y + map_square_size] in locations:
            # Multiple Results Present
            if locations.count([x, y + map_square_size]) > 1:
                loc_of_health = (len(locations) -1) - list(reversed(locations)).index([x, y + map_square_size])
            else:
                loc_of_health = locations.index([x, y + map_square_size])
            # And is An X
            if player_health_list[loc_of_health][0] > 0 and player_health_list[loc_of_health][1] <= 0:
                # Two Squares Above
                if [x, y + map_square_size * 2] in locations:
                    if locations.count([x, y + map_square_size * 2]) > 1:
                        loc_of_healthv2 = (len(locations) -1) - list(reversed(locations)).index([x, y + map_square_size * 2])
                    else:
                        loc_of_healthv2 = locations.index([x, y + map_square_size * 2])
                    # And is An X
                    if player_health_list[loc_of_healthv2][0] > 0 and player_health_list[loc_of_healthv2][1] <= 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                            boss_chance_redo = 0
                        # If just died
                        elif dead_counter == 1:
                            boss = 2
                            boss_chance_redo = 0
        
        ## Down
        # One Square Below
        if [x, y - map_square_size] in locations:
            # Multiple Results Present
            if locations.count([x, y + map_square_size]) > 1:
                loc_of_health = (len(locations) -1) - list(reversed(locations)).index([x, y - map_square_size])
            else:
                loc_of_health = locations.index([x, y - map_square_size])
            # And is An X
            if player_health_list[loc_of_health][0] > 0 and player_health_list[loc_of_health][1] <= 0:
                # Two Squares Below
                if [x, y - map_square_size * 2] in locations:
                    if locations.count([x, y - map_square_size * 2]) > 1:
                        loc_of_healthv2 = (len(locations) -1) - list(reversed(locations)).index([x, y - map_square_size * 2])
                    else:
                        loc_of_healthv2 = locations.index([x, y - map_square_size * 2])
                    # And is An X
                    if player_health_list[loc_of_healthv2][0] > 0 and player_health_list[loc_of_healthv2][1] <= 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                            boss_chance_redo = 0
                        # If just died
                        elif dead_counter == 1:
                            boss = 2
                            boss_chance_redo = 0
        
        ## Left
        # One Square Left
        if [x - map_square_size, y] in locations:
            # Multiple Results Present
            if locations.count([x - map_square_size, y]) > 1:
                loc_of_health = (len(locations) -1) - list(reversed(locations)).index([x - map_square_size, y])
            else:
                loc_of_health = locations.index([x - map_square_size, y])
            # And is An X
            if player_health_list[loc_of_health][0] > 0 and player_health_list[loc_of_health][1] <= 0:
                # Two Squares Left
                if [x - map_square_size * 2, y] in locations:
                    # Check for Doubles
                    if locations.count([x - map_square_size * 2, y]) > 1:
                        loc_of_healthv2 = (len(locations) -1) - list(reversed(locations)).index([x - map_square_size * 2, y])
                    else:
                        loc_of_healthv2 = locations.index([x - map_square_size * 2, y])
                    # And is An X
                    if player_health_list[loc_of_healthv2][0] > 0 and player_health_list[loc_of_healthv2][1] <= 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                            boss_chance_redo = 0
                        # If just died
                        elif dead_counter == 1:
                            boss = 2
                            boss_chance_redo = 0
        
        ## Right
        # One Square Right
        if [x + map_square_size, y] in locations:
            # Multiple Results Present
            if locations.count([x + map_square_size, y]) > 1:
                loc_of_health = (len(locations) -1) - list(reversed(locations)).index([x + map_square_size, y])
            else:
                loc_of_health = locations.index([x + map_square_size, y])
            # And is An X
            if player_health_list[loc_of_health][0] > 0 and player_health_list[loc_of_health][1] <= 0:
                # Two Squares Right
                if [x + map_square_size * 2, y] in locations:
                    if locations.count([x + map_square_size * 2, y]) > 1:
                        loc_of_healthv2 = (len(locations) -1) - list(reversed(locations)).index([x + map_square_size * 2, y])
                    else:
                        loc_of_healthv2 = locations.index([x + map_square_size * 2, y])
                    # And is An X
                    if player_health_list[loc_of_healthv2][0] > 0 and player_health_list[loc_of_healthv2][1] <= 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                            boss_chance_redo = 0
                        # If just died
                        elif dead_counter == 1:
                            boss = 2
                            boss_chance_redo = 0
        
        # Between Top and Bottom
        # One Square Above
        if [x, y + map_square_size] in locations:
            # Multiple Results Present
            if locations.count([x, y + map_square_size]) > 1:
                loc_of_health = (len(locations) -1) - list(reversed(locations)).index([x, y + map_square_size])
            else:
                loc_of_health = locations.index([x, y + map_square_size])
            # And is An X
            if player_health_list[loc_of_health][0] > 0 and player_health_list[loc_of_health][1] <= 0:
                # One Square Below
                if [x, y - map_square_size] in locations:
                    if locations.count([x, y - map_square_size]) > 1:
                        loc_of_healthv2 = (len(locations) -1) - list(reversed(locations)).index([x, y - map_square_size])
                    else:
                        loc_of_healthv2 = locations.index([x, y - map_square_size])
                    # And is An X
                    if player_health_list[loc_of_healthv2][0] > 0 and player_health_list[loc_of_healthv2][1] <= 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                            boss_chance_redo = 0
                        # If just died
                        elif dead_counter == 1:
                            boss = 2
                            boss_chance_redo = 0

        ## Between Left and Right
        # One Square Right
        if [x + map_square_size, y] in locations:
            # Multiple Results Present
            if locations.count([x + map_square_size, y]) > 1:
                loc_of_health = (len(locations) -1) - list(reversed(locations)).index([x + map_square_size, y])
            else:
                loc_of_health = locations.index([x + map_square_size, y])
            # And is An X
            if player_health_list[loc_of_health][0] > 0 and player_health_list[loc_of_health][1] <= 0:
                # One Square Left
                if [x - map_square_size, y] in locations:
                    if locations.count([x - map_square_size, y]) > 1:
                        loc_of_healthv2 = (len(locations) -1) - list(reversed(locations)).index([x - map_square_size, y])
                    else:
                        loc_of_healthv2 = locations.index([x - map_square_size, y])
                    # And is An X
                    if player_health_list[loc_of_healthv2][0] > 0 and player_health_list[loc_of_healthv2][1] <= 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                            boss_chance_redo = 0
                        # If just died
                        elif dead_counter == 1:
                            boss = 2
                            boss_chance_redo = 0
    return boss, boss_chance_redo

## Draw Squares on the screen ## 5x5
def setupmapscreen():
    size_of_screen = 230
    map_square_size = size_of_screen * 2 / 5
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
    player_map.showturtle()
    tracer(True)
    return size_of_screen, map_square_size

def movement_boxes(size_of_screen):
    tracer(False)
    for i in range(4):
        # Top Left Corner
        boxturtle.setposition(-size_of_screen + (i*120), -270)
        #print(writer.xcor())  -230
        #print(writer.ycor())  -270
        boxturtle.down()
        
        # Top Right Corner
        boxturtle.setposition(-size_of_screen + (i*120) + 100, -270)
        #print(writer.xcor())  -130
        #print(writer.ycor())  -270
        #writer.up()
        
        # Bottom Right Corner
        boxturtle.setposition(-size_of_screen + (i*120) + 100, -270 -50)
        #print(writer.xcor())  -130
        #print(writer.ycor())  -320  
        # Bottom Left Corner
        boxturtle.setposition(-size_of_screen + (i*120), -270 -50)
        #print(writer.xcor())  -270
        #print(writer.ycor())  -320  
        # Back to Top Left
        
        boxturtle.setposition(-size_of_screen + (i*120), -270)
        #print(writer.xcor())  -230
        #print(writer.ycor())  -270
        boxturtle.up()

    for j in range(4):
        writer.setposition(-size_of_screen + (j*120) + 50, -270 - 30)
        if j == 0:
            writer.write("Up", False, align="center", font=("Arial", 15, "normal"))
        if j == 1:
            writer.write("Left", False, align="center", font=("Arial", 15, "normal"))       
        if j == 2:
            writer.write("Right", False, align="center", font=("Arial", 15, "normal"))
        if j == 3:
            writer.write("Down", False, align="center", font=("Arial", 15, "normal"))

    tracer(True)                     

def attack_boxes():
    tracer(False)
    for i in range(3):
        # Top Left Corner
        boxturtle.setposition(-220 + (i*150), -250)
        boxturtle.down()
        
        # Top Right Corner
        boxturtle.setposition(-220 + (i*150) + 140, -250)
        
        # Bottom Right Corner
        boxturtle.setposition(-220 + (i*150) + 140, -250 -50)

        # Bottom Left Corner
        boxturtle.setposition(-220 + (i*150), -250 -50)

        # Back to Top Left        
        boxturtle.setposition(-220 + (i*150), -250)

        boxturtle.up()

    for j in range(3):
        boxturtle.setposition(-220 + (j*150) + 70, -250 - 30)
        if j == 0:
            boxturtle.write("High", False, align="center", font=("Arial", 15, "normal"))
        if j == 1:
            boxturtle.write("Normal", False, align="center", font=("Arial", 15, "normal"))       
        if j == 2:
            boxturtle.write("Low", False, align="center", font=("Arial", 15, "normal"))

    tracer(True)  

def perks_boxes():
    tracer(False)

    starting_x = -350
    starting_y = 60
    box_width = 50
    box_height = 50
    gap = 10
    dist_to_next_box = box_width + gap

    protectionturtle.setposition(starting_x + 20 - 5, starting_y)
    protectionturtle.write("Protecting against half enemies damage?", False, align="left", font=("Arial", 15, "normal"))
    
    for i in range(2):
        # Top Left Corner
        protectionturtle.setposition(starting_x , starting_y - (i* dist_to_next_box))
        protectionturtle.down()
        
        # Top Right Corner
        protectionturtle.setposition(starting_x + box_width, starting_y - (i*dist_to_next_box))
        
        # Bottom Right Corner
        protectionturtle.setposition(starting_x + box_width, starting_y - box_height - (i*dist_to_next_box))

        # Bottom Left Corner
        protectionturtle.setposition(starting_x, starting_y - box_height - (i*dist_to_next_box))

        # Back to Top Left        
        protectionturtle.setposition(starting_x, starting_y - (i*dist_to_next_box))

        protectionturtle.up()

    for j in range(2):
        protectionturtle.setposition(starting_x  + box_width/2, starting_y - box_height/2 - 5 - (j*dist_to_next_box))
        if j == 0:
            protectionturtle.write("Yes", False, align="center", font=("Arial", 15, "normal"))
        if j == 1:
            protectionturtle.write("No", False, align="center", font=("Arial", 15, "normal"))       

    tracer(True)  

def check_location(map_movement_counter, m, locations, player_health_list, map_movement):

    if map_movement == 'U' or map_movement == 'D':
        # Check for an X
        x_pos = round(player_map.xcor())
        y_pos = round(m)
    elif map_movement == 'L' or map_movement == 'R':
        x_pos = round(m)
        y_pos = round(player_map.ycor())
    current = [x_pos, y_pos]

    #print(current)
    #print(locations)
    
    # If the location currently exists in Locations of everywhere been
    if current in locations:
        # Check for number of occurances
        indices = [i for i, x in enumerate(locations) if x == current]
        indices_counter = 0
        # Check to see if its a save or finished
        for loc_index in indices:
            # Player or Monster is dead therefore place is finished
            if player_health_list[loc_index][0] <= 0 or player_health_list[loc_index][1] <= 0:
               indices_counter += 1
            
        # If Player or Monster is dead then square over
        if indices_counter == 1:
            map_movement = None
            map_movement_counter = 0
            screen.update()
        #If Saved or Not Dead
        else:
            map_movement_counter = 1
    else:
        map_movement_counter = 1

    return map_movement_counter, map_movement
    
## Map Movement
def mapmovement(size_of_screen, map_square_size, locations, player_health_list):
    map_movement = None
    map_movement_counter = 0
    movement_boxes(size_of_screen)
    
    def selecting_movement(x, y):
        nonlocal map_movement
        updater.goto(x, y)
        #print(x,y)
        if x >= -230 and x <= -130 and y >= -320 and y <= -270:
            map_movement = 'U'

        elif x >= -110 and x <= -10 and y >= -320 and y <= -270:
            map_movement = 'L'

        elif x >= 10 and x <= 110 and y >= -320 and y <= -270:
            map_movement = 'R'    

        elif x <= 230 and x >= 130 and y >= -320 and y <= -270:
            map_movement = 'D'    


    screen.onclick(selecting_movement)
    
    while map_movement_counter != 1:
        #map_movement = textinput("Move The Map", """Press 'U' for UP or 
        #'D' for Down or 'L' for Left or 'R' for Right""")
        
        while map_movement is None:
            screen.update()
        
        
        if map_movement == 'U':
            org_pos_y = player_map.ycor()
            org_pos_y = org_pos_y + map_square_size #Size of square
    #        # If outside try again
            if org_pos_y > size_of_screen:
                map_movement = None
                map_movement_counter = 0
            else:
                player_map.setposition(player_map.xcor(), org_pos_y)
            
                [map_movement_counter, map_movement] = check_location(map_movement_counter, org_pos_y, locations,
                                                                  player_health_list, map_movement)
                        

            #print(map_movement_counter)
            #print(map_movement)
            
        elif map_movement == 'D':
            org_pos_y = player_map.ycor()
            org_pos_y = org_pos_y - map_square_size #Size of square

            if org_pos_y > size_of_screen:
                map_movement = None
                map_movement_counter = 0
            else:
                player_map.setposition(player_map.xcor(), org_pos_y)
            
                [map_movement_counter, map_movement] = check_location(map_movement_counter, org_pos_y, locations,
                                                                  player_health_list, map_movement)
            
        elif map_movement == 'L':
            org_pos_x = player_map.xcor()
            org_pos_x = org_pos_x - map_square_size #Size of square
            # If outside try again            
            if org_pos_x < -size_of_screen:
                map_movement = None
                map_movement_counter = 0
            else:
                player_map.setposition(org_pos_x, player_map.ycor())
            
                [map_movement_counter, map_movement] = check_location(map_movement_counter, org_pos_x, locations,
                                                                  player_health_list, map_movement)
            
        elif map_movement == 'R':            
            org_pos_x = player_map.xcor()
            org_pos_x = org_pos_x + map_square_size #Size of square
            # If outside try again            
            if org_pos_x > size_of_screen:
                map_movement = None
                map_movement_counter = 0
            else:
                player_map.setposition(org_pos_x, player_map.ycor())
            
                [map_movement_counter, map_movement] = check_location(map_movement_counter, org_pos_x, locations,
                                                                  player_health_list, map_movement)

        #map_movement_counter = 0        
        map_movement = None

    #print(locations)
    #screen.clear()    
    displayturtle()
    player_map.hideturtle()
    
    [x, y] = player_map.pos()
    recording_cords = [x, y]
    locations.append(recording_cords)
    
    return locations
    
## Place X's
def placexs(counter, locations, player_health_list, map_square_size):
    counter += 1
    for i in range(len(locations)):
        # No Repetitions
        last_occurence = (len(locations) - 1) - list(reversed(locations)).index(locations[i])
        if i == last_occurence:
            updater.setposition(locations[i][0], locations[i][1])
            if player_health_list[i][0] > 0 and player_health_list[i][1] <= 0:
                updater.write("X", False, align="center", font=("Arial", round(map_square_size / 4), "normal"))
            elif player_health_list[i][0] <= 0:
                updater.write("0", False, align="center", font=("Arial", round(map_square_size / 4), "normal"))
            elif player_health_list[i][0] > 0 and player_health_list [i][1] > 0:
                updater.write("-", False, align="center", font=("Arial", round(map_square_size / 4), "normal"))

    return counter, locations

## Clear Every Turtle
def clearturtle():
    writer.clear()
    writer.hideturtle()
    announcer.clear()
    announcer.hideturtle()
    updater.clear()
    updater.hideturtle()
    player1.clear()
    player1.hideturtle()
    player2.clear()
    player2.hideturtle()
    monster_updater.clear()
    monster_updater.hideturtle()
    player_updater.clear()
    player_updater.hideturtle()
    player_map.clear()
    player_map.hideturtle()
    boxturtle.clear()
    boxturtle.hideturtle()
    protectionturtle.clear()
    protectionturtle.hideturtle()

##### Starting Conditions ######
def starting_conditions():
    
    ### General ###
    battle_count = 1;

    ### Player ###
    player_level = 1;
    current_exp = 0;
    starting_remaining_exp = 10;
    remaining_exp = starting_remaining_exp;
    starting_player_health = 10;
    player_health = starting_player_health;
    player_bonus = 0;
    boss = 0
    armour = 0
    health_pot = 0
    
    ### Monster ###
    monster_level = 1;
    starting_monster_health = 10;
    monster_health = starting_monster_health;
    item_count = 0;
    return battle_count, player_level, player_bonus, current_exp, \
        remaining_exp, starting_remaining_exp, starting_player_health, \
        player_health, monster_level, monster_health, starting_monster_health, \
        armour, boss, health_pot, item_count

# Setup of Battle Screen    
def setupbattlescreen(battle_count, player_level, player_bonus, armour, remaining_exp, starting_remaining_exp, starting_player_health, 
            player_health, monster_level, monster_health, starting_monster_health, protection):

    tracer(False)
    #Player Stats
    writer.setposition(-300, 250)
    writer.write("Player Level =", False, align="left", font=("Arial", 15, "normal"))
    writer.setposition(-300, 230)
    writer.write("Health =", False, align="left", font=("Arial", 15, "normal"))
    writer.setposition(-300, 210)
    writer.write("Player Bonus =", False, align="left", font=("Arial", 15, "normal"))
    writer.setposition(-300, 190)
    writer.write("Armour =", False, align="left", font=("Arial", 15, "normal"))
    writer.setposition(-300, 170)
    writer.write("Protections Left =", False, align="left", font=("Arial", 15, "normal"))    
    writer.setposition(-300, 150)
    writer.write("Exp =", False, align="left", font=("Arial", 15, "normal"))
    
    #Monster Max Hit
    writer.setposition(290, 210)
    writer.write("Max Hit: " + str(math.ceil(monster_level * 1.5)), False, align="right", font=("Arial", 15, "normal"));
    
    #Boss Stats
    writer.setposition(250, 250)
    writer.write("Level =", False, align="right", font=("Arial", 15, "normal"))
    writer.setposition(220, 230)
    writer.write("Health =", False, align="right", font=("Arial", 15, "normal"))
    
    #Battle
    writer.setposition(-70, 250)
    writer.write("Battle No: ", False, align="left", font=("Arial", 15, "normal"))

    #Battle Number
    writer.setposition(30, 250)
    writer.write(str(battle_count), False, align="center", font=("Arial", 15, "normal"))
    
    #Update Player
    player_updater.setposition(-170, 250)
    player_updater.write(str(player_level), False, align="left", font=("Arial", 15, "normal"))
    player_updater.setposition(-220, 230)
    player_updater.write(str(player_health) + " / " + str(starting_player_health), False, align="left", font=("Arial", 15, "normal"))
    player_updater.setposition(-140, 170)
    player_updater.write(str(protection), False, align="left", font=("Arial", 15, "normal"))
    player_updater.setposition(-240, 150)
    player_updater.write(str(remaining_exp) + " / " + str(starting_remaining_exp), False, align="left", font=("Arial", 15, "normal"))  

    updater.setposition(-210, 190)
    updater.write(str(armour), False, align="left", font=("Arial", 15, "normal"))
    updater.setposition(-160, 210)
    updater.write(str(player_bonus), False, align="left", font=("Arial", 15, "normal"))      
    
    #Update Boss
    monster_updater.setposition(270, 250)
    monster_updater.write(str(monster_level), False, align="right", font=("Arial", 15, "normal"))
    monster_updater.setposition(280, 230)
    monster_updater.write(str(monster_health) + " / " + str(starting_monster_health), False, align="right", font=("Arial", 15, "normal"))
    tracer(True)

    return

# Mid Battle Screen
def midbattleupdate(player_level, player_health, starting_player_health, remaining_exp, starting_remaining_exp, monster_level, monster_health, starting_monster_health, protection):

    tracer(False)
    #Update Player
    for i in range(7):
        player_updater.undo()

    player_updater.setposition(-170, 250)
    player_updater.write(str(player_level), False, align="left", font=("Arial", 15, "normal"))
    player_updater.setposition(-220, 230)
    player_updater.write(str(player_health) + " / " + str(starting_player_health), False, align="left", font=("Arial", 15, "normal"))
    player_updater.setposition(-140, 170)
    player_updater.write(str(protection), False, align="left", font=("Arial", 15, "normal"))    
    player_updater.setposition(-240, 150)
    player_updater.write(str(remaining_exp) + " / " + str(starting_remaining_exp), False, align="left", font=("Arial", 15, "normal"))         
    
    for i in range(4):
        monster_updater.undo()
    #Update Boss
    monster_updater.setposition(270, 250)
    monster_updater.write(str(monster_level), False, align="right", font=("Arial", 15, "normal"))
    monster_updater.setposition(280, 230)
    monster_updater.write(str(monster_health) + " / " + str(starting_monster_health), False, align="right", font=("Arial", 15, "normal"))
    tracer(True)
    return

# Level Up Screen
def levelupdate(player_level, player_health, starting_player_health, remaining_exp, starting_remaining_exp, protection):
    for i in range(7):
        player_updater.undo()
    player_updater.setposition(-170, 250)
    player_updater.write(str(player_level), False, align="left", font=("Arial", 15, "normal"))
    player_updater.setposition(-220, 230)
    player_updater.write(str(player_health) + " / " + str(starting_player_health), False, align="left", font=("Arial", 15, "normal"))
    player_updater.setposition(-140, 170)
    player_updater.write(str(protection), False, align="left", font=("Arial", 15, "normal"))    
    player_updater.setposition(-240, 150)
    player_updater.write(str(remaining_exp) + " / " + str(starting_remaining_exp), False, align="left", font=("Arial", 15, "normal"))
    

### Attack Movements
def player1movement():
    player1.setposition(200, -200)
    player1.undo()

def player2movement():
    player2.setposition(-200, -200)
    player2.undo()

## Help Display Text
def displayturtle():
    display.setposition(-200,0)
    display.undo()
    display.setposition(200,0)
    display.undo()

## Items
def damage(player_bonus, bonus):
    announcer.undo()
    announcer.home()
    announcer.write('Damage Boost', False, align="center", font=("Arial", 15, "normal"))
    displayturtle()
    player_bonus = player_bonus + bonus;
    return player_bonus

def health(player_health, starting_player_health, bonus):
    announcer.undo()
    announcer.home()
    announcer.write('Health Gained', False, align="center", font=("Arial", 15, "normal"))
    displayturtle()
    player_health = player_health + bonus;
    return player_health, starting_player_health

def health_pot_gained(health_pot, bonus):
    announcer.undo()
    announcer.home()
    announcer.write('Health Pot Gained', False, align="center", font=("Arial", 15, "normal"))
    displayturtle()
    
    health_pot += bonus
    return health_pot

def max_health(player_health, starting_player_health, bonus):
    # If at max health do overheal of 10
    if player_health >= starting_player_health:
        announcer.undo()
        announcer.home()
        announcer.write('Overheal', False, align="center", font=("Arial", 15, "normal"))
        displayturtle()
        
        player_health += bonus
    else:
        announcer.undo()
        announcer.home()
        announcer.write('Max Heal', False, align="center", font=("Arial", 15, "normal"))
        displayturtle()
        player_health = starting_player_health;
        
    return player_health, starting_player_health

def bonus_level(player_level, player_health, starting_player_health):
    announcer.undo()
    announcer.home()
    announcer.write('Bonus Level', False, align="center", font=("Arial", 15, "normal"))
    displayturtle()
    player_level += 1
    starting_player_health += 1
    if player_health + 1 < starting_player_health:
        player_health = starting_player_health
    else:
        player_health += 1
    return player_level, player_health, starting_player_health

def starting_health_increase(starting_player_health, bonus):
    announcer.undo()
    announcer.home()
    announcer.write('Starting Health Increase', False, align="center", font=("Arial", 15, "normal"))
    displayturtle()
    
    starting_player_health += bonus
    return starting_player_health

def armour_increase(armour, bonus):
    announcer.undo()
    announcer.home()
    announcer.write('Armour Increase', False, align="center", font=("Arial", 15, "normal"))
    displayturtle()    
    
    armour += bonus
    return armour

def winning_conditions(boss, locations, map_square_size, player_health_list, dead_counter):
    
    [x, y] = player_map.pos()
    current_pos = [x, y]
    # If Chance for 3 in a Row
    if len(locations) >= 3:
        
        ## Up
        # One Square Above
        if [x, y + map_square_size] in locations:
            loc_of_health = locations.index([x, y + map_square_size])
            # And is An X
            if player_health_list[loc_of_health] > 0:
                # Two Squares Above
                if [x, y + map_square_size * 2] in locations:
                    loc_of_healthv2 = locations.index([x, y + map_square_size * 2])
                    # And is An X
                    if player_health_list[loc_of_healthv2] > 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                        # If just died
                        elif dead_counter == 1:
                            boss = 2
        
        ## Down
        # One Square Below
        if [x, y - map_square_size] in locations:
            loc_of_health = locations.index([x, y - map_square_size])
            # And is An X
            if player_health_list[loc_of_health] > 0:
                # Two Squares Below
                if [x, y - map_square_size * 2] in locations:
                    loc_of_healthv2 = locations.index([x, y - map_square_size * 2])
                    # And is An X
                    if player_health_list[loc_of_healthv2] > 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                        # If just died
                        elif dead_counter == 1:
                            boss = 2    
        
        ## Left
        # One Square Left
        if [x - map_square_size, y] in locations:
            loc_of_health = locations.index([x - map_square_size, y])
            # And is An X
            if player_health_list[loc_of_health] > 0:
                # Two Squares Left
                if [x - map_square_size * 2, y] in locations:
                    loc_of_healthv2 = locations.index([x - map_square_size * 2, y])
                    # And is An X
                    if player_health_list[loc_of_healthv2] > 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                        # If just died
                        elif dead_counter == 1:
                            boss = 2           
        
        ## Right
        # One Square Right
        if [x + map_square_size, y] in locations:
            loc_of_health = locations.index([x + map_square_size, y])
            # And is An X
            if player_health_list[loc_of_health] > 0:
                # Two Squares Right
                if [x + map_square_size * 2, y] in locations:
                    loc_of_healthv2 = locations.index([x + map_square_size * 2, y])
                    # And is An X
                    if player_health_list[loc_of_healthv2] > 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                        # If just died
                        elif dead_counter == 1:
                            boss = 2              
        
        # Between Top and Bottom
        # One Square Above
        if [x, y + map_square_size] in locations:
            loc_of_health = locations.index([x, y + map_square_size])
            # And is An X
            if player_health_list[loc_of_health] > 0:
                # One Square Below
                if [x, y - map_square_size] in locations:
                    loc_of_healthv2 = locations.index([x, y - map_square_size])
                    # And is An X
                    if player_health_list[loc_of_healthv2] > 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                        # If just died
                        elif dead_counter == 1:
                            boss = 2

        ## Between Left and Right
        # One Square Right
        if [x + map_square_size, y] in locations:
            loc_of_health = locations.index([x + map_square_size, y])
            # And is An X
            if player_health_list[loc_of_health] > 0:
                # One Square Left
                if [x - map_square_size, y] in locations:
                    loc_of_healthv2 = locations.index([x - map_square_size, y])
                    # And is An X
                    if player_health_list[loc_of_healthv2] > 0:
                        # GOING TO WIN SUPER BOSS
                        # If alive:
                        if dead_counter == 0:
                            boss = 3
                        # If just died
                        elif dead_counter == 1:
                            boss = 2
    return boss
    
# Unlock Conditions Beat 3 Bosses
# Weapon's Types
## Double Attack Every Attack 3rd Attack i.e. Reroll the accuracy thing
## Crit every 3rd Strike
## Every attack in the battles goes up by 2 damage

### To Do ###
# Boss Reset Definition to create
# Check Multiple saves

# Run the Game
main()
