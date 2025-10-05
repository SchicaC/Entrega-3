import tkinter as tk
from tkinter import messagebox
from models.validators import validate_numeric_input, validate_text_length, validate_special_chars
from models.image_manager import ImageManager
from utils.export import export_to_excel, export_to_pdf, export_with_filters
from views.competiciones_view import CompeticionesView


class CompeticionesController:
    def __init__(self, parent, db_manager):
        self.db_manager = db_manager
        self.view = CompeticionesView(parent)
        self.image_manager = ImageManager()
        self.setup_events()

    def setup_events(self):
        # Conectar eventos de los botones
        self.view.btn_buscar.config(command=self.buscar_competicion)
        self.view.btn_guardar.config(command=self.save_competicion)
        self.view.btn_actualizar.config(command=self.update_competicion)
        self.view.btn_eliminar.config(command=self.delete_competicion)
        self.view.btn_limpiar.config(command=self.clear_form)
        self.view.btn_cargar_lista.config(command=self.cargar_lista_competiciones)

        # Eventos de imagen
        self.view.btn_cargar_imagen.config(command=self.load_comp_image_dialog)
        self.view.btn_blur.config(command=lambda: self.apply_comp_image_filter("BLUR"))
        self.view.btn_enfocar.config(command=lambda: self.apply_comp_image_filter("SHARPEN"))

        # Eventos de exportación
        self.view.btn_export_excel.config(
            command=lambda: export_to_excel(self.view.treeview, "competiciones.xlsx")
        )
        self.view.btn_export_pdf.config(
            command=lambda: export_to_pdf(self.view.treeview, "Reporte Competiciones", "competiciones.pdf",
                                          self.db_manager)
        )
        self.view.btn_filtros.config(
            command=lambda: export_with_filters(self.view.treeview, "Competiciones")
        )

    def buscar_competicion(self):
        id_comp = self.view.IDCompeticiones.get()
        if not id_comp:
            messagebox.showwarning("Advertencia", "Por favor ingrese el ID de la competición")
            return

        if not id_comp.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número válido")
            return

        result = self.db_manager.execute_procedure('sp_LeerCompeticion', [int(id_comp)])
        if result and len(result) > 0:
            comp = result[0]
            self.clear_form()

            # Llenar campos
            self.view.IDCompeticiones.insert(0, str(comp[0]))
            self.view.Codigo_comp.insert(0, comp[1])
            self.view.Nombre_comp.insert(0, comp[2])
            self.view.Disciplina_comp.insert(0, comp[3])
            self.view.Tipo_comp.insert(0, comp[4])
            self.view.Organizador_comp.insert(0, comp[5])
            self.view.Sedes_comp.insert(0, comp[6])
            self.view.Fechas_comp.set_date(comp[7]) if comp[7] else None
            self.view.Categorias_comp.insert(0, comp[8])
            self.view.Formato_comp.insert(0, comp[9])
            self.view.RequisitosInscripcion_comp.insert(0, comp[10])
            self.view.Reglamento_comp.insert(0, comp[11])
            self.view.Premios_comp.insert(0, comp[12])
            self.view.IDDisciplinaDeportiva_comp.insert(0, str(comp[13]) if comp[13] else "")
            self.view.EstadoCompeticion_comp.set(comp[14] if comp[14] else "Proxima")

            # Cargar imagen si existe
            self.load_comp_image(comp[0])
        else:
            messagebox.showinfo("No encontrado", "No se encontró la competición con ese ID")

    def load_comp_image(self, comp_id):
        """Carga la imagen de la competición desde la base de datos"""
        image_data = self.db_manager.get_image_from_db("competiciones", "IDCompeticiones", comp_id, "ImagenCompeticion")
        if image_data:
            try:
                from PIL import Image, ImageTk
                import io

                image = Image.open(io.BytesIO(image_data))

                # Crear fondo del tamaño fijo
                background = Image.new('RGB', (300, 300), (240, 240, 240))
                image.thumbnail((280, 280), Image.Resampling.LANCZOS)
                x = (300 - image.width) // 2
                y = (300 - image.height) // 2
                background.paste(image, (x, y))

                photo = ImageTk.PhotoImage(background)
                self.view.image_label.configure(image=photo)
                self.view.image_label.image = photo

                # Actualizar el image manager
                self.image_manager.current_image_data = background
                self.image_manager.original_image_data = image.copy()

            except ImportError:
                print("PIL no disponible, no se puede cargar la imagen")
            except Exception as e:
                print(f"Error al cargar imagen: {e}")

    def cargar_lista_competiciones(self):
        try:
            # Limpiar treeview
            for item in self.view.treeview.get_children():
                self.view.treeview.delete(item)

            # Obtener todas las competiciones
            result = self.db_manager.execute_procedure('sp_LeerTodasCompeticiones')
            if result:
                for comp in result:
                    self.view.treeview.insert('', 'end', values=(
                        comp[0], comp[1], comp[2], comp[3], comp[4], comp[5],
                        comp[6], str(comp[7]) if comp[7] else "", comp[8], comp[9],
                        comp[10], comp[11], comp[12], comp[13] if comp[13] else "",
                        comp[14] if comp[14] else ""
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la lista: {e}")

    def save_competicion(self):
        # Validaciones
        if not validate_text_length(self.view.Nombre_comp.get(), 2, 100):
            messagebox.showerror("Error", "El nombre debe tener entre 2 y 100 caracteres")
            return

        if not validate_special_chars(self.view.Nombre_comp.get()):
            messagebox.showerror("Error", "El nombre contiene caracteres no permitidos")
            return

        try:
            params = [
                self.view.Codigo_comp.get(),
                self.view.Nombre_comp.get(),
                self.view.Disciplina_comp.get(),
                self.view.Tipo_comp.get(),
                self.view.Organizador_comp.get(),
                self.view.Sedes_comp.get(),
                self.view.Fechas_comp.get_date(),
                self.view.Categorias_comp.get(),
                self.view.Formato_comp.get(),
                self.view.RequisitosInscripcion_comp.get(),
                self.view.Reglamento_comp.get(),
                self.view.Premios_comp.get(),
                int(self.view.IDDisciplinaDeportiva_comp.get()) if self.view.IDDisciplinaDeportiva_comp.get() else None,
                self.view.EstadoCompeticion_comp.get()
            ]

            if self.db_manager.execute_procedure('sp_CrearCompeticion', params):
                messagebox.showinfo("Éxito", "Competición guardada correctamente")

                # Guardar imagen si hay una cargada
                comp_id = self.get_last_comp_id()
                if comp_id and self.image_manager.current_image_path:
                    self.image_manager.save_image_to_db(self.db_manager, "competiciones", comp_id, "ImagenCompeticion")

                self.clear_form()
                self.cargar_lista_competiciones()
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos ingresados: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def get_last_comp_id(self):
        """Obtiene el ID de la última competición insertada"""
        try:
            result = self.db_manager.execute_procedure('sp_ObtenerUltimaCompeticion')
            if result and len(result) > 0:
                return result[0][0]
        except:
            pass
        return None

    def update_competicion(self):
        if not self.view.IDCompeticiones.get():
            messagebox.showwarning("Advertencia", "Primero busque la competición que desea actualizar")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea actualizar esta competición?"):
            return

        try:
            params = [
                int(self.view.IDCompeticiones.get()),
                self.view.Codigo_comp.get(),
                self.view.Nombre_comp.get(),
                self.view.Disciplina_comp.get(),
                self.view.Tipo_comp.get(),
                self.view.Organizador_comp.get(),
                self.view.Sedes_comp.get(),
                self.view.Fechas_comp.get_date(),
                self.view.Categorias_comp.get(),
                self.view.Formato_comp.get(),
                self.view.RequisitosInscripcion_comp.get(),
                self.view.Reglamento_comp.get(),
                self.view.Premios_comp.get(),
                int(self.view.IDDisciplinaDeportiva_comp.get()) if self.view.IDDisciplinaDeportiva_comp.get() else None,
                self.view.EstadoCompeticion_comp.get()
            ]

            if self.db_manager.execute_procedure('sp_ActualizarCompeticion', params):
                # Guardar imagen si hay una cargada
                if self.image_manager.current_image_path:
                    self.image_manager.save_image_to_db(
                        self.db_manager, "competiciones",
                        int(self.view.IDCompeticiones.get()), "ImagenCompeticion"
                    )

                messagebox.showinfo("Éxito", "Competición actualizada correctamente")
                self.cargar_lista_competiciones()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")

    def delete_competicion(self):
        if not self.view.IDCompeticiones.get():
            messagebox.showwarning("Advertencia", "Primero busque la competición que desea eliminar")
            return

        if messagebox.askyesno("Confirmar",
                               "¿Está seguro de que desea eliminar esta competición?\nEsta acción no se puede deshacer."):
            if self.db_manager.execute_procedure('sp_EliminarCompeticion', [int(self.view.IDCompeticiones.get())]):
                messagebox.showinfo("Éxito", "Competición eliminada correctamente")
                self.clear_form()
                self.cargar_lista_competiciones()

    def clear_form(self):
        # Limpiar todos los campos de entrada
        entries = [
            self.view.IDCompeticiones, self.view.Codigo_comp, self.view.Nombre_comp,
            self.view.Disciplina_comp, self.view.Tipo_comp, self.view.Organizador_comp,
            self.view.Sedes_comp, self.view.Categorias_comp, self.view.Formato_comp,
            self.view.RequisitosInscripcion_comp, self.view.Reglamento_comp, self.view.Premios_comp,
            self.view.IDDisciplinaDeportiva_comp
        ]

        for entry in entries:
            entry.delete(0, tk.END)

        # Restablecer combobox
        self.view.EstadoCompeticion_comp.set("Proxima")

        # Limpiar imagen
        self.view.image_label.configure(image='')
        self.view.image_label.image = None
        self.image_manager.current_image_path = None
        self.image_manager.current_image_data = None
        self.image_manager.original_image_data = None

    def load_comp_image_dialog(self):
        """Carga imagen para competición"""
        self.image_manager.load_image(self.view.image_label)

    def apply_comp_image_filter(self, filter_type):
        """Aplica filtro a la imagen de competición"""
        photo, filtered_image = self.image_manager.apply_filter(filter_type, self.view.image_label)
        if photo and filtered_image:
            # La actualización ya se hizo dentro de apply_filter
            pass