#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as time_counter

init()


clock = time.Clock()
FPS = 60


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    


class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__(player_image=player_image, player_x=player_x, player_y=player_y, player_speed=player_speed, player_size_x=player_size_x, player_size_y=player_size_y)
    def update(self):
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_LEFT] or keys_pressed[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys_pressed[K_RIGHT] or keys_pressed[K_d]) and self.rect.x < 625:
            self.rect.x += self.speed
    def shot(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 15, self.rect.top, 7, 30, 30)
        bullets.add(bullet)

lost = 0
knocked_down = 0
health = 100
num_fire = 5
rel_time = False

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__(player_image=player_image, player_x=player_x, player_y=player_y, player_speed=player_speed,player_size_x=player_size_x, player_size_y=player_size_y)
    def update(self):
        self.speed = 1
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = randint(-15, 10)
            self.rect.x = randint(5, 650)
            lost += 1
       

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__(player_image=player_image, player_x=player_x, player_y=player_y, player_speed=player_speed, player_size_x=player_size_x, player_size_y=player_size_y)
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__(player_image=player_image, player_x=player_x, player_y=player_y, player_speed=player_speed,player_size_x=player_size_x, player_size_y=player_size_y)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = randint(-150, 0)
            self.rect.x = randint(5, 650)




window = display.set_mode((700, 500))
display.set_caption('Шутер')


background = transform.scale(image.load('galaxy.jpg'), (700, 500))
game = True
finish = False

hero = Player('rocket.png', 325, 425, 10, 65, 65)

monsters = sprite.Group()
monster = Enemy('ufo.png', randint(3, 650), randint(-10, 10), 1, 65, 65)
monster1 = Enemy('ufo.png', randint(3, 650), randint(-60,-10 ), 1, 65, 65)
monster2 = Enemy('ufo.png',  randint(3, 650), randint(-110, -60), 1, 65, 65)
monster3 = Enemy('ufo.png', randint(3, 650), randint(-160, -110), 1, 65, 65)
monster4 = Enemy('ufo.png', randint(3, 650), randint(-210, -160), 1, 65, 65)

asteroids = sprite.Group()
asteroid = Asteroid('asteroid.png', randint(-150, 0), randint(5, 650), 1, 65, 65)
asteroid1 = Asteroid('asteroid.png', randint(-225, -75), randint(5, 650), 1, 65, 65)
asteroid2 = Asteroid('asteroid.png', randint(-300, -150), randint(5, 650), 1, 65, 65)

bullets = sprite.Group()


monsters.add(monster)
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)

asteroids.add(asteroid)
asteroids.add(asteroid1)
asteroids.add(asteroid2)

font1 = font.SysFont('Arial', 30)
knocked_down_name = font1.render('Сбито:' + str(knocked_down), True, (255, 255, 255))
lost_name = font1.render('Пропущено:' + str(lost), True, (255, 255, 255))
health_name = font1.render('Здоровье:' + str(health), True, (255, 255, 255))
num_fire_name = font1.render('Патрронов в абойме' + str(num_fire), True, (255, 255, 255))

font3 = font.SysFont('Arial', 30)
recharge = font3.render('Ждите, идёт перезарядка. Wait, reload...', True, (255, 0, 0))

mixer.music.load('space.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()
shot_sound = mixer.Sound('fire.ogg')

while game:
    if finish != True:
        window.blit(background, (0, 0))
        hero.reset()
        hero.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        knocked_down_name = font1.render('Сбито:' + str(knocked_down), True, (255, 255, 255))
        lost_name = font1.render('Пропущено:' + str(lost), True, (255, 255, 255))
        health_name = font1.render('Здоровье:' + str(health), True, (255, 255, 255))
        num_fire_name = font1.render('Патрронов в абойме ' + str(num_fire), True, (255, 255, 255))
        window.blit(knocked_down_name, (10, 10))
        window.blit(lost_name, (10, 40))
        window.blit(health_name, (10, 70))
        window.blit(num_fire_name, (10, 100))
        hero_monsters_ccollision = sprite.spritecollide(hero, monsters, True)
        monsters_bullet_collision = sprite.groupcollide(bullets, monsters, True, True)
        hero_meteorite_ccollision = sprite.spritecollide(hero, asteroids, True)

        for colides in monsters_bullet_collision:
            knocked_down += 1
            monster5 = Enemy('ufo.png', randint(3, 650), randint(-60,-10 ), 2, 65, 65)
            monsters.add(monster5)

        for colission in hero_monsters_ccollision:
            health -= 35
            monster6 = Enemy('ufo.png', randint(3, 650), randint(-60,-10 ), 2, 65, 65)
            monsters.add(monster6)

        for meteorite in hero_meteorite_ccollision:
            health -= 50
            asteroid4 = Asteroid('asteroid.png', randint(-150, 0), randint(5, 650), 2, 65, 65)
            asteroids.add(asteroid4)

        if knocked_down >= 20:
            finish = True
            font2 = font.SysFont(None, 70)
            you_win = font2.render('You WIN', True, (255, 0, 0))
            window.blit(you_win, (215, 215))
            mixer.music.stop()

        if lost >= 5:
            font2 = font.SysFont(None, 70)
            you_lose = font2.render('You LOSE', True, (255, 0, 0))
            window.blit(you_lose, (215, 215))
            finish = True
            mixer.music.stop()

    if health <= 0:
        font2 = font.SysFont(None, 70)
        you_lose = font2.render('You LOSE', True, (255, 0, 0))
        window.blit(you_lose, (215, 215))
        finish = True
        mixer.music.stop()

    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire > 0 and rel_time == False:
                    num_fire -= 1
                    hero.shot()
                    shot_sound.play()
                if num_fire <= 0 and rel_time == False:
                    rel_time = True
                    time1 = time_counter()
    if rel_time:
        time2 = time_counter()
        if time2 - time1 < 3:
            window.blit(recharge, (100, 460))
        else:
            num_fire = 5
            rel_time = False
                        
    window.blit(health_name, (10, 70))            

    display.update()
    clock.tick(FPS)