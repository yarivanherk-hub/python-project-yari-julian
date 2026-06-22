import pygame
import random

pygame.init()
# Scherm
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Uprising")


player_img = pygame.image.load("resources/player.jpg").convert_alpha()
enemy_img= pygame.image.load("resources/enemy1.webp").convert_alpha()
enemy2_img = pygame.image.load("resources/enemy2.jpg").convert_alpha()
bullet_img = pygame.image.load("resources/bullet").convert_alpha()
bossfight1_img = pygame.image.load("resources/bossfight.jpg").convert_alpha()


player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
enemy2_img = pygame.transform.scale(enemy2_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (50, 60))
bossfight1_img = pygame.transform.scale(bossfight1_img, (80, 90))



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

#Bossfight
boss = None
boss_spawned = False

running = True

game_state = "menu"

highscore = 0

upgrades = []
upgrade_timer = 0

rapid_fire_level = 0
triple_shot_level = 0
shield = False
speed_level = 0

fire_delay = 15
fire_counter = 0

def draw_text(text, x, y, size=50):
        font_menu = pygame.font.SysFont(None, size)
        surface = font_menu.render(text, True, WHITE)
        screen.blit(surface, (x, y))



while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if game_state == "menu":
        # menu code
        screen.fill(BLACK)

        draw_text("GALACTIC UPRISING", 200, 100, 50)

        draw_text("SPACE = Start Game", 250, 250, 35)

        draw_text(
            f"Highscore: {highscore}",
            300,
            350,
            35
        )

        pygame.display.flip()


        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:

            # reset game
            score = 0
            lives = 3
            bullets.clear()
            enemies.clear()
            boss = None
            boss_spawned = False

            rapid_fire_level = 0
            triple_shot_level = 0
            speed_level = 0
            shield = False

            game_state = "playing"


    elif game_state == "playing":
        #huidige game code

        # Events
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

                    bullets.append(pygame.Rect(player.centerx - 30, player.top, 10, 15))
                    bullets.append(pygame.Rect(player.centerx - 15, player.top, 10, 15))
                    bullets.append(pygame.Rect(player.centerx, player.top, 10, 15))
                    bullets.append(pygame.Rect(player.centerx + 15, player.top, 10, 15))
                    bullets.append(pygame.Rect(player.centerx + 30, player.top, 10, 15))
            
                elif triple_shot_level >= 1:
                    bullets.append(pygame.Rect(player.centerx - 15, player.top, 10, 15))
                    bullets.append(pygame.Rect(player.centerx, player.top, 10, 15))
                    bullets.append(pygame.Rect(player.centerx + 15, player.top, 10, 15))
                else:
                    bullets.append(pygame.Rect(player.centerx - 3, player.top, 10, 15))
        # Spawn enemies
        enemy_spawn_timer += 1

        if enemy_spawn_timer > 70:
            enemy_spawn_timer = 0

            if random.random() < 0.2:  #kans op sterke enemy
                enemies.append({
                "rect": pygame.Rect(random.randint(0, WIDTH - 50), -50, 50, 50),
                "health": 3,
                "speed": 1,
                "type": "strong"
            })
            else:
                enemies.append({
                "rect": pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40),
                "health": 1,
                "speed": 2,
                "type": "normal"
            })

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= 10

            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move enemies
        for enemy in enemies[:]:
            enemy["rect"].y += enemy["speed"]
            
            if enemy["rect"].top > HEIGHT:
                enemies.remove(enemy)
                lives -= 1

            elif enemy["rect"].colliderect(player):
                enemies.remove(enemy)

                if shield:
                    shield = False
                else:
                    lives -= 1
        # move upgrades
        for upgrade in upgrades[:]:
            upgrade["rect"].y += 3

            if upgrade["rect"].y > HEIGHT:
                upgrades.remove(upgrade)

            elif player.colliderect(upgrade["rect"]):

                choice = upgrade["type"]
 
                if choice == "rapid":
                    rapid_fire_level += 1

                elif choice == "triple":
                    triple_shot_level += 1

                elif choice == "shield":
                    shield = True

                elif choice == "speed":
                    speed_level += 1

                upgrades.remove(upgrade)


        # Bullet collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:

                if bullet.colliderect(enemy["rect"]):
                    if bullet in bullets:
                        bullets.remove(bullet)

                        enemy["health"] -= 1

                        if enemy["health"] <= 0:

                            enemies.remove(enemy)

                            if enemy["type"] == "strong":
                                score += 30
                            else:
                                score += 10

                            if random.random() < 0.2:
                                upgrades.append ({
                                    "rect": pygame.Rect(enemy["rect"].x,
                                        enemy["rect"].y,
                                        30,
                                        30),
                                    "type": random.choice(
                                        ["rapid", "triple", "shield", "speed"]
                                    )
                                })

                    

                    break

        if boss:
            for bullet in bullets[:]:

                if boss and bullet.colliderect(boss["rect"]):

                    bullets.remove(bullet)

                    boss["health"] -= 1

                    print("Boss geraakt!", boss["health"])

                    if boss["health"] <= 0:
                        score += 500
                        boss = None

                
            
        if score >= 1000 and not boss_spawned:
            boss = {
                "rect": pygame.Rect(WIDTH // 2 - 100, 50, 200, 100),
                "health": 100,
                "speed": 3,
                "direction": 1
            }

            boss_spawned = True
            enemies.clear() #alle andere enemies weg

        # Boss movement
        if boss:

            boss["rect"].x += boss["speed"] * boss["direction"]

            if boss["rect"].left <= 0 or boss["rect"].right >= WIDTH:
                boss["direction"] *= -1

        # Game over
        if lives <= 0:

            if score > highscore:
                highscore = score

            game_state = "gameover"

    

        # Draw
        screen.fill(BLACK)

        #draw boss
        if boss:

            background = pygame.image.load("resources/achtergrondsterren.jpg")
            screen.blit(background, (0, 0))
            screen.blit(player_img, player)


            screen.blit(
                bossfight1_img,
                boss["rect"]
            )

            # health bar
            pygame.draw.rect(
                screen,
                RED,
                (200, 20, 400, 20)
            )

            pygame.draw.rect(
                screen,
                GREEN,
                (200, 20, boss["health"] * 4, 20)
            )
        
        #draw enemies
        for enemy in enemies:

            if enemy["type"] == "strong":
                screen.blit(enemy2_img, enemy["rect"])
            else:
                screen.blit(enemy_img, enemy["rect"])

        if upgrades:

            for upgrade in upgrades:
                color = WHITE

                if upgrade["type"] == "rapid":
                    color = RED

                elif upgrade["type"] == "triple":
                    color = BLUE

                elif upgrade["type"] == "shield":
                    color = GREEN

                elif upgrade["type"] == "speed":
                    color = (255, 255, 0)  # geel

                pygame.draw.rect(screen, color, upgrade["rect"])

        for bullet in bullets:
            screen.blit(bullet_img, bullet)

        
        screen.blit(player_img, player)


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


    elif game_state == "gameover":

        screen.fill(BLACK)

        draw_text("GAME OVER", 280, 150, 60)

        draw_text(
            f"Score: {score}",
            330,
            250,
            40
        )

        draw_text(
            f"Highscore: {highscore}",
            300,
            320,
            40
        )  

        draw_text(
           "SPACE = opnieuw spelen",
            220,
            450,
            35
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:

                score = 0
                lives = 3

                bullets.clear()
                enemies.clear()

                rapid_fire_level = 0
                triple_shot_level = 0
                speed_level = 0
                shield = False

                upgrades.clear()

                player.x = WIDTH // 2 - 25
                player.y = HEIGHT - 70

                game_state = "playing"
   

pygame.quit()