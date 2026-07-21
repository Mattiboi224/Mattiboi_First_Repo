import Config as C
w = C.MAP_WIDTH
h = C.MAP_HEIGHT
spawns = [(1,2), (3,4), (5,6)]

resource_tiles = [[C.T_GRASS for _ in range(w)] for _ in range(h)]
resource_amounts = [[C.T_GRASS for _ in range(w)] for _ in range(h)]

for i in range(h):
    for j in range(w):

        if (j, i) in spawns:
            # Spawn tiles always get a guaranteed resource
            key = 2
            resource_amount = 15

        elif (j - 1, i - 1) in spawns:
            print(i, j)
            # Spawn tiles always get a guaranteed resource
            key = 4
            resource_amount = 15


        else:
            key = 6
            resource_amount = 0

        resource_tiles[i][j] = key
        resource_amounts[i][j] = resource_amount

print(resource_tiles[3][2])