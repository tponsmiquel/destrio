import pandas as pd
from model import Model
from view import View
import tkinter as tk

class Controller:
    def __init__(self, root):
        self.model = Model()
        self.view = View(root, self)

        self.view.populate_table(self.model.current_data)

    def get_next_value(self, current_value):
        values = ["", "No", "Si"]
        next_index = (values.index(current_value) + 1) % len(values)
        return values[next_index]

    def update_record(self, client, day, value):
        self.model.update_record(client, day, value)
        self.view.populate_table(self.model.current_data)

    def save_data(self):
        return self.model.save_data()
