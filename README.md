# 🚀 Global Solution 2025 – O Futuro do Trabalho: Otimização de Portfólio

**Disciplina:** Dynamic Programming  
**Professor:** Marcelo Amorim  
**Curso:** Engenharia de Software (FIAP)

## 👥 Integrantes
* **Nickolas Moreno Cardoso** – RM557132
* **Mateus dos Santos da Silva** – RM558436
* **André Giovanne de Maria** – RM556384

---

## 📋 Sobre o Projeto
Este projeto foi desenvolvido como parte da **Global Solution FIAP 2025**, com o tema *"O Futuro do Trabalho"*.

O objetivo é resolver o problema de **Otimização de Portfólio de Projetos**, onde uma empresa de consultoria precisa selecionar o melhor conjunto de projetos para maximizar o lucro/impacto, respeitando um limite rígido de **Horas-Especialista** disponíveis.

Algoritmicamente, este desafio é uma aplicação direta do **Problema da Mochila 0/1 (0/1 Knapsack Problem)**.

---

## 🛠️ Estratégias Implementadas

O código fonte (`main.py`) contém as quatro abordagens exigidas no enunciado:

### 1. Fase 1: Estratégia Gulosa (Greedy)
* **Lógica:** Prioriza os projetos com a maior densidade de valor (Razão `Valor ÷ Horas`).
* **Resultado:** É extremamente rápida, mas **não garante a solução ótima**, pois pode deixar espaços vazios na capacidade total que poderiam ser melhor preenchidos.

### 2. Fase 2: Solução Recursiva Pura
* **Lógica:** Explora a árvore de decisão completa ("levar" ou "não levar" o item).
* **Resultado:** Encontra a solução ótima, mas é computacionalmente inviável para muitos projetos devido à complexidade exponencial.

### 3. Fase 3: PD Top-Down (Memoização)
* **Lógica:** Utiliza a recursão, mas armazena os resultados dos subproblemas (estado `i, capacidade`) em um dicionário.
* **Resultado:** Encontra a solução ótima de forma eficiente, evitando recálculos.

### 4. Fase 4: PD Bottom-Up (Iterativa)
* **Lógica:** Elimina a recursão construindo uma tabela (matriz) de baixo para cima.
* **Resultado:** É a solução mais robusta para ambientes de produção, garantindo a solução ótima sem risco de estouro de pilha (Stack Overflow).

---

## 📊 Análise de Complexidade Teórica

| Estratégia | Complexidade de Tempo | Complexidade de Espaço | Garante o Ótimo? |
| :--- | :--- | :--- | :--- |
| **Greedy** | $O(N \log N)$ | $O(N)$ | ❌ Não |
| **Recursiva** | $O(2^N)$ | $O(N)$ (pilha) | ✅ Sim |
| **Memoização** | $O(N \cdot C)$ | $O(N \cdot C)$ | ✅ Sim |
| **Bottom-Up** | $O(N \cdot C)$ | $O(N \cdot C)$ | ✅ Sim |

> *Onde $N$ é o número de projetos e $C$ é a capacidade total de horas.*

---

## 💻 Como Executar

### Pré-requisitos
* Python 3.x instalado.
* Nenhuma biblioteca externa é necessária (apenas bibliotecas padrão: `sys`, `typing`).

### Passo a Passo
1.  Clone este repositório.
2.  Navegue até a pasta do projeto no terminal.
3.  Execute o arquivo principal:

```bash
python main.py
