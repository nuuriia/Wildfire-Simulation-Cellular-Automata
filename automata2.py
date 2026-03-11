import numpy as np
import matplotlib.pyplot as plt

def wolfram_rule(rule_number):
    """
    Genera la regla de Wolfram a partir de un número de regla.
    La regla se define como un diccionario que mapea cada posible vecindario (tupla de 3 bits) a un nuevo estado.
    """
    rule = {}
    for i in range(8):  # Hay 8 posibles combinaciones de 3 bits (2^3)
        binary = np.binary_repr(i, width=3)  # Representación binaria de 3 bits
        neighborhood = tuple(map(int, list(binary)))  # Vecindario como tupla de enteros
        new_state = (rule_number >> i) & 1  # Estado nuevo según la regla
        rule[neighborhood] = new_state
    return rule

def evolve_cellular_automaton(rule, initial_state, steps):
    """
    Evoluciona el autómata celular según la regla de Wolfram.
    """
    state = initial_state.copy()
    history = [state]  # Guarda la historia de estados para visualización
    for _ in range(steps):
        new_state = np.zeros_like(state)
        for i in range(1, len(state) - 1):  # Ignora los bordes
            neighborhood = tuple(state[i-1:i+2])  # Vecindario de 3 celdas
            new_state[i] = rule.get(neighborhood, 0)  # Aplica la regla
        state = new_state
        history.append(state)
    return np.array(history)

def plot_cellular_automaton(history):
    """
    Grafica la evolución del autómata celular.
    """
    plt.imshow(history, cmap='binary', interpolation='nearest')
    plt.title("Evolución del Autómata Celular")
    plt.xlabel("Celdas")
    plt.ylabel("Pasos de Tiempo")
    plt.show()

def combine_rules(rule1, rule2, weight=0.5):
    """
    Combina dos reglas de Wolfram en una sola regla.
    weight: Peso para la combinación (0.5 significa igual contribución de ambas reglas).
    """
    combined_rule = {}
    for neighborhood in rule1.keys():
        # Combina los estados de ambas reglas usando el peso
        combined_state = int((weight * rule1[neighborhood] + (1 - weight) * rule2[neighborhood]) > 0.5)
        combined_rule[neighborhood] = combined_state
    return combined_rule

# Parámetros
rule_number1 = 30  # Primera regla de Wolfram
rule_number2 = 110  # Segunda regla de Wolfram
initial_state = np.zeros(100, dtype=int)
initial_state[50] = 1  # Inicializa el autómata con una sola celda viva en el centro
steps = 50  # Número de pasos de tiempo

# Generar las reglas de Wolfram
rule1 = wolfram_rule(rule_number1)
rule2 = wolfram_rule(rule_number2)

# Combinar las reglas
combined_rule = combine_rules(rule1, rule2, weight=0.5)

# Evolucionar el autómata con la regla combinada
history = evolve_cellular_automaton(combined_rule, initial_state, steps)

# Graficar la evolución
plot_cellular_automaton(history)

def multilayer_automaton(rules, initial_states, steps):
    """
    Evoluciona un autómata multicapa donde cada capa tiene su propia regla.
    rules: Lista de reglas (una por capa).
    initial_states: Lista de estados iniciales (uno por capa).
    steps: Número de pasos de tiempo.
    """
    layers = [state.copy() for state in initial_states]
    history = [np.stack(layers, axis=0)]  # Guarda la historia de todas las capas
    for _ in range(steps):
        new_layers = []
        for layer, rule in zip(layers, rules):
            new_layer = np.zeros_like(layer)
            for i in range(1, len(layer) - 1):
                neighborhood = tuple(layer[i-1:i+2])
                new_layer[i] = rule.get(neighborhood, 0)
            new_layers.append(new_layer)
        layers = new_layers
        history.append(np.stack(layers, axis=0))
    return np.array(history)

