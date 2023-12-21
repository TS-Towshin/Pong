import pygame
import random
import time

pygame.init()

collision_sound = pygame.mixer.Sound("collision.wav")
win_sound = pygame.mixer.Sound("win.wav")


WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font(None, 40)

pygame.display.set_caption("Pong")

start = time.time()

class Player1:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

class Player2:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

class Ball:
    def __init__(self, x, y, r, v):
        self.x = x
        self.y = y
        self.r = r
        self.v = v

font = pygame.font.Font(None, 30)

p1 = Player1(0, 0, 8, 110, 7)
p2 = Player2(692, 0, 8, 110, 7)
ball = Ball(WIDTH//2, HEIGHT//2, 15, [5, 5])

clock = pygame.time.Clock()

running = True
boosted = False
alpha = 255

while running:

    if alpha > 0 and time.time()-start >= 3:
        alpha -= 1
    print(ball.v)
    print(f"Coordinates: {ball.x, ball.y}")
    print(f"P1 Coordinates: {p1.x, p1.y}")
    print(f"P2 Coordinates: {p2.x, p2.y}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ball.x += ball.v[0]
    ball.y += ball.v[1]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if p1.y > 0:
            p1.y -= p1.speed
    if keys[pygame.K_s]:
        if p1.y < 390:
            p1.y += p1.speed
    if keys[pygame.K_UP]:
        if p2.y > 0:
            p2.y -= p2.speed
    if keys[pygame.K_DOWN]:
        if p2.y < 390:
            p2.y += p2.speed

    if ball.y > p1.y and ball.y < p1.y + 110 and ball.x <= 8 and ball.x >= 0:
        if keys[pygame.K_SPACE] and not boosted:
            ball.v[0] *= 2
            ball.v[1] *= 2
            boosted = True
        elif keys[pygame.K_SPACE] and boosted:
            pass
        elif boosted:
            ball.v[0] /= 2
            ball.v[1] /= 2
            boosted = False
        ball.v[0] *= -1
        pygame.mixer.Sound.play(collision_sound)
        ball.x += ball.v[0]
        ball.y += ball.v[1]

    if ball.y > p2.y and ball.y < p2.y + 110 and ball.x >= 692 and ball.x <= WIDTH:
        if keys[pygame.K_SPACE] and not boosted:
            ball.v[0] *= 2
            ball.v[1] *= 2
            boosted = True
        elif keys[pygame.K_SPACE] and boosted:
            pass
        elif boosted:
            ball.v[0] /= 2
            ball.v[1] /= 2
            boosted = False
        ball.v[0] *= -1
        pygame.mixer.Sound.play(collision_sound)
        ball.x += ball.v[0]
        ball.y += ball.v[1]

    if ball.y <= 0 or ball.y >= HEIGHT:
        ball.v[1] *= -1
        pygame.mixer.Sound.play(collision_sound)
        ball.x += ball.v[0]
        ball.y += ball.v[1]

    if ball.x < 0 or ball.x > WIDTH:
        ball.x, ball.y = WIDTH//2, HEIGHT//2
        if boosted:
            ball.v[0] /= 2
            ball.v[1] /= 2
            boosted = False
        ball.v = [random.choice([-5, 5]), random.choice([-5, 5])]
        pygame.mixer.Sound.play(win_sound)
    screen.fill((0, 0, 0))
    clock.tick(60)

    pygame.draw.rect(screen, (255, 255, 255), (p1.x, p1.y, p1.width, p1.height))
    pygame.draw.rect(screen, (255, 255, 255), (p2.x, p2.y, p2.width, p2.height))
    pygame.draw.circle(screen, (255, 255, 255), (ball.x, ball.y), ball.r)

    message = font.render("Press space while hitting for a boost!", True, (255, 255, 255))
    faded_message = message.copy()
    faded_message.set_alpha(alpha)
    screen.blit(faded_message, (WIDTH//2-200, 2))

    pygame.display.update()

pygame.quit()