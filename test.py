import funciones as d

a = d.id_can_datos
#print(a)

tag = "0x18feee00"

if tag in a:
    value = 10
    objectos = a[tag]
    for objeto in objectos:
        print(value)
        print(objeto.values_to_pub(value))
        value += 10
else:
    print("Tag no reconocido")


