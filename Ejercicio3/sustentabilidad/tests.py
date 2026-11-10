import unittest

# Al estar dentro de la app de Django, usamos el punto (.) 
# para indicar que emisiones.py está en esta misma carpeta.
from .emisiones import calcular_emisiones_carbono


class TestCalculoEmisiones(unittest.TestCase):

    def test_calculo_nominal_con_factor_por_defecto(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(1000), 400.0)

    def test_calculo_con_decimales(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(250.5), 100.2)

    def test_calculo_con_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(500, factor_emision=0.5), 250.0)

    def test_consumo_cero_devuelve_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0)

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-10)

    def test_mensaje_de_error_en_consumo_negativo(self):
        with self.assertRaises(ValueError) as contexto:
            calcular_emisiones_carbono(-0.1)
        self.assertIn("negativo", str(contexto.exception))


if __name__ == "__main__":
    unittest.main()