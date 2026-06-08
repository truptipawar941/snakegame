import pygame
import random
import os

pygame.init()

# SCREEN
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Python Project")

clock = pygame.time.Clock()

# COLORS
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 35)

# HIGH SCORE FILE
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        return int(open(HIGH_SCORE_FILE).read())
    return 0

def save_high_score(score):
    open(HIGH_SCORE_FILE, "w").write(str(score))

high_score = load_high_score()

# RESET GAME
def reset():
    snake = [100, 50]
    body = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    food = [random.randrange(1, WIDTH//10)*10,
            random.randrange(1, HEIGHT//10)*10]
    score = 0
    lives = 3
    return snake, body, direction, food, score, lives

snake, body, direction, food, score, lives = reset()
change_to = direction

state = "START"

# PERFORMANCE MESSAGE
def performance(score):
    if score >= 20:
        return "🔥 BEST"
    elif score >= 10:
        return "👍 BETTER"
    else:
        return "🙂 AVERAGE"

def draw_text(text, x, y, color=WHITE, size=font):
    screen.blit(size.render(text, True, color), (x, y))

# GAME LOOP
running = True

while running:
    screen.fill(BLACK)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if state == "START":
                if event.key == pygame.K_RETURN:
                    state = "PLAY"

            if event.key == pygame.K_r:
                snake, body, direction, food, score, lives = reset()
                change_to = direction
                state = "START"

            if state == "PLAY":
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"

    # START SCREEN
    if state == "START":
        draw_text("SNAKE GAME PROJECT", 170, 100, GREEN, big_font)
        draw_text("Press ENTER to Start", 190, 170)
        draw_text("Python + Pygame Project", 190, 200)
        pygame.display.update()
        continue

    # MOVE SNAKE
    direction = change_to

    if direction == "UP":
        snake[1] -= 10
    if direction == "DOWN":
        snake[1] += 10
    if direction == "LEFT":
        snake[0] -= 10
    if direction == "RIGHT":
        snake[0] += 10

    body.insert(0, list(snake))

    # FOOD
    if snake == food:
        score += 1
        food = [random.randrange(1, WIDTH//10)*10,
                random.randrange(1, HEIGHT//10)*10]
    else:
        body.pop()

    # DRAW FOOD
    pygame.draw.rect(screen, RED, (food[0], food[1], 10, 10))

    # DRAW SNAKE
    for b in body:
        pygame.draw.rect(screen, GREEN, (b[0], b[1], 10, 10))

    # UI
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", 10, 30)
    draw_text(f"High Score: {high_score}", 10, 50)

    # WALL COLLISION (3 LIVES)
    if snake[0] < 0 or snake[0] >= WIDTH or snake[1] < 0 or snake[1] >= HEIGHT:
        lives -= 1
        snake = [100, 50]
        body = [[100, 50], [90, 50], [80, 50]]

        if lives <= 0:
            state = "GAMEOVER"

    # GAME OVER
    if state == "GAMEOVER":
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        draw_text("GAME OVER", 220, 150, RED, big_font)
        draw_text(performance(score), 240, 200, YELLOW)
        draw_text("Press R to Restart", 200, 240)

    pygame.display.update()
    clock.tick(10)

pygame.quit()