def multilayer_automaton_interactive(rules, initial_states, steps):
    """
    Evoluciona un autómata multicapa donde las capas interactúan entre sí.
    rules: Lista de reglas (una por capa).
    initial_states: Lista de estados iniciales (uno por capa).
    steps: Número de pasos de tiempo.
    """
    layers = [state.copy() for state in initial_states]
    history = [np.stack(layers, axis=0)]  # Guarda la historia de todas las capas

    for _ in range(steps):
        new_layers = []
        for idx, (layer, rule) in enumerate(zip(layers, rules)):
            new_layer = np.zeros_like(layer)
            for i in range(1, len(layer) - 1):
                # Vecindario de la capa actual
                neighborhood = tuple(layer[i-1:i+2])
                # Interacción con capas vecinas (si existen)
                if idx > 0:  # Capa superior
                    neighborhood = tuple(np.bitwise_or(neighborhood, layers[idx-1][i-1:i+2]))
                if idx < len(layers) - 1:  # Capa inferior
                    neighborhood = tuple(np.bitwise_or(neighborhood, layers[idx+1][i-1:i+2]))
                # Aplica la regla
                new_layer[i] = rule.get(neighborhood, 0)
            new_layers.append(new_layer)
        layers = new_layers
        history.append(np.stack(layers, axis=0))
    
    return np.array(history)

def multilayer_automaton_combined(rules_list, initial_states, steps, weights_list):
    """
    Evoluciona un autómata multicapa donde cada capa puede combinar múltiples reglas.
    rules_list: Lista de listas de reglas (cada sublista contiene las reglas a combinar para una capa).
    initial_states: Lista de estados iniciales (uno por capa).
    steps: Número de pasos de tiempo.
    weights_list: Lista de listas de pesos para combinar las reglas de cada capa.
    """
    # Generar reglas combinadas para cada capa
    combined_rules = [
        combine_rules(*rules, weight=weights[0]) if len(rules) == 2 else rules[0]
        for rules, weights in zip(rules_list, weights_list)
    ]

    layers = [state.copy() for state in initial_states]
    history = [np.stack(layers, axis=0)]  # Guarda la historia de todas las capas

    for _ in range(steps):
        new_layers = []
        for idx, (layer, rule) in enumerate(zip(layers, combined_rules)):
            new_layer = np.zeros_like(layer)
            for i in range(1, len(layer) - 1):
                # Vecindario de la capa actual
                neighborhood = tuple(layer[i-1:i+2])
                # Aplica la regla combinada
                new_layer[i] = rule.get(neighborhood, 0)
            new_layers.append(new_layer)
        layers = new_layers
        history.append(np.stack(layers, axis=0))
    
    return np.array(history)

# Ejemplo de uso con dos capas
rules = [rule1, rule2]
initial_states = [initial_state, initial_state]
history = multilayer_automaton(rules, initial_states, steps)

# Graficar la evolución de cada capa
for i, layer_history in enumerate(history.transpose(1, 0, 2)):
    plt.imshow(layer_history, cmap='binary', interpolation='nearest')
    plt.title(f"Capa {i + 1}")
    plt.show()

# Reglas para cada capa
rules_list = [[rule1, rule2], [rule2, rule1]]  # Cada capa combina dos reglas
weights_list = [[0.7, 0.3], [0.5, 0.5]]  # Pesos para combinar las reglas de cada capa

# Estados iniciales para cada capa
initial_states = [initial_state, initial_state]

# Evolucionar el autómata multicapa con reglas combinadas
history = multilayer_automaton_combined(rules_list, initial_states, steps, weights_list)

# Graficar la evolución combinada de todas las capas
combined_history = np.sum(history, axis=1)  # Suma las capas
plt.imshow(combined_history, cmap='binary', interpolation='nearest')
plt.title("Evolución del Autómata Multicapa con Reglas Combinadas")
plt.xlabel("Celdas")
plt.ylabel("Pasos de Tiempo")
plt.show()