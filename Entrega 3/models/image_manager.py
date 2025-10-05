from PIL import Image, ImageTk, ImageFilter
from tkinter import filedialog, messagebox
import io
import os

class ImageManager:
    def __init__(self):
        self.current_image_path = None
        self.current_image_data = None
        self.original_image_data = None

    def load_image(self, image_label, max_size=(300, 300)):
        """Carga y muestra una imagen"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("GIF", "*.gif"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                # Validar tamaño del archivo (máximo 5MB)
                file_size = os.path.getsize(file_path)
                if file_size > 5 * 1024 * 1024:
                    messagebox.showerror("Error", "La imagen no puede ser mayor a 5MB")
                    return

                # Cargar y procesar imagen
                image = Image.open(file_path)
                self.original_image_data = image.copy()

                # Crear una imagen de fondo del tamaño exacto que queremos
                background = Image.new('RGB', (300, 300), (240, 240, 240))

                # Redimensionar manteniendo la relación de aspecto
                image.thumbnail((280, 280), Image.Resampling.LANCZOS)

                # Calcular posición para centrar la imagen
                x = (300 - image.width) // 2
                y = (300 - image.height) // 2

                # Pegar la imagen en el centro del fondo
                background.paste(image, (x, y))

                # Convertir a formato compatible con tkinter
                photo = ImageTk.PhotoImage(background)
                image_label.configure(image=photo)
                image_label.image = photo

                self.current_image_path = file_path
                self.current_image_data = background

                messagebox.showinfo("Éxito", "Imagen cargada correctamente")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def apply_filter(self, filter_type, image_label, max_size=(300, 300)):
        """Aplica filtros a la imagen y actualiza la visualización"""
        if not self.current_image_data and not self.original_image_data:
            messagebox.showwarning("Advertencia", "Primero cargue una imagen")
            return None, None

        try:
            # Usar la imagen original si está disponible, sino la actual
            base_image = self.original_image_data if self.original_image_data else self.current_image_data

            if filter_type == "BLUR":
                filtered_image = base_image.filter(ImageFilter.BLUR)
            elif filter_type == "SHARPEN":
                filtered_image = base_image.filter(ImageFilter.SHARPEN)
            elif filter_type == "CONTOUR":
                filtered_image = base_image.filter(ImageFilter.CONTOUR)
            elif filter_type == "EMBOSS":
                filtered_image = base_image.filter(ImageFilter.EMBOSS)
            else:
                filtered_image = base_image

            # Crear fondo del tamaño fijo para visualización consistente
            background = Image.new('RGB', (300, 300), (240, 240, 240))
            display_image = filtered_image.copy()
            display_image.thumbnail((280, 280), Image.Resampling.LANCZOS)
            x = (300 - display_image.width) // 2
            y = (300 - display_image.height) // 2
            background.paste(display_image, (x, y))

            # Convertir para tkinter
            photo = ImageTk.PhotoImage(background)

            # Actualizar la visualización
            image_label.configure(image=photo)
            image_label.image = photo

            # Guardar la imagen filtrada como current (sin fondo para procesamiento)
            self.current_image_data = filtered_image

            return photo, filtered_image

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtro: {e}")
            return None, None

    def save_image_to_db(self, db_manager, table_name, record_id, image_field_name):
        """Guarda la imagen actual en la base de datos"""
        if not self.current_image_data or not record_id:
            messagebox.showwarning("Advertencia", "Primero cargue una imagen y seleccione un registro")
            return False

        try:
            # Guardar la imagen actual en un buffer
            img_byte_arr = io.BytesIO()

            # Determinar el formato basado en la ruta o usar PNG por defecto
            if self.current_image_path:
                format = 'JPEG' if self.current_image_path.lower().endswith(('.jpg', '.jpeg')) else 'PNG'
            else:
                format = 'PNG'

            self.current_image_data.save(img_byte_arr, format=format)
            img_byte_arr = img_byte_arr.getvalue()

            cursor = db_manager.connection.cursor()

            # Usar los nombres correctos de las columnas ID según la tabla
            if table_name == "competiciones":
                query = f"UPDATE {table_name} SET {image_field_name} = %s WHERE ID_Competiciones = %s"
            elif table_name == "entrenadores":
                query = f"UPDATE {table_name} SET {image_field_name} = %s WHERE ID_Entrenadores = %s"
            elif table_name == "miembros":
                query = f"UPDATE {table_name} SET {image_field_name} = %s WHERE ID_Miembros = %s"
            elif table_name == "entrenamientos":
                query = f"UPDATE {table_name} SET {image_field_name} = %s WHERE ID_Entrenamientos = %s"
            else:
                query = f"UPDATE {table_name} SET {image_field_name} = %s WHERE ID = %s"

            cursor.execute(query, (img_byte_arr, record_id))
            db_manager.connection.commit()
            cursor.close()

            messagebox.showinfo("Éxito", "Imagen guardada en la base de datos correctamente")
            return True

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar imagen en BD: {e}")
            return False