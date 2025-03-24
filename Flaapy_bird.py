import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky blue color
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
FPS = 60


BIRD_IMAGE_PATH = "bird.png"        # Must be PNG
PIPE_IMAGE_PATH = "pipe.png"    # Must be PNG
BACKGROUND_IMAGE_PATH = "background.jpg"  # Remove if not using


try:
    # Load images with transparency
    bird_img = pygame.image.load(BIRD_IMAGE_PATH).convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (40, 40))

    pipe_img = pygame.image.load(PIPE_IMAGE_PATH).convert_alpha()
    pipe_img = pygame.transform.scale(pipe_img, (60, 400))

    # Load background if available
    bg_img = pygame.image.load(BACKGROUND_IMAGE_PATH).convert() if BACKGROUND_IMAGE_PATH else None
    if bg_img:
        bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print(f"Error loading images: {e}")
    sys.exit()

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Global variables
player_name = ""
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
GRAVITY = 0.5
FLAP_STRENGTH = -9
PIPE_SPEED = 4
pipe_width = 60
pipe_gap = 150
pipe_x = SCREEN_WIDTH
pipe_y = random.randint(200, 400)
score = 0
current_state = MENU

# Fonts
font = pygame.font.Font(None, 36)
name_font = pygame.font.Font(None, 32)

def draw_background():
    if bg_img:
        screen.blit(bg_img, (0, 0))
    else:
        screen.fill(BLUE)  # Fallback color

def draw_bird(x, y):
    screen.blit(bird_img, (x, y))

def draw_pipe(x, y):
    screen.blit(pygame.transform.flip(pipe_img, False, True), (x, y - pipe_img.get_height()))
    screen.blit(pipe_img, (x, y + pipe_gap))

def check_collision():
    bird_rect = pygame.Rect(bird_x, bird_y, bird_img.get_width(), bird_img.get_height())
    top_pipe_rect = pygame.Rect(pipe_x, pipe_y - pipe_img.get_height(), pipe_img.get_width(), pipe_img.get_height())
    bottom_pipe_rect = pygame.Rect(pipe_x, pipe_y + pipe_gap, pipe_img.get_width(), pipe_img.get_height())
    return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

def show_score_card():
    screen.fill(WHITE)
    draw_background()

    # Score card
    card_rect = pygame.Rect(50, 150, 300, 300)
    pygame.draw.rect(screen, GRAY, card_rect)

    text_y = 180
    texts = [
        f"Game Over!",
        f"Player: {player_name}",
        f"Final Score: {score}",
        "Press SPACE to play again",
        "Press Q to quit"
    ]

    for text in texts:
        rendered = font.render(text, True, BLACK)
        screen.blit(rendered, (SCREEN_WIDTH // 2 - rendered.get_width() // 2, text_y))
        text_y += 40

    pygame.display.update()

def game_loop():
    global bird_y, bird_velocity, pipe_x, pipe_y, score, current_state, player_name

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and player_name.strip():  # Ensure name isn't empty
                        current_state = PLAYING
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode

            elif current_state == PLAYING:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird_velocity = FLAP_STRENGTH

            elif current_state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Reset game
                        bird_y = SCREEN_HEIGHT // 2
                        bird_velocity = 0
                        pipe_x = SCREEN_WIDTH
                        pipe_y = random.randint(200, 400)
                        score = 0
                        current_state = PLAYING
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if current_state == MENU:
            # Draw menu screen
            draw_background()

            # Title
            title = font.render("Flappy Bird", True, BLACK)
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

            # Name input
            input_rect = pygame.Rect(100, 300, 200, 32)
            pygame.draw.rect(screen, pygame.Color('dodgerblue2'), input_rect, 2)
            name_surface = name_font.render(player_name, True, BLACK)
            screen.blit(name_surface, (input_rect.x + 5, input_rect.y + 5))

            # Instruction
            instr = font.render("Enter Name and Press ENTER", True, BLACK)
            screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, 400))

            pygame.display.update()

        elif current_state == PLAYING:
            # Game logic
            bird_velocity += GRAVITY
            bird_y += bird_velocity * dt * 60

            pipe_x -= PIPE_SPEED * dt * 60
            if pipe_x < -pipe_width:
                pipe_x = SCREEN_WIDTH
                pipe_y = random.randint(200, 400)
                score += 1

            if check_collision() or bird_y > SCREEN_HEIGHT or bird_y < 0:
                current_state = GAME_OVER

            # Draw game
            draw_background()
            draw_pipe(pipe_x, pipe_y)
            draw_bird(bird_x, bird_y)

            # Score display
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.update()

        elif current_state == GAME_OVER:
            show_score_card()

if __name__ == "__main__":
    game_loop()
