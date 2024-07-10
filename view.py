import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import pandas as pd
from datetime import datetime

class View:
    def __init__(self, root, controller):
        """
        Inicializa la clase View, que maneja la interfaz de usuario.
        
        Args:
            root (tk.Tk): La ventana principal de Tkinter.
            controller: El controlador que maneja la lógica de negocio.
        """
        self.controller = controller
        self.root = root
        self.root.title("Destrio")

        self.current_editable_day = None  # Día de la semana que puede ser editado

        # Crear el marco del calendario
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        # Crear el marco de la tabla
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Crear los widgets de la interfaz
        self.create_widgets()

        # Mostrar mensaje al iniciar la aplicación
        self.root.after(100, self.show_initial_message)

    def create_widgets(self):
        """
        Crea y configura los widgets de la interfaz de usuario.
        """
        # Crear y configurar el calendario
        self.calendar = Calendar(self.calendar_frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.pack(pady=20)
        self.calendar.bind("<<CalendarSelected>>", self.on_calendar_select)

        # Crear el botón de guardar
        self.save_button = tk.Button(self.root, text="Guardar", command=self.save_data)
        self.save_button.pack(pady=20)

        # Añadir barras de desplazamiento
        self.tree_scroll_y = tk.Scrollbar(self.table_frame, orient=tk.VERTICAL)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_scroll_x = tk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Crear y configurar la tabla
        self.tree = ttk.Treeview(self.table_frame, columns=('Cliente', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'), show='headings', yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        self.tree.heading('Cliente', text='Cliente')
        for day in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
            self.tree.heading(day, text=day)
            self.tree.column(day, width=100, anchor='center')

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Configurar las barras de desplazamiento
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # Vincular el doble clic en la tabla a un método
        self.tree.bind("<Double-1>", self.on_double_click)

    def show_initial_message(self):
        """
        Muestra un mensaje al usuario al iniciar la aplicación para que seleccione un día en el calendario.
        """
        messagebox.showinfo("Selección de Fecha", "Por favor, seleccione un día en el calendario para editar.")

    def on_calendar_select(self, event):
        """
        Maneja la selección de una fecha en el calendario.
        
        Args:
            event: El evento generado por la selección en el calendario.
        """
        selected_date = self.calendar.get_date()
        day_of_week = datetime.strptime(selected_date, "%m/%d/%y").strftime("%A")
        day_map = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        self.current_editable_day = day_map.get(day_of_week)
        messagebox.showinfo("Día Seleccionado", f"Solo se puede editar la columna: {self.current_editable_day}")

    def populate_table(self, data):
        """
        Rellena la tabla con los datos proporcionados.
        
        Args:
            data (DataFrame): Los datos a mostrar en la tabla.
        """
        self.tree.delete(*self.tree.get_children())
        for row in data.itertuples(index=False):
            self.tree.insert("", tk.END, values=[val if val != 'nan' else '' for val in row])

    def on_double_click(self, event):
        """
        Maneja el evento de doble clic en la tabla para editar una celda.
        
        Args:
            event: El evento generado por el doble clic.
        """
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        col_num = int(col.replace('#', '')) - 1
        client = self.tree.item(item, 'values')[0]
        current_value = self.tree.set(item, column=col_num)
        day = self.tree.heading(col)['text']
        if day != self.current_editable_day:
            messagebox.showerror("Error", f"Solo se puede editar la columna: {self.current_editable_day}")
            return
        new_value = self.controller.get_next_value(current_value)
        self.controller.update_record(client, day, new_value)
        self.tree.set(item, column=col_num, value=new_value)

    def save_data(self):
        """
        Guarda los datos y muestra un mensaje de éxito o error.
        """
        if self.controller.save_data():
            messagebox.showinfo("Éxito", "Los datos se han guardado correctamente.")
        else:
            messagebox.showerror("Error", "Hubo un problema al guardar los datos.")
