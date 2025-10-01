import pygame
import sys
import random

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TRACK_WIDTH = 400
CAR_WIDTH = 50
CAR_HEIGHT = 100
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 204, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 32)

# Load assets (placeholder rectangles for now)
def draw_car(x, y):
    pygame.draw.rect(screen, RED, (x, y, CAR_WIDTH, CAR_HEIGHT), border_radius=12)
    pygame.draw.rect(screen, BLACK, (x+10, y+70, 30, 20), border_radius=8)  # wheels

def draw_obstacle(x, y):
    pygame.draw.rect(screen, YELLOW, (x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT), border_radius=8)

def draw_track():
    track_x = (SCREEN_WIDTH - TRACK_WIDTH) // 2
    pygame.draw.rect(screen, GRAY, (track_x, 0, TRACK_WIDTH, SCREEN_HEIGHT))
    # Lane lines
    for i in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 5, i, 10, 20))

def main():
    car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
    car_y = SCREEN_HEIGHT - CAR_HEIGHT - 30
    car_speed = 7
    obstacles = []
    obstacle_timer = 0
    score = 0
    start_ticks = pygame.time.get_ticks()
    final_time = None
    running = True
    game_over = False

    while running:
        screen.fill(GREEN)
        draw_track()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] and car_x > (SCREEN_WIDTH - TRACK_WIDTH)//2:
                car_x -= car_speed
            if keys[pygame.K_RIGHT] and car_x < (SCREEN_WIDTH + TRACK_WIDTH)//2 - CAR_WIDTH:
                car_x += car_speed

        # Obstacles
        if not game_over:
            obstacle_timer += 1
            if obstacle_timer > 50:
                obs_x = random.randint((SCREEN_WIDTH - TRACK_WIDTH)//2, (SCREEN_WIDTH + TRACK_WIDTH)//2 - OBSTACLE_WIDTH)
                obstacles.append([obs_x, -OBSTACLE_HEIGHT])
                obstacle_timer = 0
            for obs in obstacles:
                obs[1] += 8
            obstacles = [obs for obs in obstacles if obs[1] < SCREEN_HEIGHT]

        # Draw car and obstacles
        draw_car(car_x, car_y)
        for obs in obstacles:
            draw_obstacle(obs[0], obs[1])

        # Collision detection
        for obs in obstacles:
            car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
            obs_rect = pygame.Rect(obs[0], obs[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            if car_rect.colliderect(obs_rect):
                if not game_over:
                    game_over = True
                    final_time = (pygame.time.get_ticks() - start_ticks) // 1000

        # Score and timer
        if not game_over:
            score += 1
            time_elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
        else:
            time_elapsed = final_time if final_time is not None else 0
        score_text = font.render(f"Score: {score}", True, BLACK)
        time_text = font.render(f"Time: {time_elapsed}s", True, BLACK)
        screen.blit(score_text, (20, 20))
        screen.blit(time_text, (20, 60))

        if game_over:
            over_text = font.render("Game Over! Press R to Restart", True, RED)
            screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//2))
            if keys[pygame.K_r]:
                main()
                return

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
