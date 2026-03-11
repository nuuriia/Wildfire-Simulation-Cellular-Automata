import numpy as np
import matplotlib.pyplot as plt

def read_idrisi_file(filepath):
    """
    Lee un archivo en formato IDRISI32 y devuelve los datos como un array de NumPy.
    """
    with open(filepath, 'r') as file:
        lines = file.readlines()
        data_start = False
        data = []
        for line in lines:
            if data_start:
                data.append(list(map(float, line.strip().split())))
            if "legend cats" in line.lower():
                data_start = True
        return np.array(data)

def read_initialize_file(filepath):
    """
    Lee un archivo en formato IDRISI32 (como Initialize (1).doc) y devuelve los parámetros necesarios.
    """
    params = {}
    with open(filepath, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.split(':', 1)
                params[key.strip().lower()] = value.strip()
    return params

def generate_layer(rows, cols, min_value, max_value):
    """
    Genera una capa bidimensional con valores aleatorios entre min_value y max_value.
    """
    return np.random.uniform(min_value, max_value, size=(rows, cols))

def read_categorical_layer(filepath):
    """
    Lee un archivo categórico (como Initialize.img) y devuelve una capa numérica basada en las categorías.
    """
    # Mapeo de categorías a valores numéricos
    category_map = {
        "LL": 1.0,  # Bosque (alta propagación)
        "CT": 0.1,  # Ciudad (baja propagación)
        "TE": 0.5,  # Terreno árido (media propagación)
        "GR": 0.7,  # Pastizales (media-alta propagación)
        "CC": 0.3,  # Cultivos (baja propagación)
        "AA": 0.6,  # Arbustos (media propagación)
        "BS": 0.2,  # Suelo desnudo (muy baja propagación)
        "BN": 0.0,  # Agua (sin propagación)
        "BC": 0.4,  # Bosque claro (media propagación)
        "CAT": 0.8  # Categoría especial (alta propagación)
    }

    with open(filepath, 'r') as file:
        lines = file.readlines()
        categorical_layer = []
        for line in lines:
            row = [category_map.get(cell.strip(), 0.0) for cell in line.split()]
            categorical_layer.append(row)
        return np.array(categorical_layer)

def evolve_fire(humidity_layer, fuel_layer, fire_layer, steps):
    """
    Modelo de propagación de incendio forestal con propagación gradual.
    humidity_layer: Capa de humedad (valores entre 0 y 1).
    fuel_layer: Capa de combustible (valores entre 0 y 1).
    fire_layer: Capa inicial del incendio (valores entre 0 y 1).
    steps: Número de pasos de tiempo.
    """
    rows, cols = fire_layer.shape
    history = [fire_layer.copy()]
    intensity_increment = 0.1  # Incremento gradual de la intensidad

    for _ in range(steps):
        new_fire_layer = fire_layer.copy()
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                if fire_layer[i, j] > 0:  # Si ya está en llamas
                    # Incrementar la intensidad gradualmente hasta el máximo
                    new_fire_layer[i, j] = min(1, fire_layer[i, j] + intensity_increment)
                else:
                    # Propagación del fuego basada en humedad y combustible
                    neighbors = fire_layer[i-1:i+2, j-1:j+2]
                    max_neighbor_fire = np.max(neighbors)  # Intensidad máxima de los vecinos
                    prob_fire = fuel_layer[i, j] * (1 - humidity_layer[i, j]) * max_neighbor_fire
                    if prob_fire > 0.01:  # Umbral para propagación
                        new_fire_layer[i, j] = min(1, prob_fire)  # Limitar la intensidad a 1
        fire_layer = new_fire_layer
        history.append(fire_layer.copy())

    return np.array(history)

def plot_fire_propagation(history):
    """
    Grafica la propagación del incendio a lo largo del tiempo.
    """
    rows, cols = history[0].shape
    for t, fire_layer in enumerate(history):
        plt.imshow(fire_layer, cmap='hot', interpolation='nearest', extent=[0, cols, 0, rows])
        plt.title(f"Propagación del Incendio - Paso {t}")
        plt.colorbar(label="Intensidad del Fuego")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

# SESIÓN 1: Implementación de las reglas de Wolfram
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
        new_state = state.copy()
        for i in range(1, len(state) - 1):
            neighborhood = tuple(state[i-1:i+2])  # Vecindario de 3 celdas
            new_state[i] = rule.get(neighborhood, 0)
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

# SESIÓN 1: Ejemplo de uso del autómata celular
rule_number = 30
initial_state = np.zeros(100, dtype=int)
initial_state[50] = 1
steps = 50

rule = wolfram_rule(rule_number)
history = evolve_cellular_automaton(rule, initial_state, steps)
plot_cellular_automaton(history)

# SESIÓN 2: Ejemplo de uso del modelo de incendio
params = read_initialize_file("Initialize (1).doc")
rows = int(params.get('rows', 10))
cols = int(params.get('columns', 10))
humidity_layer = generate_layer(rows, cols, 0, 1)
fuel_layer = generate_layer(rows, cols, 0, 1)
fire_layer = np.zeros((rows, cols))
fire_layer[rows // 2, cols // 2] = 1

categorical_layer = read_categorical_layer("Initialize.img")
fuel_layer *= categorical_layer

history = evolve_fire(humidity_layer, fuel_layer, fire_layer, steps)
plot_fire_propagation(history)