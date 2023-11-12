import turtle as trtl
import random as rand
from threading import Thread

#----SetUp----#
wn =trtl.Screen()
wn.setup(width=1.0, height=1.0)
wn.bgcolor("azure")

targets_trtl = []
ammo = []
direction = {'Left': 10, 'Right': -10} #angle change
movement = {'w': 90, 'a': 180, 's': -90, 'd': 0} #diration
t_font = ('Arial', 20, 'bold')

timer = 30
interval = 1000
timer_up = False

#Start Screen
play_button = 'play.gif'
wn.addshape(play_button)
start = trtl.Turtle()
start.pu()
start.pencolor('sandy brown')
start.write('Turle Shoot', align='center', font=('Arial', 80, 'bold'))
start.sety(-100)
start.shape(play_button)
start.turtlesize(5)

#==========================FUNCTIONS==========================#
def shoot_bullet(): #Shoot bullet
    if not timer_up: 
        if not not ammo: #There is ammo to use
            ammo.remove(bullet)
            bounce(bullet)
            bullet_reset()
    else:
        bullet.clear()
        
def bullet_reset():
    ammo.append(bullet)
    bullet.hideturtle()

def change_direct(direct):
    if not timer_up:
        
        player.seth(player.heading()+(direction[direct]))
        draw_guide()

def bound(key):
    if not timer_up:
        if key == 'w':
            if player.ycor() < 155:
                move_trtl(key)
        elif key == 's':
            if player.ycor() > -160:
                move_trtl(key)
        elif key == 'a':
            if player.xcor() > -160:
                move_trtl(key)
        elif key == 'd':
            if player.xcor() < 160:
                move_trtl(key)

def move_trtl(key):
    player.seth(movement[key])
    player.forward(10)
    draw_guide()
    
def draw_target(trtl): #Randomly spawn a coin somewhere
    trtl.shape('circle')
    trtl.color('gold')
    trtl.goto((rand.randint(-140,140)), rand.randint(-140,-10)) and (player.xcor(-140,130), player.ycor(10,140))

def bounce(trtl): #Make thing bounce off of wall
    trtl.speed(0)
    trtl.goto(player.pos())
    trtl.seth(player.heading())
    trtl.showturtle()
    trtl.forward(20)
    trtl.speed(1)
    while not (abs(player.ycor()- trtl.ycor()) < 15 and abs(player.xcor()- trtl.xcor()) < 15):
        if not pic_collisions(trtl):
            if -160 < trtl.xcor() < 160 and -160 < trtl.ycor() < 155:
                trtl.forward(10)
                if trtl == guide:
                    trtl.stamp()
            else:
                trtl.left(90)
                trtl.forward(10)
        else:
            if trtl == bullet:
                global timer
                timer +=1
                bullet_reset()
                draw_target(pic_collisions(trtl))
            break

def pic_collisions(trtl): #detect collission for coin
    for coin in targets_trtl:
        if abs(coin.ycor() - trtl.ycor()) < 15 and abs(coin.xcor() - trtl.xcor()) < 15:
            return coin

def countdown(): #Timer
    global timer, timer_up
    counter.clear()
    if timer <= 0:
        counter.write("Time's Up", align= 'center', font=t_font)
        timer_up = True
    else:
        counter.write(f'Time left: {str(timer)}s',  align= 'center', font=t_font)
        timer -= 1
        counter.getscreen().ontimer(countdown, interval) 
        
def draw_guide(): #Guide for the player
    wn.tracer(False)
    guide.clear()
    bounce(guide)
    wn.tracer(True)
    wn.update()

def game(x, y): #Game Screen
    wn.clear()
    global counter, player, bullet, guide
    wn.bgcolor("azure")
    wn.tracer(False)
    board = trtl.Turtle() #board
    board.pensize(3)
    board.speed(0)
    board.pu()
    board.goto(-160,160)
    board.pd()
    for i in range (4):
        board.forward(320)
        board.right(90)
    board.hideturtle()

    counter = trtl.Turtle() #Timer
    counter.pu()
    counter.hideturtle()
    counter.goto(275, 125)
    
    player = trtl.Turtle("turtle") 
    player.color("red")
    player.pu()
    player.speed(0)

    guide = trtl.Turtle()
    guide.hideturtle()
    guide.pu()
    guide.color('dark gray')

    for targets in range (3): #Create 3 coin 
        target = trtl.Turtle()
        target.pu()
        target.speed(0)
        targets_trtl.append(target)
        
    bullet = trtl.Turtle()
    bullet.hideturtle()
    bullet.pu()
    ammo.append(bullet) #add bullet to ammo
    for targets in range (3): #Spawn the 3 coin at a random location
        draw_target(targets_trtl[targets])
    wn.tracer(True)
    wn.update()

    for directions in direction.keys():
        Thread(target=wn.onkeypress(lambda x=directions: change_direct(x), directions)).start()
    for move in movement.keys():
        Thread(target=wn.onkeypress(lambda x=move: bound(x), move)).start()
    Thread(target=wn.onkeypress(shoot_bullet, "space")).start() #Allow for bullet and player to move at the same timer
    wn.listen()
    wn.ontimer(countdown, interval)

#=============Game============#
start.onclick(game)
wn.mainloop()