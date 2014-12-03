"""
Week 3 Mini-project

Descprition: Implementation of "Stopwatch: The Game"
     Author: Itamar M. B. Lourenço
       Date: 2014-10-13
"""

import simplegui

# global variables
tenths = 0
timer_running = False
score = 0
num_of_tries = 0
score_display = "0/0"

# helper functions
def format(t):
    """ converts time from tenths of seconds into formatted string A:BC.D (m:s.ts)
        where A, C and D are digits in the range 0-9 and B is in the range 0-5 """
    # 10 tenths = 1 second, get the reminder and convert to string
    tens = str(t % 10)
    
    # get seconds from tenths of seconds
    seconds = t / 10
    
    # get minutes from seconds
    minutes = seconds / 60

    # apply proper value range [0-59] to seconds value
    seconds = seconds % 60

    # seconds leading zero when needed
    if seconds < 10:
        secs = "0" + str(seconds)
    else:
        secs = str(seconds)
        
    mins = str(minutes)
     
    if int(mins) >= 10:
        if timer_running:
        		# just stops the timer so the player has to reset the stopwatch
            timer.stop()
        return "DONE"
    else:
        return mins + ":" + secs + "." + tens

def update_score():
    """ Validates and updates the player score """
    global timer_running, tenths, score, num_of_tries, score_display
    if timer_running:
        num_of_tries += 1
        
        # checks if time is a whole second
        if (tenths % 10 == 0):
            score += 1
            
    score_display = str(score) + "/" + str(num_of_tries)
 

# event handlers
def start():
    """ Starts the timer - button """
    global timer_running
    if not timer_running:
        timer.start()
        timer_running = True

def stop():
    """ Stops the timer - button """
    global timer_running
    if timer_running:
        timer.stop()
        update_score()
        timer_running = False

def reset():
    """ Resets the timer - button """
    global timer_running, tenths, score, num_of_tries
    if timer_running:
        stop()
    tenths = 0
    score = 0
    num_of_tries = 0
    update_score()

def update_timer():
    """ Updates / Increments the timer """
    global tenths
    tenths += 1
    
# draw handler
def draw(canvas):
    canvas.draw_text(format(tenths), [39, 115], 48, "White")
    canvas.draw_text(score_display, [150, 24], 24, "Orange")


# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 200, 200)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button("Start", start, 200)
frame.add_button("Stop", stop, 200)
frame.add_button("Reset", reset, 200)

timer = simplegui.create_timer(100, update_timer)

# start frame
frame.start()
