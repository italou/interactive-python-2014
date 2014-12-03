"""
Week 4 Mini-project

Descprition: Implementation of Pong
     Author: Itamar M. B. Lourenço
       Date: 2014-10-14
"""

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
# paddle1_pos is the vertical distante of the (center of) left paddle from top
paddle1_pos = HEIGHT / 2
# paddle1_vel is the vertical velocity of left paddle
paddle1_vel = 0
# paddle2_pos is the  vertical distante of the (center of) right paddle from top
paddle2_pos = HEIGHT / 2
# paddle2_vel is the vertical velocity of right paddle
paddle2_vel = 0
# speed factor for game (paddles)
game_speed = 5
score1 = 0
score2 = 0

p1_name = "Player 1"
p2_name = "Player 2"

computer_player = False

# variables for game info
game_paused = False
old_ball_vel = [0, 0]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # initialize ball position and velocity
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    
    # generates random ball velocity (60 = canvas refresh rate)
    vel_x = random.randrange(120, 240) / 60
    vel_y = random.randrange(60, 180) / 60

    # sets the correct direction of speed    
    if direction == RIGHT:
        ball_vel = [vel_x, -vel_y]
    elif direction == LEFT:
        ball_vel = [-vel_x, -vel_y]

# Exits the game
def exit():
    frame.stop()

# Pauses / Continues the game
def pause():
    global game_paused, ball_vel, old_ball_vel, paddle1_vel, paddle2_vel
    if game_paused:
        ball_vel = old_ball_vel
        game_paused = False
        pause_btn.set_text("Pause")
    else:
        old_ball_vel = ball_vel
        ball_vel = [0, 0]
        game_paused = True
        pause_btn.set_text("Continue")
    # to reset paddles when pausing/continuing the game
    paddle1_vel = 0
    paddle2_vel = 0
        
        
# formats score into two digits string
def format_score(value):
    if value < 10:
        return "0" + str(value)
    else:
        return str(value)
    
# switch between computer and human player
def switch_pc_player():
    global computer_player, p1_name, p2_name, paddle1_vel
    if computer_player:
        computer_player = False
        pc_player_btn.set_text("PC vs Player")
        p1_name = "Player 1"
        paddle1_vel = 0
    else:
        computer_player = True
        pc_player_btn.set_text("Player vs Player")
        p1_name = "Computer"
        
    new_game()
        

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global game_paused
    
    # sets paddles initial position
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    
    # score reset
    score1 = 0
    score2 = 0
    
    pause_btn.set_text("Pause")
    collision_label.set_text("Last collision:") # for game info
    game_paused = False
    
    # random initial ball start
    if random.randrange(0, 2) == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

