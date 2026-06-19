# Relatório — Malha rodoviária como grafo

## Domínio escolhido

Resolvi modelar a malha rodoviária da região onde moro: Francisco Morato e as
cidades vizinhas, incluindo Franco da Rocha, Caieiras, Cajamar, Mairiporã, Várzea
Paulista, Campo Limpo Paulista, Jundiaí, Atibaia, Osasco, Guarulhos e a capital,
São Paulo. É um cenário que conheço de andar de carro pela região, então fica fácil
de validar se os resultados fazem sentido.

Nesse grafo:

- **Cada vértice é uma cidade.**
- **Cada aresta é um trecho de estrada** ligando duas cidades diretamente.
- **O peso da aresta é a distância em quilômetros** desse trecho.

O grafo é **não direcionado**, porque uma estrada que vai de Francisco Morato para
Franco da Rocha também volta de Franco da Rocha para Francisco Morato, com a mesma
distância. E é **ponderado**, porque cada trecho tem um custo (a quilometragem), e
é justamente isso que permite falar em rota mais curta.

A malha montada tem 12 cidades e 16 trechos.

## Representação em memória: lista de adjacência

Para guardar o grafo escolhi **lista de adjacência**. Na prática, cada cidade
guarda uma lista com seus vizinhos diretos e a distância até cada um. No código,
isso é um dicionário em que a chave é a cidade e o valor é uma lista de pares
`(cidade_vizinha, distancia)`.

A justificativa é o tamanho e o formato do grafo. Esse é um grafo **esparso**: cada
cidade se liga a poucas outras (duas ou três, em geral), e não a todas. Numa matriz
de adjacência eu precisaria de uma tabela 12 x 12, ou seja, 144 posições, sendo que
a maioria ficaria vazia (preenchida com zero ou infinito) só para dizer "não existe
estrada aqui". O custo de memória da matriz cresce com o quadrado do número de
cidades, enquanto o da lista cresce com o número de trechos que realmente existem.

Para 12 cidades a diferença é pequena, mas o raciocínio importa: se eu fosse
estender isso para todas as cidades do estado de São Paulo, a matriz ficaria enorme
e quase toda vazia, e a lista continuaria proporcional à quantidade de estradas de
verdade. Como o ganho prático da matriz seria poder consultar "existe estrada entre
A e B?" em tempo constante, e isso não é o gargalo aqui, a lista compensa mais.

Os dados não estão fixos no código: o programa lê o arquivo `dados/malha.csv` e
monta o grafo a partir dele. Trocar o cenário é só trocar o arquivo.

## Travessia: busca em largura (BFS)

Implementei as duas travessias, mas a que uso para responder a pergunta principal —
"quais cidades consigo alcançar a partir daqui?" — é a **busca em largura (BFS)**.

A BFS parte de uma cidade de origem e visita primeiro todos os vizinhos imediatos,
depois os vizinhos dos vizinhos, e assim por diante, em ondas. A estrutura auxiliar
que ela exige é uma **fila**: as cidades descobertas entram no fim e são processadas
na ordem em que chegaram, o que garante esse avanço por níveis. Também uso um
conjunto de cidades já marcadas para não visitar a mesma duas vezes e não entrar
em loop.

Partindo de Francisco Morato, a BFS visita as 12 cidades, o que mostra que toda a
malha é conectada — dá para chegar de qualquer cidade a qualquer outra. A ordem que
saiu foi:

```
Francisco Morato -> Franco da Rocha -> Varzea Paulista -> Caieiras -> Mairipora
-> Campo Limpo Paulista -> Jundiai -> Cajamar -> Sao Paulo -> Atibaia -> Guarulhos
-> Osasco
```

Dá para reparar que ela primeiro lista os vizinhos diretos de Francisco Morato
(Franco da Rocha e Várzea Paulista) e só depois desce para o nível seguinte.

A diferença para a busca em profundidade (DFS) fica clara comparando as ordens.
A DFS, que usa uma **pilha** no lugar da fila, mergulha o quanto consegue por um
caminho antes de voltar. A partir de Francisco Morato ela produziu:

```
Francisco Morato -> Franco da Rocha -> Caieiras -> Cajamar -> Osasco -> Sao Paulo
-> Guarulhos -> Atibaia -> Jundiai -> Campo Limpo Paulista -> Varzea Paulista
-> Mairipora
```

Ela "afunda" por Franco da Rocha → Caieiras → Cajamar → Osasco antes de explorar o
outro lado. As duas visitam o grafo inteiro e servem para confirmar conectividade,
mas a BFS, por avançar por níveis, é a que se aproxima da ideia de "o que está perto
primeiro".

Para a pergunta "essas duas cidades estão ligadas?", uso a própria BFS: se o destino
aparece entre as cidades alcançadas a partir da origem, existe caminho.

## Caminho mínimo: Dijkstra

Como o grafo tem pesos, o problema de caminho mínimo é encontrar a rota de **menor
quilometragem total** entre duas cidades. Para isso usei o **algoritmo de Dijkstra**.

