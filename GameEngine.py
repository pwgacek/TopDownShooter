import pygame
from Hero import Hero
from Map import Map


class GameEngine:
    def __init__(self):
        pygame.init()
        # self.screen = pygame.Surface((800, 600))
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Top-Down Shooter")

    def run(self):
        w, h = self.screen.get_size()
        running = True
        game_map = Map(w, h)

        while running:
            self.screen.fill((0, 255, 0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_w:
                        game_map.hero.dir["up"] = True
                    if event.key == pygame.K_s:
                        game_map.hero.dir["down"] = True
                    if event.key == pygame.K_a:
                        game_map.hero.dir["left"] = True
                    if event.key == pygame.K_d:
                        game_map.hero.dir["right"] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        game_map.hero.dir["up"] = False
                    if event.key == pygame.K_s:
                        game_map.hero.dir["down"] = False
                    if event.key == pygame.K_a:
                        game_map.hero.dir["left"] = False
                    if event.key == pygame.K_d:
                        game_map.hero.dir["right"] = False

            game_map.move_hero()
            x, y = game_map.get_camera_position()
            self.screen.blit(game_map.image, pygame.math.Vector2(0, 0), pygame.Rect(x, y, 800, 600))

            self.screen.blit(game_map.hero.rot_center(), game_map.hero.screen_position)
            #print(game_map.hero.map_position)


            pygame.display.update()
