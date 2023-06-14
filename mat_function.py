import time
import random

# De un valor numerico %DD retornamos:
# [LB HB]
def num_to_byte(value, n_byte):
    array_byte = list(value.to_bytes(n_byte,'big'))
    array_byte = array_byte[::-1]
    return array_byte

# Devolvemos un PWM con slope y hold
def function_sube_baja(holding, max, min, incremento, valor, counter):
    n_hold  = holding
    max_value = max
    min_value = min

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
                actual_value += incremento
                if actual_value >= max_value:
                    hold_counter = 0
        # Decremento
        if hold_counter < 0:
            if actual_value > min_value:
                actual_value -= incremento
                if actual_value <= min_value:
                    hold_counter = 0
    
    return actual_value, hold_counter


def ruido_blanco(value, var):
    #var = int(value *0.05)
    noise = random.randint(-var , var)
    return value + noise

def slope_rising(value, slope):
    return value + slope