import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import pandas as pd
from datetime import datetime

class View:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Destrio")

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.calendar = Calendar(self.calendar_frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.pack(pady=20)

        self.save_button = tk.Button(self.root, text="Guardar", command=self.save_data)
        self.save_button.pack(pady=20)

        self.tree = ttk.Treeview(self.table_frame, columns=('Cliente', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'), show='headings')
        self.tree.heading('Cliente', text='Cliente')
        for day in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
            self.tree.heading(day, text=day)
            self.tree.column(day, width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)

    def populate_table(self, data):
        self.tree.delete(*self.tree.get_children())
        for row in data.itertuples(index=False):
            self.tree.insert("", tk.END, values=[val if val != 'nan' else '' for val in row])

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        col_num = int(col.replace('#', '')) - 1
        client = self.tree.item(item, 'values')[0]
        current_value = self.tree.set(item, column=col_num)
        new_value = self.controller.get_next_value(current_value)
        day = self.tree.heading(col)['text']
        self.controller.update_record(client, day, new_value)
        self.tree.set(item, column=col_num, value=new_value)

    def save_data(self):
        if self.controller.save_data():
            messagebox.showinfo("Éxito", "Los datos se han guardado correctamente.")
        else:
            messagebox.showerror("Error", "Hubo un problema al guardar los datos.")
