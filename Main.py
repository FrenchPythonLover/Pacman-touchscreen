import pygame
import sys
import math
import time
import random

# Pygame initialistion
pygame.init()

# Window configuration
WIDTH, HEIGHT = 1024, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Tactile")

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Maze parameter
CELL_SIZE = 40  
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

#  0=path 1=wall
maze = [  
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
     [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
     [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
     [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
     [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1], 
     [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
     [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
     [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
     ] 

# Pacman's initial position
pacman_pos = [9, 3]

dots = []
for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == 0:
            dots.append((x, y))

# Initial score
score = 0

# Clock to control speed
clock = pygame.time.Clock()
FPS = 15  

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            current_pos = pygame.mouse.get_pos()
            dx = current_pos[0] - start_pos[0]
            dy = current_pos[1] - start_pos[1]
          
            if abs(dx) > abs(dy):
                if dx > 0 and pacman_pos[0] + 1 < GRID_WIDTH and maze[pacman_pos[1]][pacman_pos[0] + 1] == 0:
                    pacman_pos[0] += 1
                elif dx < 0 and pacman_pos[0] - 1 >= 0 and maze[pacman_pos[1]][pacman_pos[0] - 1] == 0:
                    pacman_pos[0] -= 1
            else:
                if dy > 0 and pacman_pos[1] + 1 < GRID_HEIGHT and maze[pacman_pos[1] + 1][pacman_pos[0]] == 0:
                    pacman_pos[1] += 1
                elif dy < 0 and pacman_pos[1] - 1 >= 0 and maze[pacman_pos[1] - 1][pacman_pos[0]] == 0:
                    pacman_pos[1] -= 1

            start_pos = current_pos

    if (pacman_pos[0], pacman_pos[1]) in dots:
        dots.remove((pacman_pos[0], pacman_pos[1]))
        score += 1

    screen.fill(BLACK)

    # Draw the maze
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for dot in dots:
        pygame.draw.circle(screen, WHITE, (dot[0] * CELL_SIZE + CELL_SIZE // 2, dot[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 10)

    # Draw Pac-man
    pygame.draw.circle(screen, YELLOW, (pacman_pos[0] * CELL_SIZE + CELL_SIZE // 2, pacman_pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

    # Show score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
  
    pygame.display.flip()
  
    clock.tick(FPS)

pygame.quit()
sys.exit()

