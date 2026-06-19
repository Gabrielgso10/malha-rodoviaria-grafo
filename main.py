import os
import sys

from grafo import Grafo


def caminho_dos_dados():
    if len(sys.argv) > 1:
        return sys.argv[1]
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "dados", "malha.csv")


def escolher_cidade(grafo, mensagem):
    cidades = grafo.cidades()
    for indice, cidade in enumerate(cidades, start=1):
        print(f"  {indice} - {cidade}")
    escolha = input(mensagem).strip()
    if escolha.isdigit():
        posicao = int(escolha)
        if 1 <= posicao <= len(cidades):
            return cidades[posicao - 1]
    if escolha in cidades:
        return escolha
    print("Cidade invalida.")
    return None


def mostrar_malha(grafo):
    print(f"\nA malha tem {len(grafo.cidades())} cidades e {grafo.quantidade_trechos()} trechos.\n")
    for cidade in grafo.cidades():
        ligacoes = ", ".join(f"{destino} ({int(peso)} km)" for destino, peso in sorted(grafo.vizinhos(cidade)))
        print(f"{cidade}: {ligacoes}")


def opcao_travessia(grafo):
    origem = escolher_cidade(grafo, "Cidade de origem: ")
    if origem is None:
        return
    largura = grafo.busca_em_largura(origem)
    profundidade = grafo.busca_em_profundidade(origem)
    print(f"\nA partir de {origem} consigo alcancar {len(largura)} cidades.")
    print("Ordem por largura (BFS):")
    print("  " + " -> ".join(largura))
    print("Ordem por profundidade (DFS):")
    print("  " + " -> ".join(profundidade))


def opcao_conexao(grafo):
    origem = escolher_cidade(grafo, "Primeira cidade: ")
    if origem is None:
        return
    destino = escolher_cidade(grafo, "Segunda cidade: ")
    if destino is None:
        return
    if grafo.existe_caminho(origem, destino):
        print(f"\nExiste pelo menos um caminho ligando {origem} e {destino}.")
    else:
        print(f"\nNao existe caminho entre {origem} e {destino}.")


def opcao_caminho_minimo(grafo):
    origem = escolher_cidade(grafo, "Cidade de origem: ")
    if origem is None:
        return
    destino = escolher_cidade(grafo, "Cidade de destino: ")
    if destino is None:
        return
    caminho, custo = grafo.caminho_minimo(origem, destino)
    if caminho is None:
        print(f"\nNao ha rota entre {origem} e {destino}.")
        return
    print(f"\nRota mais curta de {origem} ate {destino}:")
    print("  " + " -> ".join(caminho))
    print(f"Distancia total: {int(custo)} km")


def opcao_arvore_minima(grafo):
    arvore, custo = grafo.arvore_geradora_minima()
    print("\nTrechos escolhidos para conectar todas as cidades gastando o minimo:")
    for origem, destino, peso in arvore:
        print(f"  {origem} -- {destino}  ({int(peso)} km)")
    print(f"Comprimento total da rede: {int(custo)} km")


def main():
    caminho = caminho_dos_dados()
    grafo = Grafo.carregar_de_csv(caminho)
    print("Malha rodoviaria carregada a partir de:", caminho)

    opcoes = {
        "1": ("Mostrar a malha", mostrar_malha),
        "2": ("Percorrer a malha a partir de uma cidade", opcao_travessia),
        "3": ("Verificar se duas cidades estao ligadas", opcao_conexao),
        "4": ("Rota mais curta entre duas cidades", opcao_caminho_minimo),
        "5": ("Rede minima que conecta todas as cidades", opcao_arvore_minima),
    }

    while True:
        print("\n==============================")
        for chave, (descricao, _) in opcoes.items():
            print(f"{chave} - {descricao}")
        print("0 - Sair")
        escolha = input("Escolha uma opcao: ").strip()
        if escolha == "0":
            print("Ate mais.")
            break
        if escolha in opcoes:
            opcoes[escolha][1](grafo)
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
