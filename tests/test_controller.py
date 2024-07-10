import unittest
import os
from unittest.mock import MagicMock
import pandas as pd
from controller import Controller
from model import Model
from view import View
import tkinter as tk

class TestController(unittest.TestCase):
    def setUp(self):
        """
        Configuración antes de cada prueba.
        Crea un archivo de clientes de prueba y configura el modelo, la vista y el controlador.
        """
        # Crear un archivo de clientes de prueba antes de instanciar el modelo
        self.clients_file = 'clients_test.txt'
        with open(self.clients_file, 'w') as f:
            f.write("Cliente1\nCliente2\nCliente3\n")

        # Configurar el modelo y la vista con mock
        self.root = tk.Tk()
        self.model = Model(clients_file=self.clients_file, data_dir='data_test')
        self.view = View(self.root, self)
        self.controller = Controller(self.root)
        self.controller.model = self.model
        self.controller.view = self.view

    def tearDown(self):
        """
        Limpieza después de cada prueba.
        Elimina los archivos y directorios de prueba.
        """
        # Eliminar archivos de prueba
        if os.path.exists(self.clients_file):
            os.remove(self.clients_file)
        if os.path.exists('data_test'):
            for file in os.listdir('data_test'):
                os.remove(os.path.join('data_test', file))
            os.rmdir('data_test')

    def test_get_next_value(self):
        """
        Prueba la función get_next_value para asegurar que cicla correctamente entre '', 'No' y 'Si'.
        """
        print("Prueba get_next_value: iniciando...")
        self.assertEqual(self.controller.get_next_value(""), "No")
        print("Prueba get_next_value: '' -> 'No' OK")
        self.assertEqual(self.controller.get_next_value("No"), "Si")
        print("Prueba get_next_value: 'No' -> 'Si' OK")
        self.assertEqual(self.controller.get_next_value("Si"), "")
        print("Prueba get_next_value: 'Si' -> '' OK")
        print("Prueba get_next_value: finalizada con éxito")

    def test_update_record(self):
        """
        Prueba la actualización de un registro en el modelo y verifica que el valor se actualiza correctamente.
        """
        print("Prueba update_record: iniciando...")
        self.controller.update_record("Cliente1", "Lunes", "Si")
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente1", "Lunes"].values[0], "Si")
        print("Prueba update_record: Cliente1, Lunes, 'Si' OK")
        print("Prueba update_record: finalizada con éxito")

    def test_save_data(self):
        """
        Prueba la función save_data del controlador para asegurar que se llama al método save_data del modelo.
        """
        print("Prueba save_data: iniciando...")
        self.model.save_data = MagicMock(return_value=True)
        self.assertTrue(self.controller.save_data())
        self.model.save_data.assert_called_once()
        print("Prueba save_data: llamada al método save_data OK")
        print("Prueba save_data: finalizada con éxito")

if __name__ == '__main__':
    unittest.main()
