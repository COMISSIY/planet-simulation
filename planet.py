import pygame
from math import sqrt
from random import randint
pygame.init()

w, h = 800, 500
sc = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
pause = True
show_data = True
size = 10
current_obj = -1
def ret_r(p1, p2): #get lenght between two object
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

class Interface: #class for showing planet data on main screen
    font_size = 12
    f1 = pygame.font.SysFont('arial', font_size)
    def show_data(self, obj):
        data = vars(obj)
        for n, i in enumerate(data):
            text = self.f1.render(f'{i} = {data[i]}', 0, (255, 255, 255))
            sc.blit(text, (0, n*self.font_size))

class Planet: #main planet class
    def __init__(self, pos, data=[10, 0, 0, 1, 1], static=False):
        self.pos = list(pos)#updatable data (planet possition)
        self.mass = data[0] #planet's mass
        self.vx, self.vy = [data[1], data[2]] #planet speed on X and Y axis
        self.ax, self.ay = [data[3], data[4]] #planet acceleration (will use to change planet speed)
        self.rad = self.mass #default planet radius equals planet mass (can be changed)
        self.color = [*[randint(100, 255)]*3] #random planet color from 100 to 255 for RGB
        self.static = static #planet static status (if True then planet will not move but affects on other planets)
        self.custom = False #custom orbit mode status (if True then after click on the planet will be changed planet speed)
        self.last_m_pos = self.pos #last mouse possition (needs for calculate planet speed while custom mode)

    def physics_handler(self, obj=None): #main function for calculating planet's variables
        global current_obj
        if not pause:
            if not self.static:
                if obj != None:
                    r = ret_r(self.pos, obj.pos)
                    #main calculation for a planet
                    self.ax = obj.mass * (obj.pos[0] - self.pos[0]) / r**3
                    self.ay = obj.mass * (obj.pos[1] - self.pos[1]) / r**3
                    if r < max(self.rad, obj.rad):
                        if self.mass >= obj.mass:
                            self.mass += obj.mass / 2
                            self.rad += obj.rad // 10
                            planets.remove(obj)
                        else:
                            obj.mass += self.mass / 2
                            obj.rad += self.mass // 10
                            planets.remove(self)

                        current_obj = -1
                
                    self.vx += self.ax 
                    self.vy += self.ay 
                self.pos[0] += self.vx
                self.pos[1] += self.vy
                
    def custom_parametrs(self): #function for change speed to custom speed
        global current_obj
        if pause:
            if pygame.mouse.get_pressed()[0]:
                if ret_r(self.pos, pygame.mouse.get_pos()) <= self.rad:
                    if not self.custom:
                        self.custom = True
                        self.static = False
                if self.custom:
                    current_obj = planets.index(self)
                    self.last_m_pos = pygame.mouse.get_pos()
                    pygame.draw.line(sc, (255, 0, 0), self.pos, self.last_m_pos, 2)
                    self.vx, self.vy = -(self.pos[0] - self.last_m_pos[0])/100, -(self.pos[1] - self.last_m_pos[1])/100
            else:
                self.custom = False
               
            pygame.draw.line(sc, (0, 255, 0), self.pos, self.last_m_pos)
        
    def draw(self):
        if self in planets:
            if planets.index(self) == current_obj:
                if show_data:
                    interface.show_data(self)
                pygame.draw.circle(sc, (255, 255, 255), self.pos, self.rad+1)
        if self.static:
            pygame.draw.circle(sc, (255, 0, 0), self.pos, self.rad)
        else:
            pygame.draw.circle(sc, self.color, self.pos, self.rad)

planets = []
interface = Interface()
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_t:
                show_data = not show_data
            if i.key == pygame.K_TAB:
                if current_obj + 1 > len(planets):
                    current_obj = 0
                else:
                    current_obj += 1
            if i.key == pygame.K_UP:
                planets[current_obj].mass += 10
            if i.key == pygame.K_d:
                planets.pop(current_obj)
            if i.key == pygame.K_LEFT:
                planets[current_obj].rad -= 1
            if i.key == pygame.K_s:
                planets[current_obj].static = not planets[current_obj].static
            if i.key == pygame.K_DOWN:
                planets[current_obj].mass -= 1
            if i.key == pygame.K_RIGHT:
                planets[current_obj].rad += 1
            if i.key == pygame.K_SPACE:
                pause = not pause
            if i.key == pygame.K_n:
                planets.append(Planet(pygame.mouse.get_pos(), static=False))
    sc.fill((0, 0, 0))
    clock.tick(30)
    for i in planets:
        for _ in planets:
            if _ != i:
                i.physics_handler(_)
        if len(planets) == 1:
            i.physics_handler()
        i.draw()
        i.custom_parametrs()

    pygame.display.update()
