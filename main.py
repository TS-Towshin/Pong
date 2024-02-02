import pygame
import random
import time


pygame.init()

collision_sound = pygame.mixer.Sound("collision.wav")
win_sound = pygame.mixer.Sound("win.wav")

# settings:
ai = True # True for Player vs AI and False for Player vs Player
player_speed = 10 # Change the speed to 10 on Player vs AI to increase the difficulty and 8 for medium difficulty.


WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pong")

TRANSPARENT_ALPHA = 150

shade_surface = pygame.Surface((WIDTH, HEIGHT))
shade_surface.set_alpha(TRANSPARENT_ALPHA)

start = time.time()

class Player1:
    def __init__(self, x, y, width, height, speed, score):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.score = score

class Player2:
    def __init__(self, x, y, width, height, speed, score):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.score = score

class Ball:
    def __init__(self, x, y, r, v, color):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.color = color

font = pygame.font.Font(None, 30)
paused_font = pygame.font.Font(None, 100)
paused_screen = pygame.image.load("paused_screen.png")

p1 = Player1(0, 0, 8, 110, player_speed, 0) 
p2 = Player2(692, 0, 8, 110, player_speed, 0)
ball = Ball(WIDTH//2, HEIGHT//2, 15, [5, 5], (255, 255, 255))

clock = pygame.time.Clock()

running = True
boosted = False
paused = False
alpha = 255



while running:
    rect_player1 = pygame.Rect(p1.x, p1.y-15, p1.width, p1.height+30) # The value is increased because the radius of the ball is 15 and it would only register it as a collision if the center coordinate is the same as the player. And so the player would see that if the ball is still in touch with the player but in a corner, it would count as a miss.
    rect_player2 = pygame.Rect(p2.x, p2.y-15, p2.width, p2.height+30)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.key == pygame.K_ESCAPE:
                    paused = True
            elif paused:
                if event.key == pygame.K_ESCAPE:
                    paused = False

    if not paused:
        if alpha > 0 and time.time()-start >= 3:
            alpha -= 1

        ball.x += ball.v[0]
        ball.y += ball.v[1]

        if keys[pygame.K_w]:
            if p1.y > 0:
                p1.y -= p1.speed
        if keys[pygame.K_s]:
            if p1.y < 390:
                p1.y += p1.speed
        if ai:
            if p2.y > ball.y:
                if ball.v[0] > 0:
                    p2.y -= p2.speed
            elif p2.y + p2.height < ball.y:
                if ball.v[0] > 0:
                    p2.y += p2.speed

        else:
            if keys[pygame.K_UP]:
                if p2.y > 0:
                    p2.y -= p2.speed
            if keys[pygame.K_DOWN]:
                if p2.y < 390:
                    p2.y += p2.speed

        if rect_player1.collidepoint(ball.x-15, ball.y):
            if keys[pygame.K_SPACE] and not boosted:
                ball.v[0] *= 2
                ball.v[1] *= 2
                ball.color = (255, 0, 0)
                pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)
                pygame.display.update()
                boosted = True
            elif keys[pygame.K_SPACE] and boosted:
                pass
            elif boosted:
                ball.v[0] /= 2
                ball.v[1] /= 2
                ball.color = (255, 255, 255)
                pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)
                pygame.display.update()
                boosted = False
            ball.v[0] *= -1
            pygame.mixer.Sound.play(collision_sound)
            ball.x += ball.v[0]
            ball.y += ball.v[1]

        if rect_player2.collidepoint(ball.x+15, ball.y):
            if ai:
                chance = random.randint(0, 1)
                if bool(chance) and not boosted:
                    ball.v[0] *= 2
                    ball.v[1] *= 2
                    ball.color = (255, 0, 0)
                    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)
                    pygame.display.update()
                    boosted = True
                elif bool(chance) and boosted:
                    pass
                elif boosted:
                    ball.v[0] /= 2
                    ball.v[1] /= 2
                    ball.color = (255, 255, 255)
                    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)
                    pygame.display.update()
                    boosted = False
            else:
                if keys[pygame.K_SPACE] and not boosted:
                    ball.v[0] *= 2
                    ball.v[1] *= 2
                    ball.color = (255, 0, 0)
                    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)
                    pygame.display.update()
                    boosted = True
                if keys[pygame.K_SPACE] and boosted:
                    pass
                elif boosted:
                    ball.v[0] /= 2
                    ball.v[1] /= 2
                    ball.color = (255, 255, 255)
                    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)
                    pygame.display.update()
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

        if ball.x < 0:
            p2.score += 1
            ball.x, ball.y = WIDTH//2, HEIGHT//2
            if boosted:
                ball.v[0] /= 2
                ball.v[1] /= 2
                ball.color = (255, 255, 255)
                pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)
                pygame.display.update()
                boosted = False
            ball.v = [random.choice([-5, 5]), random.choice([-5, 5])]
            pygame.mixer.Sound.play(win_sound)
        elif ball.x > WIDTH:
            p1.score += 1
            ball.x, ball.y = WIDTH//2, HEIGHT//2
            if boosted:
                ball.v[0] /= 2
                ball.v[1] /= 2
                ball.color = (255, 255, 255)
                pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)
                pygame.display.update()
                boosted = False
            ball.v = [random.choice([-5, 5]), random.choice([-5, 5])]
            pygame.mixer.Sound.play(win_sound)

        clock.tick(60)

    screen.fill((0, 0, 0))
    

    pygame.draw.rect(screen, (255, 255, 255), (p1.x, p1.y, p1.width, p1.height))
    pygame.draw.rect(screen, (255, 255, 255), (p2.x, p2.y, p2.width, p2.height))
    pygame.draw.circle(screen, ball.color, (ball.x, ball.y), ball.r)

    for i in range(1, 25, 2):
        pygame.draw.line(screen, (255, 255, 255), (WIDTH//2, 20*i), (WIDTH//2, 20*i+30), 3)

    score_font = pygame.font.Font(None, 100)
    p1_score = score_font.render(str(p1.score), True, (255, 255, 255))
    p2_score = score_font.render(str(p2.score), True, (255, 255, 255))
    screen.blit(p1_score, (175, 200))
    screen.blit(p2_score, (550, 200))

    message = font.render("Press space while hitting for a boost!", True, (255, 255, 255))
    faded_message = message.copy()
    faded_message.set_alpha(alpha)
    screen.blit(faded_message, (WIDTH//2-200, 2))
    if paused:
        screen.blit(shade_surface, (0, 0))
        screen.blit(paused_screen, (WIDTH//2-230, HEIGHT//2-200))
        clock.tick(12) # This is for optimization. When we pause the game, we don't have to change
                       # any frames so its better to have as low fps as possible. But it will decrease
                       # the response time for the game to pause or unpause.
    pygame.display.flip()


pygame.quit()
