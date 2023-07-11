import time
import random

# Convierte un valor decimal a bytes (hexadecimal) invertido
def num_to_byte(value, n_byte):
    array_byte = list(value.to_bytes(n_byte,'big'))
    array_byte = array_byte[::-1]
    return array_byte


# Devolvemos un PWM con slope y hold
def function_sube_baja(min_value, max_value, change, counter, holding_max, holding_min):
    counter_max_to_min = (max_value-min_value) / change
    periodo = holding_max + holding_min + counter_max_to_min * 2
    wait_rising = holding_min + counter_max_to_min
    wait_falling = wait_rising + holding_max
    pos_x = (counter % periodo)

    if pos_x < wait_rising:
        if pos_x >= holding_min:
            value_return = min_value + change * (pos_x - holding_min)
            value_return = min(value_return, max_value)
        else:
            value_return = min_value
    else:
        if pos_x >= wait_falling:
            value_return = max_value - change * (pos_x - wait_falling)
            value_return = max(value_return, min_value)
        else:
            value_return = max_value
    return int(value_return)


# Valor offset con perturbaciones
def ruido_blanco(value, var):
    #var = int(value *0.05)
    noise = random.randint(-var , var)
    return value + noise

# Valor con solo incremento
def slope_rising(value, slope):
    return value + slope
