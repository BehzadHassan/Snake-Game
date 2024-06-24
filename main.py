import time
from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
import random

WIDTH = 600
HEIGHT = 600
SPEED = 150
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#00ff00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
NO_OF_BLOCKS = 4
BLOCK_COLOR = "gray"
pause = 1
snake = object
block = object
food = object
canvas = Canvas
label = Label
score = 0
direction = 'down'
WINDOW_COLOR = "#373737"
resumebtn = Button
pausebtn = Button


class Snake:
    def __init__(self):
        global canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, width=0,
                                             tags="Snake")
            self.squares.append(square)


class Food:
    def __init__(self, snake, block):
        global canvas
        global food
        while True:
            x = random.randint(0, (WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

            self.coordinates = [x, y]
            self.x1 = 0
            for body_part in snake.coordinates[0:]:
                if x == body_part[0] and y == body_part[1]:
                    self.x1 += 1
            if self.x1 == 0 and block.coordinates != []:
                for body_part in block.coordinates[0:]:
                    if x == body_part[0] and y == body_part[1]:
                        self.x1 += 1
            if self.x1 == 0:
                break
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, width=0, tag="food")


class Block(snake):
    def __init__(self):
        global canvas
        self.coordinates = []
        self.blocks = []
        for i in range(0, NO_OF_BLOCKS):
            x = random.randint(0, (WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            if x == 0 and (
                    y == 0 or y == SPACE_SIZE or y == SPACE_SIZE * 2 or y == SPACE_SIZE * 3 or y == SPACE_SIZE * 4 or y == SPACE_SIZE * 5 or y == SPACE_SIZE * 6):
                x = random.randint(0, (WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
                y = random.randint(6, (HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates.append([x, y])

        for x, y in self.coordinates:
            block = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BLOCK_COLOR, width=0,
                                            tags="block")
            self.blocks.append(block)


class snake_game:
    def __init__(self):

        def next_turn(window):
            global snake
            global block
            global food
            global score
            global canvas
            global label
            x, y = snake.coordinates[0]

            if direction == "up":
                y -= SPACE_SIZE
            elif direction == "down":
                y += SPACE_SIZE
            elif direction == "left":
                x -= SPACE_SIZE
            elif direction == "right":
                x += SPACE_SIZE

            snake.coordinates.insert(0, (x, y))

            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, width=0, fill=SNAKE_COLOR)

            snake.squares.insert(0, square)

            if x == food.coordinates[0] and y == food.coordinates[1]:
                global score
                score += 1
                label.config(text="SCORE : {}".format(score))
                canvas.delete("food")
                food = Food(snake, block)
            else:
                del snake.coordinates[-1]
                canvas.delete(snake.squares[-1])
                del snake.squares[-1]
            global pause
            if check_collision(snake, block):
                game_over(window)
            elif pause == 0:
                window.after(SPEED, next_turn, window)

        def change_direction(new_direction):
            global direction

            if new_direction == 'left':
                if direction != 'right':
                    direction = new_direction
            elif new_direction == 'right':
                if direction != 'left':
                    direction = new_direction
            elif new_direction == 'up':
                if direction != 'down':
                    direction = new_direction
            elif new_direction == 'down':
                if direction != 'up':
                    direction = new_direction

        def check_collision(snake, block):
            x, y = snake.coordinates[0]
            if x < 0 or x >= WIDTH:
                return True
            if y < 0 or y >= HEIGHT:
                return True

            for body_part in snake.coordinates[1:]:
                if x == body_part[0] and y == body_part[1]:
                    return True

            for body_part in block.coordinates[0:]:
                if x == body_part[0] and y == body_part[1]:
                    return True

        def game_over(window):
            global score
            global canvas
            canvas.delete(ALL)
            canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("console", 50),
                               text="GAME OVER", fill=FOOD_COLOR)

        def start(window):
            global snake
            global block
            global food
            snake = Snake()
            block = Block()
            food = Food(snake, block)
            next_turn(window)
            messagebox.showinfo("INFO", "PRESS SPACE OR RESUME BUTTON TO START")

        def restart_game():
            global direction
            global score
            global pause
            global canvas
            global pausebtn
            pausebtn.config(image=resumeimg)
            pause = 1
            score = 0
            label.config(text="SCORE : {}".format(score))
            direction = "down"
            canvas.delete(ALL)
            start(window)

        def pause_game1():
            global pausebtn
            global resumeimg
            global pause
            pauseimg = PhotoImage(file="pause.png")
            resumeimg = PhotoImage(file="resume.png")
            if not check_collision(snake, block):
                pause = 1
                pausebtn.config(image=resumeimg, command=resume_game1)

        def pause_game(event):
            global pausebtn
            global resumeimg
            global pause
            pauseimg = PhotoImage(file="pause.png")
            resumeimg = PhotoImage(file="resume.png")
            if not check_collision(snake, block):
                pause = 1
                pausebtn.config(image=resumeimg, command=resume_game1)

        def resume_game(event):
            global pausebtn
            global pauseimg
            global pause
            pauseimg = PhotoImage(file="pause.png")
            resumeimg = PhotoImage(file="resume.png")
            if not check_collision(snake, block):
                pause = 0
                next_turn(window)
                pausebtn.config(image=pauseimg, command=pause_game1)

        def resume_game1():
            global pausebtn
            global pauseimg
            global pause
            pauseimg = PhotoImage(file="pause.png")
            resumeimg = PhotoImage(file="resume.png")
            if not check_collision(snake, block):
                pause = 0
                next_turn(window)
                pausebtn.config(image=pauseimg, command=pause_game1)

        def pause_game3(event):
            if pause == 0:
                pause_game1()
            else:
                resume_game1()

        def snake_color():
            color = colorchooser.askcolor()
            if color[1] != None:
                global SNAKE_COLOR
                SNAKE_COLOR = color[1]
                snakecolor.config(bg=SNAKE_COLOR)
                restart_game()

        def food_color():
            color = colorchooser.askcolor()
            if color[1] != None:
                global FOOD_COLOR
                FOOD_COLOR = color[1]
                foodcolor.config(bg=FOOD_COLOR)
                restart_game()

        def block_color():
            color = colorchooser.askcolor()
            if color[1] != None:
                global BLOCK_COLOR
                BLOCK_COLOR = color[1]
                blockcolor.config(bg=BLOCK_COLOR)
                restart_game()

        def back_color():
            color = colorchooser.askcolor()
            if color[1] != None:
                global BACKGROUND_COLOR
                BACKGROUND_COLOR = color[1]
                backcolor.config(bg=BACKGROUND_COLOR)
                canvas.config(bg=BACKGROUND_COLOR)
                restart_game()

        def setblocks():
            no = int(scale1.get())
            global NO_OF_BLOCKS
            NO_OF_BLOCKS = no
            restart_game()

        def setspace():
            no = int(scale2.get())
            global SPACE_SIZE
            global NO_OF_BLOCKS
            SPACE_SIZE = no
            if no == 10:
                scale1.config(to=200, tickinterval=40, resolution=10)
                NO_OF_BLOCKS = 0
                scale1.set(0)
            elif no == 20:
                scale1.config(to=50, tickinterval=15, resolution=5)
                NO_OF_BLOCKS = 0
                scale1.set(0)
            elif no == 30:
                scale1.config(to=40, tickinterval=10, resolution=3)
                NO_OF_BLOCKS = 0
                scale1.set(0)
            elif no == 40:
                scale1.config(to=20, tickinterval=5, resolution=2)
                NO_OF_BLOCKS = 0
                scale1.set(0)
            elif no == 50:
                scale1.config(to=10, tickinterval=2, resolution=1)
                NO_OF_BLOCKS = 0
                scale1.set(0)
            restart_game()

        def setbody():
            no = int(scale3.get())
            global BODY_PARTS
            BODY_PARTS = no
            scale3.set(no)
            restart_game()

        def setspeed():
            no = int(scale4.get())
            global SPEED
            global SPACE_SIZE
            if SPACE_SIZE == 10 or SPACE_SIZE == 20:
                SPEED = no * SPACE_SIZE * int(no / 2)
            else:
                SPEED = no * SPACE_SIZE

            scale4.set(no)
            # restart_game()

        global pausebtn
        global resumebtn
        global canvas
        global score
        global label
        global WINDOW_COLOR
        window = Tk()
        window.resizable(width=False, height=False)
        window.title("Snake Game")
        window.iconphoto(True, PhotoImage(file="snake_icon.png"))
        window.config(bg=WINDOW_COLOR)

        pauseimg = PhotoImage(file="pause.png")
        resumeimg = PhotoImage(file="resume.png")
        restartimg = PhotoImage(file="restart.png")
        score = 0

        label = Label(
            window,
            text="SCORE : {}".format(score),
            fg="#00ff00",
            bg=WINDOW_COLOR,
            font=("console", 20)
        )
        label.place(x=240, y=5)

        pausebtn = Button(
            window,
            bg="black",
            image=resumeimg,
            command=resume_game1
        )
        pausebtn.place(x=550, y=1)

        Button(
            window,
            bg="black",
            image=restartimg,
            command=restart_game
        ).place(x=480, y=1)

        canvas = Canvas(
            window,
            bg=BACKGROUND_COLOR,
            width=WIDTH,
            height=HEIGHT
        )
        canvas.place(x=5, y=40)

        window.update()

        window_width = window.winfo_width()
        window_height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        window.geometry("950x650")

        window.bind("<Left>", lambda event: change_direction('left'))
        window.bind("<Right>", lambda event: change_direction('right'))
        window.bind("<Up>", lambda event: change_direction('up'))
        window.bind("<Down>", lambda event: change_direction('down'))
        window.bind("<p>", pause_game)
        window.bind("<P>", pause_game)
        window.bind("<r>", resume_game)
        window.bind("<R>", resume_game)
        window.bind("<space>", pause_game3)

        Button(
            window,
            text="SNAKE COLOR",
            font=("console", 15),
            bg="BLACK",
            fg="#00ff00",
            command=snake_color
        ).place(x=650, y=15)

        snakecolor = Label(
            window,
            bg=SNAKE_COLOR,
            width=5,
            bd=5,
            relief=RAISED,
            font=("concole", 18)
        )
        snakecolor.place(x=830, y=15)

        Button(
            window,
            text="FOOD COLOR",
            font=("console", 15),
            bg="BLACK",
            fg="#00ff00",
            command=food_color
        ).place(x=650, y=75)

        foodcolor = Label(
            window,
            bg=FOOD_COLOR,
            width=5,
            bd=5,
            relief=RAISED,
            font=("concole", 18)
        )
        foodcolor.place(x=830, y=75)

        Button(
            window,
            text="BLOCK COLOR",
            font=("console", 15),
            bg="BLACK",
            fg="#00ff00",
            command=block_color
        ).place(x=650, y=135)

        blockcolor = Label(
            window,
            bg=BLOCK_COLOR,
            width=5,
            bd=5,
            relief=RAISED,
            font=("concole", 18)
        )
        blockcolor.place(x=830, y=135)

        Button(
            window,
            text="BACK COLOR",
            font=("console", 15),
            bg="BLACK",
            fg="#00ff00",
            command=back_color
        ).place(x=650, y=195)

        backcolor = Label(
            window,
            bg=BACKGROUND_COLOR,
            width=5,
            bd=5,
            relief=RAISED,
            font=("concole", 18)
        )
        backcolor.place(x=830, y=195)

        Label(
            window,
            text="NO OF BLOCKS",
            font=("console", 11),
            bg=WINDOW_COLOR,
            fg="#00ff00"
        ).place(x=690, y=315)

        scale1 = Scale(
            window,
            bg="black",
            troughcolor="#00ff00",
            fg="#00ff00",
            font=("arial", 10),
            from_=0,
            to=20,
            length=200,
            tickinterval=5,
            orient=HORIZONTAL,
            showvalue=1,
            resolution=2
        )
        scale1.place(x=640, y=250)
        scale1.set(4)
        Button(
            window,
            bg="black",
            fg="#00ff00",
            text="SET",
            font=("console", 15),
            command=setblocks
        ).place(x=860, y=260)

        Label(
            window,
            text="SQUARE SIZE",
            font=("console", 11),
            bg=WINDOW_COLOR,
            fg="#00ff00"
        ).place(x=695, y=410)

        scale2 = Scale(
            window,
            troughcolor="#00ff00",
            bg="black",
            fg="#00ff00",
            font=("arial", 10),
            from_=10,
            to=50,
            length=200,
            tickinterval=10,
            orient=HORIZONTAL,
            showvalue=1,
            resolution=10
        )
        scale2.place(x=640, y=340)
        scale2.set(40)
        Button(
            window,
            bg="black",
            fg="#00ff00",
            text="SET",
            font=("console", 15),
            command=setspace
        ).place(x=860, y=360)

        Label(
            window,
            text="NO OF BODY PARTS",
            font=("console", 11),
            bg=WINDOW_COLOR,
            fg="#00ff00"
        ).place(x=675, y=505)

        scale3 = Scale(
            window,
            troughcolor="#00ff00",
            bg="black",
            fg="#00ff00",
            font=("arial", 10),
            from_=2,
            to=10,
            length=200,
            tickinterval=2,
            orient=HORIZONTAL,
            showvalue=1,
            resolution=1
        )
        scale3.place(x=640, y=440)
        scale3.set(3)
        Button(
            window,
            bg="black",
            fg="#00ff00",
            text="SET",
            font=("console", 15),
            command=setbody
        ).place(x=860, y=460)

        Label(
            window,
            text="SPEED OF SNAKE",
            font=("console", 11),
            bg=WINDOW_COLOR,
            fg="#00ff00"
        ).place(x=680, y=605)

        scale4 = Scale(
            window,
            troughcolor="#00ff00",
            bg="black",
            fg="#00ff00",
            font=("arial", 10),
            from_=2,
            to=10,
            length=200,
            tickinterval=2,
            orient=HORIZONTAL,
            showvalue=1,
            resolution=1
        )
        scale4.place(x=640, y=540)
        scale4.set(3)
        Button(
            window,
            bg="black",
            fg="#00ff00",
            text="SET",
            font=("console", 15),
            command=setspeed
        ).place(x=860, y=560)

        start(window)

        window.mainloop()


if __name__ == '__main__':
    snake_game()
