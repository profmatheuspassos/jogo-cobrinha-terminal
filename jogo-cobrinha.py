import curses

def gameLoop(window):
    window.addstr(f"Pressione alguma tecla:")
    while True:
        window.timeout(1000)
        char = window.getch()
        window.clear()
        match char:
            case curses.KEY_UP:
                window.addstr(f"Mover para cima")
            case curses.KEY_LEFT:
                window.addstr(f"Mover para esquerda")
            case curses.KEY_DOWN:
                window.addstr(f"Mover para baixo")
            case curses.KEY_RIGHT:
                window.addstr(f"Mover para direita")
            case _:
                window.addstr(f"Não mover")
        
if __name__ == "__main__":
    curses.wrapper(gameLoop)