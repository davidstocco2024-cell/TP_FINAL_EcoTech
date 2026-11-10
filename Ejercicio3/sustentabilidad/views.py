from django.shortcuts import render


from .emisiones import obtener_metricas_consumo




def vista_panel_sustentabilidad(request):
   
    registros = {
        "Planta Norte": [1200.0, 1350.0, 1100.0],
        "Planta Sur": [900.0, 950.0, 1000.0],
        "Planta Este": [1500.0, 1600.0, 1450.0],
    }


    metricas = obtener_metricas_consumo(registros)


    contexto = {
        "titulo": "Panel de Sustentabilidad - EcoTech Solutions",
        "total_emisiones": round(metricas["total_emisiones"], 2),
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "consumo_mayor_kwh": metricas["consumo_mayor_kwh"],
        "emisiones_por_planta": metricas["emisiones_por_planta"],
    }
    return render(request, "sustentabilidad/panel.html", contexto)
