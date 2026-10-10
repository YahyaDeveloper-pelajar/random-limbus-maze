#loading
from pygame import *

win_width = 600
win_height = 400
window = display.set_mode((win_width, win_height))
fps = time.Clock()

#gambar
Bg = image.load('Background.png')
Bg = transform.scale(Bg, (win_width, win_height))


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
        #gerak horizontal, berhenti di tepi jendela
        if self.rect.x + self.xspeed >= 0 and self.rect.x + self.rect.width + self.xspeed <= win_width:
            self.rect.x += self.xspeed
        #kalau nabrak dinding, mentok di pinggirnya
        kena_dinding = sprite.spritecollide(self, barriers, False)
        if self.xspeed > 0:
            for d in kena_dinding:
                self.rect.right = min(self.rect.right, d.rect.left)
        elif self.xspeed < 0:
            for d in kena_dinding:
                self.rect.left = max(self.rect.left, d.rect.right)

        #gerak vertikal, berhenti di tepi jendela
        if self.rect.y + self.yspeed >= 0 and self.rect.y + self.rect.height + self.yspeed <= win_height:
            self.rect.y += self.yspeed
        #kalau nabrak dinding, mentok di pinggirnya
        kena_dinding = sprite.spritecollide(self, barriers, False)
        if self.yspeed > 0:
            for d in kena_dinding:
                self.rect.bottom = min(self.rect.bottom, d.rect.top)
        elif self.yspeed < 0:
            for d in kena_dinding:
                self.rect.top = max(self.rect.top, d.rect.bottom)

    #nembak dari posisi player sekarang
    def fire(self):
        peluru = Bullet('bullet.png', 15, 10, self.rect.right, self.rect.centery, 10)
        bullets.add(peluru)


#ngejar sekarang mondar-mandir sendiri (patroli)
class Enemy(GameSprite):
    def __init__(self, img, lebar, tinggi, x, y, speed):
        super().__init__(img, lebar, tinggi, x, y, speed)
        self.arah = "kanan"

    def update(self):
        #balik arah kalau kena tepi jendela
        if self.rect.x <= 0:
            self.arah = "kanan"
        if self.rect.x >= win_width - self.rect.width:
            self.arah = "kiri"

        if self.arah == "kanan":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed


#peluru yang ditembakkan player
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        #hilang kalau sudah keluar layar
        if self.rect.x > win_width:
            self.kill()


barriers = sprite.Group()
musuh = sprite.Group()
bullets = sprite.Group()

player = Player('Araya.png', 40, 40, 100, 0, 6)
ngejar = Enemy('Ngejar.png', 60, 60, 0, 100, 4)
d1 = GameSprite('Dinding.png', 100, 100, 250, 150, 0)
d2 = GameSprite('Dinding.png', 150, 100, 400, 150, 0)
d3 = GameSprite('Dinding.png', 150, 100, 50, 150, 0)
final_sprite = GameSprite('sprite_terakhir.png', 30, 30, 280, 300, 0)

barriers.add(d1, d2, d3)
musuh.add(ngejar)

#status akhir game: None selama masih main, 'kalah' atau 'menang' saat selesai
selesai = None

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
            if e.key == K_SPACE:
                            player.fire()
        if e.type == KEYUP:
                    if e.key == K_w:
                        player.yspeed = 0
                    if e.key == K_a:
                        player.xspeed = 0
                    if e.key == K_s:
                        player.yspeed = 0
                    if e.key == K_d:
                        player.xspeed = 0

    if not selesai:
        window.blit(Bg, (0, 0))

        final_sprite.reset()
        player.reset()
        player.update()
        d1.reset()
        d2.reset()
        d3.reset()

        #musuh cuma jalan & digambar kalau masih hidup
        if ngejar.alive():
            ngejar.update()
            ngejar.reset()

        bullets.update()
        for peluru in bullets:
            peluru.reset()

        #peluru kena musuh -> musuh hilang, peluru juga hilang
        sprite.groupcollide(musuh, bullets, True, True)
        #peluru kena dinding -> peluru hilang, dinding tetap
        sprite.groupcollide(bullets, barriers, True, False)

        #kalau player nabrak ngejar (yang masih hidup) -> kalah
        if ngejar.alive() and sprite.collide_rect(player, ngejar):
            selesai = 'kalah'
            
            gambar_kalah = transform.scale(image.load('kalah.png'), (win_width, win_height))

        #kalau nyampe sprite terakhir -> menang
        if sprite.collide_rect(player, final_sprite):
            selesai = 'menang'
            
            gambar_menang = transform.scale(image.load('thumb.jpg'), (win_width, win_height))

    elif selesai == 'kalah':
        window.blit(gambar_kalah, (0, 0))

    elif selesai == 'menang':
        window.blit(gambar_menang, (0, 0))

    display.update()