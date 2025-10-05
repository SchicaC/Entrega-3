import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1200x700')
        self.root.title("Sistema de Gestión - Atletas Unidos")

        # Configurar favicon
        try:
            icon_image = Image.new('RGB', (16, 16), color='blue')
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, icon_photo)
        except:
            pass

        self.notebook = ttk.Notebook(self.root)
        self.tabs = {}

    def setup_ui(self):
        # Crear frames para las pestañas
        self.tabs["competiciones"] = ttk.Frame(self.notebook)
        self.tabs["entrenadores"] = ttk.Frame(self.notebook)
        self.tabs["miembros"] = ttk.Frame(self.notebook)
        self.tabs["entrenamientos"] = ttk.Frame(self.notebook)

        # Añadir pestañas al Notebook
        self.notebook.add(self.tabs["competiciones"], text="🏆 Competiciones")
        self.notebook.add(self.tabs["entrenadores"], text="👨‍🏫 Entrenadores")
        self.notebook.add(self.tabs["miembros"], text="👥 Miembros")
        self.notebook.add(self.tabs["entrenamientos"], text="⚽ Entrenamientos")

        self.notebook.pack(expand=True, fill="both")

        # Frame de información
        self.info_frame = tk.Frame(self.root, bg="#f0f0f0", height=60)
        self.info_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.info_label = tk.Label(self.info_frame,
                                   text="Sistema CRUD - Club Atletas Unidos | Conecte a la base de datos MySQL antes de usar",
                                   font=("Arial", 10), bg="#f0f0f0", fg="#666666")
        self.info_label.pack(pady=20)

    def get_tab(self, tab_name):
        return self.tabs.get(tab_name)

    def update_info_label(self, text, color="#666666"):
        self.info_label.config(text=text, fg=color)

    def set_close_callback(self, callback):
        self.root.protocol("WM_DELETE_WINDOW", callback)

    def mainloop(self):
        self.root.mainloop()