#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import copy
import math


# In[ ]:


cont = 0
auxiliar = None


# In[ ]:


#operadores suportados e operandos
ops = ["and","or", "not", "p", "q", "r"]


# In[ ]:


TAMANHO_POP = 100
TAXA_CRUZAMENTO = 0.6


# In[ ]:


#Escolhemos a tabela 6

# VERDADEIRO VERDADEIRO VERDADEIRO FALSO
#
# VERDADEIRO VERDADEIRO FALSO      FALSO
#
# VERDADEIRO FALSO      VERDADEIRO VERDADEIRO
#
# VERDADEIRO FALSO      FALSO      FALSO
#
# FALSO      VERDADEIRO VERDADEIRO FALSO
#
# FALSO      VERDADEIRO FALSO      FALSO
#
# FALSO      FALSO      VERDADEIRO FALSO
#
# FALSO      FALSO      FALSO      FALSO

tabela6 = [[True, True, True, False],
            [True, True, False, False],
            [True, False, True, True],
            [True, False, False, False],
            [False, True, True, False],
            [False, True, False, False],
            [False, False, True, False],
            [False, False, False, False]]


# In[ ]:


class Tree:
    propositions = ["p", "q", "r"]
    operators = ["or", "not", "and"]
    def __init__(self, op, t_left = None, t_right = None, value = None, fitness = 0):
        self.op = op#tipo do nó. Algum dentre ops
        self.t_left = t_left#subarvore esquerda
        self.t_right = t_right#subarvore direita
        self.value = value#valor que vai ser avaliado durante a execução da arvore
        self.fitness = 0
    
    def print_tree_expr(self, tree):
        "Retorna uma string representando a arvore como uma expressão lógica"
        if tree.op in tree.propositions:
            return tree.op + " "
        if tree.op == "not":
            #print(tree.op,end = " ")
            str_ = tree.op + " ("
            str_ += (self.print_tree_expr(tree.t_left) + ")")
            return str_
        else:
            str_ = " ("
            str_ += self.print_tree_expr(tree.t_left) 
            str_ += " "+ tree.op + " "
            #print(tree.op, end = " ")
            str_ += (self.print_tree_expr(tree.t_right) + ")")
            return str_ 
       
    
    
    def __deepcopy__(self, memo):#dicionário não é usado
        if self.op in self.propositions:#folha
            return Tree(self.op, t_left = None, t_right = None, value = self.value)
        elif self.t_right != None:#não está em um nó not
            return Tree(self.op,
                        t_left = self.t_left.__deepcopy__(memo),
                        t_right = self.t_right.__deepcopy__(memo),
                        value = self.value)
        else:#está em um nó not
            return Tree(self.op,
                        t_left = self.t_left.__deepcopy__(memo),
                        t_right = None,
                        value = self.value)
    
    def __str__(self):
        return self.print_tree_expr(self)


# In[ ]:


def print_tree_not(tree, q_spc):
    """Printa a arvore como uma estrutura de diretório"""
    if(tree != None):
        for i in range(q_spc):
            print("-", end = "")
        if tree.op == "not":
            print(tree.op, end = "\n")
            print_tree_not(tree.t_left, q_spc+1)
        else:
            print(tree.op, end = "\n")
            print_tree_not(tree.t_left, q_spc+1)
            print_tree_not(tree.t_right, q_spc+1)


# In[ ]:


def exec_node(tree, lvalue, rvalue):
    """
    recebe um nó de uma arvore
    retorna o resultado daquele nó
    """
   
    if tree.op == "or":
        return lvalue or rvalue
    elif tree.op == "and":
        return lvalue and rvalue
    elif tree.op == "not":
         return not lvalue
    elif tree.op in ["p", "q", "r"]:
        return lvalue
    else:
        raise Exception("tree.op inválido.")


# In[ ]:


def exec_tree(tree, p, q, r):
    """
    Executa o resultado da arvore que possui tree como raíz
    p, q, e r são as atribuições das 3 proposições
    Essa função funciona como um avaliador de arvore
    A arvore é uma expressão lógica, então ela pode ser avaliada.
    A avaliação é feita primeiro nas subarvore depois na raiz da subarvore
    """
    if tree.op == "p":
        tree.value = p#atribui o valor da proposição a arvore
    elif tree.op == "q":
        tree.value = q
    elif tree.op == "r":
        tree.value = r
    else:#se tree não for uma proposição é um or, not ou and
        if tree.op == "not":#quando tree.op == 'not' tree não possui subarvore a direita
            exec_tree(tree.t_left, p, q, r)
            lvalue = tree.t_left.value
            tree.value = exec_node(tree, lvalue, None)
        else:
            exec_tree(tree.t_left, p, q, r)#calcula o resultado a esquerda
            exec_tree(tree.t_right, p, q, r)#calcula o resultado a direta
            lvalue = tree.t_left.value
            rvalue = tree.t_right.value
            tree.value = exec_node(tree, lvalue, rvalue)#calcula o valor do nó


