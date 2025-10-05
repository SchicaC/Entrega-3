# Sistema de Gestión - Club Atletas Unidos

Sistema CRUD completo desarrollado en Python para la gestión integral de un club deportivo, con interfaz gráfica moderna y funcionalidades avanzadas.

## Características Destacadas

### Gestión Completa de Datos
- **CRUD Completo**: Crear, Leer, Actualizar y Eliminar registros
- **Cuatro Módulos Principales**:
  - Competiciones: Gestión de eventos y torneos
  - Entrenadores: Administración del personal técnico  
  - Miembros: Control de socios y atletas
  - Entrenamientos: Planificación de sesiones deportivas

### Gestión de Imágenes Avanzada
- Carga y visualización de imágenes para cada registro
- Filtros aplicables: Blur, Enfocar, Contorno, Emboss
- Almacenamiento seguro en base de datos
- Validación de tamaño (máximo 5MB)

### Exportación Profesional
- Exportación a Excel (.xlsx) con filtros aplicables
- Exportación a PDF (.pdf) con diseño profesional
- Filtros por fecha y categoría
- Reportes personalizables y listos para impresión

### Validaciones y Seguridad
- Validación de formato de email
- Control de caracteres especiales peligrosos
- Validación de longitud de textos
- Entradas numéricas validadas

## Instalación y Configuración

### Prerrequisitos
```bash
pip install mysql-connector-python
pip install Pillow
pip install openpyxl
pip install reportlab
pip install tkcalendar