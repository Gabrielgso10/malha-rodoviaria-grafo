# Malha rodoviária como grafo

Modelagem de uma malha rodoviária da região de Francisco Morato e cidades vizinhas
como um grafo, com travessia, caminho mínimo (Dijkstra) e árvore geradora mínima
(Kruskal).

## O que o programa faz

A partir de um arquivo de dados com os trechos de estrada, o programa monta o grafo
e oferece um menu para:

1. Mostrar a malha (cidades e ligações)
2. Percorrer a malha a partir de uma cidade (BFS e DFS)
3. Verificar se duas cidades estão ligadas
4. Encontrar a rota mais curta entre duas cidades (Dijkstra)
5. Calcular a rede mínima que conecta todas as cidades (Kruskal)

## Requisitos

- Python 3.8 ou superior. Não usa nenhuma biblioteca externa, só a biblioteca padrão.

Para conferir a versão:

```
python3 --version
```

## Como executar do zero

Clone o repositório e entre na pasta:

```
git clone <url-do-repositorio>
cd malha-grafo
```

Rode o programa:

```
python3 src/main.py
```

Por padrão ele lê o arquivo `dados/malha.csv`. Para usar outro arquivo de dados,
passe o caminho como argumento:

```
python3 src/main.py caminho/para/outro_arquivo.csv
```

## Formato dos dados

O arquivo `dados/malha.csv` tem uma linha de cabeçalho e, depois, um trecho por linha:

```
origem,destino,distancia_km
Francisco Morato,Franco da Rocha,6
Franco da Rocha,Caieiras,9
```

Cada linha representa uma estrada ligando duas cidades, com a distância em quilômetros.
Como o grafo é não direcionado, basta registrar cada trecho uma vez.

## Estrutura

```
malha-grafo/
├── README.md
├── relatorio.md
├── dados/
│   └── malha.csv
└── src/
    ├── grafo.py
    └── main.py
```
