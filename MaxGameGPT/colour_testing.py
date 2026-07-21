import Config as C
from PIL import Image
from collections import Counter

image_to_open = C.ENTITY_STATS["Big Construction"]["image"]

image = Image.open(image_to_open).convert("RGB")
pixels = list(image.getdata())

#print(pixels)

counts = Counter(pixels)
print("Counts of all items:")
for item, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{item}: {count}")

# (96, 68, 42): 1485
# (25, 22, 18): 431
# (210, 175, 40): 415
# (115, 117, 120): 325
# (255, 255, 255): 252
# (150, 150, 148): 188
# (100, 40, 30): 140
# (196, 168, 108): 113
# (122, 122, 120): 99
# (150, 60, 45): 90
# (168, 138, 82): 80
# (180, 150, 92): 74
# (70, 71, 73): 64
# (85, 85, 83): 60
# (150, 152, 155): 56
# (120, 96, 56): 48
# (84, 58, 36): 45
# (108, 78, 48): 37
# (74, 50, 30): 37
# (75, 30, 22): 36
# (50, 36, 22): 21

old = (168, 138, 82)

new = C.TEAM_COLORS[1]      # red

updated = [new if p == old else p for p in pixels]

out = Image.new("RGB", image.size)
out.putdata(updated)
out.save("player_red.png")

# Convert This Colour to Team Colour
# Tanks
# (74, 98, 48)

# Ammo Truck
# (74, 104, 40)

# Soldier
# (52, 68, 32)