import time
import curses

def gameLoop():
    for i in range(10):
        print(f"O valor de i é {i}.")
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(gameLoop)