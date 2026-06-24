COST_SOLDIER = 60
COST_BARRACKS = 75
COST_TANK = 150

labels = ['Barracks','Soldier', 'Tank']
for i in labels:
    if i == 'Barracks':
        cost = COST_BARRACKS
    if i == 'Soldier':
        cost = COST_SOLDIER 
    if i == 'Tank':
        cost = COST_TANK