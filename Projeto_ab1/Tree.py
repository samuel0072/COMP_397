#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import copy


# In[ ]:


#operadores suportados e operandos
ops = ["and", "or", "not", "p", "q", "r"]


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
    def __init__(self, op, t_left = None, t_right = None, value = None):
        self.op = op#tipo do nó. Algum dentre ops
        self.t_left = t_left#subarvore esquerda
        self.t_right = t_right#subarvore direita
        self.value = value#valor que vai ser avaliado durante a execução da arvore
    
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
    
    def print_tree_not(self,tree, q_spc):
        """Printa a arvore como uma estrutura de diretório"""
        if(tree != None):
            for i in range(q_spc):
                print("-", end = "")
            if tree.op == "not":
                print(tree.op, end = "\n")
                self.print_tree_not(tree.t_left, q_spc+1)
            else:
                print(tree.op, end = "\n")
                self.print_tree_not(tree.t_left, q_spc+1)
                self.print_tree_not(tree.t_right, q_spc+1)
    
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
        tree.value = exec_node(tree, lvalue, rvalue)#calcula o valor do nó


# In[ ]:


def gen_ind(tree):
    """Retorna a(s) subarvore(s) de tree"""
    global ops
    if tree.op == "not":
        op, = random.sample(ops, k = 1)#random.sample retorna uma lista. Usando a , apenas o elemento é atribuido para op
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


# In[ ]:


def gen_subtree(tree):
    """Retorna a(s) subarvore(s) de tree"""
    ops = ["and", "or", "not", "prop"]
    prop = ["p", "q", "r"]
    if tree.op == "not":
        op, = random.sample(ops, k = 1)#random.sample retorna uma lista. Usando a , apenas o elemento é atribuido para op
        if op == 'prop':
            op, = random.sample(prop, k = 1)
        d_tree = Tree(op)
        return [d_tree, None]#como tree é um not então só possui uma subarvore
    
    elif tree.op in prop:#verifica se a raíz dessa subarvore é uma proposição
        return [None, None]# como tree é uma proposição, então não possui subarvore
    
    else:
        #caso seja um 'or' ou 'and'

        op1, op2 = random.sample(ops, k = 2)
        if op1 == 'prop':
            op1, = random.sample(prop, k = 1)
        if op2 == 'prop':
            op2, = random.sample(prop, k = 1)
        l_tree = Tree(op1)#subarvore esquerda
        r_tree = Tree(op2)#subarvore direita
         
        return [l_tree, r_tree]


# In[ ]:


def init_pop(pop_size):
    pop = []
    global ops
    for i in range(pop_size):
        op, = random.sample(ops, k = 1)
        root = Tree(op)
        left, right = gen_ind(root)
        root.t_left = left
        root.t_right = right
        pop.append(root)
    return pop


# # Testes

# ### Inicializar a população

# In[ ]:


pop = init_pop(100)


# In[ ]:


for idx, ind in enumerate(pop):
    print(idx,ind, end = "\n")


# In[ ]:


ind = pop[55]


# In[ ]:


print(ind)


# In[ ]:


ind.print_tree_not(ind, 0)


# ### avaliação da árvore

# In[ ]:


exec_tree(ind, False, False, True)


# In[ ]:


ind.value


# ### cópia da arvore

# In[ ]:


a = copy.deepcopy(ind)


# In[ ]:


print(a, a.value)


# In[ ]:


a.op = 'or'


# In[ ]:
#HENRIQUE
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

def selecao(populacao):
    ordenaPop = sorted(populacao, key = lambda tree: fitness(tree))
    return ordenaPop[0:TAMANHO_POP]
def mutacao(tree):
    if random.randint(1, 100) <= 5:
        node = walkTree(tree)
    else:
        return tree
  




