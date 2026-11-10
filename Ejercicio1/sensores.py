def limpiar_registro_sensor(registro_raw):
    UBICACION_DEFAULT = "Desconocida"

    # 1. Limpiar el identificador.
    sensor_id = str(registro_raw.get("sensor_id", "")).strip()

    # 2. Obtener la temperatura y eliminar el sufijo "C".
    temp_raw = str(registro_raw.get("temperatura", "")).strip().upper()

    for sufijo in ("°C", "C"):
        if temp_raw.endswith(sufijo):
            temp_raw = temp_raw[:-len(sufijo)]
            break

    # Eliminar espacios sobrantes    
    temp_raw = temp_raw.strip().replace(",", ".")
   
    # 3. Convertir la temperatura a float.
    try:
        temperatura = float(temp_raw)
    except ValueError:
        temperatura = None

    # 4. Obtener la ubicación.
    # Si no existe, utilizar "Ubicación desconocida".
    ubicacion = registro_raw.get("ubicacion")
    ubicacion = str(ubicacion).strip() if ubicacion else ""

    if not ubicacion:
        ubicacion = UBICACION_DEFAULT

    # 5. Crear un nuevo diccionario con los datos limpios.
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion
    }

def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    lista_sensores_alerta = []
    suma= 0.0
    cantidad = 0

    for sensor in lista_sensores_limpios:
        temp = sensor["temperatura"]
       
        if temp is None: # Ignora temp invalidas
            continue

        suma += temp
        cantidad += 1

        # Detectar sensores que superen el umbral
        if temp > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    # Calculo el promedio
    promedio_temperatura = suma / cantidad if cantidad > 0 else 0.0

    return (lista_sensores_alerta, promedio_temperatura)


# ==========================================
# Ejecucion
# ==========================================
if __name__ == "__main__":
    registros_crudos = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": " 31.2 C ", "ubicacion": "  Planta Sur "},
        {"sensor_id": "  SENSOR-003", "temperatura": "28°C"},                    
        {"sensor_id": "SENSOR-004 ", "temperatura": "35,8C", "ubicacion": ""},    
        {"sensor_id": "SENSOR-005", "temperatura": "22.0", "ubicacion": "Almacén"},
    ]
    UMBRAL = 30.0

    # Paso 1: Limpieza (¡Ahora sí, todo indentado!)
    registros_limpios = [
        limpiar_registro_sensor(r)
        for r in registros_crudos
    ]

    # Paso 2: Resumen
    alertas, promedio = generar_resumen_sensores(
        registros_limpios,
        UMBRAL
    )

    # Paso 3: Reporte
    print("=" * 75)
    print("           REPORTE TÉRMICO - ECOTECH SOLUTIONS")
    print("=" * 75)

    print(f"{'ID':<15}{'TEMP (°C)':>12}  {'UBICACIÓN':<20}{'ESTADO':<15}")
    print("-" * 75)

    for sensor in registros_limpios:
        temp = sensor["temperatura"]

        # Clasificar estado del sensor
        if temp is None:
            estado = "SIN DATOS"
            temp_formateada = "N/D"
        else:
            temp_formateada = f"{temp:.1f}"

            if temp > UMBRAL:
                estado = "ALERTA"
            elif temp >= 25.0:
                estado = "PRECAUCIÓN"
            else:
                estado = "NORMAL"

        print(
            f"{sensor['sensor_id']:<15}"
            f"{temp_formateada:>12}  "
            f"{sensor['ubicacion']:<20}"
            f"{estado:<15}"
        )

    print("-" * 75)

    print(f"Umbral de alerta: {UMBRAL:.1f} °C")
    print(f"Promedio global: {promedio:.2f} °C")
    print(f"Cantidad de sensores: {len(registros_limpios)}")
    print(f"Sensores con alerta: {len(alertas)}")

    print(
        f"IDs en alerta: {', '.join(alertas) if alertas else 'Ninguno'}"
    )

    print("=" * 75)