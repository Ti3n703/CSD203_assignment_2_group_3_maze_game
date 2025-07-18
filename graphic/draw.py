import pygame
import random
# Universal color variables
BG_COLOR = (0,0,0)      # White background
WALL_COLOR = (66, 245, 72)          
WALL_THICKNESS = 4 # Universal wall thickness
SAFE_PLACE_COLOR = (9, 0, 64)
EXIT_COLOR = (0, 0, 255)        
PLAYER_COLOR = (255, 215, 0)  
Ghost_COLOR = 	(255, 0, 0)  
generate_speed = 0.005 # Speed of maze generation animation
from logic.graph import Graph
from logic.mazegenerator import maze_generator
from graphic.core import init_window
from graphic.entity import Player
from graphic.entity import Ghost
# draw raw grid
def draw_grid(screen, size, cell_size, color=WALL_COLOR):
    # Only draw the outer border, not all cell borders, to avoid double-thick walls
    for i in range(size + 1):
        # Vertical lines
        pygame.draw.line(screen, color, (i * cell_size, 0), (i * cell_size, size * cell_size), WALL_THICKNESS)
        # Horizontal lines
        pygame.draw.line(screen, color, (0, i * cell_size), (size * cell_size, i * cell_size), WALL_THICKNESS)

#draw maze based on graph structure
def draw_maze(screen, graph, size, cell_size, wall_color=WALL_COLOR, bg_color=BG_COLOR, safe_places=None):
    screen.fill(bg_color)
    if safe_places is None:
        safe_places = []
    draw_safe_places(screen, safe_places, cell_size)
    for row in range(size):
        for col in range(size):
            current = f"{row},{col}"
            x = col * cell_size
            y = row * cell_size

            neighbors = graph.vertices_list.get(current, {})

            # Top wall
            if f"{row-1},{col}" not in neighbors:
                pygame.draw.line(screen, wall_color, (x, y), (x + cell_size, y), WALL_THICKNESS)
            # Left wall
            if f"{row},{col-1}" not in neighbors:
                pygame.draw.line(screen, wall_color, (x, y), (x, y + cell_size), WALL_THICKNESS)
            # Bottom wall
            if f"{row+1},{col}" not in neighbors:
                pygame.draw.line(screen, wall_color, (x, y + cell_size), (x + cell_size, y + cell_size), WALL_THICKNESS)
            # Right wall
            if f"{row},{col+1}" not in neighbors:
                pygame.draw.line(screen, wall_color, (x + cell_size, y), (x + cell_size, y + cell_size), WALL_THICKNESS)

# Draw the player at a given position
def draw_player(screen, x, y, cell_size, color=PLAYER_COLOR):
    px = x * cell_size + cell_size // 2
    py = y * cell_size + cell_size // 2
    pygame.draw.circle(screen, color, (px, py), cell_size // 4)

# Draw the ghost at a given position
def draw_ghost(screen, x, y, cell_size, color=Ghost_COLOR):
    gx = x * cell_size + cell_size // 2
    gy = y * cell_size + cell_size // 2
    pygame.draw.circle(screen, color, (gx, gy), cell_size // 4)

# Draw the exit
def draw_exit(screen, x, y, cell_size, exit_color=EXIT_COLOR):
    ex = x * cell_size + cell_size // 2
    ey = y * cell_size + cell_size // 2
    pygame.draw.circle(screen, exit_color, (ex, ey), cell_size // 4)
#draw safe places, when play reach these places, they are safe from ghost
def draw_safe_places(screen, safe_places, cell_size, SAFE_PLACE_COLOR=SAFE_PLACE_COLOR):
    for y, x in safe_places:
        pygame.draw.rect(screen, SAFE_PLACE_COLOR, (x * cell_size + 2, y * cell_size + 2, cell_size - 4, cell_size - 4))


def draw_maze_animation(screen, graph, size, cell_size, build_steps, wall_color=WALL_COLOR, bg_color=BG_COLOR, delay=generate_speed):
    import time
    from logic.graph import Graph
    temp_graph = Graph()
    temp_graph.add_grid(size)
    screen.fill(bg_color)
    draw_grid(screen, size, cell_size, color=wall_color)
    pygame.display.flip()
    time.sleep(0.5) #
    highlight_color = (255, 0, 0)  # Red
    for (cell1, cell2) in build_steps:
        # Event handling: Process Pygame events to prevent crashes on alt-tab
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() # Exit the program if the user closes the window during animation

        temp_graph.add_edge(cell1, cell2, 1)
        draw_maze(screen, temp_graph, size, cell_size, wall_color=wall_color, bg_color=bg_color)
        # Highlight the cell being carved
        row_from, col_from = map(int, cell1.split(','))
        x_from, y_from = col_from * cell_size, row_from * cell_size
        pygame.draw.rect(screen, highlight_color, (x_from+2, y_from+2, cell_size-4, cell_size-4))
        pygame.display.update()
        time.sleep(delay) # 
    # Final redraw to ensure all walls are correct
    draw_maze(screen, graph, size, cell_size, wall_color=wall_color, bg_color=bg_color)
    pygame.display.update()

# New function to draw text on the screen
def draw_text(screen, text, font_size, x, y, color=(215, 215, 215)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect # Return the rect for click detection

# New function for the main menu
def main_menu(screen, screen_width, screen_height):
    menu_running = True
    while menu_running:
        screen.fill(BG_COLOR) # Clear screen for menu
        title_rect = draw_text(screen, "Maze Game", 72, screen_width // 2, screen_height // 4)
        start_button_rect = draw_text(screen, "Start Game", 48, screen_width // 2, screen_height // 2)
        exit_button_rect = draw_text(screen, "Exit", 48, screen_width // 2, screen_height // 2 + 70)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "start" # User clicked Start Game
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
    return None # Should not be reached
