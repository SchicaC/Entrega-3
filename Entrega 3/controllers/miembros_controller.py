import tkinter as tk
from tkinter import messagebox
from models.validators import validate_numeric_input, validate_text_length, validate_special_chars, validate_email
from models.image_manager import ImageManager
from utils.export import export_to_excel, export_to_pdf, export_with_filters
from views.miembros_view import MiembrosView


class MiembrosController:
    def __init__(self, parent, db_manager):
        self.db_manager = db_manager
        self.view = MiembrosView(parent)
        self.image_manager = ImageManager()
        self.setup_events()

    def setup_events(self):
        self.view.btn_buscar.config(command=self.buscar_miembro)
        self.view.btn_guardar.config(command=self.save_miembro)
        self.view.btn_actualizar.config(command=self.update_miembro)
        self.view.btn_eliminar.config(command=self.delete_miembro)
        self.view.btn_limpiar.config(command=self.clear_form)
        self.view.btn_cargar_lista.config(command=self.cargar_lista_miembros)

        self.view.btn_cargar_imagen.config(command=self.load_mem_image_dialog)
        self.view.btn_blur.config(command=lambda: self.apply_mem_image_filter("BLUR"))
        self.view.btn_enfocar.config(command=lambda: self.apply_mem_image_filter("SHARPEN"))

        self.view.btn_export_excel.config(
            command=lambda: export_to_excel(self.view.treeview, "miembros.xlsx")
        )
        self.view.btn_export_pdf.config(
            command=lambda: export_to_pdf(self.view.treeview, "Reporte Miembros", "miembros.pdf", self.db_manager)
        )
        self.view.btn_filtros.config(
            command=lambda: export_with_filters(self.view.treeview, "Miembros")
        )

    def buscar_miembro(self):
        id_miembro = self.view.IDMiembros.get()
        if not id_miembro:
            messagebox.showwarning("Advertencia", "Por favor ingrese el ID del miembro")
            return

        if not id_miembro.isdigit():
            messagebox.showerror("Error", "El ID debe ser un número válido")
            return

        result = self.db_manager.execute_procedure('sp_LeerMiembro', [int(id_miembro)])
        if result and len(result) > 0:
            mem = result[0]
            self.clear_form()

            self.view.IDMiembros.insert(0, str(mem[0]))
            self.view.NumeroSocio.insert(0, str(mem[1]))
            self.view.Nombres.insert(0, mem[2])
            self.view.Apellidos.insert(0, mem[3])
            self.view.DocumentoIdentidad.insert(0, str(mem[4]))
            self.view.FechaNacimiento.set_date(mem[5]) if mem[5] else None
            self.view.Direccion.insert(0, mem[6] if mem[6] else "")
            self.view.Telefono.insert(0, mem[7] if mem[7] else "")
            self.view.CorreoElectronico.insert(0, mem[8])
            self.view.FechaIngreso.set_date(mem[9]) if mem[9] else None
            self.view.Categoria.insert(0, mem[10])
            self.view.ModalidadDeportiva.insert(0, mem[11])
            self.view.Nivel.insert(0, mem[12])
            self.view.HistorialMedico.insert(0, mem[13] if mem[13] else "")
            self.view.CuotaAsignada.insert(0, mem[14])
            self.view.Estado.set(mem[15])
            self.view.IDEquipos.insert(0, str(mem[16]) if mem[16] else "")
            self.view.FechaPago.set_date(mem[17]) if mem[17] else None
            self.view.FechaVencimiento.set_date(mem[18]) if mem[18] else None
            self.view.EstadoPago.set(mem[19] if mem[19] else "")

            self.load_mem_image(mem[0])
        else:
            messagebox.showinfo("No encontrado", "No se encontró el miembro con ese ID")

    def load_mem_image(self, mem_id):
        image_data = self.db_manager.get_image_from_db("miembros", "IDMiembros", mem_id, "FotoMiembro")
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

    def cargar_lista_miembros(self):
        try:
            for item in self.view.treeview.get_children():
                self.view.treeview.delete(item)

            result = self.db_manager.execute_procedure('sp_LeerTodosMiembros')
            if result:
                for mem in result:
                    self.view.treeview.insert('', 'end', values=(
                        mem[0], mem[1], mem[2], mem[3], mem[4], str(mem[5]) if mem[5] else "",
                        mem[6] if mem[6] else "", mem[7] if mem[7] else "", mem[8],
                        str(mem[9]) if mem[9] else "", mem[10], mem[11], mem[12],
                        mem[13] if mem[13] else "", mem[14], mem[15], mem[16] if mem[16] else "",
                        str(mem[17]) if mem[17] else "", str(mem[18]) if mem[18] else "",
                        mem[19] if mem[19] else ""
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la lista: {e}")

    def save_miembro(self):
        if not validate_text_length(self.view.Nombres.get(), 2, 50):
            messagebox.showerror("Error", "Los nombres deben tener entre 2 y 50 caracteres")
            return

        if not validate_text_length(self.view.Apellidos.get(), 2, 50):
            messagebox.showerror("Error", "Los apellidos deben tener entre 2 y 50 caracteres")
            return

        if not validate_special_chars(self.view.Nombres.get()) or not validate_special_chars(self.view.Apellidos.get()):
            messagebox.showerror("Error", "Los nombres o apellidos contienen caracteres no permitidos")
            return

        if self.view.CorreoElectronico.get() and not validate_email(self.view.CorreoElectronico.get()):
            messagebox.showerror("Error", "El formato del email no es válido")
            return

        try:
            params = [
                int(self.view.NumeroSocio.get()),
                self.view.Nombres.get(),
                self.view.Apellidos.get(),
                int(self.view.DocumentoIdentidad.get()),
                self.view.FechaNacimiento.get_date(),
                self.view.Direccion.get() if self.view.Direccion.get() else None,
                self.view.Telefono.get() if self.view.Telefono.get() else None,
                self.view.CorreoElectronico.get(),
                self.view.FechaIngreso.get_date(),
                self.view.Categoria.get(),
                self.view.ModalidadDeportiva.get(),
                self.view.Nivel.get(),
                self.view.HistorialMedico.get() if self.view.HistorialMedico.get() else None,
                self.view.CuotaAsignada.get(),
                self.view.Estado.get(),
                int(self.view.IDEquipos.get()) if self.view.IDEquipos.get() else None,
                self.view.FechaPago.get_date() if self.view.FechaPago.get() else None,
                self.view.FechaVencimiento.get_date() if self.view.FechaVencimiento.get() else None,
                self.view.EstadoPago.get() if self.view.EstadoPago.get() else None
            ]

            result = self.db_manager.execute_procedure('sp_CrearMiembro', params)

            if result:
                messagebox.showinfo("Éxito", "Miembro guardado correctamente")

                mem_id = self.get_last_mem_id()
                if mem_id and self.image_manager.current_image_path:
                    self.image_manager.save_image_to_db(self.db_manager, "miembros", mem_id, "FotoMiembro")

                self.clear_form()
                self.cargar_lista_miembros()
            else:
                if not self.db_manager.connection or not self.db_manager.connection.is_connected():
                    messagebox.showinfo("Reconectando", "Reconectando a la base de datos...")
                    if self.db_manager.connect():
                        result = self.db_manager.execute_procedure('sp_CrearMiembro', params)
                        if result:
                            messagebox.showinfo("Éxito", "Miembro guardado correctamente después de reconectar")
                            self.clear_form()
                            self.cargar_lista_miembros()
                        else:
                            messagebox.showerror("Error", "No se pudo guardar el miembro después de reconectar")
                    else:
                        messagebox.showerror("Error", "No se pudo reconectar a la base de datos")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {e}")

    def get_last_mem_id(self):
        try:
            result = self.db_manager.execute_procedure('sp_ObtenerUltimoMiembro')
            if result and len(result) > 0:
                return result[0][0]
        except:
            pass
        return None

    def update_miembro(self):
        if not self.view.IDMiembros.get():
            messagebox.showwarning("Advertencia", "Primero busque el miembro que desea actualizar")
            return

        if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea actualizar este miembro?"):
            return

        try:
            params = [
                int(self.view.IDMiembros.get()),
                int(self.view.NumeroSocio.get()),
                self.view.Nombres.get(),
                self.view.Apellidos.get(),
                int(self.view.DocumentoIdentidad.get()),
                self.view.FechaNacimiento.get_date(),
                self.view.Direccion.get() if self.view.Direccion.get() else None,
                self.view.Telefono.get() if self.view.Telefono.get() else None,
                self.view.CorreoElectronico.get(),
                self.view.FechaIngreso.get_date(),
                self.view.Categoria.get(),
                self.view.ModalidadDeportiva.get(),
                self.view.Nivel.get(),
                self.view.HistorialMedico.get() if self.view.HistorialMedico.get() else None,
                self.view.CuotaAsignada.get(),
                self.view.Estado.get(),
                int(self.view.IDEquipos.get()) if self.view.IDEquipos.get() else None,
                self.view.FechaPago.get_date() if self.view.FechaPago.get() else None,
                self.view.FechaVencimiento.get_date() if self.view.FechaVencimiento.get() else None,
                self.view.EstadoPago.get() if self.view.EstadoPago.get() else None
            ]

            if self.db_manager.execute_procedure('sp_ActualizarMiembro', params):
                if self.image_manager.current_image_path:
                    self.image_manager.save_image_to_db(
                        self.db_manager, "miembros",
                        int(self.view.IDMiembros.get()), "FotoMiembro"
                    )

                messagebox.showinfo("Éxito", "Miembro actualizado correctamente")
                self.cargar_lista_miembros()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {e}")

    def delete_miembro(self):
        if not self.view.IDMiembros.get():
            messagebox.showwarning("Advertencia", "Primero busque el miembro que desea eliminar")
            return

        if messagebox.askyesno("Confirmar",
                               "¿Está seguro de que desea eliminar este miembro?\nEsta acción no se puede deshacer."):
            if self.db_manager.execute_procedure('sp_EliminarMiembro', [int(self.view.IDMiembros.get())]):
                messagebox.showinfo("Éxito", "Miembro eliminado correctamente")
                self.clear_form()
                self.cargar_lista_miembros()

    def clear_form(self):
        for widget in [self.view.IDMiembros, self.view.NumeroSocio, self.view.Nombres, self.view.Apellidos,
                       self.view.DocumentoIdentidad, self.view.Direccion, self.view.Telefono,
                       self.view.CorreoElectronico, self.view.Categoria, self.view.ModalidadDeportiva,
                       self.view.Nivel, self.view.HistorialMedico, self.view.CuotaAsignada, self.view.IDEquipos]:
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

        self.view.Estado.set("Activo")
        self.view.EstadoPago.set("Pendiente")
        self.view.image_label.configure(image='')
        self.view.image_label.image = None
        self.image_manager.current_image_path = None

    def load_mem_image_dialog(self):
        self.image_manager.load_image(self.view.image_label)

    def apply_mem_image_filter(self, filter_type):
        photo, filtered_image = self.image_manager.apply_filter(filter_type, self.view.image_label)
        if photo and filtered_image:
            pass