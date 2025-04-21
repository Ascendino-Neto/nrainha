from genetico import executar_algoritmo

if __name__ == '__main__':
    valores_n = [8, 9, 10, 11, 12, 13, 32, 64, 128]

    for n in valores_n:
        print(f"\nExecutando n = {n}")
        print("Tamanho | Solução encontrada | Melhor | Média da população | Nós analisados | Tempo (ms)")
        print("--------------------------------------------------------------------------------------------")

        resultado = executar_algoritmo(n)
        solucao = "Sim" if resultado["solucao"] else "Não"
        melhor = abs(resultado["melhor_fitness"])
        media = abs(resultado["media_fitness"])
        nos = resultado["num_nos"]
        tempo = round(resultado["tempo"] * 1000)

        print(f"{n:<8}| {solucao:<21}| {melhor:<7}| {media:<20.2f}| {nos:<14}| {tempo}")
