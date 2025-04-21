import random

# Gera posições de bloqueio aleatórias no tabuleiro
def gerar_obstaculos(tamanho, semente=42):
    random.seed(semente)
    area_total = tamanho * tamanho
    minimo = int(0.07 * area_total)
    maximo = int(0.13 * area_total)
    total_bloqueios = random.randint(minimo, maximo)

    bloqueios = set()
    while len(bloqueios) < total_bloqueios:
        linha = random.randint(0, tamanho - 1)
        coluna = random.randint(0, tamanho - 1)
        bloqueios.add((linha, coluna))
    return bloqueios

# Verifica se uma posição é válida considerando bloqueios e outras rainhas
def posicao_valida(rainhas, linha, coluna, bloqueios):
    if (linha, coluna) in bloqueios:
        return False
    for r, c in rainhas:
        if c == coluna or abs(r - linha) == abs(c - coluna):
            return False
    return True

# Imprime o tabuleiro com rainhas (Q), bloqueios (X) e espaços vazios (.)
def exibir_tabuleiro(tamanho, solucao, bloqueios):
    tabuleiro = [["." for _ in range(tamanho)] for _ in range(tamanho)]

    for i, j in bloqueios:
        tabuleiro[i][j] = "X"

    if isinstance(solucao[0], int):
        for i, j in enumerate(solucao):
            tabuleiro[i][j] = "Q"
    else:
        for i, j in solucao:
            tabuleiro[i][j] = "Q"

    for linha in tabuleiro:
        print(" ".join(linha))
