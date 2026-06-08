import pygame
import random

pygame.init()

# Scherm
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Uprising")

clock = pygame.time.Clock()

# Kleuren
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 36)

# Player
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 70, 50, 50)
player_speed = 6

# Bullets
bullets = []

# Enemies
enemies = []
enemy_spawn_timer = 0

score = 0
lives = 3

running = True

while running:
    clock.tick(60)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(
                    pygame.Rect(
                        player.centerx - 3,
                        player.top,
                        6,
                        15
                    )
                )

    # Input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed

    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Spawn enemies
    enemy_spawn_timer += 1

    if enemy_spawn_timer > 40:
        enemy_spawn_timer = 0

        enemies.append(
            pygame.Rect(
                random.randint(0, WIDTH - 40),
                -40,
                40,
                40
            )
        )

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= 10

        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        enemy.y += 3

        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            lives -= 1

        if enemy.colliderect(player):
            enemies.remove(enemy)
            lives -= 1

    # Bullet collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:

            if bullet.colliderect(enemy):

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy in enemies:
                    enemies.remove(enemy)

                score += 10
                break

    # Game over
    if lives <= 0:
        running = False

    # Draw
    screen.fill(BLACK)

    pygame.draw.rect(screen, BLUE, player)

    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, bullet)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    lives_text = font.render(
        f"Lives: {lives}",
        True,
        WHITE
    )

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    pygame.display.flip()

pygame.quit()