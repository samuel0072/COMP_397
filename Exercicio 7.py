#!/usr/bin/env python
# coding: utf-8

# In[273]:


import random
import math
import copy


# # Assinatura padrão

# In[274]:


class Individuo:
    def __init__(self, grafo, fitness = 0, paredes_presentes = []):
        self.grafo = grafo #grafo que representa o individuo
        self.fitness = fitness#fitness do individuo
        self.paredes_presentes = paredes_presentes #paredes derrubadas por indiviuo, um subconjunto das paredes totais


# In[275]:


TAMANHO_POP = 50


# In[276]:


TAXA_DE_CRUZAMENTO = 0.3


# In[277]:


CHANCE_MUTACAO = 5


# In[278]:


vertices = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10']


# In[279]:


paredes_totais = [("a1", "a6"),("a6", "a7"),("a6", "a2"),("a7", "a8"),("a7", "a9"),("a7", "a5"),
("a5", "a9"),("a5", "a2"),("a5", "a4"),("a5", "a10"),("a9", "a10"),("a10", "a4"),("a4", "a2"), ("a4", "a3")]


# In[280]:


def fitness(individuo):
    return len(individuo.paredes_presentes)#retorna a quantidade de arestas do grafo


# In[281]:


def mutacao(filho, chance_mutacao):
    #chance de mutação em 5%
    if chance_mutacao != 100:
        chance_mutacao = 5
    #variaveis globais
    global vertices
    global paredes_totais
    #If para definir se vai haver ou não mutação
    if chance_mutacao >= random.randint(1, 100):
        #escolher um vértices aleatório no conjunto de vertices
        novo_vertice = random.choice(vertices)
        #Se o vértices escolhido pertencer ao conjunto de vertices do filho, ele será alterado juntamente com as arestas adjacentes
        #por se tratar de alterção no individuo, temos duas variaves auxiliares
        vert = copy.deepcopy(filho.grafo)
        arest = copy.deepcopy(filho.paredes_presentes)
        aux = []
        t = 0
     
        #remoção das arestas desse vértices
        
        if novo_vertice in filho.grafo:
            for i in vertices:
                if novo_vertice in filho.grafo[i]:
                    filho.grafo[i].remove(novo_vertice)
                    filho.grafo[novo_vertice].remove(i)
                    aux = i
                    break
            for j in range(0, len(filho.paredes_presentes)):
                if filho.paredes_presentes[j] == (aux,novo_vertice) or filho.paredes_presentes[j] == (novo_vertice, aux):
                    del filho.paredes_presentes[j]
                    #t = 1
                    break
            #checar se o filho continua conexo
            if checar_individuo(filho):
                return filho
            #caso seja desconexo, chama mais uma vez a função com a garantia que ele irá mutar novamente
            #caso a mutação não seja válida, é chamada a função novamente com alta probabilidade de mutação
            filho.grafo = vert
            filho.paredes_presentes = arest
            if(chance_mutacao == 5):
                chance_mutacao = 100
            return mutacao(filho, chance_mutacao - 4)                        
 
    else:
        return filho


# In[282]:


def selecao(populacao):
    "retorna os 100 melhores individuos"
    pop_ord = sorted(populacao, key = lambda individuo: individuo.fitness)
    return pop_ord[0:TAMANHO_POP]
    


# # Implementação Cruzamento

# In[283]:


def seleciona_pais(populacao, taxa_de_cruzamento):
    "Seleciona os candidatos a pais"
    
    if(len(populacao )< 2):
        raise Exception("População muito pequena.")
        
    pop_ord = sorted(populacao, key = lambda individuo: individuo.fitness)#ordena a população pelo seu fitness
    candidatos = []
    
    
    len_pop = len(populacao)
    quantidade_de_individuos = math.ceil(len_pop*taxa_de_cruzamento)#calcula a quantidade de individuos e arredonda o resultado para o maior inteiro mais proximo
    
    if (quantidade_de_individuos % 2) != 0:#arredonda para o maior inteiro par mais proximo
        quantidade_de_individuos+=1
    
    for i in range(quantidade_de_individuos):#seleção elitista
        candidatos.append(pop_ord[i])
    
    return candidatos
    


# In[284]:


def cruza_populacao(candidatos_pais):
    "Retorna os filhos criados pelos candidatos a pais"
    filhos = []
    
    global CHANCE_MUTACAO
    
    random.shuffle(candidatos_pais)#embaralha a lista de candidatos a pais
    
    for i in range(0, len(candidatos_pais), 2):#cruza os pais 2 a 2
        filho_1, filho_2 = cruzamento(candidatos_pais[i], candidatos_pais[i+1])
        filho_1 = mutacao(filho_1, CHANCE_MUTACAO)#muta os filhos
        filho_2 = mutacao(filho_2, CHANCE_MUTACAO)#muta os filhos
        filhos.append(filho_1)
        filhos.append(filho_2)
        
    return filhos


# In[285]:


