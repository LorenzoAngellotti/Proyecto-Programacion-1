"""
SISTEMA DE RESERVAS DE HOTEL
Alcance: solo reservas en septiembre (30 días).
Anticipación mínima: 7 días.
Se valida restando directamente números de día (sin librerías).
"""
import FunTP1


def main():
    
    TIPOS = ["ESTANDAR", "PREMIUM", "KING"]     
    PISOS = [3, 2, 1]                           
    TARIFAS_BASE = [60000.0, 90000.0, 120000.0] 
    COCHERA_VALOR = 10000.0
    HABITACIONES = 5
    TIPOS_CANT = 3
    DIAS_SEPTIEMBRE = 30
    hoy_dia = 3
    print("===== SISTEMA RESERVA HOTEL (SEPTIEMBRE 2025) =====")
    print("Hoy es 3 de septiembre de 2025 (día fijo = " + str(hoy_dia) + ")")

    Habitaciones = HABITACIONES
    TiposHabitacion = TIPOS_CANT
    ventaXHabitacion = [0] * Habitaciones
    VTAxTIPO = [0] * TiposHabitacion
    m = [[0] * TiposHabitacion for i in range(Habitaciones)]
    disponibilidad = [[[] for i in range(len(TIPOS))] for i in range(HABITACIONES)]

    
    hubo_venta, disponibilidad = FunTP1.cargar_importes(
        m, TIPOS, PISOS, TARIFAS_BASE, COCHERA_VALOR, HABITACIONES, DIAS_SEPTIEMBRE, hoy_dia, disponibilidad
    )
    if not hubo_venta:
        print("No se registraron reservas.")
        return
    print('---ESTADISTICAS---')
    
    print("\n=== (1) Listado matriz ===")
    FunTP1.listado_puntoA(m, Habitaciones, TiposHabitacion)

    
    FunTP1.SumaMatrizxFila(m, ventaXHabitacion, Habitaciones)
    print("\n=== (2) Total por habitación ===")
    for i in range(len(ventaXHabitacion)):
        print("Habitación ".ljust(12) + str(i+1).rjust(2) + ": $" + str(int(ventaXHabitacion[i])).rjust(10))

    
    FunTP1.sumaMatrizXCOL(m, VTAxTIPO, TiposHabitacion, Habitaciones)
    print("\n=== (3) Total por tipo de habitacion ===")
    print("Tipo".ljust(10) + "Total $".rjust(12))
    for i in range(len(VTAxTIPO)):
        tipo_str = str(i+1).rjust(2) + " (" + TIPOS[i].ljust(8) + ")"
        total_str = "$" + str(int(VTAxTIPO[i])).rjust(10)
        print(tipo_str + "\t" + total_str)

    
    ventaMaxima = max(VTAxTIPO)
    print("\n=== (4) Tipo/s de habitacion/es con mayor venta ===")
    print("Mayor venta: $" + str(int(ventaMaxima)).rjust(10))
    mejores_tipos = []
    for i in range(len(VTAxTIPO)):
        if VTAxTIPO[i] == ventaMaxima:
            mejores_tipos.append(i+1)
    print("Tipo/s: " + str(mejores_tipos))

    
    ventaMinima = min(VTAxTIPO)
    print("\n=== (4b) Tipo/s de habitacion/es con menor venta ===")
    print("Menor venta: $" + str(int(ventaMinima)).rjust(10))
    peores_tipos = []
    for i in range(len(VTAxTIPO)):
        if VTAxTIPO[i] == ventaMinima:
            peores_tipos.append(i+1)
    print("Tipo/s: " + str(peores_tipos))

    
    print("\n=== (5) Promedio por habitación por tipo ===")
    print("Tipo".ljust(10) + "Promedio $".rjust(12))
    for i in range(len(VTAxTIPO)):
        prom = VTAxTIPO[i] / HABITACIONES
        tipo_str = str(i+1).rjust(2) + " (" + TIPOS[i].ljust(8) + ")"
        total_str = "$" + str(int(prom)).rjust(10)
        print(tipo_str + "\t" + total_str)

    
    print("\n=== (6) Habitaciones sin reservas por tipo ===")
    for i in range(TiposHabitacion):   
        print(TIPOS[i] + ":")
        sin_reserva = False
        for j in range(Habitaciones):   
            if m[j][i] == 0:        
                print("  Habitación " + str(j+1))
                sin_reserva = True
        if not sin_reserva:         
            print("  Todas las habitaciones reservadas")

    
    total_periodo = FunTP1.sumarMatriz(m, Habitaciones)
    print("\n=== (7) Venta total del período ===")
    print("Total: $" + str(int(total_periodo)).rjust(10))

    
    porc, libres, total = FunTP1.porcentaje_no_reservadas(m, Habitaciones, TiposHabitacion)
    print("\n=== (8) Porcentaje de habitaciones no reservadas ===")
    print(f"Libres: {libres} de {total} ({porc:.2f}%)")

    
    total_reservas = 0
    for i in range(Habitaciones):
        for j in range(TiposHabitacion):
            if m[i][j] > 0:
                total_reservas += 1
    print(f"\n=== (9) Número total de reservas realizadas=== ")
    print(f"Total reservas: {total_reservas}")

    
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


if __name__ == "__main__":

    main()
