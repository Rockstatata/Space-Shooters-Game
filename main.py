import os
import pygame as pg

pg.display.init()
pg.font.init()
pg.mixer.init()
Width = 800
Height = 600
Display = pg.display.set_mode((Width, Height))
pg.display.set_caption("Space Shooters")
Border = pg.Rect(Width // 2 - 5, 0, 10, Height)

Background_music = pg.mixer.Sound(os.path.join('Assets', 'background.wav'))
Bullet_Hit_sound = pg.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
Bullet_Fire_sound = pg.mixer.Sound(os.path.join('Assets', 'Gun+silencer.mp3'))
HEALTH_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 40)
player1 = "Red"
player2 = "Yellow"
FPS = 60
Vel = 5
Bullet_vel = 7
Max_Bullets = 3
Yellow_Hit = pg.USEREVENT + 1
Red_Hit = pg.USEREVENT + 2
Yellow_spaceship = pg.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
Yellow_spaceship = pg.transform.rotate(pg.transform.scale(Yellow_spaceship, (32, 32)), 90)
Red_spaceship = pg.image.load(os.path.join('Assets', 'spaceship_red.png'))
Red_spaceship = pg.transform.rotate(pg.transform.scale(Red_spaceship, (32, 32)), 270)
space = pg.transform.scale(pg.image.load(os.path.join('Assets', 'space.png')), (Width, Height))


def draw_window(red, yellow, red_bullets, yellow_bullets, Red_Health, Yellow_Health):
    Display.blit(space, (0, 0))
    pg.draw.rect(Display, (0, 0, 0), Border)
    red_health_text = HEALTH_FONT.render("Health: " + str(Red_Health), 1, (255, 255, 255))
    yellow_health_text = HEALTH_FONT.render("Health: " + str(Yellow_Health), 1, (255, 255, 255))
    Display.blit(yellow_health_text, (Width - yellow_health_text.get_width() - 10, 10))
    Display.blit(red_health_text, (10, 10))
    Display.blit(Yellow_spaceship, (yellow.x, yellow.y))
    Display.blit(Red_spaceship, (red.x, red.y))
    for bullet in red_bullets:
        pg.draw.rect(Display, (255, 0, 0), bullet)
    for bullet in yellow_bullets:
        pg.draw.rect(Display, (255, 255, 0), bullet)
    pg.display.update()


def red_movement(keys_pressed, red):
    if keys_pressed[pg.K_a] and red.x - Vel > 0:  # Left
        red.x -= Vel
    if keys_pressed[pg.K_d] and red.x + Vel + red.width < Border.x:  # Right
        red.x += Vel
    if keys_pressed[pg.K_w] and red.y - Vel > 0:  # Up
        red.y -= Vel
    if keys_pressed[pg.K_s] and red.y + Vel + red.width < Height:  # Down
        red.y += Vel


def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pg.K_LEFT] and yellow.x - Vel > Border.x + 10:  # Left
        yellow.x -= Vel
    if keys_pressed[pg.K_RIGHT] and yellow.x + Vel + yellow.width < Width:  # Right
        yellow.x += Vel
    if keys_pressed[pg.K_UP] and yellow.y - Vel > 0:  # Up
        yellow.y -= Vel
    if keys_pressed[pg.K_DOWN] and yellow.y + Vel + yellow.width < Height:  # Down
        yellow.y += Vel


def bullet_movement(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x -= Bullet_vel
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(Red_Hit))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += Bullet_vel
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(Yellow_Hit))
            red_bullets.remove(bullet)
        elif bullet.x > Width:
            red_bullets.remove(bullet)

def game_over(text):
    draw_text = WINNER_FONT.render(text,1, (255,255,255))
    Display.blit(draw_text, (Width // 2 - draw_text.get_width()//2, Height // 2 - draw_text.get_height()//2))
    pg.display.update()
    Background_music.stop()
    pg.time.delay(5000)
def main():
    red = pg.Rect(100, 300, 32, 32)
    yellow = pg.Rect(700, 300, 32, 32)
    red_bullets = []
    yellow_bullets = []
    Yellow_Health = 10
    Red_Health = 10
    running = True
    Background_music.play(-1)

    clock = pg.time.Clock()
    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                exit(-1)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(red_bullets) < Max_Bullets:
                    bullet = pg.Rect(red.x + red.width, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    Bullet_Fire_sound.play()

                if event.key == pg.K_RCTRL and len(yellow_bullets) < Max_Bullets:
                    bullet = pg.Rect(yellow.x, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    Bullet_Fire_sound.play()

            if event.type == Red_Hit:
                Red_Health -= 1
                Bullet_Hit_sound.play()
            if event.type == Yellow_Hit:
                Yellow_Health -= 1
                Bullet_Hit_sound.play()

        winner_text = ""
        if Red_Health <= 0:
            winner_text = player2 + " wins"
        if Yellow_Health <= 0:
            winner_text = player1 + " wins"
        if winner_text != "":
            game_over(winner_text)
            break
        keys_pressed = pg.key.get_pressed()
        red_movement(keys_pressed, red)
        yellow_movement(keys_pressed, yellow)
        bullet_movement(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, Red_Health, Yellow_Health)
    main()

if __name__ == "__main__":
    main()
