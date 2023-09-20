# AI_BattleShip_Environment
import pygame

class AiBattleshipEnvironment():
    def __init__(self):
    self.x = 300
    self.y = 500

    de# Initialize pygame
    pygame.init()

    # Create screen and set dimensions
    screen = pygame.display.set_mode((600, 600))

    # Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Blue_1 attributes
blue_1_pos = [300, 500]
blue_1_color = BLUE
blue_1_health = 1
blue_1_weapon_range = 150
blue_1_actions = ["move_east", "move_west", "move_south", "move_north", "fire"]
blue_1_speed = [0, 1, 2, 3]

# Red_1 attributes
red_1_pos = [300, 100]
red_1_color = RED
red_1_health = 1
red_1_weapon_range = 130
red_1_speed = [0, 1, 2]

def draw_red_line():
    pygame.draw.line(screen, RED, (0, 300), (600, 300), 1)

def draw_ship(pos, color):
    pygame.draw.circle(screen, color, pos, 5)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def main():
    running = True
    while running:
        # Fill screen with white background
        screen.fill(WHITE)

        # Draw red line in the center
        draw_red_line()

        # Draw ships
        draw_ship(blue_1_pos, blue_1_color)
        draw_ship(red_1_pos, red_1_color)

        # Update the display
        pygame.display.flip()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Implement your reinforcement learning algorithm here

    pygame.quit()

if __name__ == "__main__":
    main()
