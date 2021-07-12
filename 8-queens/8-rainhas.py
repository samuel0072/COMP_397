import random

SIZE_BOARD = 8
QUEEN_COUNT = 8
POP_SIZE = 100

class BConfig:
    """
    Essa classe é o cromossomo do algoritmo

    Representa uma consiguração para o posicionamento das rainhas nos tabuleiros
    o tabuleiro é padrão 8x8
    
    """
    def __init__(self, pos):
        """
        pos é uma lista de posições das rainhas no tabuleiro
        os indices da lista representam as colunas no tabuleiro
        o conteúdo de cada posição representa a linha no tabuleiro
        """

        if pos == None or len(pos) != QUEEN_COUNT:
            raise Exception("Configuração inválida")
        
        self.pos = pos 

    def __str__(self):
        str_ = ""
        for i in self.pos:
            str_ += str(i) + " "
        return str_

def init_pop():
    """
        Inicia a população com configurações aleatórias de tabuleiro
    """

    random.seed()

    pop = []

    for k in range(POP_SIZE):
        cont = 0 # conta quantas rainhas foram posicionadas
        pos = [] # posição de cada rainha

        while cont < QUEEN_COUNT:
            pos_test = random.randint(0, QUEEN_COUNT-1)#indexando do 0 até o número de rainhas
            if pos_test not in pos: #checa se a coluna já foi escolhida com uma rainha
                pos.append(pos_test)
                cont += 1
        chromosome = BConfig(pos)
        pop.append(chromosome)
    
    return pop

def eval_fitness(chromo):
    """
    Calcula a adaptação de um cromossomo
    """
    positions = [] # chaves são as linhas e conteudo é a coluna da rainha
    fitness = 0
    pos = chromo.pos
    for line in range(len(pos)):
        positions.append(pos[line])

    for line in range(len(pos)):
        #checando rainhas na mesma coluna da rainha na linha line
        count = 1# inicia com uma rainha na coluna line
        for j in range(line, len(pos)):
            if (pos[line] == pos[j]) and (line != j):
                count += 1
        
        if count == 1:
            fitness += 1
        elif count > 1:
            fitness -= count
    
    return fitness

pop = init_pop()

for i in pop:
    print("c: ", i," f: ", eval_fitness(i),end = "\n")