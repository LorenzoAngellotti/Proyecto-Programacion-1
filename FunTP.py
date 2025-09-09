import random

def cargar_importes(matriz, TIPOS, PISOS, TARIFAS_BASE, COCHERA_VALOR, HABITACIONES, DIAS_SEPTIEMBRE, hoy_dia):
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

        # --- Día de reserva ---
        dia_reserva = int(input("Ingrese el día de septiembre para la reserva (1-30): "))
        if dia_reserva < 1 or dia_reserva > DIAS_SEPTIEMBRE:
            print("❌ Día inválido. Debe estar entre 1 y 30.")
        else:
            dif = dia_reserva - hoy_dia
            if dif < 0:
                print("❌ Esa fecha ya pasó.")
            elif dif < 7:
                print("❌ Anticipación insuficiente (" + str(dif) + " días). Se requieren 7 o más.")
            else:
                # Preguntar por cantidad de días
                dias_estadia = int(input("¿Cuántos días desea reservar? "))
                if dia_reserva + dias_estadia - 1 > DIAS_SEPTIEMBRE:
                    print("❌ La estadía se pasa de septiembre. Máximo permitido: " + str(DIAS_SEPTIEMBRE - dia_reserva + 1) + " días")
                else:
                    col = tipo - 1  #-1 para asi ir en 0,1,2 y no en 1,2,3
                    # mostrar habitaciones libres
                    print("Habitaciones disponibles: ")
                    hab_disponibles = []
                    for i in range(HABITACIONES):
                        if matriz[i][col] == 0:
                            hab_disponibles.append(i)
                            print("  Habitación " + str(i+1))


                    # elegir habitación
                    eleccion = input("Ingrese número de habitación o 'A' para aleatoria: ").strip().upper()
                    if eleccion == 'A':
                        fila_libre = random.randint(0, len(hab_disponibles)-1)
                        fila_libre = hab_disponibles[fila_libre]
                    else:
                        fila_libre = int(eleccion) - 1
                        if fila_libre not in hab_disponibles:
                            print("⚠️ Habitación no disponible, se asignará aleatoria")
                            fila_libre = random.randint(0, len(hab_disponibles)-1)
                            fila_libre = hab_disponibles[fila_libre]

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
                    matriz[fila_libre][col] = total
                    hubo_venta = True 
                    print("Reserva realizada con exito!✅ A continuacion le dejamos los datos de su reserva= " + TIPOS[col] + " (Piso " + str(PISOS[col]) + ") | Hab " + str(fila_libre+1) + " | Día " + str(dia_reserva) + " por " + str(dias_estadia) + " días | Total $" + str(int(total)))

        tipo = int(input("\n Si desea continuar con otra reserva seleccione el tipo de habitacion (1/2/3) o -99 para terminar: "))

    return hubo_venta


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

    for i in range(cantidadfilas):  # recorre las filas (habitaciones)
        print(str(i+1).rjust(2), end="\t\t   ")

        for j in range(cantidadcolumnas):  # recorre las columnas (tipos)
            print("$" + str(int(matriz[i][j])).rjust(10), end="\t")

        print()  # salto de línea al terminar cada fila


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
