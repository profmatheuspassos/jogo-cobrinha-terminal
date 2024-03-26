import curses
import random
import time
import os

def desenharTela(janela):
    janela.clear()
    janela.border(0)

def desenharCobra(cobra, janela):
    cabeca = cobra[0]
    desenharAtor(ator = cabeca, janela = janela, caractere = "@")
    corpo = cobra[1:]
    for parteCorpo in corpo:
        desenharAtor(ator = parteCorpo, janela = janela, caractere = "=")

def desenharAtor(ator, janela, caractere):
    janela.addch(ator[0], ator[1], caractere)

def obterNovaDirecao(janela, tempoEspera):
    janela.timeout(tempoEspera)
    direcao = janela.getch()
    if direcao in [curses.KEY_UP, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_DOWN]:
        return direcao
    return None

def moverAtor(ator, direcao):
    match direcao:
        case curses.KEY_UP:
            ator[0] -= 1
        case curses.KEY_LEFT:
            ator[1] -= 1
        case curses.KEY_DOWN:
            ator[0] += 1
        case curses.KEY_RIGHT:
            ator[1] += 1

def atorAtingiuBorda(ator, janela):
    altura, largura = janela.getmaxyx()
    if (ator[0] <= 0) or (ator[0] >= altura - 1):
        return True
    if (ator[1] <= 0) or (ator[1] >= largura - 1):
        return True
    return False

def moverCobra(cobra, direcao, cobraComeuFruta):
    cabeca = cobra[0].copy()
    moverAtor(ator = cabeca, direcao = direcao)
    cobra.insert(0, cabeca)
    if not cobraComeuFruta:
        cobra.pop()

def cobraAtingiuBorda(cobra, janela):
    cabeca = cobra[0]
    return atorAtingiuBorda(ator = cabeca, janela = janela)

def obterNovaFruta(janela):
    altura, largura = janela.getmaxyx()
    return [random.randint(1, altura - 2), random.randint(1, largura - 2)]

def cobraAtingiuFruta(cobra, fruta):
    return fruta in cobra

def cobraAtingiuSiMesma(cobra):
    cabeca = cobra[0]
    corpo = cobra[1:]
    return cabeca in corpo

def direcaoEhOposta(direcao, direcaoAtual):
    match direcao:
        case curses.KEY_UP:
            return direcaoAtual == curses.KEY_DOWN
        case curses.KEY_LEFT:
            return direcaoAtual == curses.KEY_RIGHT
        case curses.KEY_DOWN:
            return direcaoAtual == curses.KEY_UP
        case curses.KEY_RIGHT:
            return direcaoAtual == curses.KEY_LEFT

def finalizarJogo(pontuacao, janela):
    desenharTela(janela = janela)
    altura, largura = janela.getmaxyx()
    mensagem = f"Fim de jogo! Você coletou {pontuacao} frutas!"
    y = int(altura / 2)
    x = int((largura - len(mensagem)) / 2)
    janela.addstr(y, x, mensagem)
    janela.refresh()
    time.sleep(3)

def selecionarDificuldade():
    dificuldade = {
        "1": 1000,
        "2": 500,
        "3": 250,
        "4": 125,
        "5": 62
    }
    while True:
        resposta = input("Selecione a dificuldade de 1 (mais fácil) a 5 (mais difícil): ")
        velocidadeJogo = dificuldade.get(resposta)
        if velocidadeJogo is not None:
            return velocidadeJogo
        print("Escolha a dificuldade de 1 (mais fácil) a 5 (mais difícil)!")

def loopJogo(janela, velocidadeJogo):
    # Configuração inicial
    curses.curs_set(0)
    cobra = [
        [10, 15],
        [9, 15],
        [8, 15],
        [7, 15],
    ]
    fruta = obterNovaFruta(janela = janela)
    direcaoAtual = curses.KEY_DOWN
    cobraComeuFruta = False
    pontuacao = 0

    # Vamos jogar!
    while True:
        desenharTela(janela = janela)
        desenharCobra(cobra = cobra, janela = janela)
        desenharAtor(ator = fruta, janela = janela, caractere = curses.ACS_DIAMOND)
        direcao = obterNovaDirecao(janela = janela, tempoEspera = velocidadeJogo)
        if direcao is None:
            direcao = direcaoAtual
        if direcaoEhOposta(direcao = direcao, direcaoAtual = direcaoAtual):
            direcao = direcaoAtual
        moverCobra(cobra = cobra, direcao = direcao, cobraComeuFruta = cobraComeuFruta)
        if cobraAtingiuBorda(cobra = cobra, janela = janela):
            break
        if cobraAtingiuSiMesma(cobra = cobra):
            break
        if cobraAtingiuFruta(cobra = cobra, fruta = fruta):
            cobraComeuFruta = True
            fruta = obterNovaFruta(janela = janela)
            pontuacao += 1
        else:
            cobraComeuFruta = False
        direcaoAtual = direcao
    finalizarJogo(pontuacao = pontuacao, janela = janela)
        
if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    curses.wrapper(loopJogo, velocidadeJogo = selecionarDificuldade())
