"""
Week 7 Mini-project

Descprition: Implementation of Spaceship
     Author: Itamar M. B. Lourenço
       Date: 2014-11-05
"""
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

TURN_FACTOR = math.radians(4) # degrees to radians
THRUST_FACTOR = 0.35 # acceleration
FRICTION_FACTOR = 0.02 # de-acceleration factor

ROCK_MAX_ROT = 0.10

MISSILE_SPEED_FACTOR = 8

# DEBUG
DEBUG = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://dl.dropbox.com/s/rpnyczqnoha2a50/thrustmm.mp3")
#ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        ship_thrust_sound.rewind()
        
    def draw(self,canvas):
        if self.thrust: # if moving, draw ship image with thrust flames
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0],
                                           self.image_center[1]], 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # for debug only
        if DEBUG:
            canvas.draw_circle(self.pos, self.radius, 2, "White")

    def update(self):
        # if ship is moving, update angular velocity
        if self.thrust:
            self.vel[0] += THRUST_FACTOR * angle_to_vector(self.angle)[0]
            self.vel[1] += THRUST_FACTOR * angle_to_vector(self.angle)[1]
        # update ship angle
        self.angle = (self.angle + self.angle_vel) % math.radians(360)
        # apply friction to velocity
        self.vel[0] *= (1 - FRICTION_FACTOR)
        self.vel[1] *= (1 - FRICTION_FACTOR)
        # update ship position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # some math to always have ship inside canvas
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        # for debug only
        if DEBUG:
            shiplabel_pos.set_text("Position: [" + str(int(my_ship.pos[0])) + ", " + 
                                                       str(int(my_ship.pos[1])) + "]")
            shiplabel_vel.set_text("Velocity: [" + str(round(my_ship.vel[0], 3)) + ", " + 
                                                       str(round(my_ship.vel[1], 3)) + "]")
            shiplabel_ang.set_text("Angle: " + str(round(my_ship.angle, 3)))
            shiplabel_ang_v.set_text("Angle Vel: " + str(round(my_ship.angle_vel, 3)))
            
    # set ship angle (turn) velocity, or stops turning if 0
    def set_angle_vel(self, angle_vel = 0):
        if angle_vel == 0:
            self.angle_vel = 0
        else:
            self.angle_vel += angle_vel

    # switch thrusters on and off
    def switch_thrust(self):
        self.thrust = not self.thrust
        # if on, play thrusters sound
        if self.thrust:
            ship_thrust_sound.play()
        # if off, stop/rewind thrusters sound
        else:
            ship_thrust_sound.rewind()

    # turn ship left
    def turn_left(self):
        self.set_angle_vel(-TURN_FACTOR)
    
    # turn ship right    
    def turn_right(self):
        self.set_angle_vel(TURN_FACTOR)

    # shoot a missile
    def shoot(self):
        global a_missile
        # get ship angle for missile start position and velocity
        angle = angle_to_vector(self.angle)
        # missile start position from ship tip position
        missile_pos = [self.pos[0] + angle[0] * self.image_center[0],
                       self.pos[1] + angle[1] * self.image_center[1]]
        # missile velocity is ship velocity (and direction) plus own velocity
        missile_vel = [self.vel[0] + MISSILE_SPEED_FACTOR * angle[0],
                       self.vel[1] + MISSILE_SPEED_FACTOR * angle[1]]
        # spawn missile
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
# END Chip class        
  
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        # for debug only    
        if DEBUG:
            canvas.draw_circle(self.pos, self.radius, 2, "Red")
    
    def update(self):
        # update object (turning) angle
        self.angle = (self.angle + self.angle_vel) % math.radians(360)
        # update object position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # some math to always have object inside canvas
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
        # for debug only
        if DEBUG:
            rocklabel_pos.set_text("Position: [" + str(int(a_rock.pos[0])) + ", " + 
                                                       str(int(a_rock.pos[1])) + "]")
            rocklabel_vel.set_text("Velocity: [" + str(round(a_rock.vel[0], 2)) + ", " + 
                                                       str(round(a_rock.vel[1], 2)) + "]")
            rocklabel_ang.set_text("Angle: " + str(round(a_rock.angle, 3)))
            rocklabel_ang_v.set_text("Angle Vel: " + str(round(a_rock.angle_vel, 3)))
            
            misslabel_pos.set_text("Position: [" + str(int(a_missile.pos[0])) + ", " + 
                                                       str(int(a_missile.pos[1])) + "]")
            misslabel_vel.set_text("Velocity: [" + str(round(a_missile.vel[0], 2)) + ", " + 
                                                       str(round(a_missile.vel[1], 2)) + "]")
            misslabel_ang.set_text("Angle: " + str(round(a_missile.angle, 3)))
            misslabel_ang_v.set_text("Angle Vel: " + str(round(a_missile.angle_vel, 3)))
# END Sprite class
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    canvas.draw_text("Lives", [20, 30], 20, "White")
    canvas.draw_text(str(lives), [20, 55], 20, "White")
    
    canvas.draw_text("Score", [WIDTH - 80, 30], 20, "White")
    canvas.draw_text(str(score), [WIDTH - 80, 55], 20, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    vel = [random.choice([-1, 1]) * (random.random() + ROCK_MAX_ROT),
           random.choice([-1, 1]) * (random.random() + ROCK_MAX_ROT)]
    rotation = random.choice([-1, 1]) * (random.random() * ROCK_MAX_ROT) 
    a_rock = Sprite(pos, vel, 0, rotation, asteroid_image, asteroid_info)

# keydown handler
def keydown(key):
    for i in move_keys:
        if key == simplegui.KEY_MAP[i]:
            move_keys[i]()

# keyup handler
def keyup(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.switch_thrust()
    elif key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.set_angle_vel()
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
# def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

move_keys = {"up": my_ship.switch_thrust,
             "left": my_ship.turn_left,
             "right": my_ship.turn_right,
             "space": my_ship.shoot}

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# some game debug info
if DEBUG:
    frame.add_label("Ship Info:")
    shiplabel_pos = frame.add_label("Position:" + str(my_ship.pos))
    shiplabel_vel = frame.add_label("Velocity:" + str(my_ship.vel))
    shiplabel_ang = frame.add_label("Angle:" + str(my_ship.angle))
    shiplabel_ang_v = frame.add_label("Angle Vel:" + str(my_ship.angle_vel))
    frame.add_label("")
    frame.add_label("Rock Info:")
    rocklabel_pos = frame.add_label("Position:" + str(a_rock.pos))
    rocklabel_vel = frame.add_label("Velocity:" + str(a_rock.vel))
    rocklabel_ang = frame.add_label("Angle:" + str(a_rock.angle))
    rocklabel_ang_v = frame.add_label("Angle Vel:" + str(a_rock.angle_vel))
    frame.add_label("")
    frame.add_label("Missile Info:")
    misslabel_pos = frame.add_label("Position:" + str(a_missile.pos))
    misslabel_vel = frame.add_label("Velocity:" + str(a_missile.vel))
    misslabel_ang = frame.add_label("Angle:" + str(a_missile.angle))
    misslabel_ang_v = frame.add_label("Angle Vel:" + str(a_missile.angle_vel))
    frame.add_label("")

# get things rolling
timer.start()
frame.start()
