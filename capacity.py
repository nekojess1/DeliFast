from pulp import LpMaximize, LpProblem, LpVariable

def getData():
    file = open('items.txt', 'r')
    items = []
    while True:
        line = file.readline().strip().split(' ')   # Lê a próxima linha do arquivo
        if not line or len(line) != 3:  # Se a linha estiver vazia (fim do arquivo), sai do loop
            break
        item = {"pedido": (line[0]), "peso": int(line[1]), "prioridade": int(line[2])}  # Define o dicionário com os itens
        items.append(item)
    return items

def getCapacity():
    # Lista que armazena as viagens que o motorista terá que realizar
    deliveries = []
    items = getData()
    while items:
        capacity = 10  # Capacidade máxima da mochila

        # Criação do problema de otimização
        prob = LpProblem("knapsack_problem", LpMaximize)

        """ Variável de decisão, se o item vai ou não na mochila.
            Se cria um dicionário, como esse abaixo:
            {'A': Item_A, 'B': Item_B, 'C': Item_C, 'D': Item_D, 'E': Item_E}
            Ao definir o dicionário, o varprioridade de cada item será None até resolver. Após resolver se o item for selecionado, o valor ficar 1. Caso contrário, ficará 0. 
        """
    
        item_selected = LpVariable.dicts("Item", [item["pedido"] for item in items], cat='Binary')
        
        # Função objetivo de maximizar o número de itens possíveis na entrega contabilizando pelo valor deles como nível de prioridade
        prob += sum(item_selected[item["pedido"]] * item["prioridade"] for item in items)

        # Restrição de capacidade, o peso do item não pode ser maior do que a capacidade máxima da bolsa
        prob += sum(item_selected[item["pedido"]] * item["peso"] for item in items) <= capacity

        # Resolvendo o problema usando o pulp 
        prob.solve()

        # Exibindo o resultado
        selected_items_trip  = []
        for item in items[:]:  # Criando cópia da lista e removendo os itens que já foram nessa entrega, para separar os itens das próximas entregas
            if item_selected[item["pedido"]].varValue == 1:
                items.remove(item)
                selected_items_trip.append(item)                
        deliveries.append(selected_items_trip )
    return deliveries
