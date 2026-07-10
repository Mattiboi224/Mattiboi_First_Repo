import Config as C
from PIL import Image
from collections import Counter

image = Image.open(C.GAME_MAP).convert("RGB")
pixels = list(image.getdata())

#print(pixels)

width, height = image.size
print(f"Image size: {width}x{height}")
print(C.GRID_W, C.GRID_H)

counts = Counter(pixels)
print("Counts of all items:")
for item, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{item}: {count}")

# (96, 94, 84): 310
# (74, 84, 58): 185
# (25, 28, 22): 122
# (91, 102, 71): 121
# (70, 68, 60): 102

# old = (104, 114, 78)

# new = C.TEAM_COLORS[1]      # red

# updated = [new if p == old else p for p in pixels]

# out = Image.new("RGB", image.size)
# out.putdata(updated)
# out.save("player_red.png")

# Convert This Colour to Team Colour
# Tanks
# (74, 98, 48)

# Ammo Truck
# (74, 104, 40)

# Soldier
# (52, 68, 32)