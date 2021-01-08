import sys

matrix = []
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
variables = []
minus = 0

# vedem toate variabilele
def parse(expression):
    # print(expression)
    contor = 0
    contorRows = 0
    while contor < len(expression):
        current = 0
        # testam daca suntem intr-o paranteza
        if not expression[contor] in ['(', ')']:
            if expression[contor] in number:
                # formam numarul pana dam de un caracter non-number
                while expression[contor] in number:
                    current = current * 10 + int(expression[contor])
                    contor = contor + 1
                # print(current) 
                if not current in variables:
                    variables.append(current)
        if expression[contor] in ['^']:
            contorRows = contorRows + 1
        # crestem contorul
        contor = contor + 1
        
    # cream o matrice de 0-uri
    global matrix
    matrix = [([0]*len(variables)) for i in range(contorRows + 1)]
    
# formam matricea conform cursului
def createMatrix(expression):
    # print(expression)
    i = 0
    j = 0
    contor = 0
    minus = 0
    while contor < len(expression):
        # formam variabila in current
        current = 0
        # testam daca suntem intr-o paranteza
        if not expression[contor] in ['(', ')']:
            if expression[contor] == '~':
                minus = 1
            # daca suntem intr-o paranteza
            # testam daca formam o variabila
            if expression[contor] in number:
                # formam numarul pana dam de un caracter non-number
                while expression[contor] in number:
                    current = current * 10 + int(expression[contor])
                    contor = contor + 1
                # print(current) 
            # aici trebuie sa punem in matrice
            if current != 0:
                if minus == 1:
                    # inseamna ca punem -1
                    matrix[i][variables.index(current)] = -1
                    minus = 0
                else:
                    # inseamna ca punem 1
                    matrix[i][variables.index(current)] = 1
                    minus = 0
        # sarim la randul urmator
        if expression[contor] in ['^']:
            i = i+1
        # crestem contorul
        contor = contor + 1

# functie auxiliara pentru realizarea backtrackingului
def backtrackingAux(n, s):
    # cazul de baza
    if n == 1:
        return s
    # recurenta generala
    return [d + b for d in backtrackingAux(1, s) 
             for b in backtrackingAux(n - 1, s)]
# functia prin care rezolvam task-ul propriu-zis
def resolve(bktr):
    # consideram ca toate randurile sunt 1
    rowCorect = 1
    # iteram prin toate elementele generate de backtraking
    for el in bktr:
        # reinitializam cu 1
        rowCorect = 1
        # iteram prin randuri
        for i in range(0,len(matrix)):
            # consideram ca un rand este gresit
            colCorect = 0
            # iteram prin coloane
            for j in range(0,len(matrix[0])):
                # daca elementul e 1 
                # atat in matrice cat si in backtraking
                # inseamna ca randul are cel putin un 1
                # si e corect
                if matrix[i][j] == 1:
                    if int(el[j]) == 1:
                        colCorect = 1
                        break
                # daca elementul e -1 
                # in matrice si 0 in backgraking
                # inseamna ca randul are cel putin un 1
                # si e corect
                if matrix[i][j] == -1:
                    if int(el[j]) == 0:
                        colCorect = 1
                        break
            # daca randul nu e corect, sarim la urmatorul set
            # de backtraking
            if colCorect == 0:
                rowCorect = 0
                break
        # daca un set de backtraking este corect
        # returnam direct 1
        if rowCorect == 1:
            return 1
    # cazul final, daca nu a fost niciun set corect
    # returnam 0
    return 0


    
def main():
    
    f = open(sys.argv[1], "r")
    expression = f.read()
    # sfarsit pentru local
    
    # pentru HR
    # expression = input()
    # sfarsit pentru HR
    # parsam expresia
    
    # citim expresia
    # expression = input()
    # parsam expresia
    parse(expression)
    # cream matricea
    createMatrix(expression)
    # generam posibilitatile
    bktr = backtrackingAux(len(variables),'10')
    # test
    # print(matrix)
    # rezolvam
    print(resolve(bktr))
    
if __name__ == "__main__":
    main()