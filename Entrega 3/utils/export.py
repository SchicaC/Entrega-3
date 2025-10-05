import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog, messagebox
import openpyxl
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

# Definir variables globales para evitar errores
db_manager = None
root = None


def export_to_excel(treeview, filename="exportacion.xlsx"):
    """Exporta datos de un treeview a Excel"""
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Datos Exportados"

        # Encabezados
        headers = [treeview.heading(col)['text'] for col in treeview['columns']]
        ws.append(headers)

        # Datos
        for item in treeview.get_children():
            values = treeview.item(item)['values']
            ws.append(values)

        # Guardar archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=filename
        )

        if file_path:
            wb.save(file_path)
            messagebox.showinfo("Éxito", f"Datos exportados a {file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar a Excel: {e}")


def export_to_pdf(treeview, title="Reporte", filename="reporte.pdf", db_manager_param=None):
    """Exporta TODOS los datos de un treeview a PDF - VERSIÓN CORREGIDA"""
    # Usar el parámetro o la variable global
    db_manager = db_manager_param if db_manager_param is not None else globals().get('db_manager')

    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=filename
        )

        if not file_path:
            return

        # Obtener TODOS los datos del treeview
        headers = [treeview.heading(col)['text'] for col in treeview['columns']]
        data = [headers]

        # Obtener TODOS los items del treeview SIN FILTROS
        all_items = treeview.get_children()

        # Si no hay items en el treeview, intentar cargar datos directamente desde la BD
        if not all_items and db_manager:
            messagebox.showinfo("Información", "Cargando datos desde la base de datos...")

            # Determinar qué procedimiento almacenado llamar según el título
            if "Entrenamientos" in title:
                result = db_manager.execute_procedure('sp_LeerTodosEntrenamientos')
            elif "Miembros" in title:
                result = db_manager.execute_procedure('sp_LeerTodosMiembros')
            elif "Entrenadores" in title:
                result = db_manager.execute_procedure('sp_LeerTodosEntrenadores')
            elif "Competiciones" in title:
                result = db_manager.execute_procedure('sp_LeerTodasCompeticiones')
            else:
                result = None

            if result:
                for row in result:
                    # Convertir todos los valores a string
                    str_values = []
                    for val in row:
                        if val is None:
                            str_values.append("")
                        else:
                            text = str(val)
                            # Truncar textos muy largos para mejor visualización
                            if len(text) > 50:
                                text = text[:47] + "..."
                            str_values.append(text)
                    data.append(str_values)
            else:
                messagebox.showwarning("Advertencia", "No hay datos para exportar")
                return
        else:
            # Usar los datos del treeview
            for item in all_items:
                values = treeview.item(item)['values']
                # Convertir todos los valores a string y manejar None, truncar textos muy largos
                str_values = []
                for val in values:
                    if val is None:
                        str_values.append("")
                    else:
                        text = str(val)
                        # Truncar textos muy largos para mejor visualización
                        if len(text) > 50:
                            text = text[:47] + "..."
                        str_values.append(text)
                data.append(str_values)

        if len(data) <= 1:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return

        print(f"Exportando {len(data) - 1} registros a PDF para: {title}")

        # Configurar el documento PDF en orientación horizontal
        doc = SimpleDocTemplate(file_path, pagesize=landscape(letter),
                                rightMargin=10, leftMargin=10,
                                topMargin=20, bottomMargin=20)
        elements = []

        # Estilos
        styles = getSampleStyleSheet()

        # Título más pequeño
        title_para = Paragraph(f"<b>{title}</b>", styles['Heading1'])
        elements.append(title_para)

        # Información del reporte con fuente más pequeña
        info_text = f"Total de registros: {len(data) - 1} | Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        info_para = Paragraph(info_text, styles['Normal'])
        elements.append(info_para)
        elements.append(Paragraph("<br/>", styles['Normal']))

        # Calcular anchos de columna dinámicamente
        def calculate_column_widths(data, max_width=700):
            if not data or len(data) < 2:
                return [40] * len(headers)

            col_widths = [30] * len(headers)
            for row in data:
                for i, cell in enumerate(row):
                    if i < len(col_widths):
                        cell_width = len(str(cell)) * 2.8
                        col_widths[i] = max(col_widths[i], min(cell_width, 80))
            return col_widths

        col_widths = calculate_column_widths(data)

        # Crear tabla con todos los datos
        table = Table(data, colWidths=col_widths, repeatRows=1)

        # Estilo de la tabla ultra compacto para múltiples columnas
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
            ('TOPPADDING', (0, 0), (-1, 0), 4),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 5),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#DDDDDD')),
            ('WORDWRAP', (0, 0), (-1, -1), True),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 1), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 1),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ])

        table.setStyle(table_style)
        elements.append(table)

        # Pie de página compacto
        elements.append(Paragraph("<br/>", styles['Normal']))
        footer_text = f"Sistema de Gestión - Club Atletas Unidos | Página 1"
        footer_para = Paragraph(footer_text, styles['Italic'])
        elements.append(footer_para)

        # Generar el PDF
        doc.build(elements)

        messagebox.showinfo("Éxito",
                            f"Reporte PDF generado exitosamente:\n"
                            f"Archivo: {file_path}\n"
                            f"Registros exportados: {len(data) - 1}\n"
                            f"Columnas: {len(headers)}")

    except Exception as e:
        messagebox.showerror("Error",
                             f"Error al exportar a PDF:\n{str(e)}")
        print(f"Error detallado en exportación PDF: {e}")


