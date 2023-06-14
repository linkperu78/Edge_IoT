import time
import matplotlib.pyplot as plt

def actualizar_valor(valor, counter):
    n_hold  = 100
    max_value = 32768
    min_value = 6400

    actual_value = valor
    hold_counter = counter

    if abs(hold_counter) < n_hold:
        if (actual_value < max_value):
            hold_counter += 1
        elif (actual_value > min_value):
            hold_counter -= 1
    if abs(hold_counter) >= n_hold:
        # Incremento
        if hold_counter > 0:
            if actual_value < max_value:
                actual_value += 1000
                if actual_value >= max_value:
                    hold_counter = 0
        # Decremento
        if hold_counter < 0:
            if actual_value > min_value:
                actual_value -= 1000
                if actual_value <= min_value:
                    hold_counter = 0
    
    return actual_value, hold_counter

counter = 0
valor = 6400
i = 0
resultados = []
contadores = []

while i < 3000:
    valor, counter = actualizar_valor(valor, counter)
    resultados.append(valor)
    i += 1
    contadores.append(i)

plt.scatter(contadores,resultados)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gráfico de dispersión')
plt.show()
