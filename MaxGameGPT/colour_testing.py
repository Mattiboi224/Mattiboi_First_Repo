import Config as C
from PIL import Image
from collections import Counter

image_to_open = C.ENTITY_STATS["Concrete Block"]["image"]

image = Image.open(image_to_open).convert("RGB")
pixels = list(image.getdata())

#print(pixels)

counts = Counter(pixels)
print("Counts of all items:")
for item, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{item}: {count}")

# (140, 138, 132): 676
# (150, 148, 142): 64
# (95, 93, 88): 62
# (160, 158, 152): 62
# (120, 118, 112): 54
# (128, 126, 120): 53
# (122, 120, 114): 44
# (100, 98, 92): 9

old = (150, 148, 142)

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