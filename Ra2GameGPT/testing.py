from PIL import Image
from collections import Counter

w = 32
h = 22

# Tile types
T_GRASS = 0
T_WALL = 1
T_RESOURCE = 2
T_PLAYER_LOC = 3
T_GEMS = 4

TILE_COLORS = {
    #T_GRASS: (40, 110, 40),
    T_GRASS: (34, 177, 76),
    #T_WALL: (70, 70, 70),
    T_WALL: (127, 127, 127),
    #T_RESOURCE: (120, 85, 30),
    T_RESOURCE: (255, 242, 0),
    T_PLAYER_LOC: (237, 28, 36),
    T_GEMS: (163, 73, 164)
}

# Load the image
image = Image.open('game_map.png')

# Resize for faster processing
#image = image.resize((32, 22))

# Get pixel data
pixels = list(image.getdata())
rgb_pixel = [t[:3] for t in pixels]
#print(pixels)

print(rgb_pixel)

# for i in range(h):
#     for j in range(w):
#         for key, value in TILE_COLORS.items():
#             if value == rgb_pixel[j + (i - 1) * w]:
#                 print(key)



# Count colors
color_counts = Counter(pixels)

#print(color_counts)

# Find the most common color
dominant_color = color_counts.most_common(1)[0][0]

#print(f"Dominant Color: {dominant_color}")