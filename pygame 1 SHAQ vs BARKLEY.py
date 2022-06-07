
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1050, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Basketball Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect( 0, HEIGHT//2 - 5, WIDTH, 10)



#BULLET_HIT_SOUND = pygame.mixer.Sound('Pictures', 'Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Pictures', 'Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
BASKETBALL_WIDTH, BASKETBALL_HEIGHT = 200, 200

BULLET_HIT_SOUND = pygame.mixer.Sound('Pictures/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Pictures/Gun+Silencer.mp3')

SHAQ_IMAGE = pygame.image.load(os.path.join('Pictures', 'shaqlakers.jpg'))
SHAQ_IMAGE = pygame.transform.scale(
    SHAQ_IMAGE, (BASKETBALL_WIDTH, BASKETBALL_HEIGHT))

CHARLESBARKLEY_IMAGE = pygame.image.load(os.path.join('Pictures', 'barkleysuns.jpg'))
CHARLESBARKLEY_IMAGE = pygame.transform.scale(
    CHARLESBARKLEY_IMAGE, (BASKETBALL_WIDTH, BASKETBALL_HEIGHT))

SHAQ_HIT = pygame.USEREVENT + 1
BARKLEY_HIT = pygame.USEREVENT + 2

COURT = pygame.transform.scale(pygame.image.load(
os.path.join('Pictures', 'basketballcourt.jpg')), (WIDTH , HEIGHT ))

def draw_window(barkley, shaq, barkley_bullets, shaq_bullets, barkley_health, shaq_health):
    WIN.blit(COURT, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    barkley_health_text = HEALTH_FONT.render(
        "Health: " + str(barkley_health), 1, BLACK)
    shaq_health_text = HEALTH_FONT.render(
        "Health: " + str(shaq_health), 1, BLACK)
    WIN.blit(barkley_health_text, (WIDTH - shaq_health_text.get_width() - 10, 10))
    WIN.blit(shaq_health_text, (10, 10))

    WIN.blit(SHAQ_IMAGE, (shaq.x, shaq.y))
    WIN.blit(CHARLESBARKLEY_IMAGE, (barkley.x, barkley.y))

    for bullet in barkley_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in shaq_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def shaq_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL >  0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.height < 1000:  # RIGHT
     yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL >  BORDER.y :  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.width < HEIGHT:  # DOWN
        yellow.y += VEL


def charlesbarkley_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0 :  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.height < 1100:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < 330:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.y += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SHAQ_HIT)) 
            yellow_bullets.remove(bullet)
        elif bullet.y < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BARKLEY_HIT))
            red_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    shaq = pygame.Rect(400, 0, BASKETBALL_WIDTH, BASKETBALL_HEIGHT)
    barkley = pygame.Rect(400, 700, BASKETBALL_WIDTH, BASKETBALL_HEIGHT)

    shaq_bullets = []
    barkley_bullets = []

    shaq_health = 10
    barkley_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(shaq_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        shaq.x, shaq.y + shaq.height//2 - 2, 10, 5)
                    shaq_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


                if event.key == pygame.K_LCTRL and len(barkley_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        barkley.x + barkley.width, barkley.y + barkley.height//2-2, 10,5)
                    barkley_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == BARKLEY_HIT:
                shaq_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == SHAQ_HIT:
                barkley_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if barkley_health <= 0:
            winner_text = "Shaquille O'Neal Wins!"

        if shaq_health <= 0:
            winner_text = "Charles Barkley Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        shaq_handle_movement(keys_pressed, barkley)
        charlesbarkley_handle_movement(keys_pressed, shaq)

        handle_bullets(shaq_bullets, barkley_bullets, barkley, shaq)

        draw_window(shaq, barkley, barkley_bullets, shaq_bullets,
                    barkley_health, shaq_health)

    main()


if __name__ == "__main__":
    main()