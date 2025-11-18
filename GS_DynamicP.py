from typing import List, Tuple, Dict
import sys

# Aumenta o limite de recursão para casos de teste muito grandes, se necessário
sys.setrecursionlimit(2000)

# Tipo para projetos: (nome, valor, horas)
Project = Tuple[str, int, int]

def greedy_knapsack(projects: List[Project], capacity: int) -> Tuple[int, List[int]]:
    """
    FASE 1: ESTRATÉGIA GULOSA (GREEDY)
    
    Prioriza projetos com a maior densidade de valor (Valor / Horas).
    Seleciona itens sequencialmente enquanto houver capacidade.
    
    Complexidade: O(N log N) devido à ordenação.
    """
    # Cria lista com índice original e razão V/E: (index, name, val, cost, ratio)
    indexed = [(i, p[0], p[1], p[2], p[1] / p[2]) for i, p in enumerate(projects)]
    
    # Ordena decrescente pela razão (ratio)
    indexed.sort(key=lambda x: x[4], reverse=True)

    total_value = 0
    total_hours = 0
    chosen = []

    for i, name, value, hours, ratio in indexed:
        if total_hours + hours <= capacity:
            chosen.append(i)
            total_hours += hours
            total_value += value

    return total_value, chosen


def recursive_knapsack(projects: List[Project], capacity: int) -> Tuple[int, List[int]]:
    """
    FASE 2: SOLUÇÃO RECURSIVA PURA
    
    Explora a árvore de decisão completa: para cada item, decide entre incluir ou não.
    Sofre de recálculo de subproblemas idênticos.
    
    Complexidade: O(2^N) - Exponencial. Inviável para N grande.
    """
    n = len(projects)

    def solve(i: int, c: int) -> int:
        # Caso base: sem itens ou capacidade esgotada
        if i < 0 or c <= 0:
            return 0
        
        _, value, hours = projects[i]
        
        # Opção 1: Não incluir o item atual
        exclude = solve(i - 1, c)
        
        # Opção 2: Incluir o item (se couber)
        include = 0
        if hours <= c:
            include = value + solve(i - 1, c - hours)
            
        return max(include, exclude)

    max_val = solve(n - 1, capacity)

    # Reconstrução da escolha (necessária pois a função retorna apenas o valor)
    # Nota: Isso reexecuta a lógica recursiva, o que é custoso, mas serve para demonstração.
    chosen = []
    c = capacity
    for i in range(n - 1, -1, -1):
        if solve(i, c) != solve(i - 1, c):
            # Se o valor mudou, significa que o item 'i' foi incluído
            chosen.append(i)
            c -= projects[i][2]
    
    chosen.reverse()
    return max_val, chosen


def memo_knapsack(projects: List[Project], capacity: int) -> Tuple[int, List[int]]:
    """
    FASE 3: PROGRAMAÇÃO DINÂMICA TOP-DOWN (MEMOIZAÇÃO)
    
    Usa recursão, mas armazena os resultados em um dicionário 'memo'.
    Evita recomputar estados (i, c) já visitados.
    
    Complexidade: O(N * C) - Pseudo-polinomial.
    """
    n = len(projects)
    memo = {} # Estrutura de armazenamento exigida

    def solve_memo(i: int, c: int) -> int:
        # Verifica se já calculamos esse estado
        state = (i, c)
        if state in memo:
            return memo[state]
        
        # Caso base
        if i < 0 or c <= 0:
            return 0
        
        _, value, hours = projects[i]
        
        # Lógica de decisão
        exclude = solve_memo(i - 1, c)
        include = 0
        if hours <= c:
            include = value + solve_memo(i - 1, c - hours)
        
        result = max(exclude, include)
        memo[state] = result # Armazena antes de retornar
        return result

    max_val = solve_memo(n - 1, capacity)

    # Reconstrução usando a tabela memo já preenchida
    chosen = []
    c = capacity
    for i in range(n - 1, -1, -1):
        # Se couber e o valor com o item for maior que sem ele...
        # (Aqui usamos a lógica de verificar a transição de estado na memo)
        val_exclude = solve_memo(i - 1, c)
        val_include = -1
        if projects[i][2] <= c:
            val_include = projects[i][1] + solve_memo(i - 1, c - projects[i][2])
            
        if val_include > val_exclude:
            chosen.append(i)
            c -= projects[i][2]
            
    chosen.reverse()
    return max_val, chosen


