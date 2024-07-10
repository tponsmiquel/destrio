import pandas as pd
from model import Model
from view import View
import tkinter as tk

class Controller:
    def __init__(self, root):
        """
        Inicializa la clase Controller, que maneja la interacción entre el modelo y la vista.
        
        Args:
            root (tk.Tk): La ventana principal de Tkinter.
        """
        self.model = Model()  # Inicializa el modelo
        self.view = View(root, self)  # Inicializa la vista y pasa la referencia del controlador

        # Rellena la tabla en la vista con los datos actuales del modelo
        self.view.populate_table(self.model.current_data)

    def get_next_value(self, current_value):
        """
        Determina el próximo valor cíclico para una celda de la tabla.
        
        Args:
            current_value (str): El valor actual de la celda.
        
        Returns:
            str: El siguiente valor en el ciclo ('' -> 'No' -> 'Si' -> '').
        """
        values = ["", "No", "Si"]
        next_index = (values.index(current_value) + 1) % len(values)
        return values[next_index]

    def update_record(self, client, day, value):
        """
        Actualiza el registro de un cliente para un día específico en el modelo y actualiza la vista.
        
        Args:
            client (str): Nombre del cliente.
            day (str): Día de la semana (e.g., 'Lunes').
            value (str): Valor a actualizar ('Si', 'No' o '').
        """
        self.model.update_record(client, day, value)
        # Actualiza la tabla en la vista con los datos actualizados del modelo
        self.view.populate_table(self.model.current_data)

    def save_data(self):
        """
        Guarda los datos actuales del modelo.
        
        Returns:
            bool: True si los datos se guardaron correctamente, False en caso contrario.
        """
        return self.model.save_data()
