#loading
from pygame import *

window = display.set_mode((600,400))
fps = time.Clock()

#gambar
Bg = image.load('Background.png')
Bg = transform.scale(Bg, (600,400))


#gamesprite
class GameSprite(sprite.Sprite):
    def __init__(self, img, lebar, tinggi, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (lebar, tinggi))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
   
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#Player bergerak y di pygame kebalik makin keatas makin minus makin kebawah makin plus
class Player(GameSprite):
    def __init__(self, img, lebar, tinggi, x, y, speed):
        super().__init__(img, lebar, tinggi, x, y, speed)
        self.xspeed = 0
        self.yspeed = 0

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

barriers = sprite.Group()
player = Player('Araya.png', 40, 40, 100, 0, 6)
ngejar = GameSprite('Ngejar.png', 60, 60, 0, 100, 4)
d1 = GameSprite('Dinding.png', 100, 100, 250, 150, 0)
final_sprite = GameSprite('sprite_terakhir.png', 30, 30, 80, 80, 0 )
barriers.add(d1)


#gameplay
run = True
while run:
    fps.tick(60)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_w:
                player.yspeed = -player.speed
            if e.key == K_a:
                            player.xspeed = -player.speed
            if e.key == K_s:
                            player.yspeed = player.speed
            if e.key == K_d:
                            player.xspeed = player.speed
        if e.type == KEYUP:
                    if e.key == K_w:
                        player.yspeed = 0
                    if e.key == K_a:
                        player.xspeed = 0
                    if e.key == K_s:
                        player.yspeed = 0
                    if e.key == K_d:
                        player.xspeed = 0
    window.blit(Bg, (0, 0))
    final_sprite.reset()
    player.reset()
    player.update()
    ngejar.reset()
    d1.reset()
    display.update()





