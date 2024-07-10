import pandas as pd
import os
from datetime import datetime, timedelta

class Model:
    def __init__(self):
        self.clients = self.load_clients()
        self.data_dir = 'data'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.current_data = self.load_current_data()

    def load_clients(self):
        with open('clients.txt', 'r') as file:
            clients = [line.strip() for line in file.readlines()]
        return clients

    def get_week_range(self, date):
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week

    def get_csv_filename(self, start_of_week, end_of_week):
        return f'registro_{start_of_week.strftime("%d_%m_%Y")}_to_{end_of_week.strftime("%d_%m_%Y")}.csv'

    def load_current_data(self):
        today = datetime.today()
        start_of_week, end_of_week = self.get_week_range(today)
        filename = self.get_csv_filename(start_of_week, end_of_week)
        file_path = os.path.join(self.data_dir, filename)
        if os.path.exists(file_path):
            data = pd.read_csv(file_path, index_col=0)
            data = data.astype(str).fillna('')  # Convertir a cadena y reemplazar nulos
            return data
        else:
            # Inicializa con clientes vacíos
            data = pd.DataFrame(self.clients, columns=['Cliente'])
            for day in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
                data[day] = ''
            return data

    def save_data(self):
        today = datetime.today()
        start_of_week, end_of_week = self.get_week_range(today)
        filename = self.get_csv_filename(start_of_week, end_of_week)
        file_path = os.path.join(self.data_dir, filename)
        self.current_data.to_csv(file_path, na_rep='')  # Asegura que los nulos se guarden como vacíos
        return True

    def update_record(self, client, day, value):
        self.current_data.loc[self.current_data['Cliente'] == client, day] = value
