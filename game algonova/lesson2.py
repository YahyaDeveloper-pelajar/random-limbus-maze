from pygame import *

#parent class for other sprites
class GameSprite(sprite.Sprite):
  # class constructor
  def __init__(self, player_image, player_x, player_y, size_x, size_y):
      # Calling the class constructor (Sprite):
      sprite.Sprite.__init__(self)
 
      # each sprite must store an image property - an image
      self.image = transform.scale(image.load(player_image), (size_x, size_y))

      # each sprite must store the rect property - the rectangle which it's inscribed in
      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y
 
  # the method that draws the character in the window
  def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
  #the method where the sprite is controlled by the arrow keys of the keyboard
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
      # Calling the class constructor (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)

      self.x_speed = player_x_speed
      self.y_speed = player_y_speed
  def update(self):
       "' moves the character by applying the current horizontal and vertical speed"'
       # horizontal movement first
       if player.rect.x <= win_width-80 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
         self.rect.x += self.x_speed
       # if we went behind the wall, then we will stand close to the wall
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.x_speed > 0: # go to the right, the right edge of the character is close to the left edge of the wall
           for p in platforms_touched:
               self.rect.right = min(self.rect.right, p.rect.left) # if several were touched at once, then the right edge is the minimum possible
       elif self.x_speed < 0: # go to the left, put the left edge of the character close to the right edge of the wall
           for p in platforms_touched:
               self.rect.left = max(self.rect.left, p.rect.right) # if several walls have been touched, then the left edge is the maximum
       if player.rect.y <= win_height-80 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
        self.rect.y += self.y_speed
       # if we went behind the wall, then we will stand close to the wall
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.y_speed > 0: # going down
           for p in platforms_touched:
               self.y_speed = 0
               # We're checking which of the platforms is the highest from the ones below, aligning with it, and then take it as our support:
               if p.rect.top < self.rect.bottom:
                   self.rect.bottom = p.rect.top
       elif self.y_speed < 0: # going up
           for p in platforms_touched:
               self.y_speed = 0 # when colliding with a wall, the vertical velocity is extinguished
               self.rect.top = max(self.rect.top, p.rect.bottom) # align the upper edge along the lower edges of the walls that were hit


#Creating a window
win_width = 700
win_height = 500
display.set_caption("Maze")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#setting the color according to the RGB color scheme 

#creating a group for the walls
barriers = sprite.Group()

#creating wall pictures
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)

#adding walls to the group
barriers.add(w1)
barriers.add(w2)

#creating sprites
player = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
monster = GameSprite('cyborg.png', win_width - 80, 180, 80, 80)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)

#the variable responsible for how the game has ended
finish = False
#game loop
run = True
while run:

  for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
           if e.key == K_LEFT:
               player.x_speed = -5
           elif e.key == K_RIGHT:
               player.x_speed = 5
           elif e.key == K_UP :
               player.y_speed = -5
           elif e.key == K_DOWN :
               player.y_speed = 5
 
       elif e.type == KEYUP:
           if e.key == K_LEFT :
               player.x_speed = 0
           elif e.key == K_RIGHT:
               player.x_speed = 0 
           elif e.key == K_UP:
               player.y_speed = 0
           elif e.key == K_DOWN:
               player.y_speed = 0
  if not finish:
    window.fill(back)#fill in the window with color 
    #draw objects
    # w1.reset()
    # w2.reset()
    barriers.draw(window)
    
    monster.reset()
    final_sprite.reset()
    player.reset()
    #turning on the movement
    player.update()
    #Checking the character's collision with the enemy and walls
    if sprite.collide_rect(player, monster):
        finish = True
        #calculate the ratio
        img = image.load('game-over_1.png')
        d = img.get_width() // img.get_height()
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

    if sprite.collide_rect(player, final_sprite):
        finish = True
        img = image.load('thumb.jpg')
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
  
  #the cycle is triggered every 0.05 seconds
  time.delay(50)
  
  display.update()

