import curses
import random
import time
import os

def inicializar_janela():
    """Inicializa a janela do jogo com curses."""
    janela = curses.initscr()
    curses.curs_set(0)  # Esconde o cursor
    janela.keypad(True)  # Habilita o uso de teclas especiais
    janela.timeout(100)  # Define um timeout para a entrada do usuário
    return janela

def desenhar_tela(janela):
    """Limpa e desenha a borda da tela."""
    janela.clear()
    janela.border(0)

def desenhar_cobra(janela, cobra):
    """Desenha a cobra na tela."""
    janela.addch(cobra[0][0], cobra[0][1], "@")  # Cabeça da cobra
    for parte in cobra[1:]:
        janela.addch(parte[0], parte[1], "=")

def desenhar_fruta(janela, fruta):
    """Desenha a fruta na tela."""
    janela.addch(fruta[0], fruta[1], curses.ACS_DIAMOND)

def obter_nova_direcao(janela, direcao_atual):
    """Obtém a nova direção baseada na entrada do usuário, evitando direções opostas."""
    tecla = janela.getch()
    opostos = {curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP,
               curses.KEY_LEFT: curses.KEY_RIGHT, curses.KEY_RIGHT: curses.KEY_LEFT}
    if tecla in opostos and opostos[tecla] == direcao_atual:
        return direcao_atual  # Ignora a direção se for oposta à atual
    return tecla if tecla in opostos else direcao_atual

def mover_cobra(cobra, direcao):
    """Move a cobra na direção dada."""
    y, x = cobra[0]
    if direcao == curses.KEY_UP:
        y -= 1
    elif direcao == curses.KEY_DOWN:
        y += 1
    elif direcao == curses.KEY_LEFT:
        x -= 1
    elif direcao == curses.KEY_RIGHT:
        x += 1
    nova_cabeca = (y, x)
    cobra.insert(0, nova_cabeca)
    return cobra[:-1]  # Retorna a nova cobra sem o último elemento

def verificar_colisao(cobra, janela, fruta):
    """Verifica se a cobra colidiu com a borda, consigo mesma ou com a fruta."""
    y, x = cobra[0]
    altura, largura = janela.getmaxyx()
    if y <= 0 or y >= altura - 1 or x <= 0 or x >= largura - 1 or cobra[0] in cobra[1:]:
        return "borda ou si mesma"
    if cobra[0] == fruta:
        return "fruta"
    return "nenhuma"

def loop_jogo(janela):
    direcao_atual = curses.KEY_RIGHT
    cobra = [(5, 10), (5, 9), (5, 8)]
    fruta = (10, 20)
    pontuacao = 0  # Inicializa a pontuação
    
    while True:
        desenhar_tela(janela)
        desenhar_cobra(janela, cobra)
        desenhar_fruta(janela, fruta)
        
        direcao_atual = obter_nova_direcao(janela, direcao_atual)
        cobra = mover_cobra(cobra, direcao_atual)
        colisao = verificar_colisao(cobra, janela, fruta)

        if colisao == "borda ou si mesma":
            break
        elif colisao == "fruta":
            cobra.append(cobra[-1])  # Adiciona uma nova parte à cobra
            fruta = (random.randint(1, curses.LINES - 2), random.randint(1, curses.COLS - 2))
            pontuacao += 1  # Incrementa a pontuação quando uma fruta é coletada

    finalizar_jogo(janela, pontuacao)

def finalizar_jogo(janela, pontuacao):
    """Mostra a mensagem de fim de jogo com a pontuação e espera 3 segundos antes de sair."""
    janela.clear()
    mensagem = f"Fim de jogo! Você coletou {pontuacao} {'fruta' if pontuacao == 1 else 'frutas'}!"
    altura, largura = janela.getmaxyx()
    x = int((largura // 2) - (len(mensagem) // 2))
    y = int(altura // 2)
    janela.addstr(y, x, mensagem)
    janela.refresh()
    time.sleep(3)
    janela.getch() # Aguarda o usuário pressionar uma tecla

def main():
    os.system("cls" if os.name == "nt" else "clear") # Limpa o terminal
    try:
        janela = inicializar_janela()
        loop_jogo(janela)
    finally:
        curses.endwin() # Restaura o terminal ao estado original

if __name__ == "__main__":
    main()