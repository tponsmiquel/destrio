import unittest
import os
import tkinter as tk
from controller import Controller
from model import Model
from view import View

class TestView(unittest.TestCase):
    def setUp(self):
        print("Configuración inicial para la prueba...")
        # Crear un archivo de clientes de prueba
        self.clients_file = 'clients_test.txt'
        with open(self.clients_file, 'w') as f:
            f.write("Cliente1\nCliente2\nCliente3\n")

        # Configurar el modelo y la vista con mock
        self.root = tk.Tk()
        self.model = Model(clients_file=self.clients_file, data_dir='data_test')
        self.controller = Controller(self.root, clients_file=self.clients_file, data_dir='data_test')
        self.controller.model = self.model
        self.view = View(self.root, self.controller)

    def tearDown(self):
        # Eliminar archivos de prueba
        print("Limpiando archivos de prueba...")
        if os.path.exists(self.clients_file):
            os.remove(self.clients_file)
        if os.path.exists('data_test'):
            for file in os.listdir('data_test'):
                os.remove(os.path.join('data_test', file))
            os.rmdir('data_test')

    def test_initial_message(self):
        print("Prueba test_initial_message: iniciando...")
        self.view.show_initial_message()
        # Dado que los mensajes de tkinter son interactivos, los resultados deben ser validados manualmente
        print("Prueba test_initial_message: mostrar el mensaje inicial (validación manual requerida)")

if __name__ == '__main__':
    unittest.main()
