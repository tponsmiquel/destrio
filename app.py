from controller import Controller
import tkinter as tk

def main():
    """
    Función principal para iniciar la aplicación.
    """
    root = tk.Tk()  # Crea la ventana principal de Tkinter
    root.state('zoomed')  # Iniciar en modo de pantalla completa en Windows
    app = Controller(root)  # Crea una instancia del controlador, que maneja el modelo y la vista
    root.mainloop()  # Inicia el bucle principal de la interfaz gráfica

if __name__ == "__main__":
    main()  # Ejecuta la función principal si este archivo se ejecuta directamente
