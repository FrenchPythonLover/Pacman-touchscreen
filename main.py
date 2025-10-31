import pygame
import sys
import os
import math
#musique 
pygame.mixer.init()
pygame.mixer.music.load("pacman_beginning.wav")
pygame.mixer.music.play(1) 

# Activer le support tactile
os.environ['SDL_MOUSE_TOUCH_EVENTS'] = '1'

pygame.init()

# Constantes
CELL_SIZE = 40
GRID_WIDTH = 19
GRID_HEIGHT = 21
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE + 60

# Couleurs
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

# Labyrinthe
initial_maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,0,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class TouchController:
    """Contrôleur tactile amélioré avec détection directionnelle précise"""
    def __init__(self):
        self.touch_active = False
        self.start_pos = None
        self.current_pos = None
        self.last_direction = None
        self.min_distance = 15  # Distance minimale pour détecter un mouvement
        
    def start_touch(self, pos):
        self.touch_active = True
        self.start_pos = pos
        self.current_pos = pos
        
    def update_touch(self, pos):
        if self.touch_active:
            self.current_pos = pos
            
    def end_touch(self):
        direction = self.get_direction()
        self.touch_active = False
        self.start_pos = None
        self.current_pos = None
        return direction
        
    def get_direction(self):
        """Calcule la direction basée sur le mouvement tactile"""
        if not self.start_pos or not self.current_pos:
            return None
            
        dx = self.current_pos[0] - self.start_pos[0]
        dy = self.current_pos[1] - self.start_pos[1]
        
        # Calculer la distance totale
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.min_distance:
            return None
            
        # Calculer l'angle en degrés
        angle = math.degrees(math.atan2(dy, dx))
        
        # Convertir l'angle en direction (8 directions possibles, simplifiées en 4)
        # 0° = droite, 90° = bas, 180° = gauche, -90° = haut
        if -45 <= angle < 45:
            return 'right'
        elif 45 <= angle < 135:
            return 'down'
        elif angle >= 135 or angle < -135:
            return 'left'
        else:  # -135 <= angle < -45
            return 'up'
    
    def get_current_direction(self):
        """Obtenir la direction en temps réel pendant le toucher"""
        return self.get_direction()
    
    def draw_debug(self, screen):
        """Dessiner une ligne de debug pour montrer la direction du swipe"""
        if self.touch_active and self.start_pos and self.current_pos:
            pygame.draw.line(screen, GREEN, self.start_pos, self.current_pos, 3)
            pygame.draw.circle(screen, GREEN, self.start_pos, 10, 2)
            pygame.draw.circle(screen, YELLOW, self.current_pos, 8)

class PacMan:
    def __init__(self):
        self.x = 9
        self.y = 15
        self.direction = 'right'
        self.next_direction = 'right'
        self.mouth = 0
        self.mouth_speed = 15
        
    def can_move(self, x, y, maze):
        # Permettre le mouvement dans le tunnel (ligne 9 du tableau = y=9)
        if y == 9 and (x < 0 or x >= GRID_WIDTH):
            return True
        return 0 <= x < GRID_WIDTH and 0 <= y < len(maze) and maze[y][x] != 1
        
    def update(self, maze):
        print(self.y, self.x)
        # Essayer de changer de direction
        dirs = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        dx, dy = dirs[self.next_direction]
        if self.can_move(self.x + dx, self.y + dy, maze):
            self.direction = self.next_direction
        
        # Déplacement
        dx, dy = dirs[self.direction]
        nx, ny = self.x + dx, self.y + dy
        
        if self.can_move(nx, ny, maze):
            self.x, self.y = nx, ny
        
        # Téléportation dans le tunnel (ligne y=9)
        if self.y == 10:
            if self.x == 18:
                self.x = 0
            elif self.x == 0:
                self.x = 18
            
        self.mouth = (self.mouth + self.mouth_speed) % 360
        
    def draw(self, screen):
        cx = self.x * CELL_SIZE + CELL_SIZE // 2
        cy = self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        mouth_angle = abs(self.mouth - 180) // 6
        angle_map = {'right': 0, 'left': 180, 'up': 90, 'down': 270}
        angle_offset = angle_map[self.direction]
        
        pygame.draw.circle(screen, YELLOW, (cx, cy), radius)
        
        if mouth_angle > 0:
            points = [(cx, cy)]
            for angle in range(angle_offset + mouth_angle, angle_offset + 360 - mouth_angle, 5):
                rad = angle * 3.14159 / 180
                px = cx + radius * pygame.math.Vector2(1, 0).rotate(angle).x
                py = cy + radius * pygame.math.Vector2(1, 0).rotate(angle).y
                points.append((px, py))
            if len(points) > 2:
                pygame.draw.polygon(screen, YELLOW, points)

