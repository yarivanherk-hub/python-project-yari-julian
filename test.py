import pygame
import random

pygame.init()
# Scherm
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Uprising")


player_img = pygame.image.load("resources/player.jpg").convert_alpha()
enemy_img = pygame.image.load("resources/enemy1.webp").convert_alpha()
bullet_img = pygame.image.load("resources/bullet").convert_alpha()

player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
bullet_img = pygame.transform.scale(bullet_img, (50, 60))



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
player_speed = 5

# Bullets
bullets = []

# Enemies
enemies = []
enemy_spawn_timer = 0

score = 0
lives = 3

running = True

upgrade = None
upgrade_timer = 0

rapid_fire_level = 0
triple_shot_level = 0
shield = False
speed_level = 0

fire_delay = 15
fire_counter = 0

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

    speed = min(player_speed + speed_level * 0.4, 10)

    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= speed

    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += speed

    fire_counter += 1

    if keys[pygame.K_SPACE]:

        delay = max(3, 15 - rapid_fire_level * 0.6)

        if fire_counter >= delay:
            fire_counter = 0

           

            if triple_shot_level >= 2:

                bullets.append(pygame.Rect(player.centerx - 30, player.top, 6, 15))
                bullets.append(pygame.Rect(player.centerx - 15, player.top, 6, 15))
                bullets.append(pygame.Rect(player.centerx, player.top, 6, 15))
                bullets.append(pygame.Rect(player.centerx + 15, player.top, 6, 15))
                bullets.append(pygame.Rect(player.centerx + 30, player.top, 6, 15))
            
            elif triple_shot_level >= 1:
                bullets.append(pygame.Rect(player.centerx - 15, player.top, 6, 15))
                bullets.append(pygame.Rect(player.centerx, player.top, 6, 15))
                bullets.append(pygame.Rect(player.centerx + 15, player.top, 6, 15))
            else:
                bullets.append(pygame.Rect(player.centerx - 3, player.top, 6, 15))
    # Spawn enemies
    enemy_spawn_timer += 1

    if enemy_spawn_timer > 70:
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
        enemy.y += 2

        if enemy.top > HEIGHT:
            enemies.remove(enemy)
            lives -= 1

        if enemy.colliderect(player):
            enemies.remove(enemy)

            if shield:
                shield = False
            else:
                lives -= 1
    # move upgrades
    if upgrade:
        upgrade.y += 3

        if upgrade.y > HEIGHT:
            upgrade = None

        elif player.colliderect(upgrade):
        
            choice = random.choice(["rapid", "triple", "shield", "speed"])

            if choice == "rapid":
                rapid_fire_level += 1

            elif choice == "triple":
               triple_shot_level += 1

            elif choice == "shield":
                shield = True

            elif choice == "speed":
                speed_level += 1

        upgrade = None


    # Bullet collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:

            if bullet.colliderect(enemy):

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy in enemies:
                    enemies.remove(enemy)

                score += 10

                #kans op upgrade
                if random.random() < 0.1:
                    upgrade = pygame.Rect(
                        enemy.x,
                        enemy.y,
                        30,
                        30
                )

                break
    # Game over
    if lives <= 0:
        running = False

    # Draw
    screen.fill(BLACK)

    screen.blit(player_img, player)

    for bullet in bullets:
        screen.blit(bullet_img, bullet)

    for enemy in enemies:
        screen.blit(enemy_img, enemy)

    # Upgrade tekst bepalen
    upgrade_text = "Geen upgrade"

    if rapid_fire_level > 0:
        upgrade_text = f"Rapid Fire Lv.{rapid_fire_level}"
    elif triple_shot_level > 0:
        upgrade_text = f"Triple Shot Lv.{triple_shot_level}"
    elif shield:
        upgrade_text = "Shield"
    elif speed_level > 0:
        upgrade_text = f"Speed Boost Lv.{speed_level}"

    upgrade_surface = font.render(
        f"Upgrade: {upgrade_text}",
        True,
        WHITE
    )

    screen.blit(upgrade_surface, (10, 90))

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