import random
import time
from multiprocessing import Pool, cpu_count

# Avalia um indivíduo contando o número de conflitos entre rainhas
def avaliar(individuo, tamanho):
    conflitos = 0
    for i in range(tamanho):
        for j in range(i + 1, tamanho):
            if individuo[i] == individuo[j] or abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return -conflitos  # Retorna valor negativo para facilitar comparação

# Função adaptada para multiprocessing (recebe tupla como argumento)
def avaliar_paralelo(args):
    individuo, tamanho = args
    return avaliar(individuo, tamanho)

# Gera a população inicial de indivíduos aleatórios
def criar_populacao(qtd, tamanho):
    return [random.sample(range(tamanho), tamanho) for _ in range(qtd)]

# Seleciona dois pais usando torneio
def escolher_pais(populacao, avaliacoes):
    amostra = random.sample(list(zip(populacao, avaliacoes)), 5)
    amostra.sort(key=lambda x: x[1], reverse=True)
    return amostra[0][0], amostra[1][0]

# Executa o crossover entre dois pais
def cruzar(p1, p2, tamanho):
    inicio, fim = sorted(random.sample(range(tamanho), 2))
    filho = [-1] * tamanho
    filho[inicio:fim] = p1[inicio:fim]

    idx = fim
    for valor in p2:
        if valor not in filho:
            if idx >= tamanho:
                idx = 0
            filho[idx] = valor
            idx += 1
    return filho

# Aplica uma mutação simples trocando duas posições
def aplicar_mutacao(individuo, taxa, tamanho):
    if random.random() < taxa:
        a, b = random.sample(range(tamanho), 2)
        individuo[a], individuo[b] = individuo[b], individuo[a]
    return individuo

# Utiliza backtracking para tentar completar uma solução parcial
def ajustar_com_backtracking(tabuleiro, tamanho):
    def seguro(tab, linha, col):
        for i in range(linha):
            if tab[i] == col or abs(tab[i] - col) == abs(i - linha):
                return False
        return True

    def resolver(tab, linha):
        if linha == tamanho:
            return tab
        for col in range(tamanho):
            if seguro(tab, linha, col):
                tab[linha] = col
                sol = resolver(tab, linha + 1)
                if sol:
                    return sol
        return None

    parcial = tabuleiro[:]
    return resolver(parcial, len(parcial))

# Algoritmo principal: roda o algoritmo genético com backtracking opcional
def executar_algoritmo(n, populacao_inicial=1000, max_geracoes=5000, mutacao=0.3):
    inicio = time.time()
    populacao = criar_populacao(populacao_inicial, n)

    with Pool(cpu_count()) as pool:
        avaliacoes = pool.map(avaliar_paralelo, [(ind, n) for ind in populacao])

    analisados = populacao_inicial

    for gen in range(max_geracoes):
        nova_geracao = []
        for _ in range(populacao_inicial // 2):
            p1, p2 = escolher_pais(populacao, avaliacoes)
            f1 = aplicar_mutacao(cruzar(p1, p2, n), mutacao, n)
            f2 = aplicar_mutacao(cruzar(p2, p1, n), mutacao, n)
            nova_geracao.extend([f1, f2])

        populacao = nova_geracao
        with Pool(cpu_count()) as pool:
            avaliacoes = pool.map(avaliar_paralelo, [(ind, n) for ind in populacao])

        analisados += populacao_inicial

        # Verifica se alguma solução perfeita foi encontrada
        for i, pontuacao in enumerate(avaliacoes):
            if pontuacao == 0:
                fim = time.time()
                return {
                    "solucao": populacao[i],
                    "geracoes": gen + 1,
                    "tempo": fim - inicio,
                    "num_nos": analisados,
                    "melhor_fitness": max(avaliacoes),
                    "media_fitness": sum(avaliacoes) / len(avaliacoes),
                    "geracao": gen + 1
                }

    # Tenta corrigir soluções próximas com backtracking
    for ind in populacao:
        if avaliar(ind, n) > -10:
            correcao = ajustar_com_backtracking(ind, n)
            if correcao:
                fim = time.time()
                return {
                    "solucao": correcao,
                    "geracoes": max_geracoes,
                    "tempo": fim - inicio,
                    "num_nos": analisados,
                    "melhor_fitness": max(avaliacoes),
                    "media_fitness": sum(avaliacoes) / len(avaliacoes),
                    "geracao": max_geracoes
                }

    # Nenhuma solução válida encontrada
    fim = time.time()
    return {
        "solucao": None,
        "geracoes": max_geracoes,
        "tempo": fim - inicio,
        "num_nos": analisados,
        "melhor_fitness": max(avaliacoes),
        "media_fitness": sum(avaliacoes) / len(avaliacoes),
        "geracao": max_geracoes
    }
