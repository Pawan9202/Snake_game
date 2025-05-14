import pygame
import random
import sys
from collections import deque

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL_SIZE = WIDTH // COLS
FPS = 15

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (144, 238, 144)
LIGHT_BLUE = (173, 216, 230)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

score_font = pygame.font.SysFont('Arial', 30)
gameover_font = pygame.font.SysFont('Arial', 50)
restart_font = pygame.font.SysFont('Arial', 25)

def draw_rect(color, pos, border_radius=0):
    pygame.draw.rect(screen, color, (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE), border_radius=border_radius)

def draw_text(text, font, color, position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def spawn_food(snake):
    while True:
        pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if pos not in snake:
            return pos

def update_grid(grid, snake, food):
    for y in range(ROWS):
        for x in range(COLS):
            grid[y][x] = 0
    for x, y in snake:
        if 0 <= x < COLS and 0 <= y < ROWS:
            grid[y][x] = 1
    fx, fy = food
    if 0 <= fx < COLS and 0 <= fy < ROWS:
        grid[fy][fx] = 2

def bfs(start, goal, grid):
    directions = [UP, DOWN, LEFT, RIGHT]
    queue = deque([(start, [])])
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        for direction in directions:
            next_pos = (current[0] + direction[0], current[1] + direction[1])

            if 0 <= next_pos[0] < COLS and 0 <= next_pos[1] < ROWS and next_pos not in visited and grid[next_pos[1]][next_pos[0]] != 1:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))

    return []

def game_over_screen(score):
    screen.fill(BLACK)
    draw_text("GAME OVER", gameover_font, YELLOW, (WIDTH // 6, HEIGHT // 3))
    draw_text(f"Final Score: {score}", gameover_font, LIGHT_GREEN, (WIDTH // 3, HEIGHT // 2))
    draw_text("Press R to Restart", restart_font, LIGHT_BLUE, (WIDTH // 3, HEIGHT // 1.5))
    pygame.display.flip()

def menu_screen():
    screen.fill(BLACK)
    draw_text("SNAKE GAME", gameover_font, YELLOW, (WIDTH // 6, HEIGHT // 3))
    draw_text("Press ENTER to Start", restart_font, LIGHT_GREEN, (WIDTH // 3, HEIGHT // 2))
    draw_text("Press Q to Quit", restart_font, LIGHT_BLUE, (WIDTH // 3, HEIGHT // 1.5))
    pygame.display.flip()

def main():
    snake = [(5, 5)]
    direction = RIGHT
    food = spawn_food(snake)
    score = 0
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    food_grow_animation = 0

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != DOWN:
            direction = UP
        elif keys[pygame.K_DOWN] and direction != UP:
            direction = DOWN
        elif keys[pygame.K_LEFT] and direction != RIGHT:
            direction = LEFT
        elif keys[pygame.K_RIGHT] and direction != LEFT:
            direction = RIGHT

        path = bfs(snake[0], food, grid)
        if path:
            next_step = path[0]
            direction = (next_step[0] - snake[0][0], next_step[1] - snake[0][1])

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (head in snake) or not (0 <= head[0] < COLS and 0 <= head[1] < ROWS):
            game_over_screen(score)
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            while not keys[pygame.K_r]:
                keys = pygame.key.get_pressed()
            main()

        snake.insert(0, head)
        if head == food:
            score += 1
            food = spawn_food(snake)
            food_grow_animation = 20
        else:
            snake.pop()

        update_grid(grid, snake, food)

        if food_grow_animation > 0:
            food_grow_animation -= 1
            draw_rect(RED, food, border_radius=5)
        else:
            draw_rect(RED, food, border_radius=5)

        for x in range(1, COLS):
            pygame.draw.line(screen, WHITE, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), 1)
        for y in range(1, ROWS):
            pygame.draw.line(screen, WHITE, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE), 1)

        for segment in snake:
            draw_rect(GREEN, segment, border_radius=5)

        draw_text(f"Score: {score}", score_font, LIGHT_GREEN, (10, 10))

        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 5)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    menu_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
