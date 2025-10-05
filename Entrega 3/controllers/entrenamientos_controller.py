import tkinter as tk
from tkinter import messagebox
from models.validators import validate_numeric_input, validate_text_length, validate_special_chars
from models.image_manager import ImageManager
from utils.export import export_to_excel, export_to_pdf, export_with_filters
from views.entrenamientos_view import EntrenamientosView


class EntrenamientosController:
    def __init__(self, parent, db_manager):
        self.db_manager = db_manager
        self.view = EntrenamientosView(parent)
        self.image_manager = ImageManager()
        self.setup_events()

    def setup_events(self):
        self.view.btn_buscar.config(command=self.buscar_entrenamiento)
        self.view.btn_guardar.config(command=self.save_entrenamiento)
        self.view.btn_actualizar.config(command=self.update_entrenamiento)
        self.view.btn_eliminar.config(command=self.delete_entrenamiento)
        self.view.btn_limpiar.config(command=self.clear_form)
        self.view.btn_cargar_lista.config(command=self.cargar_lista_entrenamientos)

        self.view.btn_cargar_imagen.config(command=self.load_entr_image_dialog)
        self.view.btn_blur.config(command=lambda: self.apply_entr_image_filter("BLUR"))
        self.view.btn_enfocar.config(command=lambda: self.apply_entr_image_filter("SHARPEN"))

        self.view.btn_export_excel.config(
            command=lambda: export_to_excel(self.view.treeview, "entrenamientos.xlsx")
        )
        self.view.btn_export_pdf.config(
            command=lambda: export_to_pdf(self.view.treeview, "Reporte Entrenamientos", "entrenamientos.pdf",
                                          self.db_manager)
        )
        self.view.btn_filtros.config(
            command=lambda: export_with_filters(self.view.treeview, "Entrenamientos")
        )

    def buscar_entrenamiento(self):
        id_entrena = self.view.IDEntrenamientos.get()
        if not id_entrena:
            messagebox.showwarning("Advertencia", "Por favor ingrese el ID del entrenamiento")
            return

        if not id_entrena.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número válido")
            return

        result = self.db_manager.execute_procedure('sp_LeerEntrenamiento', [int(id_entrena)])
        if result and len(result) > 0:
            entr = result[0]
            self.clear_form()

            self.view.IDEntrenamientos.insert(0, str(entr[0]))
            self.view.Codigo.insert(0, entr[1])
            self.view.EquipoOGrupo.insert(0, entr[2] if entr[2] else "")
            self.view.Fecha.set_date(entr[3]) if entr[3] else None
            self.view.Horario.insert(0, entr[4])
            self.view.Instalacion.insert(0, entr[5] if entr[5] else "")
            self.view.Entrenador.insert(0, entr[6])
            self.view.Objetivos.insert(0, entr[7] if entr[7] else "")
            self.view.ActividadProgramada.insert(0, entr[8] if entr[8] else "")
            self.view.Asistentes.insert(0, entr[9] if entr[9] else "")
            self.view.Observaciones.insert(0, entr[10] if entr[10] else "")
            self.view.EvaluacionCumplimiento.insert(0, entr[11])
            self.view.AsistenciaPromedio.insert(0, str(entr[12]))
            self.view.Disciplina.insert(0, entr[13])
            self.view.Categoria.insert(0, entr[14])
            self.view.IDEquipos.insert(0, str(entr[15]) if entr[15] else "")
            self.view.IDEntrenadores.insert(0, str(entr[16]) if entr[16] else "")
            self.view.IDInstalaciones.insert(0, str(entr[17]) if entr[17] else "")

            self.load_entr_image(entr[0])
        else:
            messagebox.showinfo("No encontrado", "No se encontró el entrenamiento con ese ID")

    def load_entr_image(self, entr_id):
        image_data = self.db_manager.get_image_from_db("entrenamientos", "IDEntrenamientos", entr_id,
                                                       "ImagenEntrenamiento")
        if image_data:
            try:
                from PIL import Image, ImageTk
                import io

                image = Image.open(io.BytesIO(image_data))
                background = Image.new('RGB', (300, 300), (240, 240, 240))
                image.thumbnail((280, 280), Image.Resampling.LANCZOS)
                x = (300 - image.width) // 2
                y = (300 - image.height) // 2
                background.paste(image, (x, y))

                photo = ImageTk.PhotoImage(background)
                self.view.image_label.configure(image=photo)
                self.view.image_label.image = photo

                self.image_manager.current_image_data = background
                self.image_manager.original_image_data = image.copy()

            except Exception as e:
                print(f"Error al cargar imagen: {e}")

    def cargar_lista_entrenamientos(self):
        try:
            for item in self.view.treeview.get_children():
                self.view.treeview.delete(item)

            result = self.db_manager.execute_procedure('sp_LeerTodosEntrenamientos')
            if result:
                for entr in result:
                    self.view.treeview.insert('', 'end', values=(
                        entr[0], entr[1], entr[2] if entr[2] else "", str(entr[3]) if entr[3] else "",
                        entr[4], entr[5] if entr[5] else "", entr[6], entr[7] if entr[7] else "",
                        entr[8] if entr[8] else "", entr[9] if entr[9] else "", entr[10] if entr[10] else "",
                        entr[11], entr[12], entr[13], entr[14], entr[15] if entr[15] else "",
                        entr[16] if entr[16] else "", entr[17] if entr[17] else ""
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la lista: {e}")

    def save_entrenamiento(self):
        if not validate_text_length(self.view.Codigo.get(), 2, 20):
            messagebox.showerror("Error", "El código debe tener entre 2 y 20 caracteres")
            return

        if not validate_special_chars(self.view.Codigo.get()):
            messagebox.showerror("Error", "El código contiene caracteres no permitidos")
            return

        try:
            params = [
                self.view.Codigo.get(),
                self.view.EquipoOGrupo.get() if self.view.EquipoOGrupo.get() else None,
                self.view.Fecha.get_date(),
                self.view.Horario.get(),
                self.view.Instalacion.get() if self.view.Instalacion.get() else None,
                self.view.Entrenador.get(),
                self.view.Objetivos.get() if self.view.Objetivos.get() else None,
                self.view.ActividadProgramada.get() if self.view.ActividadProgramada.get() else None,
                self.view.Asistentes.get() if self.view.Asistentes.get() else None,
                self.view.Observaciones.get() if self.view.Observaciones.get() else None,
                self.view.EvaluacionCumplimiento.get(),
                int(self.view.AsistenciaPromedio.get()),
                self.view.Disciplina.get(),
                self.view.Categoria.get(),
                int(self.view.IDEquipos.get()) if self.view.IDEquipos.get() else None,
                int(self.view.IDEntrenadores.get()) if self.view.IDEntrenadores.get() else None,
                int(self.view.IDInstalaciones.get()) if self.view.IDInstalaciones.get() else None
            ]

            if self.db_manager.execute_procedure('sp_CrearEntrenamiento', params):
                messagebox.showinfo("Éxito", "Entrenamiento guardado correctamente")

                entr_id = self.get_last_entr_id()
                if entr_id and self.image_manager.current_image_path:
                    self.image_manager.save_image_to_db(self.db_manager, "entrenamientos", entr_id,
                                                        "ImagenEntrenamiento")

                self.clear_form()
                self.cargar_lista_entrenamientos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def get_last_entr_id(self):
        try:
            result = self.db_manager.execute_procedure('sp_ObtenerUltimoEntrenamiento')
            if result and len(result) > 0:
                return result[0][0]
        except:
            pass
        return None

    def update_entrenamiento(self):
        if not self.view.IDEntrenamientos.get():
            messagebox.showwarning("Advertencia", "Primero busque el entrenamiento que desea actualizar")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea actualizar este entrenamiento?"):
            return

        try:
            params = [
                int(self.view.IDEntrenamientos.get()),
                self.view.Codigo.get(),
                self.view.EquipoOGrupo.get() if self.view.EquipoOGrupo.get() else None,
                self.view.Fecha.get_date(),
                self.view.Horario.get(),
                self.view.Instalacion.get() if self.view.Instalacion.get() else None,
                self.view.Entrenador.get(),
                self.view.Objetivos.get() if self.view.Objetivos.get() else None,
                self.view.ActividadProgramada.get() if self.view.ActividadProgramada.get() else None,
                self.view.Asistentes.get() if self.view.Asistentes.get() else None,
                self.view.Observaciones.get() if self.view.Observaciones.get() else None,
                self.view.EvaluacionCumplimiento.get(),
                int(self.view.AsistenciaPromedio.get()),
                self.view.Disciplina.get(),
                self.view.Categoria.get(),
                int(self.view.IDEquipos.get()) if self.view.IDEquipos.get() else None,
                int(self.view.IDEntrenadores.get()) if self.view.IDEntrenadores.get() else None,
                int(self.view.IDInstalaciones.get()) if self.view.IDInstalaciones.get() else None
            ]

            if self.db_manager.execute_procedure('sp_ActualizarEntrenamiento', params):
                if self.image_manager.current_image_path:
                    self.image_manager.save_image_to_db(
                        self.db_manager, "entrenamientos",
                        int(self.view.IDEntrenamientos.get()), "ImagenEntrenamiento"
                    )

                messagebox.showinfo("Éxito", "Entrenamiento actualizado correctamente")
                self.cargar_lista_entrenamientos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")

    def delete_entrenamiento(self):
        if not self.view.IDEntrenamientos.get():
            messagebox.showwarning("Advertencia", "Primero busque el entrenamiento que desea eliminar")
            return

        if messagebox.askyesno("Confirmar",
                               "¿Está seguro de que desea eliminar este entrenamiento?\nEsta acción no se puede deshacer."):
            if self.db_manager.execute_procedure('sp_EliminarEntrenamiento', [int(self.view.IDEntrenamientos.get())]):
                messagebox.showinfo("Éxito", "Entrenamiento eliminado correctamente")
                self.clear_form()
                self.cargar_lista_entrenamientos()

    def clear_form(self):
        for widget in [self.view.IDEntrenamientos, self.view.Codigo, self.view.EquipoOGrupo,
                       self.view.Horario, self.view.Instalacion, self.view.Entrenador, self.view.Objetivos,
                       self.view.ActividadProgramada, self.view.Asistentes, self.view.Observaciones,
                       self.view.EvaluacionCumplimiento, self.view.AsistenciaPromedio, self.view.Disciplina,
                       self.view.Categoria, self.view.IDEquipos, self.view.IDEntrenadores, self.view.IDInstalaciones]:
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

        self.view.image_label.configure(image='')
        self.view.image_label.image = None
        self.image_manager.current_image_path = None

    def load_entr_image_dialog(self):
        self.image_manager.load_image(self.view.image_label)

    def apply_entr_image_filter(self, filter_type):
        photo, filtered_image = self.image_manager.apply_filter(filter_type, self.view.image_label)
        if photo and filtered_image:
            pass