class Ghost:
    def __init__(self, x, y, color, personality='random'):
        self.x = x
        self.y = y
        self.color = color
        self.direction = 'up'
        self.personality = personality
        self.target_x = x
        self.target_y = y
        self.speed_counter = 0
        # Blinky (rouge) est plus lent
        self.speed_delay = 2 if personality == 'chaser' else 1
        
    def can_move(self, x, y, maze):
        # Permettre le mouvement dans le tunnel (ligne 9 du tableau = y=9)
        if y == 9 and (x < 0 or x >= GRID_WIDTH):
            return True
        return 0 <= x < GRID_WIDTH and 0 <= y < len(maze) and maze[y][x] != 1
    
    def get_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    
    def update(self, maze, pacman):
        import random
        
        # Contrôle de vitesse - Blinky se déplace moins souvent
        self.speed_counter += 1
        if self.speed_counter < self.speed_delay:
            return
        self.speed_counter = 0
        
        dirs = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
        
        if self.personality == 'chaser':
            # Blinky (Rouge) - Poursuit directement Pac-Man de manière agressive
            if random.randint(0, 2) == 0:
                self.target_x = pacman.x
                self.target_y = pacman.y
                
                best_dir = self.direction
                best_dist = float('inf')
                
                for direction, (dx, dy) in dirs.items():
                    nx, ny = self.x + dx, self.y + dy
                    if self.can_move(nx, ny, maze):
                        dist = self.get_distance(nx, ny, self.target_x, self.target_y)
                        if dist < best_dist:
                            best_dist = dist
                            best_dir = direction
                
                self.direction = best_dir
        
        elif self.personality == 'ambusher':
            # Pinky (Rose) - Essaie d'anticiper et bloquer le chemin de Pac-Man
            if random.randint(0, 3) == 0:
                # Vise 4 cases devant Pac-Man
                predict_dirs = {'up': (0, -4), 'down': (0, 4), 'left': (-4, 0), 'right': (4, 0)}
                dx, dy = predict_dirs[pacman.direction]
                self.target_x = pacman.x + dx
                self.target_y = pacman.y + dy
                
                best_dir = self.direction
                best_dist = float('inf')
                
                for direction, (dx, dy) in dirs.items():
                    nx, ny = self.x + dx, self.y + dy
                    if self.can_move(nx, ny, maze):
                        dist = self.get_distance(nx, ny, self.target_x, self.target_y)
                        if dist < best_dist:
                            best_dist = dist
                            best_dir = direction
                
                self.direction = best_dir
        
        elif self.personality == 'patrol':
            # Inky (Cyan) - Patrouille les coins, imprévisible
            if random.randint(0, 4) == 0:
                corners = [(1, 1), (GRID_WIDTH-2, 1), (1, len(maze)-2), (GRID_WIDTH-2, len(maze)-2)]
                self.target_x, self.target_y = random.choice(corners)
                
                best_dir = self.direction
                best_dist = float('inf')
                
                for direction, (dx, dy) in dirs.items():
                    nx, ny = self.x + dx, self.y + dy
                    if self.can_move(nx, ny, maze):
                        dist = self.get_distance(nx, ny, self.target_x, self.target_y)
                        if dist < best_dist:
                            best_dist = dist
                            best_dir = direction
                
                self.direction = best_dir
        
        elif self.personality == 'shy':
            # Clyde (Orange) - Timide, fuit si trop proche, sinon poursuit
            distance_to_pacman = self.get_distance(self.x, self.y, pacman.x, pacman.y)
            
            if random.randint(0, 3) == 0:
                if distance_to_pacman < 8:
                    # Fuir Pac-Man
                    self.target_x = GRID_WIDTH - 1 - pacman.x
                    self.target_y = len(maze) - 1 - pacman.y
                else:
                    # Poursuivre Pac-Man
                    self.target_x = pacman.x
                    self.target_y = pacman.y
                
                best_dir = self.direction
                best_dist = float('inf') if distance_to_pacman >= 8 else -float('inf')
                
                for direction, (dx, dy) in dirs.items():
                    nx, ny = self.x + dx, self.y + dy
                    if self.can_move(nx, ny, maze):
                        dist = self.get_distance(nx, ny, self.target_x, self.target_y)
                        if distance_to_pacman >= 8:
                            if dist < best_dist:
                                best_dist = dist
                                best_dir = direction
                        else:
                            if dist > best_dist:
                                best_dist = dist
                                best_dir = direction
                
                self.direction = best_dir
        
        # Mouvement
        dx, dy = dirs[self.direction]
        nx, ny = self.x + dx, self.y + dy
        
        if self.can_move(nx, ny, maze):
            self.x, self.y = nx, ny
            
            # Téléportation dans le tunnel (ligne y=9)
            if self.y == 9:
                if self.x < 0:
                    self.x = GRID_WIDTH - 1
                elif self.x >= GRID_WIDTH:
                    self.x = 0
        else:
            # Si bloqué, choisir une direction aléatoire valide
            import random
            valid_dirs = [d for d, (dx, dy) in dirs.items() 
                         if self.can_move(self.x + dx, self.y + dy, maze)]
            if valid_dirs:
                self.direction = random.choice(valid_dirs)
            
    def draw(self, screen):
        cx = self.x * CELL_SIZE + CELL_SIZE // 2
        cy = self.y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 2
        
        pygame.draw.circle(screen, self.color, (cx, cy - 3), radius)
        pygame.draw.rect(screen, self.color, (cx - radius, cy - 3, radius * 2, radius))
        
        pygame.draw.circle(screen, WHITE, (cx - 6, cy - 6), 5)
        pygame.draw.circle(screen, WHITE, (cx + 6, cy - 6), 5)
        pygame.draw.circle(screen, BLACK, (cx - 6, cy - 6), 2)
        pygame.draw.circle(screen, BLACK, (cx + 6, cy - 6), 2)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        
    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_maze(screen, maze):
    for y in range(len(maze)):
        for x in range(GRID_WIDTH):
            cell = maze[y][x]
            if cell == 1:
                pygame.draw.rect(screen, BLUE, 
                               (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
            elif cell == 2:
                pygame.draw.circle(screen, WHITE, 
                                 (x * CELL_SIZE + CELL_SIZE // 2, 
                                  y * CELL_SIZE + CELL_SIZE // 2), 3)
            elif cell == 3:
                pygame.draw.circle(screen, WHITE, 
                                 (x * CELL_SIZE + CELL_SIZE // 2, 
                                  y * CELL_SIZE + CELL_SIZE // 2), 7)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man Tactile Amélioré")
    clock = pygame.time.Clock()
    
    maze = [row[:] for row in initial_maze]
    pacman = PacMan()
    ghosts = [
        Ghost(9, 9, RED, 'chaser'),      # Blinky - Poursuiveur agressif
        Ghost(8, 9, PINK, 'ambusher'),   # Pinky - Tend des embuscades
        Ghost(10, 9, CYAN, 'patrol'),    # Inky - Patrouille imprévisible
        Ghost(9, 10, ORANGE, 'shy')      # Clyde - Timide
    ]
    
    touch_controller = TouchController()
    score = 0
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 28)
    game_over = False
    show_debug = False  # Mettre à True pour voir les lignes de debug
    
    restart_btn = Button(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 60, "REJOUER", YELLOW)
    
    frame = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Support clavier
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    pacman.next_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = 'down'
                elif event.key == pygame.K_LEFT:
                    pacman.next_direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = 'right'
                elif event.key == pygame.K_d:  # Toggle debug
                    show_debug = not show_debug
            
            # Début du toucher
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                if game_over and restart_btn.is_clicked(pos):
                    maze = [row[:] for row in initial_maze]
                    pacman = PacMan()
                    ghosts = [
                        Ghost(9, 9, RED, 'chaser'),
                        Ghost(8, 9, PINK, 'ambusher'),
                        Ghost(10, 9, CYAN, 'patrol'),
                        Ghost(9, 10, ORANGE, 'shy')
                    ]
                    score = 0
                    game_over = False
                else:
                    touch_controller.start_touch(pos)
            
            elif event.type == pygame.FINGERDOWN:
                pos = (int(event.x * WIDTH), int(event.y * HEIGHT))
                
                if game_over and restart_btn.is_clicked(pos):
                    maze = [row[:] for row in initial_maze]
                    pacman = PacMan()
                    ghosts = [
                        Ghost(9, 9, RED, 'chaser'),
                        Ghost(8, 9, PINK, 'ambusher'),
                        Ghost(10, 9, CYAN, 'patrol'),
                        Ghost(9, 10, ORANGE, 'shy')
                    ]
                    score = 0
                    game_over = False
                else:
                    touch_controller.start_touch(pos)
            
            # Mouvement du toucher
            elif event.type == pygame.MOUSEMOTION:
                if touch_controller.touch_active:
                    touch_controller.update_touch(event.pos)
                    # Mise à jour en temps réel
                    direction = touch_controller.get_current_direction()
                    if direction and not game_over:
                        pacman.next_direction = direction
            
            elif event.type == pygame.FINGERMOTION:
                if touch_controller.touch_active:
                    pos = (int(event.x * WIDTH), int(event.y * HEIGHT))
                    touch_controller.update_touch(pos)
                    # Mise à jour en temps réel
                    direction = touch_controller.get_current_direction()
                    if direction and not game_over:
                        pacman.next_direction = direction
            
            # Fin du toucher
            elif event.type == pygame.MOUSEBUTTONUP:
                direction = touch_controller.end_touch()
                if direction and not game_over:
                    pacman.next_direction = direction
            
            elif event.type == pygame.FINGERUP:
                direction = touch_controller.end_touch()
                if direction and not game_over:
                    pacman.next_direction = direction
        
        if not game_over:
            frame += 1
            
            if frame % 8 == 0:
                pacman.update(maze)
                
                # Manger les pastilles
                if maze[pacman.y][pacman.x] == 2:
                    maze[pacman.y][pacman.x] = 0
                    score += 10
                elif maze[pacman.y][pacman.x] == 3:
                    maze[pacman.y][pacman.x] = 0
                    score += 50
                
                # Mise à jour des fantômes
                for ghost in ghosts:
                    ghost.update(maze, pacman)
                    
                    if pacman.x == ghost.x and pacman.y == ghost.y:
                        game_over = True
        
        # Dessin
        screen.fill(BLACK)
        draw_maze(screen, maze)
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
        
        # Debug visuel
        if show_debug:
            touch_controller.draw_debug(screen)
        
        # Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 50))
        
        if not game_over:
            # Instructions
            info_text = small_font.render("Slide in the desired direction", True, YELLOW)
            text_rect = info_text.get_rect(center=(WIDTH//2, HEIGHT - 25))
            screen.blit(info_text, text_rect)
        else:
            # Game Over
            game_over_text = font.render("GAME OVER!", True, RED)
            go_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
            screen.blit(game_over_text, go_rect)
            
            final_score_text = small_font.render(f"Score Final: {score}", True, WHITE)
            fs_rect = final_score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
            screen.blit(final_score_text, fs_rect)
            
            restart_btn.draw(screen, font)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
