import pygame
import random
import math

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")
# Ustawienia gry
FPS = 60  # Liczba klatek na sekundę
score = 0
# Inicjalizacja zmiennych
enemy_shoot_timer_count = FPS * 2  # Licznik czasu strzału przeciwnika

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Funkcja do wyboru postaci
def choose_character():
    font = pygame.font.Font(None, 36)
    text1 = font.render("Choose your character:", True, WHITE)
    text2 = font.render("1. Czarkowski", True, WHITE)
    text3 = font.render("2. PanPole", True, WHITE)
    text4 = font.render("3. Bober", True, WHITE)
    screen.blit(text1, (screen_width // 2 - text1.get_width() // 2, 200))
    screen.blit(text2, (screen_width // 2 - text2.get_width() // 2, 250))
    screen.blit(text3, (screen_width // 2 - text3.get_width() // 2, 300))
    screen.blit(text4, (screen_width // 2 - text4.get_width() // 2, 350))
    pygame.display.flip()

    character = None
    while not character:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    character = "Czarkowski"
                elif event.key == pygame.K_2:
                    character = "PanPole"
                elif event.key == pygame.K_3:
                    character = "Bober"
    return character

# Funkcja generująca przeciwników
def generate_enemies():
    global wave_counter
    if wave_counter < max_wave:
        if len(enemies) < 5:  # Maksymalnie 5 przeciwników na ekranie
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = random.randint(50, 150)
            enemies.append([enemy_x, enemy_y, enemy_speed_x, enemy_speed_y])
    else:
        # Po osiągnięciu maksymalnej liczby fal, przeciwnicy przestają opadać i utrzymują się w powietrzu
        if len(enemies) == 0:
            enemies.append([random.randint(0, screen_width - enemy_width), 0, enemy_speed_x, enemy_speed_y])

# Funkcja do sprawdzania kolizji pocisków z przeciwnikami
def check_collision():
    global wave_counter
    for bullet in bullets[:]:  # Iterujemy po kopii listy bullets, aby móc bezpiecznie usuwać elementy
        for enemy in enemies[:]:  # Iterujemy po kopii listy enemies, aby móc bezpiecznie usuwać elementy
            if (bullet[0] > enemy[0] and bullet[0] < enemy[0] + enemy_width) and (
                    bullet[1] > enemy[1] and bullet[1] < enemy[1] + enemy_height):
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                if wave_counter < max_wave:
                    generate_enemies()  # Generowanie nowych przeciwników po trafieniu
# Wybór postaci
chosen_character = choose_character()

# Ładowanie obrazu postaci w zależności od wyboru
if chosen_character == "Czarkowski":
    player_img = pygame.image.load('C:/Users/czare/Downloads/czarkowski.png')
elif chosen_character == "PanPole":
    player_img = pygame.image.load('C:/Users/czare/Downloads/panpole.png')
elif chosen_character == "Bober":
    player_img = pygame.image.load('C:/Users/czare/Downloads/bober.png')

# Inicjalizacja pozycji postaci
player_width = player_img.get_width()
player_height = player_img.get_height()
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 1

# Inicjalizacja przeciwników
enemy_width = 200
enemy_height = 200
enemy_img = pygame.image.load('C:/Users/czare/Downloads/Menel.png')
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
enemies = []
enemy_speed_x = 1
enemy_speed_y = 1

bullet_img = pygame.Surface((4, 10))
bullet_img.fill(RED)
bullets = []
bullet_speed = 2

# Licznik fali
wave_counter = 0
max_wave = 5  # Maksymalna liczba fal

# Ustawienia timera dla przeciwników
enemy_shoot_cooldown = 60 * 2  # Przeciwnicy będą strzelać co 2 sekundy (60 klatek na sekundę)

# Licznik punktów
score = 0


# Inicjalizacja zmiennych
enemy_shoot_timer_count = FPS * 2  # Licznik czasu strzału przeciwnika
# Funkcja do strzelania przez przeciwników
def enemy_fire():
    for enemy in enemies:
        if random.random() < enemy_fire_rate:
            enemy_bullets.append([enemy[0] + enemy_width // 2 - 2, enemy[1] + enemy_height])

# Główna pętla gry
running = True
while running:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Płynne poruszanie gracza
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_x - player_speed >= 0:
            player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        if player_x + player_speed + player_width <= screen_width:
            player_x += player_speed

    # Obsługa strzałów gracza
    if keys[pygame.K_SPACE]:
        bullets.append([player_x + player_width // 2 - 2, player_y])

    # Generowanie przeciwników
    generate_enemies()

    # Sprawdzenie kolizji pocisków z przeciwnikami
    check_collision()

    # Sprawdzanie czy przeciwnicy powinni strzelać do gracza
    if enemy_shoot_timer_count <= 0:
        enemy_shoot_timer_count = FPS * 2  # Zresetuj licznik czasu strzału
        for enemy in enemies:
            # Kod obsługujący strzały przeciwników
            pass
    else:
        enemy_shoot_timer_count -= 1  # Dekrementuj licznik czasu strzału

    # Ruch przeciwników
    for enemy in enemies:
        enemy[0] += enemy[2]  # Ruch w poziomie
        enemy[1] += enemy[3]  # Ruch w pionie

        # Jeśli przeciwnik dotknie krawędzi ekranu, zmieniamy kierunek jego ruchu
        if enemy[0] <= 0 or enemy[0] >= screen_width - enemy_width:
            enemy[2] = -enemy[2]
        if enemy[1] <= 0 or enemy[1] >= screen_height - enemy_height:
            enemy[3] = -enemy[3]

    # Ruch pocisków
    for bullet in bullets:
        bullet[1] -= bullet_speed

    # Rysowanie
    screen.fill(BLACK)
    screen.blit(player_img, (player_x, player_y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))
    for bullet in bullets:
        pygame.draw.rect(screen, RED, pygame.Rect(bullet[0], bullet[1], 4, 10))

    # Aktualizacja okna
    pygame.display.flip()

# Zamknięcie Pygame
pygame.quit()