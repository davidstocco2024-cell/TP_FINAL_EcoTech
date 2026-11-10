

def calcular_emisiones_carbono(consumo_kwh: float, factor_emision: float = 0.4) -> float:
    """Devuelve las emisiones (kg CO2) = consumo_kwh * factor_emision."""
    if consumo_kwh < 0:
        raise ValueError("El consumo no puede ser negativo.")
    return consumo_kwh * factor_emision




def obtener_metricas_consumo(registros: dict[str, list[float | int]]) -> dict:
   
    total_emisiones = 0.0
    emisiones_por_planta: dict[str, float] = {}
    consumo_por_planta: dict[str, float] = {}


    for planta, consumos in registros.items():
        consumo_total = sum(consumos)
        consumo_por_planta[planta] = consumo_total


        emisiones_planta = sum(calcular_emisiones_carbono(c) for c in consumos)
        emisiones_por_planta[planta] = emisiones_planta
        total_emisiones += emisiones_planta


    if consumo_por_planta:
       
        planta_mayor = max(consumo_por_planta, key=lambda k: consumo_por_planta[k])
        consumo_mayor = consumo_por_planta[planta_mayor]
    else:  # sin registros
        planta_mayor, consumo_mayor = None, 0.0


    return {
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": planta_mayor,
        "consumo_mayor_kwh": consumo_mayor,
        "emisiones_por_planta": emisiones_por_planta,
    }
