import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class CompeticionesView:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True)

        # Frame izquierdo para formulario
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Título
        self.titulo = tk.Label(self.left_frame, text="🏆 GESTIÓN DE COMPETICIONES",
                               font=("Arial", 16, "bold"), fg="blue")
        self.titulo.pack(pady=10)

        # Frame del formulario
        self.form_frame = tk.Frame(self.left_frame)
        self.form_frame.pack(pady=10, anchor="w", padx=30)

        # Crear campos del formulario
        self.create_form_fields()

        # Sección de imagen
        self.create_image_section()

        # Botones
        self.create_buttons()

        # Frame derecho para lista
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Toolbar y treeview
        self.create_toolbar()
        self.create_treeview()

    def create_form_fields(self):
        # Fila 1: IDCompeticiones
        tk.Label(self.form_frame, text="ID Competición:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", padx=(0, 5), pady=5)
        self.IDCompeticiones = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.IDCompeticiones.grid(row=0, column=1, sticky="w", pady=5)

        # Botón Buscar
        self.btn_buscar = tk.Button(self.form_frame, text="🔍 Buscar", font=("Arial", 10),
                                    bg="#FFA500", fg="white", width=10)
        self.btn_buscar.grid(row=0, column=2, padx=10, pady=5)

        # Primera columna - Campos principales
        tk.Label(self.form_frame, text="Código:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Codigo_comp = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Codigo_comp.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Nombre:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Nombre_comp = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Nombre_comp.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Disciplina:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Disciplina_comp = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Disciplina_comp.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Tipo:", font=("Arial", 10)).grid(
            row=4, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Tipo_comp = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Tipo_comp.grid(row=4, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Organizador:", font=("Arial", 10)).grid(
            row=5, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Organizador_comp = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Organizador_comp.grid(row=5, column=1, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Sedes:", font=("Arial", 10)).grid(
            row=6, column=0, sticky="w", padx=(0, 5), pady=5)
        self.Sedes_comp = tk.Entry(self.form_frame, width=20, font=("Arial", 10), relief="solid", bd=1)
        self.Sedes_comp.grid(row=6, column=1, sticky="w", pady=5)

        # Segunda columna
        tk.Label(self.form_frame, text="Fechas:", font=("Arial", 10)).grid(
            row=0, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Fechas_comp = DateEntry(self.form_frame, width=23, date_pattern='yyyy-mm-dd')
        self.Fechas_comp.grid(row=0, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Categorías:", font=("Arial", 10)).grid(
            row=1, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Categorias_comp = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Categorias_comp.grid(row=1, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Formato:", font=("Arial", 10)).grid(
            row=2, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Formato_comp = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Formato_comp.grid(row=2, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Requisitos Inscripción:", font=("Arial", 10)).grid(
            row=3, column=3, sticky="w", padx=(50, 5), pady=5)
        self.RequisitosInscripcion_comp = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.RequisitosInscripcion_comp.grid(row=3, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Reglamento:", font=("Arial", 10)).grid(
            row=4, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Reglamento_comp = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Reglamento_comp.grid(row=4, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Premios:", font=("Arial", 10)).grid(
            row=5, column=3, sticky="w", padx=(50, 5), pady=5)
        self.Premios_comp = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.Premios_comp.grid(row=5, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="ID Disciplina Deportiva:", font=("Arial", 10)).grid(
            row=6, column=3, sticky="w", padx=(50, 5), pady=5)
        self.IDDisciplinaDeportiva_comp = tk.Entry(self.form_frame, width=25, font=("Arial", 10), relief="solid", bd=1)
        self.IDDisciplinaDeportiva_comp.grid(row=6, column=4, sticky="w", pady=5)

        tk.Label(self.form_frame, text="Estado Competición:", font=("Arial", 10)).grid(
            row=7, column=3, sticky="w", padx=(50, 5), pady=5)
        self.EstadoCompeticion_comp = ttk.Combobox(self.form_frame, width=23,
                                                   values=["Proxima", "Activa", "Finalizada", "Cancelada"])
        self.EstadoCompeticion_comp.grid(row=7, column=4, sticky="w", pady=5)
        self.EstadoCompeticion_comp.set("Proxima")

    def create_image_section(self):
        self.image_frame = tk.LabelFrame(self.left_frame, text="🖼️ Imagen de Competición", font=("Arial", 10))
        self.image_frame.pack(pady=10, padx=30, fill="x")

        # Frame contenedor con tamaño fijo
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

        tk.Label(self.toolbar, text="LISTA DE COMPETICIONES", font=("Arial", 14, "bold")).pack(side="left", padx=10)

        self.btn_export_excel = tk.Button(self.toolbar, text="📊 Exportar Excel", bg="#4CAF50", fg="white")
        self.btn_export_excel.pack(side="right", padx=2)

        self.btn_export_pdf = tk.Button(self.toolbar, text="📄 Exportar PDF", bg="#2196F3", fg="white")
        self.btn_export_pdf.pack(side="right", padx=2)

        self.btn_filtros = tk.Button(self.toolbar, text="🔧 Filtros", bg="#FF9800", fg="white")
        self.btn_filtros.pack(side="right", padx=2)

    def create_treeview(self):
        # Treeview para mostrar competiciones
        self.treeview = ttk.Treeview(self.right_frame,
                                     columns=('ID', 'Codigo', 'Nombre', 'Disciplina', 'Tipo', 'Organizador', 'Sedes',
                                              'Fechas', 'Categorias', 'Formato', 'Requisitos', 'Reglamento', 'Premios',
                                              'IDDisciplina', 'Estado'), show='headings', height=20)

        # Configurar headings
        self.treeview.heading('ID', text='ID')
        self.treeview.heading('Codigo', text='Código')
        self.treeview.heading('Nombre', text='Nombre')
        self.treeview.heading('Disciplina', text='Disciplina')
        self.treeview.heading('Tipo', text='Tipo')
        self.treeview.heading('Organizador', text='Organizador')
        self.treeview.heading('Sedes', text='Sedes')
        self.treeview.heading('Fechas', text='Fechas')
        self.treeview.heading('Categorias', text='Categorías')
        self.treeview.heading('Formato', text='Formato')
        self.treeview.heading('Requisitos', text='Requisitos')
        self.treeview.heading('Reglamento', text='Reglamento')
        self.treeview.heading('Premios', text='Premios')
        self.treeview.heading('IDDisciplina', text='ID Disciplina')
        self.treeview.heading('Estado', text='Estado')

        # Configurar columnas
        self.treeview.column('ID', width=50)
        self.treeview.column('Codigo', width=80)
        self.treeview.column('Nombre', width=120)
        self.treeview.column('Disciplina', width=80)
        self.treeview.column('Tipo', width=80)
        self.treeview.column('Organizador', width=100)
        self.treeview.column('Sedes', width=80)
        self.treeview.column('Fechas', width=120)
        self.treeview.column('Categorias', width=80)
        self.treeview.column('Formato', width=80)
        self.treeview.column('Requisitos', width=100)
        self.treeview.column('Reglamento', width=100)
        self.treeview.column('Premios', width=80)
        self.treeview.column('IDDisciplina', width=80)
        self.treeview.column('Estado', width=80)

        self.treeview.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar para competiciones
        self.scrollbar_vertical = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar_vertical.set)
        self.scrollbar_vertical.pack(side="left", fill="y")

        self.scrollbar_horizontal = ttk.Scrollbar(self.right_frame, orient="horizontal", command=self.treeview.xview)
        self.treeview.configure(xscrollcommand=self.scrollbar_horizontal.set)
        self.scrollbar_horizontal.pack(side="bottom", fill="x")

        # Botón para cargar lista
        self.btn_cargar_lista = tk.Button(self.right_frame, text="🔄 Cargar Lista", font=("Arial", 10),
                                          bg="#2196F3", fg="white")
        self.btn_cargar_lista.pack(pady=5)