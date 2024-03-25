# Jogo ainda em desenvolvimento

import curses
import random

def drawScreen(window):
    window.clear()
    window.border(0)

def drawSnake(snake, window):
    head = snake[0]
    drawActor(actor = head, window = window, char = "@")
    body = snake[1:]
    for bodyPart in body:
        drawActor(actor = bodyPart, window = window, char = "=")

def drawActor(actor, window, char):
    window.addch(actor[0], actor[1], char)

def getNewDirection(window, timeout):
    window.timeout(timeout)
    direction = window.getch()
    if direction in [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_DOWN]:
        return direction
    return None

def moveActor(actor, direction):
    match direction:
        case curses.KEY_UP:
            actor[0] -= 1
        case curses.KEY_LEFT:
            actor[1] -= 1
        case curses.KEY_DOWN:
            actor[0] += 1
        case curses.KEY_RIGHT:
            actor[1] += 1

def actorHitBorder(actor, window):
    height, width = window.getmaxyx()
    if (actor[0] <= 0) or (actor[0] >= height - 1):
        return True
    if (actor[1] <= 0) or (actor[1] >= width - 1):
        return True
    return False

def moveSnake(snake, direction, snakeAteFruit):
    head = snake[0].copy()
    moveActor(actor = head, direction = direction)
    snake.insert(0, head)
    if not snakeAteFruit:
        snake.pop()

def snakeHitBorder(snake, window):
    head = snake[0]
    return actorHitBorder(actor = head, window = window)

def getNewFruit(window):
    height, width = window.getmaxyx()
    return [random.randint(1, height - 2), random.randint(1, width - 2)]

def snakeHitFruit(snake, fruit):
    return fruit in snake

def gameLoop(window):
    # Setup inicial
    curses.curs_set(0)
    snake = [
        [10, 15],
        [9, 15],
        [8, 15],
        [7, 15],
    ]
    fruit = getNewFruit(window = window)
    currentDirection = curses.KEY_DOWN
    snakeAteFruit = False
    while True:
        drawScreen(window = window)
        drawSnake(snake = snake, window = window)
        drawActor(actor = fruit, window = window, char = curses.ACS_DIAMOND)
        direction = getNewDirection(window = window, timeout = 1000)
        if direction is None:
            direction = currentDirection
        moveSnake(snake = snake, direction = direction, snakeAteFruit = snakeAteFruit)
        if snakeHitBorder(snake = snake, window = window):
            return
        if snakeHitFruit(snake = snake, fruit = fruit):
            snakeAteFruit = True
            fruit = getNewFruit(window = window)
        else:
            snakeAteFruit = False
        currentDirection = direction
        
if __name__ == "__main__":
    curses.wrapper(gameLoop)