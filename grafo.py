import csv
import heapq
from collections import deque


class Grafo:
    def __init__(self):
        self.adjacencia = {}

    def adicionar_cidade(self, cidade):
        if cidade not in self.adjacencia:
            self.adjacencia[cidade] = []

    def adicionar_trecho(self, origem, destino, distancia):
        self.adicionar_cidade(origem)
        self.adicionar_cidade(destino)
        self.adjacencia[origem].append((destino, distancia))
        self.adjacencia[destino].append((origem, distancia))

    def cidades(self):
        return sorted(self.adjacencia.keys())

    def vizinhos(self, cidade):
        return self.adjacencia.get(cidade, [])

    def quantidade_trechos(self):
        total = 0
        for cidade in self.adjacencia:
            total += len(self.adjacencia[cidade])
        return total // 2

    @classmethod
    def carregar_de_csv(cls, caminho):
        grafo = cls()
        with open(caminho, encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor)
            for linha in leitor:
                if not linha or len(linha) < 3:
                    continue
                origem = linha[0].strip()
                destino = linha[1].strip()
                distancia = float(linha[2].strip())
                grafo.adicionar_trecho(origem, destino, distancia)
        return grafo

    def busca_em_largura(self, origem):
        if origem not in self.adjacencia:
            return []
        visitados = []
        marcados = {origem}
        fila = deque([origem])
        while fila:
            atual = fila.popleft()
            visitados.append(atual)
            for vizinho, _ in sorted(self.vizinhos(atual)):
                if vizinho not in marcados:
                    marcados.add(vizinho)
                    fila.append(vizinho)
        return visitados

    def busca_em_profundidade(self, origem):
        if origem not in self.adjacencia:
            return []
        visitados = []
        marcados = set()
        pilha = [origem]
        while pilha:
            atual = pilha.pop()
            if atual in marcados:
                continue
            marcados.add(atual)
            visitados.append(atual)
            for vizinho, _ in sorted(self.vizinhos(atual), reverse=True):
                if vizinho not in marcados:
                    pilha.append(vizinho)
        return visitados

    def existe_caminho(self, origem, destino):
        return destino in self.busca_em_largura(origem)

    def caminho_minimo(self, origem, destino):
        if origem not in self.adjacencia or destino not in self.adjacencia:
            return None, float("inf")
        distancias = {cidade: float("inf") for cidade in self.adjacencia}
        anteriores = {cidade: None for cidade in self.adjacencia}
        distancias[origem] = 0
        fila = [(0, origem)]
        while fila:
            distancia_atual, atual = heapq.heappop(fila)
            if distancia_atual > distancias[atual]:
                continue
            if atual == destino:
                break
            for vizinho, peso in self.vizinhos(atual):
                nova_distancia = distancia_atual + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual
                    heapq.heappush(fila, (nova_distancia, vizinho))
        if distancias[destino] == float("inf"):
            return None, float("inf")
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]
        caminho.reverse()
        return caminho, distancias[destino]

    def arvore_geradora_minima(self):
        arestas = []
        registradas = set()
        for origem in self.adjacencia:
            for destino, peso in self.adjacencia[origem]:
                chave = tuple(sorted((origem, destino)))
                if chave not in registradas:
                    registradas.add(chave)
                    arestas.append((peso, origem, destino))
        arestas.sort()

        pai = {cidade: cidade for cidade in self.adjacencia}

        def encontrar(cidade):
            while pai[cidade] != cidade:
                pai[cidade] = pai[pai[cidade]]
                cidade = pai[cidade]
            return cidade

        arvore = []
        custo_total = 0
        for peso, origem, destino in arestas:
            raiz_origem = encontrar(origem)
            raiz_destino = encontrar(destino)
            if raiz_origem != raiz_destino:
                pai[raiz_origem] = raiz_destino
                arvore.append((origem, destino, peso))
                custo_total += peso
        return arvore, custo_total
