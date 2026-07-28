import pygame
import Config as C
from building import Building
from units import Unit


class Minimap:
    def __init__(self, grid_map, width=200, height=150):
        self.grid_map = grid_map
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.terrain_cache = pygame.Surface((width, height))
        self.dirty = True  # force initial render

        self.scale_x = width / (C.MAP_WIDTH * C.TILE)
        self.scale_y = height / (C.MAP_HEIGHT * C.TILE)


    def rebuild_terrain_cache(self):
        self.terrain_cache.fill((0, 0, 0))
        for y in range(self.grid_map.h):
            for x in range(self.grid_map.w):
                color = C.TILE_COLORS[self.grid_map.tiles[y][x]]
                rect = pygame.Rect(
                    x * C.TILE * self.scale_x,
                    y * C.TILE * self.scale_y,
                    max(1, C.TILE * self.scale_x),
                    max(1, C.TILE * self.scale_y),
                )
                self.terrain_cache.fill(color, rect)
        self.dirty = False

    def render(self, units, buildings, camera_x, camera_y):
        if self.dirty:
            self.rebuild_terrain_cache()
        self.surface.blit(self.terrain_cache, (0, 0))

        entities = units + buildings

        for entity in entities:
            x = entity.x * self.scale_x
            y = entity.y * self.scale_y
            color = C.MINI_MAP_COLOURS[entity.team] if isinstance(entity, (Unit, Building)) else (200, 200, 200)
            size = 3 if isinstance(entity, Building) else 2
            pygame.draw.rect(self.surface, color, (x - size/2, y - size/2, size, size))

        self._draw_viewport(camera_x, camera_y)
        return self.surface

    def _draw_viewport(self, camera_x, camera_y):
        rect = pygame.Rect(
            camera_x * self.scale_x,
            camera_y * self.scale_y,
            C.GRID_W * C.TILE * self.scale_x,
            (C.GRID_H + 1) * C.TILE * self.scale_y,
        )
        pygame.draw.rect(self.surface, (255, 255, 255), rect, width=1)


    def handle_click(self, mouse_pos, minimap_screen_pos, camera):
        rel_x = mouse_pos[0] - minimap_screen_pos[0]
        rel_y = mouse_pos[1] - minimap_screen_pos[1]
        if 0 <= rel_x <= self.width and 0 <= rel_y <= self.height:
            world_x = rel_x / self.scale_x
            world_y = rel_y / self.scale_y
            camera.center_on(world_x, world_y)
            return True
        return False