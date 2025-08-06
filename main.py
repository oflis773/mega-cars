import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 980
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мега машины")
clock = pygame.time.Clock()

ROAD_COLOR = (50, 50, 50)
LANE_LINE_COLOR = (200, 200, 200)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)

font = pygame.font.SysFont("arial", 30)
big_font = pygame.font.SysFont("arial", 60)

player_img = pygame.image.load("player.png")
player_img = pygame.transform.rotate(player_img, 90)
player_img = pygame.transform.scale(player_img, (180, 180))

enemy_img = pygame.image.load("bluecar.png")
enemy_img = pygame.transform.rotate(enemy_img, -90)
enemy_img = pygame.transform.scale(enemy_img, (100, 180))

LANES = 4
LANE_WIDTH = WIDTH // LANES
LANE_X = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(LANES)]

player_lane = 1
player_y = HEIGHT - 180 - 30

distance = 0
best_score = 0
enemy_speed = 6
enemy_accel = 0.002
enemy_cars = []

def spawn_enemy():
    lane = random.randint(0, LANES - 1)
    y = random.randint(-800, -200)
    enemy_cars.append({"lane": lane, "y": y})

for _ in range(3):
    spawn_enemy()

lane_lines = []
for y in range(0, HEIGHT, 80):
    lane_lines.append(y)

def draw_road():
    WIN.fill(ROAD_COLOR)
    for i in range(1, LANES):
        x = i * LANE_WIDTH
        pygame.draw.line(WIN, LANE_LINE_COLOR, (x, 0), (x, HEIGHT), 5)
    for i in range(len(lane_lines)):
        pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 5, lane_lines[i], 10, 40))

def draw_window():
    draw_road()
    player_x = LANE_X[player_lane] - player_img.get_width() // 2
    WIN.blit(player_img, (player_x, player_y))
    for enemy in enemy_cars:
        enemy_x = LANE_X[enemy["lane"]] - enemy_img.get_width() // 2
        WIN.blit(enemy_img, (enemy_x, enemy["y"]))
    score_text = font.render(f"{distance} м", True, WHITE)
    WIN.blit(score_text, (20, 20))
    best_text = font.render(f"Рекорд: {best_score} м", True, WHITE)
    WIN.blit(best_text, (20, 60))
    pygame.display.update()

def reset_game():
    global player_lane, enemy_cars, distance, enemy_speed
    player_lane = 1
    enemy_cars = []
    for _ in range(3):
        spawn_enemy()
    distance = 0
    enemy_speed = 6

def show_game_over():
    WIN.fill(GRAY)
    over_text = big_font.render("АВАРИЯ!", True, WHITE)
    retry_text = font.render("Нажми [Enter], чтобы сыграть снова", True, WHITE)
    WIN.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))
    WIN.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            waiting = False

run = True
while run:
    clock.tick(60)
    distance += 1
    enemy_speed += enemy_accel

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_lane > 0:
        player_lane -= 1
        pygame.time.wait(150)
    if keys[pygame.K_d] and player_lane < LANES - 1:
        player_lane += 1
        pygame.time.wait(150)

    for i in range(len(lane_lines)):
        lane_lines[i] += enemy_speed
        if lane_lines[i] > HEIGHT:
            lane_lines[i] = -40

    for enemy in enemy_cars:
        enemy["y"] += enemy_speed
    enemy_cars = [e for e in enemy_cars if e["y"] < HEIGHT + 200]
    if len(enemy_cars) < 4:
        spawn_enemy()

    crashed = False
    for enemy in enemy_cars:
        if enemy["lane"] == player_lane:
            px = LANE_X[player_lane] - player_img.get_width() // 2
            py = player_y
            ex = LANE_X[enemy["lane"]] - enemy_img.get_width() // 2
            ey = enemy["y"]
            player_rect = pygame.Rect(px, py, player_img.get_width(), player_img.get_height())
            enemy_rect = pygame.Rect(ex, ey, enemy_img.get_width(), enemy_img.get_height())
            if player_rect.colliderect(enemy_rect):
                crashed = True
                break

    if crashed:
        if distance > best_score:
            best_score = distance
        show_game_over()
        reset_game()
        continue

    draw_window()

pygame.quit()
sys.exit()
