import json




class StockInvalidoError(Exception):


    def __init__(self, valor, mensaje=None):
        self.valor = valor
        super().__init__(
            mensaje or f"Stock inválido: {valor!r}. Debe ser un entero mayor o igual a 0."
        )




class DispositivoEcológico:


    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.__stock = 0          
        self.stock = stock        


    # --- Encapsulamiento
    @property
    def stock(self):
        return self.__stock


    @stock.setter
    def stock(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise StockInvalidoError(valor, f"Stock inválido: {valor!r}. Debe ser un entero.")
        if valor < 0:
            raise StockInvalidoError(valor)
        self.__stock = valor


    # --- Polimorfismo
    def ficha_tecnica(self):
        return (
            f"[{self.codigo}] {self.nombre}\n"
            f"  Precio: ${self.precio:,.2f} | Stock: {self.stock} unidades"
        )


    def to_dict(self):
        return {
            "tipo": type(self).__name__,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }




class PanelSolar(DispositivoEcológico):


    def __init__(self, codigo, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(codigo, nombre, precio, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia  


    # Polimorfismo
    def ficha_tecnica(self):
        return (
            f" PANEL SOLAR - {self.nombre} (Cód. {self.codigo})\n"
            f"  Potencia: {self.potencia_w} W | Eficiencia: {self.eficiencia}%\n"
            f"  Precio: ${self.precio:,.2f} | Stock disponible: {self.stock} unidades"
        )


    def to_dict(self):
        datos = super().to_dict()
        datos.update({"potencia_w": self.potencia_w, "eficiencia": self.eficiencia})
        return datos




class GestorInventario:


    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        catalogo = [d.to_dict() for d in lista_dispositivos]
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo, archivo, indent=4, ensure_ascii=False)
        return len(catalogo)




# ---------------- Bloque de prueba ----------------
if __name__ == "__main__":
    gestor = GestorInventario()
    catalogo = []


    # 1) Productos válidos
    catalogo.append(PanelSolar("PS-100", "Panel Monocristalino 450W", 320000, 15, 450, 21.5))
    catalogo.append(PanelSolar("PS-200", "Panel Policristalino 330W", 210000, 40, 330, 17.8))
    catalogo.append(DispositivoEcológico("CB-001", "Controlador de Carga MPPT", 95000, 25))


    # 2) Intento de crear un producto con stock negativo
    try:
        PanelSolar("PS-300", "Panel Defectuoso", 150000, -5, 250, 15.0)
    except StockInvalidoError as e:
        print(f"[ERROR CAPTURADO] No se pudo crear el producto: {e}")


    # 3) Intento de asignar stock negativo a un producto existente
    try:
        catalogo[0].stock = -10
    except StockInvalidoError as e:
        print(f"[ERROR CAPTURADO] Asignación rechazada: {e}")
    print(f"Stock de {catalogo[0].codigo} sin cambios: {catalogo[0].stock}\n")


    # 4) Fichas técnicas (polimorfismo)
    for dispositivo in catalogo:
        print(dispositivo.ficha_tecnica())
        print()


    # 5) Exportación a JSON
    cantidad = gestor.guardar_catalogo_json(catalogo, "catalogo_ecotech.json")
    print(f"Exportación exitosa: {cantidad} productos guardados en catalogo_ecotech.json")
