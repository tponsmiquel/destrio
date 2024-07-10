import unittest
import tkinter as tk
from view import View
from controller import Controller

class TestView(unittest.TestCase):
    def setUp(self):
        """
        Configuración antes de cada prueba.
        Inicializa la ventana principal de Tkinter, el controlador y la vista.
        """
        print("Configuración inicial para la prueba...")
        
        self.root = tk.Tk()
        self.controller = Controller(self.root)
        self.view = View(self.root, self.controller)

    def test_initial_message(self):
        """
        Prueba que se muestra el mensaje inicial al usuario.
        Nota: Los mensajes de tkinter son interactivos y deben ser validados manualmente.
        """
        print("Prueba test_initial_message: iniciando...")
        self.view.show_initial_message()
        # Dado que los mensajes de tkinter son interactivos, los resultados deben ser validados manualmente
        print("Prueba test_initial_message: mostrar el mensaje inicial (validación manual requerida)")

if __name__ == '__main__':
    unittest.main()
