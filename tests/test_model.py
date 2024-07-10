import unittest
import os
import pandas as pd
from datetime import datetime, timedelta
from model import Model

class TestModel(unittest.TestCase):
    def setUp(self):
        print("Configuración inicial para la prueba...")

        # Crear un archivo de clientes de prueba
        self.clients_file = 'clients_test.txt'
        with open(self.clients_file, 'w') as f:
            f.write("Cliente1\nCliente2\nCliente3\n")

        # Crear un directorio de datos de prueba
        self.data_dir = 'data_test'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Modificar el modelo para usar archivos de prueba
        self.model = Model(clients_file=self.clients_file, data_dir=self.data_dir)

    def tearDown(self):
        print("Limpiando archivos de prueba...")
        
        # Eliminar archivos de prueba
        if os.path.exists(self.clients_file):
            os.remove(self.clients_file)
        if os.path.exists(self.data_dir):
            for file in os.listdir(self.data_dir):
                os.remove(os.path.join(self.data_dir, file))
            os.rmdir(self.data_dir)

    def test_load_clients(self):
        print("Prueba test_load_clients: iniciando...")
        clients = self.model.load_clients()
        self.assertEqual(clients, ["Cliente1", "Cliente2", "Cliente3"])
        print("Prueba test_load_clients: finalizada con éxito")

    def test_get_week_range(self):
        print("Prueba test_get_week_range: iniciando...")
        date = datetime(2023, 7, 10)  # Lunes
        start_of_week, end_of_week = self.model.get_week_range(date)
        self.assertEqual(start_of_week, datetime(2023, 7, 10))
        self.assertEqual(end_of_week, datetime(2023, 7, 16))
        print("Prueba test_get_week_range: finalizada con éxito")

    def test_get_csv_filename(self):
        print("Prueba test_get_csv_filename: iniciando...")
        start_of_week = datetime(2023, 7, 10)
        end_of_week = datetime(2023, 7, 16)
        filename = self.model.get_csv_filename(start_of_week, end_of_week)
        self.assertEqual(filename, 'registro_10_07_2023_to_16_07_2023.csv')
        print("Prueba test_get_csv_filename: finalizada con éxito")

    def test_load_current_data(self):
        print("Prueba test_load_current_data: iniciando...")
        data = self.model.load_current_data()
        self.assertEqual(list(data['Cliente']), ["Cliente1", "Cliente2", "Cliente3"])
        self.assertTrue(all(col in data.columns for col in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']))
        print("Prueba test_load_current_data: finalizada con éxito")

    def test_save_and_load_data(self):
        print("Prueba test_save_and_load_data: iniciando...")
        
        # Añadir datos de prueba y guardar
        self.model.update_record("Cliente1", "Lunes", "Si")
        self.model.update_record("Cliente2", "Martes", "No")
        self.model.save_data()

        # Cargar los datos guardados
        loaded_data = self.model.load_current_data()
        self.assertEqual(loaded_data.loc[loaded_data['Cliente'] == "Cliente1", "Lunes"].values[0], "Si")
        self.assertEqual(loaded_data.loc[loaded_data['Cliente'] == "Cliente2", "Martes"].values[0], "No")
        print("Prueba test_save_and_load_data: finalizada con éxito")

    def test_load_data_for_selected_week(self):
        print("Prueba test_load_data_for_selected_week: iniciando...")
        
        # Guardar datos para la semana actual
        self.model.update_record("Cliente1", "Lunes", "Si")
        self.model.update_record("Cliente2", "Martes", "No")
        self.model.save_data()

        # Cambiar a una fecha dentro de 2 meses
        future_date = datetime.today() + timedelta(days=60)
        start_of_week, end_of_week = self.model.get_week_range(future_date)
        future_filename = self.model.get_csv_filename(start_of_week, end_of_week)
        future_file_path = os.path.join(self.data_dir, future_filename)

        # Crear un archivo de prueba para la semana futura con datos diferentes
        future_data = pd.DataFrame({
            'Cliente': ["Cliente1", "Cliente2", "Cliente3"],
            'Lunes': ["No", "", ""],
            'Martes': ["", "Si", ""],
            'Miércoles': ["", "", ""],
            'Jueves': ["", "", ""],
            'Viernes': ["", "", ""],
            'Sábado': ["", "", ""],
            'Domingo': ["", "", ""]
        })
        future_data.to_csv(future_file_path, index=False, na_rep='')

        # Cargar los datos para la semana futura y verificar que se han cargado correctamente
        self.model.current_data = self.model.load_current_data(date=future_date)
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente1", "Lunes"].values[0], "No")
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente2", "Martes"].values[0], "Si")
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente2", "Lunes"].values[0], "")
        print("Prueba test_load_data_for_selected_week: finalizada con éxito")

    def test_update_multiple_records(self):
        """
        Prueba la actualización de múltiples registros en el modelo.
        """
        print("Prueba test_update_multiple_records: iniciando...")
        
        self.model.update_record("Cliente1", "Lunes", "Si")
        self.model.update_record("Cliente1", "Martes", "No")
        self.model.update_record("Cliente2", "Miércoles", "Si")
        self.model.update_record("Cliente2", "Jueves", "No")
        self.model.update_record("Cliente3", "Viernes", "Si")
        self.model.save_data()

        # Verificar que los datos se han actualizado correctamente
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente1", "Lunes"].values[0], "Si")
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente1", "Martes"].values[0], "No")
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente2", "Miércoles"].values[0], "Si")
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente2", "Jueves"].values[0], "No")
        self.assertEqual(self.model.current_data.loc[self.model.current_data['Cliente'] == "Cliente3", "Viernes"].values[0], "Si")
        print("Prueba test_update_multiple_records: finalizada con éxito")

    def test_load_data_for_week_without_records(self):
        """
        Prueba la carga de datos para una semana sin datos guardados.
        """
        print("Prueba test_load_data_for_week_without_records: iniciando...")
        
        # Seleccionar una fecha para la que no hay registros
        future_date = datetime.today() + timedelta(days=60)
        self.model.current_data = self.model.load_current_data(date=future_date)

        # Verificar que los datos se han inicializado correctamente con columnas vacías
        self.assertEqual(list(self.model.current_data['Cliente']), ["Cliente1", "Cliente2", "Cliente3"])
        self.assertTrue(all(col in self.model.current_data.columns for col in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']))
        # Verificar que las celdas están vacías en lugar de nulas
        self.assertTrue((self.model.current_data[['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']] == '').all().all())
        print("Prueba test_load_data_for_week_without_records: finalizada con éxito")

if __name__ == '__main__':
    unittest.main()
