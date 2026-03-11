import numpy as np
import matplotlib.pyplot as plt

def wolfram_rule(rule_number):
    """Genera la regla de Wolfram a partir de un número de regla."""
    rule = {}
    for i in range(8):
        rule[tuple(np.array([int(x) for x in np.binary_repr(i, 3)]))] = (rule_number >> i) & 1
    return rule

def evolve_cellular_automaton(rule, initial_state, steps):
    """Evoluciona el autómata celular según la regla de Wolfram."""
    state = initial_state.copy()
    history = [state]
    for _ in range(steps):
        new_state = np.zeros_like(state)
        for i in range(1, len(state) - 1):
            neighborhood = tuple(state[i-1:i+2])
            new_state[i] = rule.get(neighborhood, 0)
        state = new_state
        history.append(state)
    return np.array(history)

def plot_cellular_automaton(history):
    """Grafica la evolución del autómata celular."""
    plt.imshow(history, cmap='binary', interpolation='nearest')
    plt.show()

# Parámetros
rule_number = 90  # Puedes cambiar este número para probar diferentes reglas
initial_state = np.zeros(100, dtype=int)
initial_state[50] = 1  # Inicializa el autómata con una sola celda viva en el centro
steps = 50

# Generar la regla de Wolfram
rule = wolfram_rule(rule_number)

# Evolucionar el autómata
history = evolve_cellular_automaton(rule, initial_state, steps)

# Graficar la evolución
plot_cellular_automaton(history)