# In[ ]:


def gen_ind(tree):
    """Retorna a(s) subarvore(s) de tree"""
    global ops
    if tree.op == "not":
        op, = random.sample(ops, k = 1)#random.sample retorna uma lista. Usando a, apenas o elemento é atribuido para op
        d_tree = Tree(op)
        d1, d2 = gen_ind(d_tree)#gera as subarvores
        d_tree.t_left = d1
        d_tree.t_right = d2
        return [d_tree, None]#como tree é um not então só possui uma subarvore
    
    elif tree.op in ["p", "q", "r"]:#verifica se a raíz dessa subarvore é uma proposição
        return [None, None]# como tree é uma proposição, então não possui subarvore
    
    else:
        #caso seja um 'or' ou 'and'

        op1, op2 = random.sample(ops, k = 2) 
        #op1, = random.sample(ops, k = 2)
        #op2, = random.sample(ops, k = 1)
        l_tree = Tree(op1)#subarvore esquerda
        l1, l2 = gen_ind(l_tree)#gera as subarvores
        l_tree.t_left = l1
        l_tree.t_right = l2
        
        
        r_tree = Tree(op2)#subarvore direita
        r1, r2 = gen_ind(r_tree)#gera as subarvores
        r_tree.t_left = r1
        r_tree.t_right = r2
        
        return [l_tree, r_tree]


# In[ ]:


def init_pop(pop_size):
    pop = []
    global ops
    while len(pop) != pop_size:
        op, = random.sample(ops, k = 1)
        root = Tree(op)
        left, right = gen_ind(root)
        root.t_left = left
        root.t_right = right
        

        if ok(root, ["p", "q", "r"]):#se a função retornar false o if é executado
            
            root.fitness = fitness(root)
            pop.append(root)
            
    return pop


# In[ ]:


def contar_profundidade(tree):
        if(tree != None):
            return max(1 + contar_profundidade(tree.t_left), 1 + contar_profundidade(tree.t_right))
        return 0


# In[ ]:


def contar_folhas(tree):
    if(tree != None):
    #print("Oi, eu sou o tee.op", tree.op)
        if tree.op in ["p", "q", "r"]:
            global cont
            cont += 1
        else:
            contar_folhas(tree.t_left)
            contar_folhas(tree.t_right)


# In[ ]:


def fitness(individuo):
    "retorna o fitness do indivíduo"
    fit = 0

    i = 0
    while(i < 8):
        lista_aux = tabela6[i]
      #p, q, r, valor_esperado
        p = lista_aux[0]
        q = lista_aux[1]
        r = lista_aux[2]
        resultado_esperado = lista_aux[3]

        exec_tree(individuo, p, q, r)
        resultado = individuo.value
      #print("Eu sou o resultado", resultado)
      #print("Eu sou o esperado", resultado_esperado)
        if(resultado == resultado_esperado):
            fit = fit + 1

        i = i + 1

    profundidade = contar_profundidade(individuo)

    global cont
    cont = 0
    contar_folhas(individuo)

    if(profundidade == 0):
        termo2 = 0
    else:
        termo2 = 1/profundidade

    if(cont == 0):
        termo3 = 0
    else:
        termo3 = 1/cont
      
    return fit + termo2 + termo3


# In[ ]:


def selecionar_sub(tree, rt_chance = 1):
    """
    Retorna um nó aleatório da árvore e o caminho percorrido da raíz até aquele nó.
    Sempre que a função alcança uma folha, a folha é retornada como nó escolhido.
    O caminho é retornado de trás pra frente.
    tree é o nó atual
    rt_chance é a chance desse nó ser escolhido.
    """
    if tree.op in tree.propositions:#verifica se o nó atual é uma folha
        return [tree, []]
    
    x = random.randint(0, rt_chance)#Quanto maior rt_chance, maior  a chance de tree ser retornado

    if x == 0:#escolheu ir pra esquerda
        tree, caminho = selecionar_sub(tree.t_left, rt_chance = rt_chance + 1)
        caminho.extend(["esquerda"])
        return [tree, caminho]
    elif x == 1:#escolheu ir pra direita
        if(tree.op == "not"):#se tree for um not ele não possuí filho à direita
            tree, caminho = selecionar_sub(tree.t_left, rt_chance = rt_chance + 1)
            caminho.extend(["esquerda"])
        else:
            tree, caminho = selecionar_sub(tree.t_right, rt_chance = rt_chance + 1)
            caminho.extend(["direita"])
        return [tree, caminho]
    else:#escolheu retornar o nó atual
        global auxiliar
        auxiliar = tree
        return [auxiliar, []]


# In[ ]:


def cruzamento(pai, mae):
    
    e_pai, c_pai = selecionar_sub(pai)#escolhe a parte do pai
    e_mae, c_mae = selecionar_sub(mae)#""     "" ""       mãe  
    
    e_pai = copy.deepcopy(e_pai)#copia para não correr o risco de alterar o pai quando for mexer no filho
    e_mae = copy.deepcopy(e_mae)#copia para não correr o risco de alterar a mãe quando for mexer no filho
    
    filho1 = copy.deepcopy(pai)#primeiro filho é uma cópia do pai
    filho2 = copy.deepcopy(mae)#primeiro filho é uma cópia do pai
    
    #o caminho retornado por selecionar_sub está invertido
    c_mae = c_mae[::-1]#inverte o caminho
    c_pai = c_pai[::-1]#inverte o caminho
    
    substituir_arvore(filho1, c_pai, e_mae)#insere no primeiro filho a parte da mãe
    substituir_arvore(filho2, c_mae, e_pai)#insere no segundo filho a parte do pai
    

    return [filho1, filho2]


# In[ ]:


def substituir_arvore(tree, caminho, parte):
    """Insere parte em tree na posição especificada em caminho."""
    l = len(caminho)
    if l > 0:
        pai = tree
        atual = tree

        #refaz o caminho que levou à parte
        for i in range(l):
            if caminho[i] == "esquerda":
                aux = atual
                atual = atual.t_left
                pai = aux
            else:
                aux = atual
                atual = atual.t_right
                pai = aux

        #verifica se a última direção tomada foi para esquerda ou direita
        if caminho[-1] == "esquerda":
            pai.t_left = parte# substitui o pai do nó a ser substituido com a parte

        elif caminho[-1] == "direita":
            pai.t_right = parte# substitui o pai do nó a ser substituido com a parte
    


# In[ ]:


#Escolhe um nó aleatório
def walkTree(root, mult, max):
    aux = None
    if root == None:
        return
    elif random.randint(1, max) <= mult:
        return root
    else:
        if random.randint(1,2) == 1:
            aux = walkTree(root.t_left, mult + 1, max)
            if aux != None:
                return aux
            aux = walkTree(root.t_right, mult + 1, max)
            if aux != None:
                return aux
        else:
            aux = walkTree(root.t_right, mult + 1, max)
            if aux != None:
                return aux
            aux = walkTree(root.t_left, mult + 1, max)
            if aux != None:
                return aux


# In[ ]:


#Mutação: altera o operador de um nó aleatório
def mutacao(tree):
    if random.randint(1, 100) <= 5:
        #node = Tree()
        node = walkTree(tree, 1, contar_profundidade(tree))
        #print(tree)
        if node.op == "p" or node.op == "q" or node.op == "r":
            if node.op == "p":
                aux = random.randint(1,3)
                if aux == 1:
                    node.op = "q"
                elif aux == 2:
                    node.op = "r"
                else:
                    node.op = "not"
                    node.t_left = Tree("p")
                return tree
            elif node.op == "q":
                aux = random.randint(1,3)
                if aux == 1:
                    node.op = "p"
                elif aux == 2:
                    node.op = "r"
                else:
                    node.op = "not"
                    node.t_left = Tree("q")
                return tree
            else:
                aux = random.randint(1,3)
                if aux == 1:
                    node.op = "q"
                elif aux == 2:
                    node.op = "p"
                else:
                    node.op = "not"
                    node.t_left = Tree("r")
                return tree
        elif node.op == "and" or node.op =="or" or node.op =="not":
            if node.op == "and":
                node.op = "or"
            elif node.op == "or":
                node.op = "and"
            return tree
    else:
        return tree


# In[ ]:


