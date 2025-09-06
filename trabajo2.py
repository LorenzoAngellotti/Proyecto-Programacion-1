import random

"""
SISTEMA DE RESERVAS DE HOTEL - VERSIÓN PRINCIPIANTE
Alcance: solo reservas en septiembre (30 días).
Anticipación mínima: 7 días.
Se valida restando directamente números de día (sin librerías).
"""

def main():
    # parametros hotel
    TIPOS = ["ESTANDAR", "PREMIUM", "KING"]     # columnas 0..2
    PISOS = [3, 2, 1]                           # alineado a TIPOS
    TARIFAS_BASE = [60000.0, 90000.0, 120000.0] # base por tipo
    COCHERA_VALOR = 10000.0
    HABITACIONES = 5
    TIPOS_CANT = 3
    DIAS_SEPTIEMBRE = 30
    hoy_dia = 3
    print("===== SISTEMA RESERVA HOTEL (SEPTIEMBRE 2025) =====")
    print(f"Hoy es 3 de septiembre de 2025 (día fijo = {hoy_dia})")

    Vendedor = HABITACIONES
    Sucursal = TIPOS_CANT
    ventaXHabitacion = [0] * Vendedor
    VTAxTIPO = [0] * Sucursal
    m = [[0] * Sucursal for _ in range(Vendedor)]

    # --- Carga ---
    hubo_venta = cargar_importes(m, TIPOS, PISOS, TARIFAS_BASE, COCHERA_VALOR, HABITACIONES, DIAS_SEPTIEMBRE, hoy_dia)
    if not hubo_venta:
        print("No se registraron reservas.")
        return

    # --- 1) Mostrar matriz ---
    mostrar_matriz(m)
    print("\n=== (1) Listado matriz ===")
    listado_puntoA(m, Vendedor, Sucursal)

    # --- 2) Total por habitación ---
    SumaMatrizxFila(m, ventaXHabitacion, Vendedor)
    print("\n=== (2) Total por habitación ===")
    i = 0
    while i < len(ventaXHabitacion):
        print(f"Habitación {i+1}: ${ventaXHabitacion[i]:,.0f}")
        i += 1

    # --- 3) Total por tipo ---
    sumaMatrizXCOL(m, VTAxTIPO, Sucursal, Vendedor)
    print("\n=== (3) Total por tipo ===")
    print("Tipo\tTotal $")
    i = 0
    while i < len(VTAxTIPO):
        print(f"{i+1:>2} ({TIPOS[i]:8s})\t${VTAxTIPO[i]:,.0f}")
        i += 1
    
    tipos_con_totales = [[i, VTAxTIPO[i]] for i in range(len(VTAxTIPO))]
    tipos_con_totales.sort(key=lambda x: x[1], reverse=True)
    print("\n=== Listado de ventas por tipo (mayor a menor) ===")
    print("Tipo\tTotal $")
    for i in range(len(tipos_con_totales)):
        print(f"{TIPOS[tipos_con_totales[i][0]]:8s}\t${tipos_con_totales[i][1]:,.0f}")

    # --- 4) Tipo/s con mayor venta ---
    ventaMaxima = max(VTAxTIPO)
    print("\n=== (4) Tipo/s con mayor venta ===")
    print(f"Mayor venta: ${ventaMaxima:,.0f}")
    mejores_tipos = [i+1 for i in range(len(VTAxTIPO)) if VTAxTIPO[i] == ventaMaxima]
    print("Tipo/s:", mejores_tipos)

    # --- 4b) Tipo/s con menor venta ---
    ventaMinima = min(VTAxTIPO)
    print("\n=== (4b) Tipo/s con menor venta ===")
    print(f"Menor venta: ${ventaMinima:,.0f}")
    peores_tipos = [i+1 for i in range(len(VTAxTIPO)) if VTAxTIPO[i] == ventaMinima]
    print("Tipo/s:", peores_tipos)

    # --- 5) Promedio por habitación por tipo ---
    print("\n=== (5) Promedio por habitación por tipo ===")
    print("Tipo\tPromedio $")
    i = 0
    while i < len(VTAxTIPO):
        prom = VTAxTIPO[i] / HABITACIONES
        print(f"{i+1:>2} ({TIPOS[i]:8s})\t${prom:,.0f}")
        i += 1

    # --- 6) Habitaciones sin reservas en cada tipo ---
    print("\n=== (6) Habitaciones sin reservas por tipo ===")
    i = 0
    while i < Sucursal:
        print(f"{TIPOS[i]}:")
        j = 0
        sin_reserva = False
        while j < Vendedor:
            if m[j][i] == 0:
                print(f"  Habitación {j+1}")
                sin_reserva = True
            j += 1
        if not sin_reserva:
            print("  Todas las habitaciones reservadas")
        i += 1

    # --- 7) Venta total ---
    total_periodo = sumarMatriz(m, Vendedor)
    print("\n=== (7) Venta total del período ===")
    print(f"Total: ${total_periodo:,.0f}")