def dfs_componentes(grafo):
    global vertices
   
    visitados = []
    componentes = []#lista de vertices agrupados por componentes
    for u in vertices:#itera sobre todos os vertices
        if not u in visitados:#verifica se o vertice já foi visitado em outra componente
            #se ele não foi então uma nova componente será criada
            componente = []
            identifica_componentes(grafo, u, visitados, componente)
            componentes.append(componente)
    return componentes#retorna a lista de ocmponentes


# In[286]:


def identifica_componentes(grafo, vertice_atual, visitados, componente):
    #a recursão nessa função ocorre até que todos os vertices da componente tenham sido vizitados
    if not vertice_atual in visitados:
        visitados.append(vertice_atual)#marca o vertice atual como visitado
        componente.append(vertice_atual)#adiciona ele na lista de componentes
        vizinhos = grafo[vertice_atual]#obtem seus vizinhos
        for u in vizinhos:#itera sobre os vizinhos
            identifica_componentes(grafo, u, visitados, componente)
    


# In[287]:


def conecta_componentes(filho, pai, mae):
    """Recebe 3 grafos e conecta os componentes do grafo filho usando arestas do grafo pai ou mãe
    corrige o filho"""
    
    while(not checar_individuo(filho)):#enquanto o filho é desconexo
        componentes = dfs_componentes(filho.grafo)
        comp1, comp2 = random.sample(componentes, 2)#retorna dois componentes aleatórios diferentes
        u = random.choice(comp1)#pega um vertice aleatorio
        v = random.choice(comp2)#pega um vertice aleatorio
        if (v in pai.grafo[u]) or (v in mae.grafo[u]):#verifica se a aresta v->u existe no pai ou na mãe
            filho.grafo[v].append(u)#adiciona a aresta v->u no filho
            filho.grafo[u].append(v)#adiciona a aresta u->v no filho
    


# In[288]:


def calc_paredes(filho):
    """Calcula as paredes derrubadas de um filho e as retorna"""
    
    grafo = filho.grafo
    paredes = []
    global vertices
    global paredes_totais
    
    for u in vertices:
        for v in grafo[u]:
            parede = (u, v)
            if parede in paredes_totais and (not parede in paredes):
                paredes.append(parede)

    return paredes


# In[289]:


def cruzamento(pai, mae):
    "Retorna o filho"
    global vertices
   
    vert_len = len(vertices)
    
    ponto = random.randint(0, vert_len)#escolhe um ponto de corte aleatorio
    
    #cria dois filhos vazios
    filho_1 = Individuo({"a1":[], "a2":[],"a3":[],"a4":[],"a5":[],"a6":[],"a7":[],"a8":[],"a9":[],"a10":[]})
    filho_2 = Individuo({"a1":[], "a2":[],"a3":[],"a4":[],"a5":[],"a6":[],"a7":[],"a8":[],"a9":[],"a10":[]})
    
    #aqui copia a primeira parte do gene dos genitores
    for i in range(0, ponto):
        #copiando gene do pai(filho_1) e da mãe(filho_2)
        # ----------------------------- filho_1 -----------------------------------
        #essas duas linhas servem para garantir que não haja elementos repetidos na lista de vizinhos do filho_1
        conjunto_1 = set(filho_1.grafo[vertices[i]])#conjunto de todos os vizinhos de vertices[i] no grafo filho_1
        conjunto_1.update(set(pai.grafo[vertices[i]]))#atualiza esse conjunto com os vizinhos de vertices[i] do pai
        
        filho_1.grafo[vertices[i]] = list(conjunto_1)#atribui o novo conjunto ao filho
        
        for element in conjunto_1:
            #esse loop é usado para atualizar a lista dos vizinhos com o vertices[i] no filho_1 e 2
            conj_1 = set(filho_1.grafo[element])
            conj_1.add(vertices[i])
            filho_1.grafo[element] = list(conj_1)
        
        # ----------------------------- filho_2 -----------------------------------
        #essas duas linhas servem para garantir que não haja elementos repetidos na lista de vizinhos do filho_2
        conjunto_2 = set(filho_2.grafo[vertices[i]])#conjunto de todos os vizinhos de vertices[i] no grafo filho_2
        conjunto_2.update(set(mae.grafo[vertices[i]]))#atualiza esse conjunto com os vizinhos de vertices[i] da mãe
        
        filho_2.grafo[vertices[i]] = list(conjunto_2)#atribui o novo conjunto ao filho_2
        
        for element in conjunto_2:  
            conj_2 = set(filho_2.grafo[element])
            conj_2.add(vertices[i])
            filho_2.grafo[element] = list(conj_2)
    
    #aqui copia a segunda parte do gene dos genitores
    for i in range(ponto, vert_len):
        #copiando gene do pai(filho_1) e da mãe(filho_2)
       
        # ------------------ filho_1 -------------------------------
        #essas duas linhas servem para garantir que não haja elementos repetidos na lista de vizinhos do filho_1
        conjunto_1 = set(filho_1.grafo[vertices[i]])#conjunto de todos os vizinhos de vertices[i] no grafo filho_1
        conjunto_1.update(set(mae.grafo[vertices[i]]))#atualiza esse conjunto com os vizinhos de vertices[i] da mãe
        
        filho_1.grafo[vertices[i]] = list(conjunto_1)#atribui o novo conjunto ao filho_1
        
        for element in conjunto_1:
            #esse loop é usado para atualizar a lista dos vizinhos com o vertices[i] no filho
            conj = set(filho_1.grafo[element])
            conj.add(vertices[i])
            filho_1.grafo[element] = list(conj)
       
        # ------------------- filho_2 -------------------------------
        conjunto_2 = set(filho_2.grafo[vertices[i]])#conjunto de todos os vizinhos de vertices[i] no grafo filho
        conjunto_2.update(set(pai.grafo[vertices[i]]))#atualiza esse conjunto com os vizinhos de vertices[i] do pai
        
        filho_2.grafo[vertices[i]] = list(conjunto_2)#atribui o novo conjunto ao filho
        
        for element in conjunto_2:    
            conj = set(filho_2.grafo[element])
            conj.add(vertices[i])
            filho_2.grafo[element] = list(conj)
    
    conecta_componentes(filho_1, pai, mae)#corrige o filho criado caso ele seja um individuo monstro
    conecta_componentes(filho_2, pai, mae)#corrige o filho criado caso ele seja um individuo monstro
    
    filho_1.paredes_presentes = calc_paredes(filho_1)
    filho_2.paredes_presentes = calc_paredes(filho_2)
    
    filho_1.fitness = fitness(filho_1)
    filho_2.fitness = fitness(filho_2)
    
            
    return [filho_1, filho_2]


