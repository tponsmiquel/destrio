from controller import Controller
import tkinter as tk

def main():
    root = tk.Tk()
    root.state('zoomed')  # Iniciar en modo de pantalla completa en Windows
    app = Controller(root)
    root.mainloop()

if __name__ == "__main__":
    main()
