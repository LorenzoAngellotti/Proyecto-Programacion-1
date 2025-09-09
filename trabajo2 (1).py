"""
SISTEMA DE RESERVAS DE HOTEL
Alcance: solo reservas en septiembre (30 días).
Anticipación mínima: 7 días.
Se valida restando directamente números de día (sin librerías).
"""
import FunTP

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
    print("Hoy es 3 de septiembre de 2025 (día fijo = " + str(hoy_dia) + ")")

    Vendedor = HABITACIONES
    Sucursal = TIPOS_CANT
    ventaXHabitacion = [0] * Vendedor
    VTAxTIPO = [0] * Sucursal
    m = [[0] * Sucursal for i in range(Vendedor)]

    # --- Carga ---
    hubo_venta = FunTP.cargar_importes(m, TIPOS, PISOS, TARIFAS_BASE, COCHERA_VALOR, HABITACIONES, DIAS_SEPTIEMBRE, hoy_dia)
    if not hubo_venta:
        print("No se registraron reservas.")
        return
    print('---ESTADISTICAS---')
    
    print("\n=== (1) Listado matriz ===")
    FunTP.listado_puntoA(m, Vendedor, Sucursal)

    # --- 2) Total por habitación ---
    FunTP.SumaMatrizxFila(m, ventaXHabitacion, Vendedor)
    print("\n=== (2) Total por habitación ===")
    for i in range(len(ventaXHabitacion)):
        print("Habitación ".ljust(12) + str(i+1).rjust(2) + ": $" + str(int(ventaXHabitacion[i])).rjust(10))


    # --- 3) Total por tipo ---
    FunTP.sumaMatrizXCOL(m, VTAxTIPO, Sucursal, Vendedor)
    print("\n=== (3) Total por tipo ===")
    print("Tipo".ljust(10) + "Total $".rjust(12))
    for i in range(len(VTAxTIPO)):
        tipo_str = str(i+1).rjust(2) + " (" + TIPOS[i].ljust(8) + ")"
        total_str = "$" + str(int(VTAxTIPO[i])).rjust(10)
        print(tipo_str + "\t" + total_str)


    # --- 4) Tipo/s con mayor venta ---
    ventaMaxima = max(VTAxTIPO)
    
    print("\n=== (4) Tipo/s con mayor venta ===")
    print("Mayor venta: $" + str(int(ventaMaxima)).rjust(10))
    mejores_tipos = []
    for i in range(len(VTAxTIPO)):
        if VTAxTIPO[i] == ventaMaxima:
            mejores_tipos.append(i+1)
    print("Tipo/s: " + str(mejores_tipos))


    # --- 4b) Tipo/s con menor venta ---
    ventaMinima = min(VTAxTIPO)
    print("\n=== (4b) Tipo/s con menor venta ===")
    print("Menor venta: $" + str(int(ventaMinima)).rjust(10))

    peores_tipos = []
    for i in range(len(VTAxTIPO)):
        if VTAxTIPO[i] == ventaMinima:
            peores_tipos.append(i+1)

    print("Tipo/s: " + str(peores_tipos))


    # --- 5) Promedio por habitación por tipo ---
    print("\n=== (5) Promedio por habitación por tipo ===")
    print("Tipo".ljust(10) + "Promedio $".rjust(12))

    for i in range(len(VTAxTIPO)):
        prom = VTAxTIPO[i] / HABITACIONES
        tipo_str = str(i+1).rjust(2) + " (" + TIPOS[i].ljust(8) + ")"
        total_str = "$" + str(int(prom)).rjust(10)
        print(tipo_str + "\t" + total_str)


   
    # --- 6) Habitaciones sin reservas por tipo ---
    print("\n=== (6) Habitaciones sin reservas por tipo ===")
    for i in range(Sucursal):   # recorre los tipos de habitación
        print(TIPOS[i] + ":")
        sin_reserva = False

        for j in range(Vendedor):   # recorre las habitaciones de ese tipo
            if m[j][i] == 0:        # si no hay reserva en esa posición
                print("  Habitación " + str(j+1))
                sin_reserva = True

        if not sin_reserva:         # si todas tenían reservas
            print("  Todas las habitaciones reservadas")


    # --- 7) Venta total ---
    total_periodo = FunTP.sumarMatriz(m, Vendedor)
    print("\n=== (7) Venta total del período ===")
    print("Total: $" + str(int(total_periodo)).rjust(10))

    # --- 8) Porcentaje de habitaciones no reservadas ---
    porc, libres, total = FunTP.porcentaje_no_reservadas(m, Vendedor, Sucursal)
    print("\n=== (8) Porcentaje de habitaciones no reservadas ===")
    print(f"Libres: {libres} de {total} ({porc:.2f}%)")

    # --- 9) Número total de reservas ---
    total_reservas = 0
    for i in range(Vendedor):
        for j in range(Sucursal):
            if m[i][j] > 0:
                total_reservas += 1
    print(f"\nNúmero total de reservas realizadas: {total_reservas}")

        # --- 10) Reservas ordenadas por monto ---
    print("\n=== (10) Reservas ordenadas por monto ===")
    reservas = []
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] > 0:
                reservas.append([i+1, TIPOS[j], m[i][j]])

    reservas_ordenadas = sorted(reservas, key=lambda x: x[2], reverse=True)
    for reserva in reservas_ordenadas:
        hab = reserva[0]
        tipo = reserva[1]
        monto = reserva[2]
        print("Hab " + str(hab) + " - " + tipo + ": $" + str(int(monto)))

# Ejecutar
main()










