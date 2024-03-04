from capacity import getCapacity
from routes import getFastestRoutes
import time

def welcome():                        
    nome=input('Digite o seu nome:\n')   
    print('\nSaudações, {}. Vamos começar os cálculos :)\n'.format(nome))
    
    time.sleep(3)    
    init_program()

def print_routes_items(routes_items):
    print("---------------------------------------------------------------------")
    print("                     Detalhes das Rotas e Itens                      ")
    print("---------------------------------------------------------------------")
    print("Quantidade de rotas: ", len(routes_items))
    for corrida, data in routes_items.items():
        print(f"\n{corrida}:")
        print("   Rota:")
        print("    -> ", end="")
        print(" -> ".join(data['rota']))
        print("\n   Itens da rota:")
        for item in data['itens']:
            print(f"      - Pedido: {item['pedido']}, Peso: {item['peso']}, Prioridade: {item['prioridade']}")
    print("---------------------------------------------------------------------")

def init_program():
    backpacks = getCapacity()
    dicionario_rota_itens = {}

    for index, items in enumerate(backpacks):  
        orders = [order['pedido'] for order in items]
        dicionario_rota_itens[f'Corrida_{index + 1}'] = {'rota': getFastestRoutes(orders), 'itens': items}
    
    print_routes_items(dicionario_rota_itens)


welcome()
