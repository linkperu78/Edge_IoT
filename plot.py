import time
import matplotlib.pyplot as plt
import mat_function as my_mat

counter = 0
valor = 6400
i = 0
resultados = []
contadores = []

while i < 3000:
    valor= my_mat.function_sube_baja(800, 2300, 10, i, 100, 100)
    resultados.append(valor)
    i += 1
    contadores.append(i)
    #print(f"Iteracion = {i} - Valor = {valor}")

plt.scatter(contadores,resultados)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Gráfico de dispersión')
plt.show()