def dp_knapsack(projects: List[Project], capacity: int) -> Tuple[int, List[int]]:
    """
    FASE 4: PROGRAMAÇÃO DINÂMICA BOTTOM-UP (ITERATIVA)
    
    Constrói uma tabela T[i][c] iterativamente, eliminando a recursão.
    Garante o preenchimento completo da matriz de subproblemas.
    
    Complexidade: O(N * C) Tempo e Espaço.
    """
    n = len(projects)
    # T[i][w] armazena o valor máximo para os primeiros 'i' itens com capacidade 'w'
    T = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, value, hours = projects[i - 1]
        for c in range(capacity + 1):
            if hours > c:
                # Não cabe: valor é o mesmo sem este item
                T[i][c] = T[i - 1][c]
            else:
                # Cabe: max entre não levar vs levar (valor + espaço restante)
                T[i][c] = max(T[i - 1][c], value + T[i - 1][c - hours])

    max_val = T[n][capacity]

    # Reconstrução (Backtracking na tabela T)
    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if T[i][c] != T[i - 1][c]:
            # Item (i-1) foi selecionado
            chosen.append(i - 1)
            c -= projects[i - 1][2]
            
    chosen.reverse()
    return max_val, chosen


# BLOCO DE ANÁLISE TEÓRICA
"""
ANÁLISE DE COMPLEXIDADE E DESEMPENHO:

1. GULOSA (Greedy):
   - Tempo: O(N log N) devido à ordenação dos projetos. O loop é O(N).
   - Espaço: O(N) para armazenar a lista ordenada.
   - Conclusão: É a mais rápida, mas NÃO garante a solução ótima (como demonstrado no Caso de Teste 2).
     Útil apenas quando se aceita uma solução aproximada com extrema velocidade.

2. RECURSIVA PURA:
   - Tempo: O(2^N). A árvore de recursão dobra a cada novo item.
   - Espaço: O(N) (profundidade da pilha de recursão).
   - Conclusão: Ineficiente. Recalcula os mesmos subproblemas (estados i, c) várias vezes. 
     Para 50 projetos, o tempo seria astronômico (trilhões de anos).

3. PD TOP-DOWN (Memoização) e BOTTOM-UP (Iterativa):
   - Tempo: O(N * C). Resolve cada subestado (item, capacidade) apenas uma vez.
   - Espaço: O(N * C) para a tabela/dicionário.
   - Conclusão: Ambas encontram a solução ÓTIMA. A Bottom-Up é geralmente preferida em produção 
     pois evita o overhead de chamadas de função (estouro de pilha), mas a lógica é matematicamente equivalente.
"""

if __name__ == "__main__":
    # CASO 1: Dados do Enunciado
    projects_fiap = [
        ("A", 12, 4),
        ("B", 10, 3),
        ("C", 7, 2),
        ("D", 4, 3),
    ]
    capacity_fiap = 10

    print("--- TESTE 1: DADOS DO ENUNCIADO ---")
    print(f"Projetos: {projects_fiap}")
    print(f"Capacidade: {capacity_fiap}")
    
    # Executa e imprime todas as estratégias
    strategies = [
        ("Greedy (Gulosa)", greedy_knapsack),
        ("Recursiva Pura", recursive_knapsack),
        ("PD Memoization", memo_knapsack),
        ("PD Bottom-Up", dp_knapsack)
    ]
    
    for name, func in strategies:
        val, idxs = func(projects_fiap, capacity_fiap)
        names = [projects_fiap[i][0] for i in idxs]
        print(f"[{name}]: Valor Max={val}, Projetos={names}")
        
    print("\n" + "="*60 + "\n")

    # CASO 2: A Falha do Guloso
    # Exemplo onde V/E (Densidade) engana a estratégia gulosa.
    # Item A: V=60, W=10 (Razão 6.0) -> Guloso pega primeiro
    # Item B: V=100, W=20 (Razão 5.0)
    # Item C: V=120, W=30 (Razão 4.0)
    # Cap=50
    
    tough_projects = [
        ("Proj_X", 60, 10), 
        ("Proj_Y", 100, 20), 
        ("Proj_Z", 120, 30), 
    ]
    tough_capacity = 50
    
    print("--- TESTE 2: ONDE O GULOSO FALHA ---")
    print(f"Projetos: {tough_projects}")
    print(f"Capacidade: {tough_capacity}")
    
    # Comparação Guloso vs PD
    g_val, g_idxs = greedy_knapsack(tough_projects, tough_capacity)
    dp_val, dp_idxs = dp_knapsack(tough_projects, tough_capacity)
    
    print(f"\n[Greedy] Valor={g_val}. Selecionou: {[tough_projects[i][0] for i in g_idxs]}")
    print(f"   -> Razão: O Guloso encheu a mochila com o item de maior densidade (X), sobrando 40h.")
    print(f"   -> Depois pegou Y (20h), sobrando 20h. Z não cabe. Total: 160.")
    
    print(f"\n[DP Ótima] Valor={dp_val}. Selecionou: {[tough_projects[i][0] for i in dp_idxs]}")
    print(f"   -> Razão: A PD percebeu que ignorar o item de maior densidade (X) permitia pegar Y e Z.")
    print(f"   -> Y(20h) + Z(30h) = 50h. Valor 100+120 = 220. Lucro muito maior!")