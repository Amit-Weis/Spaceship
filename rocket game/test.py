
# At least 1 of the following: draw.polygon(), draw.line()
# make a ui using draw.polygon()

import pygame
import math
import sys
import os
from random import randint as rint

#  coords = [(x,y), ]

pygame.init()

spaceheld = False
# Set up the display
WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship")
pygame.font.SysFont("Arial", 24)

RED = (255, 0, 0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Load an image


player = pygame.image.load("rocket game/Player_2.png")
player = pygame.transform.scale(player, (25, 25))
enemy = pygame.image.load("rocket game/enemy.png")
enemy = pygame.transform.scale(enemy, (30,26))

rotated_player = player
rotated_enemy = enemy

MAX_SPEED = 100
tempvelocity, currentmap =  [0,0], -1

class Spaceship:
    def __init__(self, x, y, delta_x, delta_y, velocity, direction_x, direction_y, planar_coords, projectiles, angle, clock_hold, dead) -> None:
        self.x = x
        self.y = y
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.velocity = velocity
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.planar_coords = planar_coords
        self.projectiles = projectiles
        self.angle = angle
        self.clock_hold = clock_hold
        self.dead = dead
        
p = Spaceship(500, 500, 0, 0, [0, 0], 0.0, 0.0, [0, 0], [], 0.0, 0, False)


astriods = []
astriod_maps = []
clock = pygame.time.Clock()
class Astroid:
    def __init__(self,x,y,velocity,destroyed, size) -> None:
        self.x = x
        self.y = y
        self.velocity = velocity
        self.destroyed = destroyed
        self.size = size

class Astroid_map:
    def __init__(self, astriods,planar_coords) -> None:
        self.astriods = astriods
        self.planar_coords = planar_coords
        
    def make_new_astriods(self, amount, delta_time):
        for i in range(amount):
            self.astriods.append(Astroid(rint(0,1000),rint(0,1000),[rint(-1,1)*delta_time, rint(-1,1)*delta_time],False, rint(5,15)))
        
        
astriod_maps.append(Astroid_map([],[0,0]))

class Projectile:
    def __init__(self, x, y, velocity, destroyed):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.destroyed = destroyed
        
def planarcheck(x,y,planar_coords):

    return x,y,planar_coords

# Main loop

gameover = False
enemies = []
enemies.append(Spaceship(100, 100, 0, 0, [0, 0], 0.0, 0.0, [0, 0], [], 0.0, 0, False))

delta_time_tracker = 0
clock_hold = 0
won = False
round = 0
deathcounter = 0


while True:
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, BLACK, (0, 0, 1000, 1000))
    pygame.draw.polygon(screen, BLACK, [[300, 300], [100, 400],[100, 300]])
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    delta_time = clock.tick(60) / 1000.0  # Convert to seconds
    delta_time_tracker += delta_time

    for e in enemies:
        if not e.dead:
            if e.x == 1000 or e.x == 0 or e.y == 1000 or e.y == 0:

                e.velocity = [0,0]
                if e.x == 1000 or e.x == 0:
                    if e.x == 1000:
                        e.planar_coords[0] += 1
                        
                    if e.x == 0:
                        e.planar_coords[0] -= 1  
                    e.x = abs(e.x-999)

                
                if e.y == 1000 or e.y == 0:
                    if e.y == 1000:
                        e.planar_coords[1] -= 1
                    if e.y == 0:      
                        e.planar_coords[1] += 1
                    e.y = abs(e.y-999)
                    
            if p.planar_coords != e.planar_coords and 4 < delta_time_tracker - e.clock_hold:
                e.clock_hold = delta_time_tracker


            if 4 > delta_time_tracker - e.clock_hold > 3 and e.clock_hold != 0 and e.planar_coords != p.planar_coords:

                e.velocity = [0,0]
                if p.planar_coords[0] - e.planar_coords[0] >= 1:
                    e.planar_coords = p.planar_coords.copy()
                    e.x = 1
                    
                elif p.planar_coords[0] - e.planar_coords[0] <= -1:
                    e.planar_coords = p.planar_coords.copy()
                    e.x = 999
                    
                if p.planar_coords[1] - e.planar_coords[1] >= 1:
                    e.planar_coords = p.planar_coords.copy()
                    e.y = 1
                    
                elif p.planar_coords[0] - e.planar_coords[0] <= -1:
                    e.planar_coords = p.planar_coords.copy()
                    e.y = 999
        

            if delta_time_tracker > 1.5 and p.planar_coords == e.planar_coords:              
                
                if math.sqrt(e.delta_x ** 2 + e.delta_y ** 2) != 0:
                    e.direction_x = e.delta_x / math.sqrt(e.delta_x ** 2 + e.delta_y ** 2)
                    e.direction_y = e.delta_y / math.sqrt(e.delta_x ** 2 + e.delta_y ** 2)
                # Calculate the velocity comeonents
                e.velocity[0] += e.direction_x * MAX_SPEED/50 
                e.velocity[1] += e.direction_y * MAX_SPEED/50 
                

                
                # Uedate the eosition of the image based on its velocity and delta time
                e.x = max(min(1000,e.x + e.velocity[0] * delta_time),0)
                e.y = max(min(1000,e.y + e.velocity[1] * delta_time),0)
                if -0.01 < delta_time_tracker % 0.017*5 < 0.01:
                    if math.degrees(math.atan2(e.delta_x, e.delta_y)) != 0.0:
                        e.angle = math.degrees(math.atan2(e.delta_x, e.delta_y))
                    e.delta_x = p.x - e.x
                    e.delta_y = p.y - e.y
                    if math.sqrt(e.delta_x ** 2 + e.delta_y ** 2) != 0:
                        e.direction_x = e.delta_x / math.sqrt(e.delta_x ** 2 + e.delta_y ** 2)
                        e.direction_y = e.delta_y / math.sqrt(e.delta_x ** 2 + e.delta_y ** 2)
                    tempvelocity[0] = e.direction_x * MAX_SPEED
                    tempvelocity[1] = e.direction_y * MAX_SPEED
                    if math.degrees(math.atan2(e.delta_y, e.delta_x)) != 0.0:
                        e.angle = math.degrees(math.atan2(e.delta_y, e.delta_x))
                    e.projectiles.append(Projectile(e.x+tempvelocity[0]*delta_time + 13, e.y+tempvelocity[1]*delta_time+13, (tempvelocity[0]+10, tempvelocity[1]+10), False))
            
            for projectile in e.projectiles:
                if (not(0 < projectile.x < WIDTH) or not(0 < projectile.y < HEIGHT)) or projectile.destroyed:
                    e.projectiles.remove(projectile)
                
                if p.x - 10 - 13 < projectile.x < p.x + 10+13 and p.y - 10-13 < projectile.y < p.y + 10+13:
                    gameover = True
                    break
                for astriod in astriod_maps[currentmap].astriods:
                    if astriod.x - astriod.size - 10 < projectile.x < astriod.x + 10+ astriod.size and astriod.y - astriod.size - 10 < projectile.y < astriod.y + astriod.size + 10 and not astriod.destroyed:
                        astriod.destroyed = True
                        projectile.destroyed = True
                    
                    if astriod.destroyed:
                        pygame.draw.circle(screen, BLACK, (astriod.x, astriod.y), astriod.size)

                if not projectile.destroyed:
                    projectile.x += projectile.velocity[0]*3 * delta_time
                    projectile.y += projectile.velocity[1]*3 * delta_time
                    pygame.draw.circle(screen, RED, (projectile.x, projectile.y), 10)
        

    
    for astriod in astriod_maps[currentmap].astriods:
        if astriod.destroyed == False:
            pygame.draw.circle(screen, BLUE, (astriod.x, astriod.y), astriod.size)
    
    p.x += 13
    p.y += 13
    for astriod in astriod_maps[currentmap].astriods:
        if astriod.x - astriod.size -13 < p.x < astriod.x + astriod.size + 13 and astriod.y - astriod.size - 13 < p.y < astriod.y + astriod.size + 13 and not astriod.destroyed:
            gameover = True
    p.x -= 13
    p.y -= 13
    
    if gameover:
        break

    for projectile in p.projectiles:
        if (not(0 < projectile.x < WIDTH) or not(0 < projectile.y < HEIGHT)) or projectile.destroyed:
            p.projectiles.remove(projectile)
        

        for i,e in enumerate(enemies):
            for pr in e.projectiles:
                if e.x - 10 - 13 < projectile.x < e.x + 10+13 and e.y - 10-13 < projectile.y < e.y + 10+13 and not e.dead and not projectile.destroyed:
                    e.dead = True
                    deathcounter += 1
                    if len(enemies) == deathcounter:
                        enemies = []
                        deathcounter = 0
                        round += 2
                        for i in range(round):
                            enemies.append(Spaceship(rint(1,999), rint(1,999), 0, 0, [0, 0], 0.0, 0.0, p.planar_coords, [], 0.0, 0, False))
                    continue    
                if pr.x - 10 < projectile.x < pr.x + 10 and pr.y - 10 < projectile.y < pr.y + 10:
                    pr.destroyed = True
                    projectile.destroyed = True
                

        for astriod in astriod_maps[currentmap].astriods:
            if astriod.x - astriod.size - 10 < projectile.x < astriod.x + 10+ astriod.size and astriod.y - astriod.size - 10 < projectile.y < astriod.y + astriod.size + 10 and not astriod.destroyed:
                astriod.destroyed = True
                projectile.destroyed = True 
            if astriod.destroyed:
                pygame.draw.circle(screen, BLACK, (astriod.x, astriod.y), astriod.size)

        if not projectile.destroyed:
            projectile.x += projectile.velocity[0]*3 * delta_time
            projectile.y += projectile.velocity[1]*3 * delta_time
            pygame.draw.circle(screen, RED, (projectile.x, projectile.y), 10)

    if math.degrees(math.atan2(p.delta_y, p.delta_x)) != 0.0:
        p.angle = math.degrees(math.atan2(p.delta_y, p.delta_x))
    p.delta_x = mouse_pos[0] - p.x
    p.delta_y = mouse_pos[1] - p.y
    
    if math.degrees(math.atan2(e.delta_x, e.delta_y)) != 0.0:
        e.angle = math.degrees(math.atan2(e.delta_x, e.delta_y))
    e.delta_x = p.x - e.x
    e.delta_y = p.y - e.y
    if math.sqrt(p.delta_x ** 2 + p.delta_y ** 2) != 0:
        e.direction_x = p.delta_x / math.sqrt(p.delta_x ** 2 + p.delta_y ** 2)
        e.direction_y = p.delta_y / math.sqrt(p.delta_x ** 2 + p.delta_y ** 2)
    

    for event in pygame.event.get():          
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_SPACE:
                spaceheld = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # 3 represents the right mouse butto
                p.delta_x = mouse_pos[0] - p.x
                p.delta_y = mouse_pos[1] - p.y
                if math.sqrt(p.delta_x ** 2 + p.delta_y ** 2) != 0:
                    p.direction_x = p.delta_x / math.sqrt(p.delta_x ** 2 + p.delta_y ** 2)
                    p.direction_y = p.delta_y / math.sqrt(p.delta_x ** 2 + p.delta_y ** 2)
                tempvelocity[0] = p.direction_x * MAX_SPEED
                tempvelocity[1] = p.direction_y * MAX_SPEED
                if math.degrees(math.atan2(p.delta_y, p.delta_x)) != 0.0:
                    p.angle = math.degrees(math.atan2(p.delta_y, p.delta_x))
                p.projectiles.append(Projectile(p.x+tempvelocity[0]*delta_time + 13, p.y+tempvelocity[1]*delta_time+13, (tempvelocity[0]+10, tempvelocity[1]+10), False))  # auto get p.directions

        elif event.type == pygame.KEYDOWN:
            # Check if the left mouse button was clicked
            if event.key == pygame.K_SPACE:
                spaceheld = True

            if event.key == pygame.K_z:
                p.delta_x = mouse_pos[0] - p.x
                p.delta_y = mouse_pos[1] - p.y
                if math.sqrt(p.delta_x ** 2 + p.delta_y ** 2) != 0:
                    p.direction_x = p.delta_x / math.sqrt(p.delta_x ** 2 + p.delta_y ** 2)
                    p.direction_y = p.delta_y / math.sqrt(p.delta_x ** 2 + p.delta_y ** 2)
                tempvelocity[0] = p.direction_x * MAX_SPEED
                tempvelocity[1] = p.direction_y * MAX_SPEED
                if math.degrees(math.atan2(p.delta_y, p.delta_x)) != 0.0:
                    p.angle = math.degrees(math.atan2(p.delta_y, p.delta_x))
                p.projectiles.append(Projectile(p.x+tempvelocity[0]*delta_time + 13, p.y+tempvelocity[1]*delta_time+13, (tempvelocity[0]+10, tempvelocity[1]+10), False))  # auto get p.directions
                
    if spaceheld == True or mouse_buttons[0]:
        if not (mouse_pos[0] - 5 < p.x < mouse_pos[0] + 5 and mouse_pos[1] - 5 < p.y < mouse_pos[1] + 5):
            player = pygame.image.load("rocket game/Fire_Player_2.png")
            player = pygame.transform.scale(player, (25, 25))
            
            # Update the velocity of the image to move towards the mouse position
            # Calculate the p.direction vector
            if math.sqrt(p.delta_x ** 2 + p.delta_y ** 2) != 0:
                p.direction_x = p.delta_x / math.sqrt(p.delta_x ** 2 + p.delta_y ** 2)
                p.direction_y = p.delta_y / math.sqrt(p.delta_x ** 2 + p.delta_y ** 2)
            # Calculate the velocity components
            p.velocity[0] += p.direction_x * MAX_SPEED/50 
            p.velocity[1] += p.direction_y * MAX_SPEED/50 
            

            
            # Update the position of the image based on its velocity and delta time
            p.x = max(min(1000,p.x + p.velocity[0] * delta_time),0)
            p.y = max(min(1000,p.y + p.velocity[1] * delta_time),0)
            spaceheld = True 
                
    if spaceheld ==False:
        player = pygame.image.load("rocket game/Player_2.png")
        player = pygame.transform.scale(player, (25, 25)) 
        p.velocity[0] += p.direction_x * -MAX_SPEED/50 if abs(p.velocity[0]) < 0.01 else 0 
        p.velocity[1] += p.direction_y * -MAX_SPEED/50 if abs(p.velocity[1]) < 0.01 else 0
        
        p.x = max(min(1000,p.x + p.velocity[0] * delta_time),0)
        p.y = max(min(1000,p.y + p.velocity[1] * delta_time),0)
    
            
    if p.x == 1000 or p.x == 0 or p.y == 1000 or p.y == 0:
        os.system('cls')
        p.projectiles = []
        for e in enemies:
            e.projectiles = []
        found_map = False
        if p.x == 1000 or p.x == 0:
            if p.x == 1000:
                p.planar_coords[0] += 1
                
            else:
                p.planar_coords[0] -= 1  
            p.x = abs(p.x-1000)

        
        if p.y == 1000 or p.y == 0:
            if p.y == 1000:
                p.planar_coords[1] -= 1
            if p.y == 0:      
                p.planar_coords[1] += 1
            p.y = abs(p.y-1000)

            
        for j,astriodmap in enumerate(astriod_maps):
            if astriodmap.planar_coords == p.planar_coords:
                found_map = True
                for i in astriodmap.astriods:
                    if i.destroyed == True:
                        pass
                        #astriodmap.astriods.remove(i)
                    else:
                        pygame.draw.circle(screen, BLUE, (i.x, i.y), i.size)
                currentmap = j
                
        if not found_map:
            astriod_maps.append(Astroid_map([],p.planar_coords.copy()))
            print(len(astriod_maps))
            for i in range(rint(25,40)):
                astriod_maps[-1].astriods.append(Astroid(rint(0,1000),rint(0,1000),[0,0],False,rint(5,15)))
            for i in astriod_maps[-1].astriods:
                i.x = max(min(1000,i.x + i.velocity[0] * delta_time),0)
                i.y = max(min(1000,i.y + i.velocity[1] * delta_time),0)
                pygame.draw.circle(screen, BLUE, (i.x, i.y), i.size)
                    
            currentmap = len(astriod_maps)-1

        
    # Blit the image onto the screen at position (p.x, py)
    rotated_player = pygame.transform.rotate(player, -p.angle-180+45)
    screen.blit(rotated_player, (p.x, p.y))
    
    for e in enemies:
        if not e.dead and p.planar_coords == e.planar_coords:
            rotated_enemy = pygame.transform.rotate(enemy, e.angle)
            screen.blit(rotated_enemy, (e.x,e.y))
    font = pygame.font.SysFont(None, 30)
    text = font.render(str(int(delta_time_tracker)), True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    # Update the display
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    boom = pygame.image.load("rocket game/boom.png")
    boom = pygame.transform.scale(boom, (120,80 ))
    if not won:
        screen.blit(boom, (p.x-40, p.y-40))
        for e in enemies:
            if e.planar_coords == p.planar_coords:
                screen.blit(rotated_enemy, (e.x,e.y))
        
    if won:
        screen.blit(boom, (e.x-40, e.y-40))
        screen.blit(rotated_player, (p.x,p.y))
    
    for projectile in p.projectiles:
        if (not(0 < projectile.x < WIDTH) or not(0 < projectile.y < HEIGHT)) or projectile.destroyed:
            p.projectiles.remove(projectile)
            

        for astriod in astriod_maps[currentmap].astriods:
            if astriod.x - astriod.size - 10 < projectile.x < astriod.x + 10+ astriod.size and astriod.y - astriod.size - 10 < projectile.y < astriod.y + astriod.size + 10 and not astriod.destroyed:
                astriod.destroyed = True
                projectile.destroyed = True
            if astriod.destroyed:
                pygame.draw.circle(screen, BLACK, (astriod.x, astriod.y), astriod.size)

        if not projectile.destroyed:
            pygame.draw.circle(screen, RED, (projectile.x, projectile.y), 10)
    
    for e in enemies:
        for projectile in e.projectiles:
            if (not(0 < projectile.x < WIDTH) or not(0 < projectile.y < HEIGHT)) or projectile.destroyed:
                e.projectiles.remove(projectile)
            
            for astriod in astriod_maps[currentmap].astriods:
                if astriod.x - astriod.size - 10 < projectile.x < astriod.x + 10+ astriod.size and astriod.y - astriod.size - 10 < projectile.y < astriod.y + astriod.size + 10 and not astriod.destroyed:
                    astriod.destroyed = True
                    projectile.destroyed = True
                
                if astriod.destroyed:
                    pygame.draw.circle(screen, BLACK, (astriod.x, astriod.y), astriod.size)

            if not projectile.destroyed:
                # projectile.x += projectile.velocity[0]*3 * delta_time
                # projectile.y += projectile.velocity[1]*3 * delta_time
                pygame.draw.circle(screen, RED, (projectile.x, projectile.y), 10)
 

    # Draw text on the polygon
    font = pygame.font.SysFont(None, 30)
    text = font.render(str(int(delta_time_tracker)), True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()
    
    # MATHEW BUGS:
    # enemies not respoawningin properly (FIXED)
    # enemies disappearing after I die (fixed)
    # left click intead of hold perma move (FIXED on my device no one else for some reason)
    # make asteroids not on edges (no)
    # maybe less asteroids (no)
    # cursor lock inside of window figure out (not possible on code hs, and so i dont want to do it)
    # 
    
    # MATHEW FEEDBACK:
#     - enemies not respawning properly (fixed)
    # - left click perma moves (fixed in my device)
    # - make asteroids not on edges of screen (fixed)
    # - maybe less asteroids and maybe no enemy spawning on top of you (no)
    # - cursor lock inside of window (not possible in code hs)
    # - retry button (no)
    # - stage/enemy/kill count (no)
    # - maybe UI? for polygon requirement (not needed)
    # - after you get hit, your spaceship gets destroyed and then the astronaut space fighter gets ejected and has different movement velocity/acceleration and has a different gun and if astronaut space fighter dies then you lose (defeintaly no)
    # - maybe storyline/start screen (no)



