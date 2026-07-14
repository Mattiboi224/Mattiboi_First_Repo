import Config as C
from PIL import Image
from collections import Counter

image = Image.open(C.GOLD_VAULT_IMAGE).convert("RGB")
pixels = list(image.getdata())

#print(pixels)

counts = Counter(pixels)
print("Counts of all items:")
for item, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{item}: {count}")

# (70, 72, 62): 59
# (50, 52, 45): 42
# (30, 30, 28): 32
# (200, 60, 40): 28
# (60, 60, 55): 20
# (35, 35, 32): 11
# (60, 62, 55): 10


old = (35, 33, 30)

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