def export_with_filters(treeview, module_name, db_manager_param=None, root_param=None):
    """Exporta datos con filtros aplicados - VERSIÓN SIMPLIFICADA Y FUNCIONAL"""
    # Usar parámetros o variables globales
    db_manager = db_manager_param if db_manager_param is not None else globals().get('db_manager')
    root = root_param if root_param is not None else globals().get('root')

    # Si root sigue siendo None, crear una ventana temporal
    if root is None:
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal temporal

    filter_window = tk.Toplevel()
    filter_window.title(f"Filtros de Exportación - {module_name}")
    filter_window.geometry("400x300")
    if root:
        filter_window.transient(root)
    filter_window.grab_set()

    tk.Label(filter_window, text="Filtros de Exportación", font=("Arial", 14, "bold")).pack(pady=10)

    # Filtros por fecha
    date_frame = tk.LabelFrame(filter_window, text="Rango de Fechas", font=("Arial", 10))
    date_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(date_frame, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
    start_date = DateEntry(date_frame, date_pattern='yyyy-mm-dd')
    start_date.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(date_frame, text="Hasta:").grid(row=1, column=0, padx=5, pady=5)
    end_date = DateEntry(date_frame, date_pattern='yyyy-mm-dd')
    end_date.grid(row=1, column=1, padx=5, pady=5)

    # Filtros por categoría
    category_frame = tk.LabelFrame(filter_window, text="Categoría", font=("Arial", 10))
    category_frame.pack(pady=10, padx=20, fill="x")

    category_var = tk.StringVar()
    categories = ["Todas", "Activo", "Inactivo", "Proxima", "Finalizada"]
    for i, category in enumerate(categories):
        tk.Radiobutton(category_frame, text=category, variable=category_var, value=category).grid(row=0, column=i,
                                                                                                  padx=5, pady=5)

    category_var.set("Todas")

    def aplicar_filtros():
        """Filtra los datos del treeview según los criterios seleccionados"""
        try:
            # Obtener todos los items del treeview
            all_items = treeview.get_children()
            if not all_items:
                messagebox.showwarning("Advertencia", "No hay datos para filtrar")
                return None

            fecha_desde = start_date.get_date()
            fecha_hasta = end_date.get_date()
            categoria = category_var.get()

            # Determinar índices de columnas según el módulo
            if module_name == "Competiciones":
                fecha_col_idx = 7  # Índice de la columna de fecha en competiciones
                estado_col_idx = 14  # Índice de la columna de estado
            elif module_name == "Entrenadores":
                fecha_col_idx = 5  # Fecha de nacimiento
                estado_col_idx = 14  # Disponibilidad
            elif module_name == "Miembros":
                fecha_col_idx = 9  # Fecha de ingreso
                estado_col_idx = 15  # Estado
            elif module_name == "Entrenamientos":
                fecha_col_idx = 3  # Fecha del entrenamiento
                estado_col_idx = None  # No hay estado específico
            else:
                fecha_col_idx = None
                estado_col_idx = None

            items_filtrados = []

            for item in all_items:
                values = treeview.item(item)['values']
                incluir_item = True

                # Filtrar por fecha si se especificó
                if fecha_col_idx is not None and fecha_col_idx < len(values):
                    fecha_item_str = values[fecha_col_idx]
                    if fecha_item_str and fecha_item_str.strip():
                        try:
                            # CORRECCIÓN: Manejar fechas con y sin hora
                            if ' ' in fecha_item_str:
                                # Fecha con hora: '2024-03-12 00:00:00'
                                fecha_item = datetime.strptime(fecha_item_str.split()[0], '%Y-%m-%d').date()
                            else:
                                # Fecha sin hora: '2024-03-12'
                                fecha_item = datetime.strptime(fecha_item_str, '%Y-%m-%d').date()

                            # Aplicar filtros de fecha
                            if fecha_desde and fecha_item < fecha_desde:
                                incluir_item = False
                            if fecha_hasta and fecha_item > fecha_hasta:
                                incluir_item = False
                        except Exception as e:
                            print(f"Error al parsear fecha: {fecha_item_str} - {e}")
                            # Si hay error al parsear la fecha, incluir el item
                            pass

                # Filtrar por categoría/estado
                if estado_col_idx is not None and estado_col_idx < len(values) and categoria != "Todas":
                    estado_item = values[estado_col_idx] if values[estado_col_idx] else ""

                    if categoria == "Activo" and "activo" not in str(estado_item).lower():
                        incluir_item = False
                    elif categoria == "Inactivo" and "inactivo" not in str(estado_item).lower():
                        incluir_item = False
                    elif categoria == "Proxima" and "proxima" not in str(estado_item).lower():
                        incluir_item = False
                    elif categoria == "Finalizada" and "finalizada" not in str(estado_item).lower():
                        incluir_item = False

                if incluir_item:
                    items_filtrados.append(item)

            return items_filtrados

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtros: {e}")
            return None

    def apply_export():
        """Exporta a Excel con filtros aplicados"""
        items_filtrados = aplicar_filtros()

        if items_filtrados is None:
            return

        if not items_filtrados:
            messagebox.showwarning("Advertencia", "No hay datos que coincidan con los filtros aplicados")
            return

        # Crear un treeview temporal con los datos filtrados
        temp_tree = ttk.Treeview()

        # Copiar la configuración de columnas del treeview original
        columns = treeview['columns']
        temp_tree['columns'] = columns

        # Configurar headings y columnas
        for col in columns:
            temp_tree.heading(col, text=treeview.heading(col)['text'])
            temp_tree.column(col, width=treeview.column(col)['width'])

        # Llenar con datos filtrados
        for item in items_filtrados:
            values = treeview.item(item)['values']
            temp_tree.insert('', 'end', values=values)

        # Generar nombre de archivo con información de filtros
        fecha_desde = start_date.get_date()
        fecha_hasta = end_date.get_date()
        categoria = category_var.get()

        filename = f"{module_name.lower()}_filtrado"
        if fecha_desde:
            filename += f"_desde_{fecha_desde}"
        if fecha_hasta:
            filename += f"_hasta_{fecha_hasta}"
        if categoria != "Todas":
            filename += f"_{categoria.lower()}"
        filename += ".xlsx"

        export_to_excel(temp_tree, filename)
        filter_window.destroy()

    def apply_pdf_export():
        """Exporta a PDF con filtros aplicados"""
        items_filtrados = aplicar_filtros()

        if items_filtrados is None:
            return

        if not items_filtrados:
            messagebox.showwarning("Advertencia", "No hay datos que coincidan con los filtros aplicados")
            return

        # Crear un treeview temporal con los datos filtrados
        temp_tree = ttk.Treeview()

        # Copiar la configuración de columnas del treeview original
        columns = treeview['columns']
        temp_tree['columns'] = columns

        # Configurar headings y columnas
        for col in columns:
            temp_tree.heading(col, text=treeview.heading(col)['text'])
            temp_tree.column(col, width=treeview.column(col)['width'])

        # Llenar con datos filtrados
        for item in items_filtrados:
            values = treeview.item(item)['values']
            temp_tree.insert('', 'end', values=values)

        # Generar título y nombre de archivo con información de filtros
        fecha_desde = start_date.get_date()
        fecha_hasta = end_date.get_date()
        categoria = category_var.get()

        titulo = f"Reporte {module_name}"
        filename = f"{module_name.lower()}_filtrado"

        info_filtros = []
        if fecha_desde:
            info_filtros.append(f"Desde: {fecha_desde}")
            filename += f"_desde_{fecha_desde}"
        if fecha_hasta:
            info_filtros.append(f"Hasta: {fecha_hasta}")
            filename += f"_hasta_{fecha_hasta}"
        if categoria != "Todas":
            info_filtros.append(f"Categoría: {categoria}")
            filename += f"_{categoria.lower()}"

        if info_filtros:
            titulo += f" ({', '.join(info_filtros)})"

        filename += ".pdf"

        export_to_pdf(temp_tree, titulo, filename, db_manager)
        filter_window.destroy()

    button_frame = tk.Frame(filter_window)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Exportar a Excel", command=apply_export, bg="#4CAF50", fg="white").pack(side="left",
                                                                                                          padx=5)
    tk.Button(button_frame, text="Exportar a PDF", command=apply_pdf_export, bg="#2196F3", fg="white").pack(side="left",
                                                                                                            padx=5)
    tk.Button(button_frame, text="Cancelar", command=filter_window.destroy, bg="#f44336", fg="white").pack(side="left",
                                                                                                           padx=5)


# Función para inicializar las variables globales
def init_export_module(db_manager_instance, root_instance):
    """Inicializa el módulo de exportación con las instancias necesarias"""
    global db_manager, root
    db_manager = db_manager_instance
    root = root_instance