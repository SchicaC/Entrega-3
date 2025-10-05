import tkinter as tk
from tkinter import messagebox
from models.validators import validate_numeric_input, validate_text_length, validate_special_chars
from models.image_manager import ImageManager
from utils.export import export_to_excel, export_to_pdf, export_with_filters
from views.entrenadores_view import EntrenadoresView


class EntrenadoresController:
    def __init__(self, parent, db_manager):
        self.db_manager = db_manager
        self.view = EntrenadoresView(parent)
        self.image_manager = ImageManager()
        self.setup_events()

    def setup_events(self):
        self.view.btn_buscar.config(command=self.buscar_entrenador)
        self.view.btn_guardar.config(command=self.save_entrenador)
        self.view.btn_actualizar.config(command=self.update_entrenador)
        self.view.btn_eliminar.config(command=self.delete_entrenador)
        self.view.btn_limpiar.config(command=self.clear_form)
        self.view.btn_cargar_lista.config(command=self.cargar_lista_entrenadores)

        self.view.btn_cargar_imagen.config(command=self.load_ent_image_dialog)
        self.view.btn_blur.config(command=lambda: self.apply_ent_image_filter("BLUR"))
        self.view.btn_enfocar.config(command=lambda: self.apply_ent_image_filter("SHARPEN"))

        self.view.btn_export_excel.config(
            command=lambda: export_to_excel(self.view.treeview, "entrenadores.xlsx")
        )
        self.view.btn_export_pdf.config(
            command=lambda: export_to_pdf(self.view.treeview, "Reporte Entrenadores", "entrenadores.pdf",
                                          self.db_manager)
        )
        self.view.btn_filtros.config(
            command=lambda: export_with_filters(self.view.treeview, "Entrenadores")
        )

    def buscar_entrenador(self):
        id_ent = self.view.IDEntrenadores.get()
        if not id_ent:
            messagebox.showwarning("Advertencia", "Por favor ingrese el ID del entrenador")
            return

        if not id_ent.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número válido")
            return

        result = self.db_manager.execute_procedure('sp_LeerEntrenador', [int(id_ent)])
        if result and len(result) > 0:
            ent = result[0]
            self.clear_form()

            self.view.IDEntrenadores.insert(0, str(ent[0]))
            self.view.CodigoEmpleado.insert(0, str(ent[1]))
            self.view.Nombres.insert(0, ent[2])
            self.view.Apellidos.insert(0, ent[3])
            self.view.DocumentoIdentidad.insert(0, str(ent[4]))
            self.view.FechaNacimiento.set_date(ent[5]) if ent[5] else None
            self.view.FormacionDeportiva.insert(0, ent[6])
            self.view.Certificaciones.insert(0, ent[7] if ent[7] else "")
            self.view.Especialidad.insert(0, ent[8] if ent[8] else "")
            self.view.Experiencia.insert(0, ent[9] if ent[9] else "")
            self.view.EquiposACargo.insert(0, ent[10])
            self.view.HorarioAsignado.insert(0, str(ent[11]))
            self.view.MetodoTrabajo.insert(0, ent[12] if ent[12] else "")
            self.view.EvaluacionResultado.insert(0, ent[13] if ent[13] else "")
            self.view.Disponibilidad.set(ent[14])

            self.load_ent_image(ent[0])
        else:
            messagebox.showinfo("No encontrado", "No se encontró el entrenador con ese ID")

    def load_ent_image(self, ent_id):
        image_data = self.db_manager.get_image_from_db("entrenadores", "IDEntrenadores", ent_id, "FotoEntrenador")
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

    def cargar_lista_entrenadores(self):
        try:
            for item in self.view.treeview.get_children():
                self.view.treeview.delete(item)

            result = self.db_manager.execute_procedure('sp_LeerTodosEntrenadores')
            if result:
                for ent in result:
                    self.view.treeview.insert('', 'end', values=(
                        ent[0], ent[1], ent[2], ent[3], ent[4], str(ent[5]) if ent[5] else "",
                        ent[6], ent[7] if ent[7] else "", ent[8] if ent[8] else "",
                        ent[9] if ent[9] else "", ent[10], str(ent[11]) if ent[11] else "",
                        ent[12] if ent[12] else "", ent[13] if ent[13] else "", ent[14]
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la lista: {e}")

    def save_entrenador(self):
        if not validate_text_length(self.view.Nombres.get(), 2, 50):
            messagebox.showerror("Error", "Los nombres deben tener entre 2 y 50 caracteres")
            return

        if not validate_text_length(self.view.Apellidos.get(), 2, 50):
            messagebox.showerror("Error", "Los apellidos deben tener entre 2 y 50 caracteres")
            return

        if not validate_special_chars(self.view.Nombres.get()) or not validate_special_chars(self.view.Apellidos.get()):
            messagebox.showerror("Error", "Los nombres o apellidos contienen caracteres no permitidos")
            return

        try:
            params = [
                int(self.view.CodigoEmpleado.get()),
                self.view.Nombres.get(),
                self.view.Apellidos.get(),
                int(self.view.DocumentoIdentidad.get()),
                self.view.FechaNacimiento.get_date(),
                self.view.FormacionDeportiva.get(),
                self.view.Certificaciones.get() if self.view.Certificaciones.get() else None,
                self.view.Especialidad.get() if self.view.Especialidad.get() else None,
                self.view.Experiencia.get() if self.view.Experiencia.get() else None,
                self.view.EquiposACargo.get(),
                self.view.HorarioAsignado.get(),
                self.view.MetodoTrabajo.get() if self.view.MetodoTrabajo.get() else None,
                self.view.EvaluacionResultado.get() if self.view.EvaluacionResultado.get() else None,
                self.view.Disponibilidad.get()
            ]

            if self.db_manager.execute_procedure('sp_CrearEntrenador', params):
                messagebox.showinfo("Éxito", "Entrenador guardado correctamente")

                ent_id = self.get_last_ent_id()
                if ent_id and self.image_manager.current_image_path:
                    self.image_manager.save_image_to_db(self.db_manager, "entrenadores", ent_id, "FotoEntrenador")

                self.clear_form()
                self.cargar_lista_entrenadores()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def get_last_ent_id(self):
        try:
            result = self.db_manager.execute_procedure('sp_ObtenerUltimoEntrenador')
            if result and len(result) > 0:
                return result[0][0]
        except:
            pass
        return None

    def update_entrenador(self):
        if not self.view.IDEntrenadores.get():
            messagebox.showwarning("Advertencia", "Primero busque el entrenador que desea actualizar")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea actualizar este entrenador?"):
            return

        try:
            params = [
                int(self.view.IDEntrenadores.get()),
                int(self.view.CodigoEmpleado.get()),
                self.view.Nombres.get(),
                self.view.Apellidos.get(),
                int(self.view.DocumentoIdentidad.get()),
                self.view.FechaNacimiento.get_date(),
                self.view.FormacionDeportiva.get(),
                self.view.Certificaciones.get() if self.view.Certificaciones.get() else None,
                self.view.Especialidad.get() if self.view.Especialidad.get() else None,
                self.view.Experiencia.get() if self.view.Experiencia.get() else None,
                self.view.EquiposACargo.get(),
                self.view.HorarioAsignado.get(),
                self.view.MetodoTrabajo.get() if self.view.MetodoTrabajo.get() else None,
                self.view.EvaluacionResultado.get() if self.view.EvaluacionResultado.get() else None,
                self.view.Disponibilidad.get()
            ]

            if self.db_manager.execute_procedure('sp_ActualizarEntrenador', params):
                if self.image_manager.current_image_path:
                    self.image_manager.save_image_to_db(
                        self.db_manager, "entrenadores",
                        int(self.view.IDEntrenadores.get()), "FotoEntrenador"
                    )

                messagebox.showinfo("Éxito", "Entrenador actualizado correctamente")
                self.cargar_lista_entrenadores()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")

    def delete_entrenador(self):
        if not self.view.IDEntrenadores.get():
            messagebox.showwarning("Advertencia", "Primero busque el entrenador que desea eliminar")
            return

        if messagebox.askyesno("Confirmar",
                               "¿Está seguro de que desea eliminar este entrenador?\nEsta acción no se puede deshacer."):
            if self.db_manager.execute_procedure('sp_EliminarEntrenador', [int(self.view.IDEntrenadores.get())]):
                messagebox.showinfo("Éxito", "Entrenador eliminado correctamente")
                self.clear_form()
                self.cargar_lista_entrenadores()

    def clear_form(self):
        for widget in [self.view.IDEntrenadores, self.view.CodigoEmpleado, self.view.Nombres, self.view.Apellidos,
                       self.view.DocumentoIdentidad, self.view.FormacionDeportiva, self.view.Certificaciones,
                       self.view.Especialidad, self.view.Experiencia, self.view.EquiposACargo,
                       self.view.HorarioAsignado,
                       self.view.MetodoTrabajo, self.view.EvaluacionResultado]:
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

        self.view.Disponibilidad.set("Disponible")
        self.view.image_label.configure(image='')
        self.view.image_label.image = None
        self.image_manager.current_image_path = None

    def load_ent_image_dialog(self):
        self.image_manager.load_image(self.view.image_label)

    def apply_ent_image_filter(self, filter_type):
        photo, filtered_image = self.image_manager.apply_filter(filter_type, self.view.image_label)
        if photo and filtered_image:
            pass