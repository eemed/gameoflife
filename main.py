#!/usr/bin/env python3

import pygame
import sys
import itertools
import time
import random
import math

ON = pygame.Color(244, 241, 66)
BG = pygame.Color(142, 36, 170)


def redraw(screen, bg_color, state, blocksize):
    """redraw screen with blocks"""

    block_width, block_height = blocksize

    screen.fill(bg_color)

    for pos, color in state.items():
        x, y = pos
        rect = pygame.Rect(
            x * block_width,
            y * block_height,
            block_width,
            block_height)
        pygame.draw.rect(screen, color, rect)

    pygame.display.flip()


def next_state(state, gridsize):
    next_state = {}
    grid_x, grid_y = gridsize
    for x in range(grid_x):
        for y in range(grid_y):
            pos = x, y
            is_on = pos in state

            neighbors = get_neighbors(pos, gridsize)
            on_amount = len([
                neighbor for neighbor in neighbors if neighbor in state
            ])

            # We are creating a new state so everythin is off by default
            # We can focus on conditions that produce active cells

            # 2. condition
            if is_on and on_amount in [2, 3]:
                next_state[pos] = ON
                continue

            # 4. condition
            if not is_on and on_amount == 3:
                next_state[pos] = ON
                continue

    return next_state


def get_neighbors(pos, maximum):
    x, y = pos

    max_x, max_y = maximum
    neighbors = list(itertools.product(
        list(range(x-1, x+2)),
        list(range(y-1, y+2))
    ))

    def filter_excessive(e):
        e_x, e_y = e
        # Is in boundaries and is not itself
        return (e_x >= 0 and
                e_x < max_x and
                e_y >= 0 and
                e_y < max_y and
                (e_x != x or e_y != y))

    neighbors = filter(filter_excessive, neighbors)
    return neighbors


def main():
    pygame.display.init()
    size = width, height = 1200, 900
    gridsize = 60, 60
    blocksize = (
        math.floor(size[0] / gridsize[0]),
        math.floor(size[1] / gridsize[1])
    )
    screen = pygame.display.set_mode(size)

    glider_state = {
        (1, 0): ON,
        (2, 1): ON,
        (0, 2): ON,
        (1, 2): ON,
        (2, 2): ON,
    }


    glider_gun = {
        (1, 5): ON,
        (2, 5): ON,
        (1, 6): ON,
        (2, 6): ON,
        (11, 5): ON,
        (11, 6): ON,
        (11, 7): ON,
        (12, 4): ON,
        (12, 8): ON,
        (13, 3): ON,
        (13, 9): ON,
        (14, 3): ON,
        (14, 9): ON,
        (15, 6): ON,
        (16, 4): ON,
        (16, 8): ON,
        (17, 5): ON,
        (17, 6): ON,
        (17, 7): ON,
        (18, 6): ON,
        (21, 3): ON,
        (21, 4): ON,
        (21, 5): ON,
        (22, 3): ON,
        (22, 4): ON,
        (22, 5): ON,
        (23, 2): ON,
        (23, 6): ON,
        (25, 1): ON,
        (25, 2): ON,
        (25, 6): ON,
        (25, 7): ON,
        (35, 3): ON,
        (35, 4): ON,
        (36, 3): ON,
        (36, 4): ON,
    }
    war = {(gridsize[0] - y, gridsize[1] - x): ON
           for x, y in glider_gun.keys()}

    war.update(glider_gun)

    random_state = {(x, y): ON
                    for x in range(gridsize[0]) for y in range(gridsize[1])
                    if random.random() > 0.6}
    state = war
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
        redraw(screen, BG, state, blocksize)
        pygame.time.wait(15)
        state = next_state(state, gridsize)


main()