def cargar_importes(matriz, TIPOS, PISOS, TARIFAS_BASE, COCHERA_VALOR, HABITACIONES, DIAS_SEPTIEMBRE, hoy_dia):
    """
    Carga reservas en la matriz:
    - Pide tipo (1..3), o -99 para salir.
    - Muestra habitaciones libres y permite elegir o asignar aleatoriamente.
    - Calcula total (base + cochera) multiplicado por cantidad de días.
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
                print(f"❌ Anticipación insuficiente ({dif} días). Se requieren 7 o más.")
            else:
                # Preguntar por cantidad de días
                dias_estadia = int(input("¿Cuántos días desea reservar? "))
                if dia_reserva + dias_estadia - 1 > DIAS_SEPTIEMBRE:
                    print(f"❌ La estadía se pasa de septiembre. Máximo permitido: {DIAS_SEPTIEMBRE - dia_reserva + 1} días")
                else:
                    col = tipo - 1
                    # listar habitaciones libres
                    habitaciones_libres = [i for i in range(HABITACIONES) if matriz[i][col] == 0]
                    
                    if not habitaciones_libres:
                        print("⚠️ No hay disponibilidad en este tipo (cupo 5 completo).")
                    else:
                        print(f"Habitaciones libres de {TIPOS[col]}: {[h+1 for h in habitaciones_libres]}")
                        hab_elegida = int(input("Ingrese número de habitación (0 para asignar aleatoriamente): "))
                        if hab_elegida == 0:
                            fila_libre = random.choice(habitaciones_libres)
                        else:
                            fila_libre = hab_elegida - 1
                            if fila_libre not in habitaciones_libres:
                                print("❌ Habitación no disponible, se asignará aleatoriamente.")
                                fila_libre = random.choice(habitaciones_libres)

                        coch = input("¿Cochera? (SI/NO): ").strip().upper()
                        coch_flag = 1 if coch == "SI" else 0
                        base = TARIFAS_BASE[col]
                        cochera_costo = COCHERA_VALOR if coch_flag == 1 else 0
                        total = (base + cochera_costo) * dias_estadia
                        matriz[fila_libre][col] = total
                        hubo_venta = True
                        print(f"✅ {TIPOS[col]} (Piso {PISOS[col]}) | Hab {fila_libre+1} | Día {dia_reserva} por {dias_estadia} días | Total ${total:,.0f}")
                        print("ℹ️ Por el momento no contamos con cargos extras adicionales.")

        tipo = int(input("\nTipo (1..3) o -99 para terminar: "))

    return hubo_venta


def mostrar_matriz(matriz):
    print("\nMatriz (filas=Hab 1..5, cols=Tipos 1..3):")
    i = 0
    while i < len(matriz):
        print(f"Habitación {i+1}: {matriz[i]}")
        i += 1


def SumaMatrizxFila(matriz, lista, cantidadFilas):
    i = 0
    while i < cantidadFilas:
        lista[i] = sum(matriz[i])
        i += 1


def sumarMatriz(matriz, cantidadFilas):
    resultado = 0.0
    f = 0
    while f < cantidadFilas:
        resultado += sum(matriz[f])
        f += 1
    return resultado


def listado_puntoA(matriz, cantidadfilas, cantidadcolumnas):
    print("\nHABITACION/TIPO \t 01\t\t 02\t\t 03")
    i = 0
    while i < cantidadfilas:
        print(i+1, end="\t\t   ")
        j = 0
        while j < cantidadcolumnas:
            print(f"${matriz[i][j]:,.0f}\t", end="")
            j += 1
        print()
        i += 1


def sumaMatrizXCOL(matriz, lista, cantidadcolumnas, cantidadfilas):
    i = 0
    while i < cantidadcolumnas:
        total_col = 0.0
        j = 0
        while j < cantidadfilas:
            total_col += matriz[j][i]
            j += 1
        lista[i] = total_col
        i += 1


# Ejecutar
main()