A ideia do Dijkstra é manter, para cada cidade, a menor distância já conhecida desde
a origem, sempre expandindo a cidade ainda não fechada que está mais perto. Usei uma
**fila de prioridade** (um heap) para pegar rapidamente essa cidade mais próxima, e
um dicionário de "anteriores" para, no final, reconstruir o trajeto de trás para
frente, do destino até a origem.

Um resultado concreto: a rota mais curta de Francisco Morato até São Paulo é

```
Francisco Morato -> Franco da Rocha -> Caieiras -> Sao Paulo = 48 km
```

Vale comparar com a alternativa óbvia de descer por Cajamar e Osasco
(Francisco Morato → Franco da Rocha → Caieiras → Cajamar → Osasco → São Paulo), que
dá 70 km. O Dijkstra escolhe a de 48 km, que é a mais curta de fato.

Outro exemplo é Jundiaí até Guarulhos, que dá 80 km passando por Atibaia. À primeira
vista parece que dar a volta por Várzea Paulista e Mairiporã poderia ser melhor, mas
aquele caminho fecha em 82 km, então o algoritmo acerta ao preferir o de 80.

No domínio, esse "menor custo" significa o **trajeto mais curto em distância**: se eu
estivesse otimizando combustível ou quilometragem rodada de uma frota, seria essa a
rota a seguir. Se eu trocasse o peso de quilômetros por tempo de viagem, o mesmo
algoritmo me daria a rota mais rápida, sem mudar nada na lógica.

## Árvore geradora mínima: Kruskal

O meu cenário também encaixa no problema de "conectar tudo gastando o mínimo
possível". Imaginei uma empresa que quer passar um cabo de fibra por dentro das
estradas existentes, ligando todas as cidades da região, e quer fazer isso usando a
menor metragem total de cabo. Não interessa que toda cidade tenha estrada direta com
toda outra; basta que exista um caminho ligando todas, e que a soma dos trechos
usados seja a menor possível. Esse é exatamente o problema da **árvore geradora
mínima**, que resolvi com o **algoritmo de Kruskal**.

O Kruskal ordena todos os trechos do menor para o maior e vai aceitando um a um,
pulando qualquer trecho que fecharia um ciclo, ou seja, que ligaria duas cidades já
conectadas por outro caminho. Para saber se duas cidades já estão no mesmo grupo
conectado, usei a estrutura de **union-find** (conjuntos disjuntos), com compressão
de caminho.

O resultado para a malha foi:

```
Varzea Paulista -- Campo Limpo Paulista   5 km
Francisco Morato -- Franco da Rocha       6 km
Franco da Rocha -- Caieiras               9 km
Varzea Paulista -- Jundiai                9 km
Caieiras -- Cajamar                       14 km
Francisco Morato -- Varzea Paulista       16 km
Sao Paulo -- Guarulhos                    18 km
Sao Paulo -- Osasco                       19 km
Cajamar -- Osasco                         22 km
Franco da Rocha -- Mairipora              24 km
Mairipora -- Atibaia                      33 km
Total: 175 km
```

São 11 trechos para 12 cidades, que é o esperado: uma árvore que liga *n* cidades
tem sempre *n − 1* arestas, sem nenhum ciclo. A intuição do resultado é que o
algoritmo sempre prefere os trechos mais baratos e só "gasta" um trecho caro quando
ele é a única forma de alcançar uma cidade ainda solta. Por isso Atibaia entra pelo
trecho de 33 km com Mairiporã, e não pelos de 35 ou 45 km que ela também tem: esses
fechariam ciclo ou custariam mais. O total de 175 km é a menor metragem de cabo que
conecta a região inteira.

## Reflexão: aplicação real e limites

Tudo o que está aqui em escala de bairro é a mesma ideia que sistemas grandes usam o
tempo todo. Aplicativos de mapa como Google Maps e Waze são, no fundo, um grafo
gigante de cruzamentos e ruas rodando variações de Dijkstra (e algoritmos mais
espertos derivados dele) para devolver a rota mais rápida. Redes sociais tratam
pessoas como vértices e amizades como arestas, e usam travessias parecidas com a BFS
para medir distância entre pessoas e sugerir conexões. Empresas de telecomunicação e
de energia usam árvore geradora mínima para planejar onde passar cabo ou linha
gastando o mínimo. A logística de entregas combina caminho mínimo com outras
restrições para montar rotas de frota.

O limite que mais aparece quando o grafo cresce é o **custo computacional e de
memória**. Aqui são 12 cidades e dá para calcular tudo num piscar de olhos. Numa
malha com milhões de cruzamentos, rodar Dijkstra puro a cada consulta fica lento
demais, e é por isso que os sistemas reais pré-processam o grafo, usam heurísticas
(como o A\*) e dividem o mapa em regiões para não ter que olhar o grafo inteiro toda
vez. A escolha de representação também pesa mais nessa escala: a lista de adjacência,
que aqui foi só uma decisão de bom senso, passa a ser praticamente obrigatória,
porque uma matriz de adjacência para milhões de vértices simplesmente não cabe na
memória.