def selecao(populacao, tamanho_max):
    
    t = len(populacao)
    
    if(tamanho_max > t ):
        raise Exception("O tamanho máximo informado é inválido.")
    elif(tamanho_max < 0):
        raise Exception("O tamanho máximo informado é inválido.")
    
    #ordena para executar a seleção elitista    
    ordenaPop = sorted(populacao, key = lambda tree: tree.fitness, reverse = True)
    ordenaPop = ordenaPop[0:tamanho_max]
    
    return ordenaPop


# In[ ]:


def selecao_pais(populacao, taxa):
    """Retorna uma população com número par de pais"""
    #ordena para executar a seleção elitista
    populacao = sorted(populacao, key = lambda tree: tree.fitness, reverse= True)
    t = len(populacao)
    q_ind = math.ceil(t *taxa)
    
    if(q_ind > t ):
        raise Exception("Quantidade de individuos na população é muito pequena.")
    if (q_ind % 2) != 0:#arredonda para o maior inteiro par mais proximo
        q_ind+=1
        
    pais = populacao[0:q_ind]
    return pais


# In[ ]:


def cruzamento_pop(candidatos_pais):
    "Retorna os filhos criados pelos candidatos a pais"
    filhos_ = []
    
    
    random.shuffle(candidatos_pais)#embaralha a lista de candidatos a pais
    
    for i in range(0, len(candidatos_pais), 2):#cruza os pais 2 a 2
        filhos = cruzamento(candidatos_pais[i], candidatos_pais[i+1])
        filhos[0] = mutacao(filhos[0])#muta o filho
        filhos[1] = mutacao(filhos[1])#muta o filho
        filhos[0].fitness = fitness( filhos[0])
        filhos[1].fitness = fitness( filhos[1])
        filhos_.extend(filhos)
        
    return filhos_


# In[ ]:


def ok(tree, rem):
    """Essa função checa se o individuo é um monstro.
    rem é uma lista de proposições que ainda não foram identificadas em tree
    Retorna True se o índividuo não possuir todas as proposições informadas em rem
    Retorna False se o individuo possuir todas as proposições informadas em rem
    Retorna True se o índividuo NÃO É um monstro
    Retorna False se o índividuo É um monstro"""
    if tree == None:#uma árvore vazia é uma arvore invalida
        return False
    if len(rem) == 0:#quando todas as proposições forem identificadas o algoritmo retorna true
        return True
    if tree.op in tree.propositions:
        if tree.op in rem:#verifica se a proposição não foi identificada
            rem.remove(tree.op)#retira a proposição da lista
    return ok(tree.t_left, rem) or ok(tree.t_right, rem)#verifica o lado esquerda e direito


# # Testes

# In[ ]:


pop = init_pop(100)


# In[ ]:


print("--------------------- Primeira Geração de Individuos ---------------------")
for idx, ind in enumerate(pop):
    print("Individuo {}: {}\t fitness: {}".format(idx, ind, ind.fitness))


# In[ ]:


print("---------------------  Execução do algoritmo ---------------------")
geracao = 1
while geracao < 300:
    print("Geração:", geracao, end= "\n")
    print("Passos:")
    pais = selecao_pais(pop, TAXA_CRUZAMENTO)
    print("\t Selecionou pais para o cruzamento")
    filhos = cruzamento_pop(pais)
    print("\t Executou o cruzamento")
    pop.extend(filhos)
    pop = selecao(pop, TAMANHO_POP)
    #pop.fitness_geracao.append(pop.individuos[0].fitness)
    print("\t Executou a seleção \n")
    print("\t Melhor individuo da geração:")
    print("\t\t {}".format(pop[0]))
    geracao += 1


# In[ ]:


print("--------------------- Individuos da última geração do algoritmo ---------------------")
for idx, ind in enumerate(pop):
    print("Individuo {}: {}\t fitness: {}".format(idx, ind, ind.fitness))


# In[ ]:


# VERDADEIRO VERDADEIRO VERDADEIRO FALSO
#
# VERDADEIRO VERDADEIRO FALSO      FALSO
#
# VERDADEIRO FALSO      VERDADEIRO VERDADEIRO
#
# VERDADEIRO FALSO      FALSO      FALSO
#
# FALSO      VERDADEIRO VERDADEIRO FALSO
#
# FALSO      VERDADEIRO FALSO      FALSO
#
# FALSO      FALSO      VERDADEIRO FALSO
#
# FALSO      FALSO      FALSO      FALSO

