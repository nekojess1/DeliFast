from random import sample, random, choice
import random
import operator
import math

# Iniciando variáveis
populationSize = 0
solution = None
endPoint = 20
mutation_tax = 0.5

# Retorna um dicionário com a posição de cada letra na matriz
def get_data(file, routes):
    positions = {}
    lineNumber, columnNumber =  map(int, file.readline().split(' '))      # Recebe o nº de linhas e colunas da matriz
    for line in range(lineNumber):
        lineList = file.readline().strip().split(' ')                     # Recebe a linha do arquivo e trata os espaços em branco
        try:
            for column in range(len(lineList)):
                if lineList[column] != '0' :                              # Verifica se o valor observado não é um "0"
                    positions[lineList[column]] = (line, column)          # Atribui a letra sua posição na matriz 
        except:
            print("Something else went wrong") 
    routes.append('L')
    items_presentes = {chave: valor for chave, valor in positions.items() if chave in routes}
    positions = items_presentes
    return positions

# Inicializa a população de cromossomos (rotas)
def initiate_population(positions):
    global populationSize
    routesWithoutR = [item for item in positions if item != 'L']
    random_permutation = []
    populationSize = math.factorial(len(routesWithoutR)) // 2
    while len(random_permutation) <= populationSize:
        permutation = sample(routesWithoutR,len(routesWithoutR))              # Gera uma rota aleatória
        if (permutation not in random_permutation):
            random_permutation.append(permutation)
    return random_permutation

# Retorna a distância entre os pontos
def getGenome(possibility):
    possibility = 'L' + "".join(possibility) + 'L'
    result = 0
    for position in range (len(possibility)-1):
        atualLetter = positions.get(possibility[position])
        nextLetter = positions.get(possibility[position + 1])
        firstSubtraction = abs(atualLetter[0] - nextLetter[0])
        secondSubtraction = abs(atualLetter[1] - nextLetter[1])

        result +=  firstSubtraction + secondSubtraction
    return result 

# Calcula a aptidão de cada cromossomo (rota)
def getFitness(population):
    fitnessResults = {}
    for individual in range(len(population)):
        fitnessResults[individual] = 1/getGenome(population[individual])
    return fitnessResults

# Obtém a melhor solução com base na aptidão dos cromossomos
def getBestSolution(rank, population):
    global solution 
    possibility = max(rank.items(), key=operator.itemgetter(1))
    if solution == None:
        solution = [population[possibility[0]], possibility[1]]
    else: 
        if possibility[1] > solution[1]:
            solution = [population[possibility[0]], possibility[1]]

# Realiza a seleção de cromossomos proporcional à sua aptidão
def selection(rank):
    global populationSize
    routes = []
    rank_list = sorted(rank.items(),  key=operator.itemgetter(1),reverse = False)
    rank_sum = populationSize * (populationSize + 1) / 2
    for iterator in range(populationSize):
        prob = (float(iterator + 1) / rank_sum) * 100
        for i in range(int(prob)):
            routes.append(rank_list[iterator])
    return routes

# Realiza o cruzamento entre dois cromossomos (rotas)
def crossover(dadOne, dadTwo):
    partDadOne = []
    partDadTwo = []
    halfDadOne = len(dadOne)//2
    for i in range(0, halfDadOne):
        partDadOne.append(dadOne[i])
    partDadTwo = [item for item in dadTwo if item not in partDadOne]
    return  partDadOne + partDadTwo

# Realiza a mutação de cromossomos
def mutatePopulation(newPopulation):
    mutatedPopulation = []
    for iterator in range(0, len(newPopulation)):
        mutation_result = mutation(newPopulation[iterator])
        mutatedPopulation.append(mutation_result)
    return mutatedPopulation

# Aplica mutação a um cromossomo
def mutation(route):
    global mutation_tax
    for targetCity in range(len(route)):
        if (random.random() < mutation_tax):  
            swapCity = int(random.random() * len(route))
            firstCity = route[targetCity]
            secondCity = route[swapCity]

            route[targetCity] = secondCity
            route[swapCity] = firstCity
    return route

# Obtém as rotas mais rápidas utilizando o algoritmo genético
def getFastestRoutes(routes):
    global solution
    global positions

    solution = None

    file = open('directions.txt', 'r')
    positions = get_data(file, routes)
    population = initiate_population(positions)

    for index in range(endPoint):
        fitnessResult = (getFitness(population))
        getBestSolution(fitnessResult, population)
        newPopulationSize = 0
        newPopulation = []
        selectionRank = selection(fitnessResult)
        while newPopulationSize < populationSize:
            dadOne, dadTwo = (population[choice(selectionRank)[0]], population[choice(selectionRank)[0]])
            sonOne = crossover(dadOne, dadTwo)
            sonTwo = crossover(dadTwo, dadOne)

            newPopulation.append(sonOne)
            newPopulation.append(sonTwo)

            newPopulationSize+=2
        population = mutatePopulation(newPopulation)
    return solution[0]