# # Implementação de checar individuo e inicializar população

# In[290]:


def checar_individuo(individuo):
    "retorna True ou False se o individuo.grafo é conexo"
    global vertices
    grafo = individuo.grafo
    visitados = []#lista de vertices visitados
    fila = []#a fila
    
    s = random.choice(vertices)#escolhe um ponto de partida aleatorio
    
    fila.append(s)#coloca ele na fila
    
    while(len(fila) > 0):#algoritmo BFS
        s = fila.pop(0)#retira o proximo elemento da fila
        if not s in visitados:#se ele não foi visitado
            visitados.append(s)#coloca na lista de visitados
            vizinhos_s = grafo[s]#os visinhos dele
            fila.extend(vizinhos_s)#adiciona os visinhos na fila
            
    return len(visitados) == len(vertices)#retorn True se visitou todos os vertices, False caso contrário


# In[291]:


def init_pop():
    "devolve uma população gerada aleatoriamente de grafos conexos",
    global TAMANHO_POP
    global paredes_totais
    
    
    pop = []#população vazia
    for i in range(TAMANHO_POP):#cria cada individuo de uma vez
        paredes_escolhidas = [("a1", "a6"),("a7", "a8"),("a4", "a3")]
        filho = Individuo({'a1': ['a6'],
                 'a2': [],
                 'a3': ['a4'],
                 'a4': ['a3'],
                 'a5': [],
                 'a6': ['a1'],
                 'a7': ['a8'],
                 'a8': ['a7'],
                 'a9': [],
                 'a10': []}, paredes_presentes = [("a1", "a6"),("a7", "a8"),("a4", "a3")])# inicializa um individuo apenas com as paredes obrigatórias
        
        while(not checar_individuo(filho)):#enquanto o filho não for um grafo conexo
            parede = random.choice(paredes_totais)#escolhe uma parede aleatória das paredes totais
            
            if (not parede[0] in filho.grafo[parede[1]]) and (not parede in paredes_escolhidas):#verifica se essa parede já foi posicionada no filho
                filho.grafo[parede[0]].append(parede[1])#adiciona nas listas de adjacência do grafo
                filho.grafo[parede[1]].append(parede[0])
                filho.paredes_presentes.append(parede)#adiciona na lista de paredes presentes no filho
                paredes_escolhidas.append(parede)
              
        filho.fitness = fitness(filho)#calcula o fitness do filho
        pop.append(filho)#adiciona o filho a população
    
    return pop


# # Loop do algoritmo

# In[292]:


populacao = init_pop()


# In[293]:


for i in range(len(populacao)):
    print("Inidividuo: ", "Fitness ", populacao[i].fitness, " ", len(populacao[i].paredes_presentes), "\n")
    print(populacao[i].grafo.__str__(), end="\n")


# In[294]:


geracao = 1


# In[295]:


while geracao <= 1000:
    print(geracao, end= "\n")
    candidatos_pais = seleciona_pais(populacao, TAXA_DE_CRUZAMENTO)
    print("seleciona pais")
    filhos = cruza_populacao(candidatos_pais)
    print("Cruzamento")
    populacao.extend(filhos)
    populacao = selecao(populacao)
    print("Seleção")
    geracao += 1


# In[296]:


for i in range(len(populacao)):
    print("Inidividuo: ", "Fitness ", populacao[i].fitness, " ", len(populacao[i].paredes_presentes), "\n")
    print(populacao[i].grafo.__str__(), end="\n")

