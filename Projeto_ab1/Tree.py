#!/usr/bin/env python
# coding: utf-8

# In[148]:


import random
import copy


# In[149]:


cont = 0
auxiliar = None


# In[150]:


#operadores suportados e operandos
ops = ["and", "or", "not", "p", "q", "r"]


# In[151]:


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


# In[152]:


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
        if(tree != None):
            if tree.op == "not":
                #print(tree.op,end = " ")
                str_ = tree.op + " "
                str_ += self.print_tree_expr(tree.t_left)
                return str_
            else:
                str_ = ""
                str_ += self.print_tree_expr(tree.t_left) 
                str_ += tree.op + " "
                #print(tree.op, end = " ")
                str_ += self.print_tree_expr(tree.t_right)
                return str_
        else:
            return ""
    
    
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


# In[153]:


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


# In[154]:


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


# In[155]:


def exec_tree(tree, p, q, r):
    """
    Executa o resultado da arvore que possui tree como raíz
    p, q, e r são as atribuições das 3 proposições
    Essa função funciona como um avaliador de arvore
    A arvore é uma expressão lógica, então ela pode ser avaliada.
    A avaliação é feita primeiro nas subarvore depois na raiz da subarvore
    """
    if tree == None:
        return None
    elif tree.op == "p":
        tree.value = p#atribui o valor da proposição a arvore
    elif tree.op == "q":
        tree.value = q
    elif tree.op == "r":
        tree.value = r
    else:#se tree não for uma proposição é um or, not ou and
        exec_tree(tree.t_left, p, q, r)#calcula o resultado a esquerda
        exec_tree(tree.t_right, p, q, r)#calcula o resultado a direta
        
        #quando tree.op == 'not' tree não possui subarvore a direita
        lvalue = tree.t_left.value if tree.t_left is not None else None#caso a subarvore a esquerda não existe o resultado é None
        rvalue = tree.t_right.value if tree.t_right is not None else None#caso a subarvore a direita não existe o resultado é None
        tree.value = exec_node(tree, tree.t_left.value, rvalue)#calcula o valor do nó


# In[156]:


def gen_ind(tree):
    """Retorna a(s) subarvore(s) de tree"""
    global ops
    global prop
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
        l_tree = Tree(op1)#subarvore esquerda
        l1, l2 = gen_ind(l_tree)#gera as subarvores
        l_tree.t_left = l1
        l_tree.t_right = l2
        
        
        r_tree = Tree(op2)#subarvore direita
        r1, r2 = gen_ind(r_tree)#gera as subarvores
        r_tree.t_left = r1
        r_tree.t_right = r2
        
        return [l_tree, r_tree]


# In[157]:


def init_pop(pop_size):
    pop = []
    global ops
    for i in range(pop_size):
        op, = random.sample(ops, k = 1)
        root = Tree(op)
        left, right = gen_ind(root)
        root.t_left = left
        root.t_right = right
        root.fitness = fitness(root)
        pop.append(root)
    return pop


# In[158]:


def contar_profundidade(tree):
        if(tree != None):
            return max(1 + contar_profundidade(tree.t_left), 1 + contar_profundidade(tree.t_right))
        return 0


# In[159]:


def contar_folhas(tree):
    if(tree != None):
    #print("Oi, eu sou o tee.op", tree.op)
        if tree.op in ["p", "q", "r"]:
            global cont
            cont += 1
        else:
            contar_folhas(tree.t_left)
            contar_folhas(tree.t_right)


# In[160]:


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


# In[198]:


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


# In[214]:


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
    
    filho1.fitness = fitness(filho1)
    filho2.fitness = fitness(filho2)

    return [filho1, filho2]


# In[184]:


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
    


# In[185]:


def walkTree(root):
    aux = 0
    if not root:
        return
    elif random.randint(1, 100) <= 20:
        return root.op
    else:
        aux = walkTree(root.t_left)
        if aux != 0:
            return aux
        aux = walkTree(root.t_right)
        if aux != 0:
            return aux


# In[165]:


def mutacao(tree):
    if random.randint(1, 100) <= 5:
        node = walkTree(tree)
    else:
        return tree


# In[166]:


def selecao(populacao):
    ordenaPop = sorted(populacao, key = lambda tree: tree.fitness, reverse = True)
    return ordenaPop[0:TAMANHO_POP]


# # Testes

# In[167]:


pop = init_pop(100)


# In[168]:


for idx, ind in enumerate(pop):
    print(idx, ind,"fitness:", ind.fitness, end = "\n")


# In[174]:


pai = pop[2]
mae = pop[0]


# In[175]:


ap = selecionar_sub(pai)


# In[176]:


am = selecionar_sub(mae)


# In[177]:


print(pai, "\n", ap[0], "\n", ap[1][::-1])


# In[178]:


print(mae, "\n", am[0], "\n", am[1][::-1])


# In[134]:


substituir_arvore(pai, ap[1][::-1], am[0])


# In[213]:


print(pai)


# In[136]:


substituir_arvore(mae, am[1][::-1], ap[0])


# In[201]:


print(mae)


# In[215]:


filhos = cruzamento(pai, mae)


# In[216]:


print(filhos[0])


# In[217]:


print(filhos[1])


# In[219]:


print_tree_not(filhos[0], 0)


# In[ ]:




