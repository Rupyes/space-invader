# import libraries

import turtle
import os
import math
import random


# set up the screen

win = turtle.Screen()
win.bgcolor("black")
win.title("Space invader")
win.bgpic("space_invaders_background.gif")
win.tracer(0)

# register the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

# draw border

border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()


# set the score to 0
score = 0

# draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# create the player turtle

player = turtle.Turtle()
player.color("gray")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

# choose a number of enemies

number_of_enemies = 5

# create an empty list of enemies
enemies = []

# add enemies to the list
for i in range(number_of_enemies):
    # create the enemies
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2

# create the player's bullet

bullet = turtle.Turtle()
bullet.color('yellow')
bullet.shape('triangle')
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 20

# define bullet state
# ready - ready to fire
# fire - bullet is firing

bulletstate = "ready"


# move the player left and right

def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)


def move_up():
    y = player.ycor()
    y += playerspeed
    if y > 250:
        y = 250
    player.sety(y)


def move_down():
    y = player.ycor()
    y -= playerspeed
    if y < -250:
        y = -250
    player.sety(y)


def fire_bullet():
    # declare bulletstate as a global if it needs changed
    global bulletstate

    if bulletstate == "ready":
        bulletstate = "fire"
        os.system("afplay laser.wav&")
        # move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


def isCollision(t1, t2):
    distance = math.sqrt(
        math.pow(t1.xcor() - t2.xcor(), 2) +
        math.pow(t1.ycor() - t2.ycor(), 2)
    )
    if distance < 15:
        return True
    else:
        return False


# create keyboard bindings

turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(move_up, "Up")
turtle.onkey(move_down, "Down")
turtle.onkey(fire_bullet, "space")


# main game loop
while True:
    win.update()
    for enemy in enemies:
        # move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # move the enemy back and down
        if enemy.xcor() > 280:
            # moves all the enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # change the enemies direction
            enemyspeed *= -1

        if enemy.xcor() < -280:
            # moves all the enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # change the enemies direction
            enemyspeed *= -1

        # check for a collision between the bullet and the enemy

        if isCollision(bullet, enemy):
            os.system("afplay explosion.wav&")
            # reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            # update the score
            score += 10
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=(
                "Arial", 14, "normal"))

            # reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)

        # check for a collision between the player and the enemy

        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            exit()

    # move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # check to see if the bullet has gone to the top

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
