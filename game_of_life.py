#!/usr/bin/env python3
import pygame
from pygame.locals import (K_ESCAPE, KEYDOWN)
import time
import random


##### functions for the game's logic #####
neighborhood_coordinates = [(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1)]

def generate_cell_neighborhood(cell):
    return [(cell[0] + coordinate[0], cell[1] + coordinate[1]) for coordinate in neighborhood_coordinates]

def generate_generation_neighborhood(generation):
    output = []
    for cell in generation:
        neighborhood = generate_cell_neighborhood(cell)
        for location in neighborhood:
            output.append(location)
    return list(set(output))

def num_live_neighbors(cell, generation):
    n = 0
    neighborhood = generate_cell_neighborhood(cell)
    for location in neighborhood:
        if location in generation:
            n += 1
    return n

def create_next_generation(current_generation):
    next_generation = []
    generation_neighborhood = generate_generation_neighborhood(current_generation)
    for location in generation_neighborhood:
        n = num_live_neighbors(location, current_generation)
        if n == 2:
            if location in current_generation:
                next_generation.append(location)
        elif n == 3:
            next_generation.append(location)
    return next_generation


##### gets input from user for size of first generation and generation speeds #####
time.sleep(.5)
number_of_cells = int(input("\n\n\nHow many cells would you like to have in the first generation?\n>>> "))
generation_rate = int((input("\n\n\nHow many generations do you want to have per second?\n>>> ")))


##### the GUI for the game #####
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750

class Generation(pygame.sprite.Sprite):
    def __init__(self):
        super(Generation, self).__init__()
        self.surf = pygame.Surface((10,10))
        self.surf.fill((255,255,255))
        self.surf_center = (
            (SCREEN_WIDTH - self.surf.get_width()) / 2,
            (SCREEN_HEIGHT - self.surf.get_height()) / 2
        )

### randomly generates first generation generation
first_generation_coordinates = []
for _ in range(number_of_cells):
    first_generation_coordinates.append((random.randint(-10,10), random.randint(-10,10)))
coordinates = first_generation_coordinates

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
generation = Generation()

### generation 1
screen.fill((0,0,0))
for cell in coordinates:
    screen.blit(generation.surf, (generation.surf_center[0] + (cell[0] * (generation.surf.get_width() + 1)), generation.surf_center[1] + (cell[1] * (generation.surf.get_width() + 1))))
pygame.display.flip()
number_of_generations = 1

### loop for new generations
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    coordinates = create_next_generation(coordinates)
    time.sleep(1 / generation_rate)
    screen.fill((0,0,0))
    for cell in coordinates:
        screen.blit(generation.surf, (generation.surf_center[0] + (cell[0] * (generation.surf.get_width() + 1)), generation.surf_center[1] + (cell[1] * (generation.surf.get_width() + 1))))
    pygame.display.flip()
    if coordinates == []:
        running = False
        time.sleep(1)
        break
    number_of_generations += 1

pygame.quit()
print("______________________________________END______________________________________")
print("\n\nStarting coordinates: \n%s" % (first_generation_coordinates))
print("\n\nNumber of generations at termination: %s" % (number_of_generations))
