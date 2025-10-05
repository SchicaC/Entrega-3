from models.database import DatabaseManager
from views.main_window import MainWindow
from controllers.competiciones_controller import CompeticionesController
from controllers.entrenadores_controller import EntrenadoresController
from controllers.miembros_controller import MiembrosController
from controllers.entrenamientos_controller import EntrenamientosController


class MainController:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.view = MainWindow()
        self.setup_controllers()

    def setup_controllers(self):
        self.view.setup_ui()

        # Inicializar controladores para cada módulo
        self.competiciones_controller = CompeticionesController(
            self.view.get_tab("competiciones"),
            self.db_manager
        )

        self.entrenadores_controller = EntrenadoresController(
            self.view.get_tab("entrenadores"),
            self.db_manager
        )

        self.miembros_controller = MiembrosController(
            self.view.get_tab("miembros"),
            self.db_manager
        )

        self.entrenamientos_controller = EntrenamientosController(
            self.view.get_tab("entrenamientos"),
            self.db_manager
        )

        # Configurar cierre de aplicación
        self.view.set_close_callback(self.on_closing)

        # Conectar a la base de datos después de un delay
        self.view.root.after(1000, self.conectar_bd_inicio)

    def conectar_bd_inicio(self):
        if self.db_manager.connect():
            self.view.update_info_label(
                "Sistema CRUD - Club Atletas Unidos | ✓ Conectado a la base de datos",
                "green"
            )
        else:
            self.view.update_info_label(
                "Sistema CRUD - Club Atletas Unidos | ✗ Error de conexión a la base de datos",
                "red"
            )

    def on_closing(self):
        self.db_manager.disconnect()
        self.view.root.destroy()

    def run(self):
        self.view.mainloop()