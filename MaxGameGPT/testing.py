
import Config as C

building_unit = [name for name, stats in C.ENTITY_STATS.items() if stats["category"] == "building"]

print(tuple(building_unit))