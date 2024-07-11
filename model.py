import pandas as pd
import os
from datetime import datetime, timedelta

class Model:
    def __init__(self, clients_file='clients.txt', data_dir='data'):
        """
        Inicializa la clase Model.
        
        Args:
            clients_file (str): Nombre del archivo que contiene la lista de clientes.
            data_dir (str): Directorio donde se guardarán los archivos CSV de registros.
        """
        self.clients_file = clients_file
        self.data_dir = data_dir
        # Cargar la lista de clientes desde el archivo
        self.clients = self.load_clients()
        # Crear el directorio de datos si no existe
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        # Cargar los datos actuales
        self.current_data = self.load_current_data()

    def load_clients(self):
        """
        Carga la lista de clientes desde el archivo especificado en clients_file.
        
        Returns:
            list: Una lista de nombres de clientes.
        """
        with open(self.clients_file, 'r') as file:
            clients = [line.strip() for line in file.readlines()]
        return clients

    def get_week_range(self, date):
        """
        Calcula el rango de fechas (inicio y fin) de la semana para una fecha dada.
        
        Args:
            date (datetime): Fecha para la cual calcular el rango de la semana.
        
        Returns:
            tuple: Fecha de inicio y fin de la semana.
        """
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week

    def get_csv_filename(self, start_of_week, end_of_week):
        """
        Genera el nombre del archivo CSV para un rango de fechas dado.
        
        Args:
            start_of_week (datetime): Fecha de inicio de la semana.
            end_of_week (datetime): Fecha de fin de la semana.
        
        Returns:
            str: Nombre del archivo CSV.
        """
        return f'registro_{start_of_week.strftime("%d_%m_%Y")}_to_{end_of_week.strftime("%d_%m_%Y")}.csv'

    def load_current_data(self, date=None):
        """
        Carga los datos actuales para la semana especificada.
        
        Args:
            date (datetime, optional): Fecha para la cual cargar los datos. Por defecto, la fecha actual.
        
        Returns:
            DataFrame: Datos cargados para la semana.
        """
        if date is None:
            date = datetime.today()
        start_of_week, end_of_week = self.get_week_range(date)
        filename = self.get_csv_filename(start_of_week, end_of_week)
        file_path = os.path.join(self.data_dir, filename)

        # Crear un DataFrame con los nombres de los clientes y columnas para cada día de la semana
        data = pd.DataFrame(self.clients, columns=['Cliente'])
        for day in ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']:
            data[day] = ''

        # Si el archivo existe, cargar los datos y combinarlos con el DataFrame de clientes
        if os.path.exists(file_path):
            loaded_data = pd.read_csv(file_path, encoding='utf-8', sep=';')
            loaded_data = loaded_data.astype(str).fillna('')  # Convertir a cadena y reemplazar nulos
            # Asegurarse de mantener todos los clientes y sus datos correspondientes
            data.set_index('Cliente', inplace=True)
            loaded_data.set_index('Cliente', inplace=True)
            data.update(loaded_data)
            data.reset_index(inplace=True)
            data = data.replace('nan', '')  # Reemplaza los valores 'nan' por cadenas vacías

        return data

    def save_data(self):
        """
        Guarda los datos actuales en un archivo CSV.
        
        Returns:
            bool: True si los datos se guardaron correctamente.
        """
        today = datetime.today()
        start_of_week, end_of_week = self.get_week_range(today)
        filename = self.get_csv_filename(start_of_week, end_of_week)
        file_path = os.path.join(self.data_dir, filename)
        self.current_data.replace('nan', '', inplace=True)  # Asegura que los valores 'nan' se reemplacen por cadenas vacías
        self.current_data.to_csv(file_path, na_rep='', index=False, encoding='utf-8', sep=';')  # Asegura que los nulos se guarden como vacíos y especifica el delimitador
        return True

    def update_record(self, client, day, value):
        """
        Actualiza el registro de un cliente para un día específico.
        
        Args:
            client (str): Nombre del cliente.
            day (str): Día de la semana (e.g., 'Lunes').
            value (str): Valor a actualizar ('Si', 'No' o '').
        """
        self.current_data.loc[self.current_data['Cliente'] == client, day] = value
