import pygame

pygame.init()

size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pong")

class Player1:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Player2:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

p1 = Player1(0, 0, 8, 110)
p2 = Player2(692, 0, 8, 110)
ball = Ball(350, 250, 15)

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if p1.y > 0:
            p1.y -= 5
    if keys[pygame.K_s]:
        if p1.y < 390:
            p1.y += 5
    if keys[pygame.K_UP]:
        if p2.y > 0:
            p2.y -= 5
    if keys[pygame.K_DOWN]:
        if p2.y < 390:
            p2.y += 5
    screen.fill((0, 0, 0))
    clock.tick(60)
    pygame.draw.rect(screen, (255, 255, 255), (p1.x, p1.y, p1.width, p1.height))
    pygame.draw.rect(screen, (255, 255, 255), (p2.x, p2.y, p2.width, p2.height))
    pygame.draw.circle(screen, (255, 255, 255), (ball.x, ball.y), ball.r)
    pygame.display.update()
pygame.quit()