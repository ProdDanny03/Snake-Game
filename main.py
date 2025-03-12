import pygame as pg
import sys
import random
import os

# Initialize Pygame
pg.init()

# Initialize the mixer for music
pg.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the display
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Snake Game")

# Clock to control the frame rate
clock = pg.time.Clock()

# Font for displaying score
font = pg.font.SysFont(None, 35)

# Get the base path for the executable
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Load and play background music
pg.mixer.music.load(os.path.join(base_path, "8bit_music.mp3"))
pg.mixer.music.play(-1)  # Play the music in a loop

# Load sound effect for game over
game_over_sound = pg.mixer.Sound(os.path.join(base_path, "game_over.mp3"))

def draw_snake(snake_body, color=GREEN):
    """Draw the snake on the screen."""
    for segment in snake_body:
        pg.draw.rect(screen, color, pg.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food(food_position):
    """Draw the food on the screen."""
    pg.draw.rect(screen, RED, pg.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE))

def show_score(score):
    """Display the current score on the screen."""
    score_surface = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surface, (10, 10))

def generate_food_position(snake_body):
    """Generate a new position for the food, ensuring it does not overlap with the snake."""
    while True:
        position = [
            random.randrange(1, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randrange(1, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        ]
        if position not in snake_body:
            return position

def main():
    """Main game loop."""
    # Initial snake position and body
    snake_position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    snake_body = [
        list(snake_position),
        [snake_position[0] - CELL_SIZE, snake_position[1]],
        [snake_position[0] - (2 * CELL_SIZE), snake_position[1]]
    ]
    direction = 'RIGHT'
    change_to = direction

    # Hide the cursor
    pg.mouse.set_visible(False)

    # Initial food position
    food_position = generate_food_position(snake_body)
    food_spawn = True

    score = 0

    while True:
        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif (event.key == pg.K_w or event.key == pg.K_UP) and direction != 'DOWN':
                    change_to = 'UP'
                elif (event.key == pg.K_s or event.key == pg.K_DOWN) and direction != 'UP':
                    change_to = 'DOWN'
                elif (event.key == pg.K_a or event.key == pg.K_LEFT) and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif (event.key == pg.K_d or event.key == pg.K_RIGHT) and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Update the direction immediately
        if change_to == 'UP' and direction != 'DOWN':
            direction = change_to
        if change_to == 'DOWN' and direction != 'UP':
            direction = change_to
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = change_to
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = change_to

        # Update the snake position
        if direction == 'UP':
            snake_position[1] -= CELL_SIZE
        elif direction == 'DOWN':
            snake_position[1] += CELL_SIZE
        elif direction == 'LEFT':
            snake_position[0] -= CELL_SIZE
        elif direction == 'RIGHT':
            snake_position[0] += CELL_SIZE

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_position))
        snake_head_rect = pg.Rect(snake_position[0], snake_position[1], CELL_SIZE, CELL_SIZE)
        food_rect = pg.Rect(food_position[0], food_position[1], CELL_SIZE, CELL_SIZE)
        
        if snake_head_rect.colliderect(food_rect):
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_position = generate_food_position(snake_body)
        food_spawn = True

        # Clear the screen
        screen.fill(BLACK)

        # Draw the snake and food
        draw_snake(snake_body)
        draw_food(food_position)

        # Check for collisions
        if (snake_position[0] < 0 or snake_position[0] >= SCREEN_WIDTH or
            snake_position[1] < 0 or snake_position[1] >= SCREEN_HEIGHT):
            game_over(snake_body)
        for block in snake_body[1:]:
            if snake_position == block:
                game_over(snake_body)

        # Display the score
        show_score(score)

        # Update the display
        pg.display.update()

        # Control the frame rate
        clock.tick(15)

def game_over(snake_body):
    """Handle game over scenario."""
    pg.mixer.music.set_volume(1.5)
    game_over_sound.play()
    
    # Make the whole snake body red
    draw_snake(snake_body, color=RED)
    pg.display.update()
    
    # Make the snake disappear piece by piece from the tail to the head
    delay = 1000 // len(snake_body)  # Calculate delay to remove each piece in 1 second
    for segment in reversed(snake_body):
        pg.time.wait(delay)
        snake_body.pop()
        screen.fill(BLACK)
        draw_snake(snake_body, color=RED)
        pg.display.update()
    
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
