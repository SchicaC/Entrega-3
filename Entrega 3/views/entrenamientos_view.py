import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class EntrenamientosView:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.titulo = tk.Label(self.left_frame, text="⚽ GESTIÓN DE ENTRENAMIENTOS",
                               font=("Arial", 16, "bold"), fg="purple")
        self.titulo.pack(pady=10)

        self.form_frame = tk.Frame(self.left_frame)
        self.form_frame.pack(pady=10, anchor="w", padx=30)

        self.create_form_fields()
        self.create_image_section()
        self.create_buttons()

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.create_toolbar()
        self.create_treeview()

    def create_form_fields(self):
        # ID y Buscar
        tk.Label(self.form_frame, text="ID Entrenamiento:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", padx=(0, 5), pady=5)
        self.IDEntrenamientos = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.IDEntrenamientos.grid(row=0, column=1, sticky="w", pady=5)

        self.btn_buscar = tk.Button(self.form_frame, text="🔍 Buscar", font=("Arial", 10),
                                    bg="#FFA500", fg="white", width=10)
        self.btn_buscar.grid(row=0, column=2, padx=10, pady=5)

        # Primera columna
        tk.Label(self.form_frame, text="Código:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Codigo = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Codigo.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Equipo/Grupo:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", padx=(0, 5), pady=5)
        self.EquipoOGrupo = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.EquipoOGrupo.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Fecha:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Fecha = DateEntry(self.form_frame, width=18, date_pattern='yyyy-mm-dd')
        self.Fecha.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Horario:", font=("Arial", 10)).grid(
            row=4, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Horario = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Horario.grid(row=4, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Instalación:", font=("Arial", 10)).grid(
            row=5, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Instalacion = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Instalacion.grid(row=5, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Entrenador:", font=("Arial", 10)).grid(
            row=6, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Entrenador = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Entrenador.grid(row=6, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Objetivos:", font=("Arial", 10)).grid(
            row=7, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Objetivos = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Objetivos.grid(row=7, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Actividad Programada:", font=("Arial", 10)).grid(
            row=8, column=0, sticky="w", padx=(0, 5), pady=5)
        self.ActividadProgramada = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.ActividadProgramada.grid(row=8, column=1, sticky="w", pady=5)

        # Segunda columna
        tk.Label(self.form_frame, text="Asistentes:", font=("Arial", 10)).grid(
            row=0, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Asistentes = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Asistentes.grid(row=0, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Observaciones:", font=("Arial", 10)).grid(
            row=1, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Observaciones = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Observaciones.grid(row=1, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Evaluación Cumplimiento:", font=("Arial", 10)).grid(
            row=2, column=3, sticky="w", padx=(50, 5), pady=5)
        self.EvaluacionCumplimiento = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.EvaluacionCumplimiento.grid(row=2, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Asistencia Promedio:", font=("Arial", 10)).grid(
            row=3, column=3, sticky="w", padx=(50, 5), pady=5)
        self.AsistenciaPromedio = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.AsistenciaPromedio.grid(row=3, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Disciplina:", font=("Arial", 10)).grid(
            row=4, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Disciplina = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Disciplina.grid(row=4, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Categoría:", font=("Arial", 10)).grid(
            row=5, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Categoria = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Categoria.grid(row=5, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="ID Equipos:", font=("Arial", 10)).grid(
            row=6, column=3, sticky="w", padx=(50, 5), pady=5)
        self.IDEquipos = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.IDEquipos.grid(row=6, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="ID Entrenadores:", font=("Arial", 10)).grid(
            row=7, column=3, sticky="w", padx=(50, 5), pady=5)
        self.IDEntrenadores = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.IDEntrenadores.grid(row=7, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="ID Instalaciones:", font=("Arial", 10)).grid(
            row=8, column=3, sticky="w", padx=(50, 5), pady=5)
        self.IDInstalaciones = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.IDInstalaciones.grid(row=8, column=4, sticky="w", pady=5)

    def create_image_section(self):
        self.image_frame = tk.LabelFrame(self.left_frame, text="🖼️ Imagen del Entrenamiento", font=("Arial", 10))
        self.image_frame.pack(pady=10, padx=30, fill="x")

        self.image_container = tk.Frame(self.image_frame, width=200, height=150, bg="lightgray")
        self.image_container.pack(pady=5)
        self.image_container.pack_propagate(False)

        self.image_label = tk.Label(self.image_container, text="Sin imagen", bg="lightgray")
        self.image_label.pack(expand=True, fill="both")

        self.image_buttons = tk.Frame(self.image_frame)
        self.image_buttons.pack(pady=5)

        self.btn_cargar_imagen = tk.Button(self.image_buttons, text="📁 Cargar Imagen", width=15)
        self.btn_cargar_imagen.pack(side="left", padx=2)

        self.btn_blur = tk.Button(self.image_buttons, text="🔄 Blur", width=8)
        self.btn_blur.pack(side="left", padx=2)

        self.btn_enfocar = tk.Button(self.image_buttons, text="🔍 Enfocar", width=8)
        self.btn_enfocar.pack(side="left", padx=2)

    def create_buttons(self):
        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(pady=15)

        self.btn_guardar = tk.Button(self.button_frame, text="💾 Guardar", font=("Arial", 12),
                                     bg="#4CAF50", fg="white", width=12)
        self.btn_guardar.pack(side=tk.LEFT, padx=5)

        self.btn_actualizar = tk.Button(self.button_frame, text="✏️ Actualizar", font=("Arial", 12),
                                        bg="#2196F3", fg="white", width=12)
        self.btn_actualizar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = tk.Button(self.button_frame, text="🗑️ Eliminar", font=("Arial", 12),
                                      bg="#f44336", fg="white", width=12)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        self.btn_limpiar = tk.Button(self.button_frame, text="🧹 Limpiar", font=("Arial", 12),
                                     bg="#FF9800", fg="white", width=12)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.toolbar.pack(fill="x", pady=5)

        tk.Label(self.toolbar, text="LISTA DE ENTRENAMIENTOS", font=("Arial", 14, "bold")).pack(side="left", padx=10)

        self.btn_export_excel = tk.Button(self.toolbar, text="📊 Exportar Excel", bg="#4CAF50", fg="white")
        self.btn_export_excel.pack(side="right", padx=2)

        self.btn_export_pdf = tk.Button(self.toolbar, text="📄 Exportar PDF", bg="#2196F3", fg="white")
        self.btn_export_pdf.pack(side="right", padx=2)

        self.btn_filtros = tk.Button(self.toolbar, text="🔧 Filtros", bg="#FF9800", fg="white")
        self.btn_filtros.pack(side="right", padx=2)

    def create_treeview(self):
        self.treeview = ttk.Treeview(self.right_frame,
                                     columns=('ID', 'Codigo', 'EquipoOGrupo', 'Fecha', 'Horario', 'Instalacion',
                                              'Entrenador', 'Objetivos', 'ActividadProgramada', 'Asistentes',
                                              'Observaciones', 'EvaluacionCumplimiento', 'AsistenciaPromedio',
                                              'Disciplina', 'Categoria', 'IDEquipos', 'IDEntrenadores',
                                              'IDInstalaciones'), show='headings', height=20)

        columns_config = [
            ('ID', 50), ('Codigo', 80), ('EquipoOGrupo', 100), ('Fecha', 80),
            ('Horario', 80), ('Instalacion', 100), ('Entrenador', 100),
            ('Objetivos', 100), ('ActividadProgramada', 120), ('Asistentes', 80),
            ('Observaciones', 100), ('EvaluacionCumplimiento', 120), ('AsistenciaPromedio', 100),
            ('Disciplina', 80), ('Categoria', 80), ('IDEquipos', 80),
            ('IDEntrenadores', 100), ('IDInstalaciones', 100)
        ]

        for col, width in columns_config:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=width)

        self.treeview.pack(fill="both", expand=True, padx=10, pady=10)

        self.scrollbar_vertical = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar_vertical.set)
        self.scrollbar_vertical.pack(side="left", fill="y")

        self.scrollbar_horizontal = ttk.Scrollbar(self.right_frame, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=self.scrollbar_horizontal.set)
        self.scrollbar_horizontal.pack(side="bottom", fill="x")

        self.btn_cargar_lista = tk.Button(self.right_frame, text="🔄 Cargar Lista", font=("Arial", 10),
                                          bg="#2196F3", fg="white")
        self.btn_cargar_lista.pack(pady=5)