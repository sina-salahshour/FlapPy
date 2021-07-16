import pygame
from random import randint
from object import object
def draw(x,y):
    try:
        x.blit(y.value, y.rect)
    except Exception:
        x.blit(y.value,y.pos)
def sdraw(x):
    draw(screen,x)
def cRectPos(obj,y):
    obj.rect.centery += y
def pipedraw(pipe):
    screen.blit(pipe.value, pipe.rect)
    screen.blit(pipe.value2, pipe.rect2)
def birddraw(bird):
    screen.blit(pygame.transform.rotate(bird.value,bird.v*-10),bird.rect)
pygame.init()
bgsurface = object(pygame.image.load('assets/background-day.png'),[0,0])
floor = object(pygame.image.load('assets/base.png'),[0,400])
bird = object(pygame.image.load('assets/yellowbird-midflap.png'),[10,0])
bird.value1 = pygame.image.load('assets/bluebird-midflap.png')
bird.value2 = pygame.image.load('assets/yellowbird-downflap.png')
bird.value3 = pygame.image.load('assets/yellowbird-upflap.png')
bird.rect = bird.value.get_rect(center = (50,bgsurface.value.get_height()/2))
pipe1 = object(pygame.image.load('assets/pipe-green.png'),[100, 200])
pipe1.rect = pipe1.value.get_rect(center = (400,400))
pipe1.value2 = pygame.transform.flip(pipe1.value, False, True)
pipe1.rect2 = pipe1.value2.get_rect(center = (400,-15))
pipe2 = object(pygame.image.load('assets/pipe-green.png'),[100, 200])
pipe2.rect = pipe1.value.get_rect(center = (400+bgsurface.value.get_width()/2+pipe1.value.get_width()/2,400))
pipe2.value2 = pygame.transform.flip(pipe1.value, False, True)
pipe2.rect2 = pipe1.value2.get_rect(center = (400+bgsurface.value.get_width()/2+pipe1.value.get_width()/2,-15))
wingsound = pygame.mixer.Sound('sounds/sfx_wing.wav')
hitsound = pygame.mixer.Sound('sounds/sfx_hit.wav')
diesound = pygame.mixer.Sound('sounds/sfx_die.wav')
pointsound = pygame.mixer.Sound('sounds/sfx_point.wav')
swooshingsound = pygame.mixer.Sound('sounds/sfx_swooshing.wav')
screen = pygame.display.set_mode((bgsurface.value.get_width(),bgsurface.value.get_height()))
pygame.display.set_caption('FlapPy',)
clock = pygame.time.Clock()
bird.v=0
gravity = 0.05
pipe1.gap = 415
pipe2.gap = 415
dead = [0,0]
betweenpipe = False
betweenpipe2 = False
dontmove = False
def die(dead):
    if dead[0] == 0:
        hitsound.play()
    dead[0]  = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if dead[0] == 0 and bird.rect.centery > 15:
                if event.key == pygame.K_SPACE:
                    bird.v = -1.5
                    wingsound.play()
    if bird.rect.centery >=375:
        die(dead)
        dontmove = True
    if bird.rect.centerx-bird.value.get_width()/2 < pipe1.rect.centerx + pipe1.value.get_width()/2 - 5 and bird.rect.centerx+ bird.value.get_width()/2 > pipe1.rect.centerx - pipe1.value.get_width()/2:
        if bird.rect.centery + bird.value.get_height()/2 > pipe1.rect.centery - pipe1.value.get_height()/2 or bird.rect.centery - bird.value.get_height()/2 < pipe1.rect2.centery + pipe1.value2.get_height()/2:
            die(dead)
        else:
            betweenpipe = True
    else:
        if betweenpipe:
            pointsound.play()
            betweenpipe = False
    if bird.rect.centerx-bird.value.get_width()/2 < pipe2.rect.centerx + pipe2.value.get_width()/2 - 5 and bird.rect.centerx+ bird.value.get_width()/2 > pipe2.rect.centerx - pipe2.value.get_width()/2:
        if bird.rect.centery + bird.value.get_height()/2 > pipe2.rect.centery - pipe2.value.get_height()/2 or bird.rect.centery - bird.value.get_height()/2 < pipe2.rect2.centery + pipe2.value2.get_height()/2:
            die(dead)
        else:
            betweenpipe2 = True
    else:
        if betweenpipe2:
            pointsound.play()
            betweenpipe2 = False
    sdraw(bgsurface)
    if dead[0] == 0:
        floor.pos[0] -=2
    if floor.pos[0] <= -floor.value.get_width():
        floor.pos[0] = 0
    deltatime = clock.get_time()/5
    if dontmove == False:
        cRectPos(bird, 0.6 * 0.02 * (deltatime**2) + bird.v * deltatime)
    bird.v += gravity * deltatime/2
    if bird.v <0:
        bird.value = bird.value2
    elif bird.v >0:
        bird.value = bird.value3
    else:
        bird.value = bird.value1
    # sdraw(bird)
    birddraw(bird)
    # print(bird.v)
    if dead[0] == 0:
        pipe1.rect.centerx -= 2
        pipe1.rect2.centerx = pipe1.rect.centerx
        pipe2.rect.centerx -= 2
        pipe2.rect2.centerx = pipe2.rect.centerx

    if dead[0] == 1:
        dead[1] +=1
        if dead[1] == 15:
            diesound.play()
        if dead[1] == 45:
            exit()

    if pipe1.rect.centerx <= -pipe1.value.get_width()/2:
        pipe1.rect.centerx = bgsurface.value.get_width()+pipe1.value.get_width()/2
        pipe1.rect.centery = randint(265, 535)
        pipe1.rect2.centery = pipe1.rect.centery - pipe1.gap
    if pipe2.rect.centerx <= -pipe2.value.get_width()/2:
        pipe2.rect.centerx = bgsurface.value.get_width()+pipe2.value.get_width()/2
        pipe2.rect.centery = randint(265, 535)
        pipe2.rect2.centery = pipe2.rect.centery - pipe2.gap
    # sdraw(pipe1)
    pipedraw(pipe1)
    pipedraw(pipe2)
    sdraw(floor)
    screen.blit(floor.value, (floor.pos[0]+floor.value.get_width(),floor.pos[1]))
    pygame.display.update()
    clock.tick(60)
