import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH = 700
HEIGHT = 800
PLAY_AREA = 600
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
FLAG_COLORS = [
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 165, 0)   # Orange
]

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flag Capture Game")

# Circle properties
circle_radius = 30
circle_x = WIDTH // 2
circle_y = HEIGHT // 2
circle_speed = 5

# Flag properties
flags = []
flag_width = 30
flag_height = 40
pole_width = 5
pole_height = 50
score = 0
flags_captured = 0

# Create flags at random positions
play_area_x = (WIDTH - PLAY_AREA) // 2
play_area_y = (HEIGHT - PLAY_AREA) // 2

for i in range(6):
    flag_x = random.randint(play_area_x + pole_width, play_area_x + PLAY_AREA - flag_width)
    flag_y = random.randint(play_area_y + pole_height, play_area_y + PLAY_AREA - pole_height)
    flags.append({
        'x': flag_x,
        'y': flag_y,
        'color': FLAG_COLORS[i],
        'captured': False
    })

# Font for score display
font = pygame.font.SysFont(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Move the circle based on arrow key presses
        if keys[pygame.K_LEFT] and circle_x - circle_radius > play_area_x:
            circle_x -= circle_speed
        if keys[pygame.K_RIGHT] and circle_x + circle_radius < play_area_x + PLAY_AREA:
            circle_x += circle_speed
        if keys[pygame.K_UP] and circle_y - circle_radius > play_area_y:
            circle_y -= circle_speed
        if keys[pygame.K_DOWN] and circle_y + circle_radius < play_area_y + PLAY_AREA:
            circle_y += circle_speed
        
        # Check for flag captures
        for flag in flags:
            if not flag['captured']:
                # Check if circle overlaps with flag
                if (abs(circle_x - flag['x']) < circle_radius + pole_width and 
                    abs(circle_y - flag['y']) < circle_radius + pole_height):
                    flag['captured'] = True
                    score += 50
                    flags_captured += 1
                    
                    # Check if all flags are captured
                    if flags_captured == 6:
                        game_over = True
    
    # Fill the screen with black
    screen.fill(BLACK)
    
    # Draw the flags
    for flag in flags:
        if not flag['captured']:
            # Draw pole
            pygame.draw.rect(screen, BROWN, (flag['x'], flag['y'] - pole_height, pole_width, pole_height))
            
            # Draw triangular flag
            flag_points = [
                (flag['x'] + pole_width, flag['y'] - pole_height),
                (flag['x'] + pole_width + flag_width, flag['y'] - pole_height + flag_height // 2),
                (flag['x'] + pole_width, flag['y'] - pole_height + flag_height)
            ]
            pygame.draw.polygon(screen, flag['color'], flag_points)
    
    # Draw the circle
    pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))
    
    # Draw game over message
    if game_over:
        game_over_text = font.render("Game Over! All flags captured!", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()