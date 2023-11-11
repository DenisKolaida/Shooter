import pygame as pg
import sys, random as rd

pg.init()
pg.mixer.init()

W, H = 700, 500
FPS = 60

run = 1

win = pg.display.set_mode((W, H))
pg.display.set_caption('Шутер')
clock = pg.time.Clock()

pg.mixer.music.load('sounds/space.ogg')
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1)

fire = pg.mixer.Sound('sounds/fire.ogg')

bg = pg.transform.scale(pg.image.load('images/galaxy.jpg'), (W, H))

player = pg.transform.scale(pg.image.load('images/rocket.png'), (80, 110))
playerR = player.get_rect(center = (W/2, H-55))

f = pg.font.Font(None, 35)
scoreT = f.render('Счёт: ', 1, 'white')
missedT = f.render('Пропущено: ', 1, 'white')
firemodeT = f.render('Режим огня [СКМ]: ', 1, 'white')
ammoT = f.render('Боекомплект: ', 1, 'white')
reloadingT = f.render('Перезарядка...', 1, 'white')

endf = pg.font.Font(None, 50)
winT = endf.render('Вы выиграли!', 1, 'white')
loseT = endf.render('Вы проиграли', 1, 'white')

ammo = 120
score = 0
missed = 0

seconds = 3
rtime = FPS * seconds

class Ufo(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.ufo = pg.transform.scale(pg.image.load('images/ufo.png'), (80, 50))
        self.rand()
    def rand(self):
        self.rect = self.ufo.get_rect(topleft = (rd.randint(0, 620), -60))
        self.speed = rd.randint(1, 3)
    def update(self, state = 0):
        if state:
            self.rand()
        elif not state:
            self.rect.y += self.speed
            win.blit(self.ufo, self.rect)

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.bullet = pg.transform.scale(pg.image.load('images/bullet.png'), (15, 20))
        self.rect = self.bullet.get_rect(topleft = pos)
        self.speed = 7
    def update(self, state = 0):
        if state:
            self.kill()
        elif not state:
            global score
            self.rect.y -= self.speed
            win.blit(self.bullet, self.rect)
            if self.rect.y < 0:
                self.kill()
            for ufo in ufoList:
                if self.rect.colliderect(ufo.rect):
                    self.kill()
                    ufo.rand()
                    score += 1

def Reload(rtime):
    global ammo, seconds
    if rtime == 0:
        ammo = 120
        return FPS * seconds
    else: return rtime - 1

ufo1 = Ufo()
ufo2 = Ufo()
ufo3 = Ufo()
ufo4 = Ufo()
ufo5 = Ufo()
ufo6 = Ufo()
ufoList = (ufo1, ufo2, ufo3, ufo4, ufo5, ufo6)
ufos = pg.sprite.Group()
ufos.add(ufoList)

bullets = pg.sprite.Group()

firemode = 1
run = 1

while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if run:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and ammo > 0:
                if firemode == 1:
                    ammo -= 1
                    bullets.add(Bullet((playerR.centerx-8, playerR.centery)))
                    fire.play()
                elif firemode == 2 and ammo > 1:
                    ammo -= 1
                    bullets.add(Bullet((playerR.centerx-20, playerR.centery)))
                    fire.play()
                    ammo -= 1
                    bullets.add(Bullet((playerR.centerx+5, playerR.centery)))
                    fire.play()
                elif firemode == 3 and ammo > 2:
                    ammo -= 1
                    bullets.add(Bullet((playerR.centerx-8, playerR.centery-5)))
                    fire.play()
                    ammo -= 1
                    bullets.add(Bullet((playerR.centerx-20, playerR.centery)))
                    fire.play()
                    ammo -= 1
                    bullets.add(Bullet((playerR.centerx+5, playerR.centery)))
                    fire.play()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 2:
                if firemode == 3: firemode = 1
                else: firemode += 1
            

    
    keys = pg.key.get_pressed()
    if run:
        if keys[pg.K_r]:
            ammo = 0
        if keys[pg.K_a]:
            if playerR.x > 0:
                playerR.x -= 5
        elif keys[pg.K_d]:
            if playerR.x < W-80:
                playerR.x += 5

        for ufo in ufoList:
            if ufo.rect.y > H:
                missed += 1
                ufo.rand()

        firemodeC = f.render(f'{firemode}', 1, 'white')
        ammoC = f.render(f'{ammo}', 1, 'white')
        scoreC = f.render(f'{score}', 1, 'white')
        missedC = f.render(f'{missed}', 1, 'white')

        win.blit(bg, (0, 0))
        if ammo == 0:
            rtime = Reload(rtime)
            win.blit(reloadingT, (W/2-100, H/2))
        ufos.update()
        bullets.update()
        win.blit(player, playerR)
        win.blit(firemodeT, (0, 10))
        win.blit(ammoT, (0, 40))
        win.blit(scoreT, (0, 80))
        win.blit(missedT, (0, 110))
        win.blit(firemodeC, (230, 10))
        win.blit(ammoC, (170, 40))
        win.blit(scoreC, (70, 80))
        win.blit(missedC, (155, 110))
    if score > 150 or missed > 9:
        run = 0
        win.blit(bg, (0, 0))
        win.blit(firemodeT, (0, 10))
        win.blit(ammoT, (0, 40))
        win.blit(scoreT, (0, 80))
        win.blit(missedT, (0, 110))
        win.blit(firemodeC, (230, 10))
        win.blit(ammoC, (170, 40))
        win.blit(scoreC, (70, 80))
        win.blit(missedC, (155, 110))
        if score > 150 and missed < 10:
            win.blit(winT, (W/2-100, H/2-10))
        elif score < 150 and missed > 9:
            win.blit(loseT,(W/2-100, H/2 - 10))

        if keys[pg.K_LALT]:
            run = 1
            score = 0
            missed = 0
            ammo = 120
            ufos.update(1)
            bullets.update(1)

    pg.display.update()
    clock.tick(FPS)