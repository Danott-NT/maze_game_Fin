x = 2500
y = 200
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

from pygame import *
import time as timer

window_width = 700
window_height = 500

window = display.set_mode( (window_width, window_height) )
display.set_caption("CATCH")

bg = transform.scale( image.load("background.jpg"), (window_width, window_height) )

class Character():
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.image = transform.scale( image.load(self.filename), (self.size_x, self.size_y) )
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Wall(Character):
    def __init__(self, size_x, size_y, pos_x, pos_y):
        self.size_x = size_x
        self.size_y = size_y
        self.image = Surface( (size_x, size_y) )
        self.image.fill( (224, 78, 67) )
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

wall_list = []
wall_list.append( Wall(15, 400, 20, 60) )
wall_list.append( Wall(15, 360, 100, 20) )
wall_list.append( Wall(440, 15, 20, 460) )
wall_list.append( Wall(280, 15, 100, 380) )
wall_list.append( Wall(15, 305, 380, 90) )
wall_list.append( Wall(15, 300, 460, 175) )
wall_list.append( Wall(255, 15, 380, 90) )
wall_list.append( Wall(175, 15, 460, 160) )

player1 = Character("cyborg.png", 50, 50, 50, 50, 5)
player1.hp = 5
isImmortal = False
immortal_time_start = timer.time()
blink_count = 0

player2 = Character("hero.png", 50, 50, 300, 300, 5)
route_list = [(100, 300), (400, 200), (50, 70), (500, 400)]
route = 0
ok_x = False
ok_y = False

treasure = Character("treasure.png", 50, 50, 600, 400, 5)

clock = time.Clock()
fps = 60
game = True
finish = False

font.init()
style = font.SysFont(None, 50)
while game:
    window.blit(bg, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    if isImmortal == False:
        player1.draw()
    else:
        if blink_count < 15:
            player1.draw()
        elif blink_count < 30:
            pass
        else:
            blink_count = 0
        blink_count += 1

    player2.draw()
    treasure.draw()
    for wall in wall_list:
        wall.draw()

    if finish == False:
        safety_x = player1.rect.x
        safety_y = player1.rect.y
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and player1.rect.x < window_width - player1.size_x:
            player1.rect.x += player1.speed
        elif keys_pressed[K_a] :
            player1.rect.x -= player1.speed
        elif keys_pressed[K_w] :
            player1.rect.y -= player1.speed
        elif keys_pressed[K_s] :
            player1.rect.y += player1.speed

        goto_x, goto_y = route_list[route]
        if (ok_x == False):
            if (player2.rect.x < goto_x):
                player2.rect.x += player2.speed
            elif (player2.rect.x > goto_x):
                player2.rect.x -= player2.speed
            else:
                ok_x = True
        if (ok_y == False):
            if (player2.rect.y < goto_y):
                player2.rect.y += player2.speed
            elif (player2.rect.y > goto_y):
                player2.rect.y -= player2.speed
            else:
                ok_y = True

        if (ok_x == True and ok_y == True):
            route += 1
            ok_x = False
            ok_y = False
            if (route >= len(route_list)):
                route = 0
        
        is_collide = sprite.collide_rect(player1, player2)
        if (is_collide and isImmortal==False): # is_collide == 1
            player1.hp -= 1
            player1.rect.x = 50
            player1.rect.y = 50
            print("Immortal time")
            isImmortal = True
            immortal_time_start = timer.time()
        
        for wall in wall_list:
            is_collide = sprite.collide_rect(player1, wall)
            if (is_collide): # is_collide == 1
                if (isImmortal==False):
                    player1.hp -= 1
                    player1.rect.x = 50
                    player1.rect.y = 50
                    print("Immortal time")
                    isImmortal = True
                    immortal_time_start = timer.time()
                else:
                    player1.rect.x = safety_x
                    player1.rect.y = safety_y
        if isImmortal == True and timer.time() - immortal_time_start > 3:
            isImmortal = False
            print("Immortal end")
        
        if player1.hp == 0:
            finish = True
            # isWin = False
        
        # if ...:
        #     finish
        #     isWin
    else:
        # if ...
        text_area = Surface( (225, 75) )
        text_area.fill( (255,255,255) )
        text = style.render("YOU LOSE", True, (230, 71, 60))
        window.blit(text_area, (225, 225))
        window.blit(text, (250, 250))
    
    display.update()
    clock.tick(fps)
