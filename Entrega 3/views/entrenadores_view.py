import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class EntrenadoresView:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True)

        # Frame izquierdo para formulario
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Título
        self.titulo = tk.Label(self.left_frame, text="👨‍🏫 GESTIÓN DE ENTRENADORES",
                               font=("Arial", 16, "bold"), fg="green")
        self.titulo.pack(pady=10)

        # Frame del formulario
        self.form_frame = tk.Frame(self.left_frame)
        self.form_frame.pack(pady=10, anchor="w", padx=30)

        self.create_form_fields()
        self.create_image_section()
        self.create_buttons()

        # Frame derecho para lista
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.create_toolbar()
        self.create_treeview()

    def create_form_fields(self):
        # ID y Buscar
        tk.Label(self.form_frame, text="ID Entrenador:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", padx=(0, 5), pady=5)
        self.IDEntrenadores = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.IDEntrenadores.grid(row=0, column=1, sticky="w", pady=5)

        self.btn_buscar = tk.Button(self.form_frame, text="🔍 Buscar", font=("Arial", 10),
                                    bg="#FFA500", fg="white", width=10)
        self.btn_buscar.grid(row=0, column=2, padx=10, pady=5)

        # Primera columna
        tk.Label(self.form_frame, text="Código Empleado:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", padx=(0, 5), pady=5)
        self.CodigoEmpleado = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.CodigoEmpleado.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Nombres:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Nombres = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Nombres.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Apellidos:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Apellidos = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Apellidos.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Doc. Identidad:", font=("Arial", 10)).grid(
            row=4, column=0, sticky="w", padx=(0, 5), pady=5)
        self.DocumentoIdentidad = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.DocumentoIdentidad.grid(row=4, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Fecha Nacimiento:", font=("Arial", 10)).grid(
            row=5, column=0, sticky="w", padx=(0, 5), pady=5)
        self.FechaNacimiento = DateEntry(self.form_frame, width=18, date_pattern='yyyy-mm-dd')
        self.FechaNacimiento.grid(row=5, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Formación Deportiva:", font=("Arial", 10)).grid(
            row=6, column=0, sticky="w", padx=(0, 5), pady=5)
        self.FormacionDeportiva = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.FormacionDeportiva.grid(row=6, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Certificaciones:", font=("Arial", 10)).grid(
            row=7, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Certificaciones = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Certificaciones.grid(row=7, column=1, sticky="w", pady=5)

        # Segunda columna
        tk.Label(self.form_frame, text="Especialidad:", font=("Arial", 10)).grid(
            row=0, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Especialidad = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Especialidad.grid(row=0, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Experiencia:", font=("Arial", 10)).grid(
            row=1, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Experiencia = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Experiencia.grid(row=1, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Equipos a Cargo:", font=("Arial", 10)).grid(
            row=2, column=3, sticky="w", padx=(50, 5), pady=5)
        self.EquiposACargo = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.EquiposACargo.grid(row=2, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Horario Asignado:", font=("Arial", 10)).grid(
            row=3, column=3, sticky="w", padx=(50, 5), pady=5)
        self.HorarioAsignado = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.HorarioAsignado.grid(row=3, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Método Trabajo:", font=("Arial", 10)).grid(
            row=4, column=3, sticky="w", padx=(50, 5), pady=5)
        self.MetodoTrabajo = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.MetodoTrabajo.grid(row=4, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Evaluación Resultado:", font=("Arial", 10)).grid(
            row=5, column=3, sticky="w", padx=(50, 5), pady=5)
        self.EvaluacionResultado = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.EvaluacionResultado.grid(row=5, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Disponibilidad:", font=("Arial", 10)).grid(
            row=6, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Disponibilidad = ttk.Combobox(self.form_frame, width=23,
                                           values=["Disponible", "No Disponible", "Vacaciones"])
        self.Disponibilidad.grid(row=6, column=4, sticky="w", pady=5)
        self.Disponibilidad.set("Disponible")

    def create_image_section(self):
        self.image_frame = tk.LabelFrame(self.left_frame, text="🖼️ Foto del Entrenador", font=("Arial", 10))
        self.image_frame.pack(pady=10, padx=30, fill="x")

        self.image_container = tk.Frame(self.image_frame, width=200, height=150, bg="lightgray")
        self.image_container.pack(pady=5)
        self.image_container.pack_propagate(False)

        self.image_label = tk.Label(self.image_container, text="Sin foto", bg="lightgray")
        self.image_label.pack(expand=True, fill="both")

        self.image_buttons = tk.Frame(self.image_frame)
        self.image_buttons.pack(pady=5)

        self.btn_cargar_imagen = tk.Button(self.image_buttons, text="📁 Cargar Foto", width=15)
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

        tk.Label(self.toolbar, text="LISTA DE ENTRENADORES", font=("Arial", 14, "bold")).pack(side="left", padx=10)

        self.btn_export_excel = tk.Button(self.toolbar, text="📊 Exportar Excel", bg="#4CAF50", fg="white")
        self.btn_export_excel.pack(side="right", padx=2)

        self.btn_export_pdf = tk.Button(self.toolbar, text="📄 Exportar PDF", bg="#2196F3", fg="white")
        self.btn_export_pdf.pack(side="right", padx=2)

        self.btn_filtros = tk.Button(self.toolbar, text="🔧 Filtros", bg="#FF9800", fg="white")
        self.btn_filtros.pack(side="right", padx=2)

    def create_treeview(self):
        self.treeview = ttk.Treeview(self.right_frame,
                                     columns=('ID', 'CodigoEmpleado', 'Nombres', 'Apellidos', 'DocumentoIdentidad',
                                              'FechaNacimiento', 'FormacionDeportiva', 'Certificaciones',
                                              'Especialidad',
                                              'Experiencia', 'EquiposACargo', 'HorarioAsignado', 'MetodoTrabajo',
                                              'EvaluacionResultado', 'Disponibilidad'), show='headings', height=20)

        columns_config = [
            ('ID', 50), ('CodigoEmpleado', 100), ('Nombres', 100), ('Apellidos', 100),
            ('DocumentoIdentidad', 100), ('FechaNacimiento', 100), ('FormacionDeportiva', 120),
            ('Certificaciones', 100), ('Especialidad', 100), ('Experiencia', 100),
            ('EquiposACargo', 100), ('HorarioAsignado', 100), ('MetodoTrabajo', 100),
            ('EvaluacionResultado', 120), ('Disponibilidad', 100)
        ]

        for col, width in columns_config:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=width)

        self.treeview.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        self.scrollbar_vertical = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar_vertical.set)
        self.scrollbar_vertical.pack(side="left", fill="y")

        self.scrollbar_horizontal = ttk.Scrollbar(self.right_frame, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=self.scrollbar_horizontal.set)
        self.scrollbar_horizontal.pack(side="bottom", fill="x")

        self.btn_cargar_lista = tk.Button(self.right_frame, text="🔄 Cargar Lista", font=("Arial", 10),
                                          bg="#2196F3", fg="white")
        self.btn_cargar_lista.pack(pady=5)