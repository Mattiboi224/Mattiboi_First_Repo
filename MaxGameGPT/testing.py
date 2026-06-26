import Config as C
from PIL import Image
from collections import Counter

image = Image.open(C.SOLDIER_IMAGE).convert("RGB")
pixels = list(image.getdata())

#print(pixels)

counts = Counter(pixels)
print("Counts of all items:")
for item, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{item}: {count}")

# (52, 68, 32): 250
# (38, 50, 22): 104
# (30, 40, 14): 71
# (50, 50, 46): 36

old = (52, 68, 32)

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