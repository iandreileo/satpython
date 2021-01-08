import math
import copy
import sys
import re

variables = []
signs = ['V', '^', ')', '(', '~']
response = 0
 
def generateTree():
    # prelucram tree-ul global
    global tree
    # setam un contor
    contor = 0
    # setam paritate de 2 (puteri a lui 2)
    paritate = 2
    # contorul pentru vectorul de variabile
    contorVector = 0
    # parcurgem toate nodurile
    while contor < len(tree):
        # completam pe nivel
        if (contor < paritate - 1):
            tree[contor] = variables[contorVector]
        # sarim la urmatorul nivel
        else:
            # crestem puterea lui 2
            paritate = paritate * 2
            # crestem contorul vectorului
            contorVector = contorVector+1
            # umplem nodul
            tree[contor] = variables[contorVector]
        contor = contor + 1


def validateExpression(exp):
    # initializam un contor cu 0
    contor = 0
    # initializam corect, considerand ca e gresit (0)
    corect = 0
    # parcurgem expresia
    while contor < len(exp):
        # iteram intre paranteze
        if exp[contor] == "(":
            # trecem pe pozitia urmatoare
            contor = contor + 1
            # consideram ca nu am gasit un 1
            gasit = 0
            # iteram pana la sfarsitul parantezei
            while exp[contor] != ")":
                # daca am gasit un 1 sau un minus 0
                if (exp[contor] == "1" and exp[contor - 1] != "~")  or (exp[contor - 1] == "~" and exp[contor] == "0"):
                    # gasit e pozitiv
                    gasit = 1
                    # iesim din while
                    break
                # iteram contorul
                contor = contor + 1
            # daca nu am gasit niciun 1
            # expresia nu e validata
            if gasit == 0:
                # iesim din functie
                return 0
        else:
            contor = contor + 1
    # returnam 1 in cazul in care
    # am gasit peste tot
    return 1

# o functie auxiliar pentru replace
# pentru ca functia replace nu era
# suficienta, de la cifre la numere
def regexAux(var, v, exp):
    # facem replace la toate posibilitatile
    regex = "\(" + var + "V"
    replaced = re.sub(regex, "(" + v + "V", exp)
    regex = "\~" + var + "V"
    replaced = re.sub(regex, "~" + v + "V", replaced)
    regex = "V" + var + "V"
    replaced = re.sub(regex, "V" + v + "V", replaced)
    regex = "\~" + var + "\)"
    replaced = re.sub(regex, "~" + v + ")", replaced)
    regex = "V" + var + "\)"
    replaced = re.sub(regex, "V" + v + ")", replaced)
    return replaced
        
def checkExpression(v):
    global response
    contor = 0
    # facem o copie deep a expresiei
    copieExpresie = copy.deepcopy(expression)
    # iteram prin vectorul de variabile primit
    while contor < len(v):
        # inlocuim in expresie variabilele cu 1/0 dupa caz
        copieExpresie = regexAux(variables[contor], str(v[contor]),copieExpresie)
        
        # pe ultimul nivel construim expresie stanga
        copieStanga = regexAux(variables[len(variables) - 1], "0", copieExpresie)
        
        # pe ultimul nivel construim expresie dreapta
        copieDreapta = regexAux(variables[len(variables) - 1], "1", copieExpresie)
        
        contor = contor + 1
    # daca pe stanga e 1
    # inseamna ca am gasit o varianta
    # si returnam
    if validateExpression(copieStanga) == 1:
        response = 1
        return 1
    # daca pe dreapta e 1
    # inseamna ca am gasit o varianta
    # si returnam
    if validateExpression(copieDreapta) == 1:
        response = 1
        return 1
    return 0


# variable preOrder
global level
lr = 0
level = 0
global copie
copie = []

def preOrder(index):
    # variabile globale necesare
    global level
    global lr
    # daca nu suntem la primul nod punem in vector 0/1
    if level != 0:
        copie.append(lr)
        
    # testam daca am ajuns la capatul unui path
    if index >= len(tree):
        # scoatem din vector ultima pozitie
        copie.pop(len(copie) - 1)
        return;
    
    # testez daca suntem pe frunza
    if tree[index] == variables[len(variables) - 1]:
        checkExpression(copie)
        # daca response e 1
        # inseamna ca e corect
        if response == 1:
            # aruncam o exceptie ca sa fim eficienti
            # si sa iesim din functie
            raise Exception("Corect")

    # nivel + pozitie 0/1
    level = level + 1
    lr = 0
    
    # stanga
    preOrder((2 * index)+1)
    
    # dreapta
    preOrder((2 * index)+2)
    
    # nivel + pozitie 0/1
    level = level -1
    lr = 1
    if len(copie) > 0:
        copie.pop(len(copie) - 1)
    
    
def parse(expression):
    # definim contor
    contor = 0
    # parcurgem expresia
    while contor < len(expression):
        # definim un auxiliar curent
        current = ""
        # testam daca suntem intr-o paranteza
        if not expression[contor] in ['(', ')']:
                if not expression[contor] in signs:
                    # formam numarul pana dam de un caracter non-number
                    while not expression[contor] in signs:
                        current += expression[contor]
                        contor = contor + 1
                    # print(current) 
                    if not current in variables:
                        variables.append(current)
        # crestem contorul
        contor = contor + 1
    # initializam un tree global
    global tree
    # il facem arbore complet cu cate nivele avem nevoie
    nodes = 1 + 2 * (pow(2, len(variables)-1)-1)
    tree = [0] * nodes
    # il completam
    generateTree()


def main():
    global expression
    # pentru local
    f = open(sys.argv[1], "r")
    expression = f.read()
    # sfarsit pentru local
    
    # pentru HR
    # expression = input()
    # sfarsit pentru HR
    # parsam expresia
    parse(expression)
    # print(tree)
    # print(expression)
    try:
        preOrder(0)
        print(response)
    except:
        print(1)


if __name__ == "__main__":
    main()