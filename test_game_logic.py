import os
import unittest

import funtions


class GameLogicTests(unittest.TestCase):
    def setUp(self):
        self.original_level_file = os.path.join(os.getcwd(), 'niveles.txt')
        with open(self.original_level_file, 'w', encoding='utf-8') as fh:
            fh.write('')
        funtions.colores_secuencia.clear()
        funtions.colores_ingresados.clear()

    def test_consult_level_defaults_to_one_when_file_is_empty(self):
        self.assertEqual(funtions.consultar_nivel(), '1')

    def test_generate_color_creates_sequence_for_current_level(self):
        funtions.generar_colores()
        self.assertEqual(len(funtions.colores_secuencia), 1)
        self.assertTrue(all(numero_color in (1, 2, 3, 4) for numero_color in funtions.colores_secuencia))


if __name__ == '__main__':
    unittest.main()
