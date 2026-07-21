from PIL import Image
import Config as C

def tile_center(tx, ty):
    return tx * C.TILE + C.TILE//2, ty * C.TILE + C.TILE//2

def to_grid(pos):
    x, y = pos
    return int(x // C.TILE), int(y // C.TILE)

def convert_image_to_team(team, rider_type):

    stats = C.RIDER_CONFIG[rider_type]

    rider_image = stats["image"]

    image = Image.open(rider_image).convert("RGBA")
    pixels = list(image.getdata())

    old = stats["colour_to_be_converted"]

    new = team.colour
    bg_colour = (0, 0, 0, 255)

    updated = [
        (0, 0, 0, 0) if p == bg_colour                 # transparent if background
        else new if p[:3] == old[:3]                    # recoloured if team colour
        else p                                          # unchanged otherwise
        for p in pixels
    ]

    out = Image.new("RGBA", image.size)
    out.putdata(updated)                    
    return out


def tile_position(i, tiles_per_row, tile_size, row_gap, origin_x=C.ORIGIN_X, origin_y=C.ORIGIN_Y):
    row, col = divmod(i, tiles_per_row)
    if row % 2 == 1:  # odd rows go right-to-left
        col = tiles_per_row - 1 - col
    x = origin_x + col * tile_size
    y = origin_y + row * (tile_size + row_gap)
    return x, y, row, col


def get_colour(i):
    if i <= C.STARTING_LENGTH:
        return C.starting_colour
    elif i >= C.FINISH_LINE:
        return C.ending_colour
    return C.main_colour