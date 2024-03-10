import turtle
import os
import time

# Turtle Object To Print the Game Screen
window = turtle.Screen()
window.title("Pong")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# Turtle Object to Print Text
title1 = turtle.Turtle()
title1.penup()
title1.speed(0)
title1.hideturtle()
title1.goto(0, 180)
title1.color("white")
title1.write("Main Menu", align="center", font=("Arial", 30, "bold"))

# Turtle Object to Print Instructions
instructions = turtle.Turtle()
instructions.penup()
instructions.hideturtle()
instructions.speed(0)
instructions.color("white")

# Turtle Object for Start Button
pen1 = turtle.Turtle()
pen1.hideturtle()
pen1.pencolor('#111111')
pen1.fillcolor('white')

# Turtle Object for Instruction Button
pen2 = turtle.Turtle()
pen2.hideturtle()
pen2.pencolor('#111111')
pen2.fillcolor('white')

# Turtle Object for Return to Menu Button
pen3 = turtle.Turtle()
pen3.hideturtle()
pen3.pencolor('#111111')
pen3.fillcolor('white')

# Height and Width of Start Button
Button_x = -50
Button_y = 10
ButtonLength = 100
ButtonWidth = 50

# Height and Width of Instruction Button
Button_x1 = -50
Button_y1 = -70
ButtonLength1 = 100
ButtonWidth1 = 50

# Height and Width of Return to Main Menu Button
Button_x2 = -80
Button_y2 = -150
ButtonLength2 = 170
ButtonWidth2 = 50


# Function To Draw Start Button
def draw_rect_button(pen1, message='Start'):
    pen1.penup()
    pen1.begin_fill()
    pen1.goto(Button_x, Button_y)
    pen1.goto(Button_x + ButtonLength, Button_y)
    pen1.goto(Button_x + ButtonLength, Button_y + ButtonWidth)
    pen1.goto(Button_x, Button_y + ButtonWidth)
    pen1.goto(Button_x, Button_y)
    pen1.end_fill()
    pen1.goto(Button_x + 15, Button_y + 15)
    pen1.write(message,  font=('Arial', 15, 'normal'))


# Function To Draw Instruction Button
def draw_rect_button1(pen2, message='Instructions'):
    pen2.penup()
    pen2.begin_fill()
    pen2.goto(Button_x1, Button_y1)
    pen2.goto(Button_x1 + ButtonLength1, Button_y1)
    pen2.goto(Button_x1 + ButtonLength1, Button_y1 + ButtonWidth1)
    pen2.goto(Button_x1, Button_y1 + ButtonWidth1)
    pen2.goto(Button_x1, Button_y1)
    pen2.end_fill()
    pen2.goto(Button_x1 + 15, Button_y1 + 15)
    pen2.write(message,  font=('Arial', 15, 'normal'))


# Function To Draw Return to Main Menu Button
def draw_rect_button2(pen3, message='Return To Main Menu'):
    pen3.penup()
    pen3.begin_fill()
    pen3.goto(Button_x2, Button_y2)
    pen3.goto(Button_x2 + ButtonLength2, Button_y2)
    pen3.goto(Button_x2 + ButtonLength2, Button_y2 + ButtonWidth2)
    pen3.goto(Button_x2, Button_y2 + ButtonWidth2)
    pen3.goto(Button_x2, Button_y2)
    pen3.end_fill()
    pen3.goto(Button_x2 + 15, Button_y2 + 15)
    pen3.write(message,  font=('Arial', 15, 'normal'))


# Function Calling
draw_rect_button(pen1)
draw_rect_button1(pen2)

# Score
score_a = 0
score_b = 0

# Paddlde A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-370, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(370, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2  # Moving the ball by 2 pixels
ball.dy = 2

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 280)


# Function
def paddle_a_up():
    y = paddle_a.ycor()  # ycor return the y coordinate
    y += 20
    paddle_a.sety(y)


def paddle_a_down():
    y = paddle_a.ycor()  # ycor return the y coordinate
    y -= 20
    paddle_a.sety(y)


def paddle_b_up():
    y = paddle_b.ycor()  # ycor return the y coordinate
    y += 20
    paddle_b.sety(y)


def paddle_b_down():
    y = paddle_b.ycor()  # ycor return the y coordinate
    y -= 20
    paddle_b.sety(y)  # Setting the new coordinate


# Keyboard Binding
window.listen()
window.onkeypress(paddle_a_up, "w")
window.onkeypress(paddle_a_down, "s")
window.onkeypress(paddle_b_up, "Up")
window.onkeypress(paddle_b_down, "Down")


# Function to Check if the Button is Pressed
def button_click(x, y):
    if Button_x <= x <= Button_x + ButtonLength:
        if Button_y <= y <= Button_y + ButtonWidth:
            title1.clear()
            pen1.clear()
            pen2.clear()
            play_game()
    if Button_x1 <= x <= Button_x1 + ButtonLength1:
        if Button_y1 <= y <= Button_y1 + ButtonWidth1:
            title1.clear()
            pen1.clear()
            pen2.clear()
            instructions.write("Instructions\n\n\n\n", align="center",  font=("Courier", 19, "normal"))
            instructions.write("This is a 2 Player Game.\nPlayer A can move using W and S Key.\nPlayer B can move using Up and Down Arrow Key.", align="center", font=("Courier", 19, "normal"))
            draw_rect_button2(pen3)

        if Button_x2 <= x <= Button_x2 + ButtonLength2:
            if Button_y2 <= y <= Button_y2 + ButtonWidth1:
                instructions.clear()
                pen3.clear()
                title1.write("Main Menu", align="center", font=("Arial", 30, "bold"))
                draw_rect_button(pen1)
                draw_rect_button1(pen2)


# Function to Set the Window when the Ball is Moving
def set_window():
    window.update()

    # Move the Ball
    ball.setx(ball.xcor() + ball.dx * 3)  # Speed of ball
    ball.sety(ball.ycor() + ball.dy * 3)


# Main Loop
def play_game():
    pen.write("Player A: 0  Player B: 0", align="center", font=("Arial", 19, "normal"))
    global score_a, score_b
    while True:
        set_window()

        # Border Checking
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
            os.system("afplay bounce.wav&")  # added & at the end to prevent delay when the sound plays

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
            os.system("afplay bounce.wav&")

        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            if score_a == 5:
                pen.clear()
                pen.write("Player A Wins", align="center", font=("Arial", 19, "normal"))
                time.sleep(1)
                score_a = 0
                score_b = 0
                set_window()
            pen.clear()
            pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Arial", 19, "normal"))

        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            if score_b == 5:
                pen.clear()
                pen.write("Player B Wins", align="center", font=("Arial", 19, "normal"))
                time.sleep(1)  # delay function imported using time library
                score_a = 0
                score_b = 0
                set_window()
            pen.clear()
            pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Arial", 19, "normal"))

        # Paddle and Ball Collision
        if ball.xcor() > 360 and ball.xcor() < 370 and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
            ball.setx(340)
            ball.dx *= -1
            os.system("afplay bounce.wav&")

        if ball.xcor() < -360 and ball.xcor() > -370 and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
            ball.setx(-340)
            ball.dx *= -1
            os.system("afplay bounce.wav&")


window.onclick(button_click)
turtle.done()
