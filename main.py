from capacity import getCapacity
import time

def welcome():                        
    nome=input('Digite o seu nome:\n')   
    print('\nSaudações, {}. Vamos começar os cálculos :)\n'.format(nome))
    
    time.sleep(3)    
    init_program()


def init_program():
    mochilas = getCapacity()
    rotas = getCapacity()
    print('Melhor organização da caixa: {}'.format(mochilas))
    print('Melhor Rota para o entregador: {}'.format(rotas))


welcome()