# draw handler
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
        
    # draw mid line
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 4, "White")
    #draw top and bottom walls
    canvas.draw_line([0, 0],[WIDTH, 0], 4, "White")
    canvas.draw_line([0, HEIGHT],[WIDTH, HEIGHT], 4, "White")
    # draw gutters
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # checks for top or bottom of screen/canvas
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        # extra check for game info only
        if ball_pos[1] <= BALL_RADIUS:
            collision_label.set_text("Last collision: Top Wall") # for game info
        else:
            collision_label.set_text("Last collision: Bottom Wall") # for game info
        ball_vel[1] = -ball_vel[1]
    # checks for left gutter collision
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        # checks left paddle collision. If yes, bounce and increases ball velocity by 10%
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            collision_label.set_text("Last collision: Left Paddle") # for game info
            ball_vel[0] = -ball_vel[0] * 1.10
            ball_vel[1] = ball_vel[1] * 1.10
        else:
            collision_label.set_text("Last collision: Left Gutter") # for game info
            score2 += 1
            spawn_ball(RIGHT)
    # checks for right gutter collision
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        # checks right paddle collision. If yes, bounce and increases ball velocity by 10%
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            collision_label.set_text("Last collision: Right Paddle") # for game info
            ball_vel[0] = -ball_vel[0] * 1.10
            ball_vel[1] = ball_vel[1] * 1.10
        else:
            collision_label.set_text("Last collision: Right Gutter") # for game info
            score1 += 1
            spawn_ball(LEFT)
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # for game info
    ball_pos_label.set_text("[" + str(round(ball_pos[0], 2)) + ", " + str(round(ball_pos[1], 2)) + "]")
    ball_vel_label.set_text("[" + str(round(ball_vel[0], 4)) + ", " + str(round(ball_vel[1], 4)) + "]")
    
    # computer player paddle movement
    if computer_player:
        # PC player only sees his side of the field
        if ball_pos[0] <= WIDTH / 2:
            if ball_pos[1] > paddle1_pos - PAD_HEIGHT/6 and ball_pos[1] < paddle1_pos + PAD_HEIGHT/6:
                paddle1_vel = 0
            elif ball_pos[1] > paddle1_pos - PAD_HEIGHT/6:
                paddle1_vel = game_speed
            else:
                paddle1_vel = -game_speed
        else:
            paddle1_vel = 0
    
    # checks if paddles new position is inside screen/canvas. If yes, updates the position
    if (paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT) and (paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT) and (paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos += paddle2_vel
    
    # transform paddles center position to top and bottom points for draw_line
    paddle1_p1 = [HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]
    paddle1_p2 = [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]
    paddle2_p1 = [WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]
    paddle2_p2 = [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]
    
    # draw paddles
    canvas.draw_line(paddle1_p1, paddle1_p2, PAD_WIDTH, "White")
    canvas.draw_line(paddle2_p1, paddle2_p2, PAD_WIDTH, "White")
    
    # for game info
    pad1_label.set_text("P1 (center): " + str(paddle1_pos) + " | V: " + str(paddle1_vel))
    pad2_label.set_text("P2 (center): " + str(paddle2_pos) + " | V: " + str(paddle2_vel))
    
    # draw scores
    canvas.draw_text(format_score(score1), (WIDTH / 3, 50), 62, 'White', 'sans-serif')
    canvas.draw_text(format_score(score2), (WIDTH / 2 + WIDTH / 20, 50), 62, 'White', 'sans-serif')
    
    # draw players name
    canvas.draw_text(p1_name, (20, HEIGHT - 10), 14, 'White', 'sans-serif')
    canvas.draw_text(p2_name, (WIDTH -75, HEIGHT - 10), 14, 'White', 'sans-serif')

# key event handlers
def keydown(key):
    global paddle1_vel, paddle2_vel, computer_player
    if not game_paused:
        if key == simplegui.KEY_MAP["w"] and not computer_player:
            paddle1_vel -= game_speed
        elif key == simplegui.KEY_MAP["s"] and not computer_player:
            paddle1_vel += game_speed
        elif key == simplegui.KEY_MAP["up"]:
            paddle2_vel -= game_speed
        elif key == simplegui.KEY_MAP["down"]:
            paddle2_vel += game_speed
    else:
        paddle1_vel = 0
        paddle2_vel = 0
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if not game_paused:
        if key == simplegui.KEY_MAP["w"] and not computer_player:
            paddle1_vel += game_speed
        elif key == simplegui.KEY_MAP["s"] and not computer_player:
            paddle1_vel -= game_speed
        elif key == simplegui.KEY_MAP["up"]:
            paddle2_vel += game_speed
        elif key == simplegui.KEY_MAP["down"]:
            paddle2_vel -= game_speed
    else:
        paddle1_vel = 0
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button("Restart", new_game, 150)
pc_player_btn = frame.add_button("PC vs Player", switch_pc_player, 150)
pause_btn = frame.add_button("Pause", pause, 150)
frame.add_button("Exit", exit, 150)

# for game info
frame.add_label("Paddles (W: " + str(PAD_WIDTH) + ", H: " +str(PAD_HEIGHT) + "):")
pad1_label = frame.add_label("P1: Center")
pad2_label = frame.add_label("P2: Center")
frame.add_label("")
frame.add_label("Ball (radius: " + str(BALL_RADIUS) + "):")
ball_pos_label = frame.add_label("[Center]")
ball_vel_label = frame.add_label("[Velocity]")
frame.add_label("")
collision_label = frame.add_label("Last collision:")
frame.add_label("")
frame.add_label("P1 keys: w / s")
frame.add_label("P2 keys: up / down arrows")

# start frame
new_game()
frame.start()