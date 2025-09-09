import random

def cargar_importes(matriz, TIPOS, PISOS, TARIFAS_BASE, COCHERA_VALOR, HABITACIONES, DIAS_SEPTIEMBRE, hoy_dia, disponibilidad):
    """
    Carga reservas en la matriz:
    - Pide tipo (1..3), o -99 para salir.
    - Verifica disponibilidad (máx 5 por tipo).
    - Calcula total (base + cochera) multiplicado por cantidad de días.
    - Asigna en la primera habitación libre.
    """
    hubo_venta = False
    print("\n(Para finalizar, ingrese tipo = -99)")
    tipo = int(input("Tipo de habitación (1=Estandar, 2=Premium, 3=King): "))

    while tipo != -99:
        while tipo < 1 or tipo > 3:
            print("Error: tipo válido 1..3")
            tipo = int(input("Tipo de habitación (1=Estandar, 2=Premium, 3=King): "))

        
        dia_reserva = int(input("Ingrese el día de septiembre para la reserva (1-30): "))
        if dia_reserva < 1 or dia_reserva > DIAS_SEPTIEMBRE:
            print(" Día inválido. Debe estar entre 1 y 30.")
        else:
            dif = dia_reserva - hoy_dia
            if dif < 0:
                print(" Esa fecha ya pasó.")
            elif dif < 7:
                print(" Anticipación insuficiente (" + str(dif) + " días). Se requieren 7 o más.")
            else:
                
                dias_estadia = int(input("¿Cuántos días desea reservar? "))
                if dia_reserva + dias_estadia - 1 > DIAS_SEPTIEMBRE:
                    print(" La estadía se pasa de septiembre. Máximo permitido: " + str(DIAS_SEPTIEMBRE - dia_reserva + 1) + " días")
                else:
                    col = tipo - 1  
                    
                    hab_disponibles = []
                    print("\nEstado de habitaciones para el tipo " + TIPOS[col] + ":")
                    for hab in range(HABITACIONES):
                        ocupada_flag = False
                        for d in range(dia_reserva, dia_reserva + dias_estadia):
                            if d in disponibilidad[hab][col]:  
                                ocupada_flag = True
                        if ocupada_flag == True:
                            estado = "Ocupada"
                        else:
                            estado = "Libre"
                            hab_disponibles.append(hab)
                        print(f"  Habitación {hab+1}: {estado}")


                    if len(hab_disponibles) == 0:
                        print(" No hay habitaciones disponibles para esos días.")
                    else:
                        
                        eleccion = input("Ingrese número de habitación o 'A' para aleatoria: ").strip().upper()
                        if eleccion == 'A':
                            fila_libre = random.choice(hab_disponibles)
                        else:
                            fila_libre = int(eleccion) - 1
                            if fila_libre not in hab_disponibles:
                                print(" Habitación no disponible, se asignará aleatoria")
                                fila_libre = random.choice(hab_disponibles)

                    coch = input("¿Cochera? (SI/NO): ").strip().upper()
                    if coch == "SI":
                        coch_flag = 1
                    else:
                        coch_flag = 0
                    base = TARIFAS_BASE[col]
                    if coch_flag == 1:
                        cochera_costo = COCHERA_VALOR
                    else:
                        cochera_costo = 0
                    total = (base + cochera_costo) * dias_estadia
                    matriz[fila_libre][col] += total  
                    for d in range(dia_reserva, dia_reserva + dias_estadia):
                        disponibilidad[fila_libre][col].append(d)


                    hubo_venta = True
                    print("Por el momento no contamos con cargos extras.")
                    print("Reserva realizada con exito! A continuacion le dejamos los datos de su reserva= " + TIPOS[col] + " (Piso " + str(PISOS[col]) + ") | Hab " + str(fila_libre+1) + " | Día " + str(dia_reserva) + " por " + str(dias_estadia) + " días | Total $" + str(int(total)))

        tipo = int(input("Tipo de habitación (1=Estandar, 2=Premium, 3=King. Para finalizar, ingrese tipo = -99): "))

    return hubo_venta,disponibilidad


def mostrar_matriz(matriz):
    print("\nMatriz (filas=Hab 1..5, cols=Tipos 1..3):")
    for i in range(len(matriz)):  
        print(f"Habitacion {i+1}: {matriz[i]}")


def SumaMatrizxFila(matriz, lista, cantidadFilas):
    for i in range(cantidadFilas):
        lista[i]=sum(matriz[i])


def sumarMatriz(matriz, cantidadFilas):
    resultado = 0
    for f in range(cantidadFilas):
        resultado += sum(matriz[f])
    return resultado



def listado_puntoA(matriz, cantidadfilas, cantidadcolumnas):
    print("\nHABITACION/TIPO \t 01\t\t 02\t\t 03")

    for i in range(cantidadfilas):  
        print(str(i+1).rjust(2), end="\t\t   ")

        for j in range(cantidadcolumnas):  
            print("$" + str(int(matriz[i][j])).rjust(10), end="\t")

        print()  



def sumaMatrizXCOL(matriz, lista, cantidadcolumnas, cantidadfilas):
    for i in range(cantidadcolumnas):
        for j in range(cantidadfilas):
            lista[i]+=matriz[j][i]

def porcentaje_no_reservadas(matriz, cantidadFilas, cantidadColumnas):
    total = cantidadFilas * cantidadColumnas
    libres = 0

    for i in range(cantidadFilas):
        for j in range(cantidadColumnas):
            if matriz[i][j] == 0:
                libres += 1

    porcentaje = (libres / total) * 100

    return porcentaje, libres, total
