import tkinter as tk
from tkinter import messagebox

from gui.guide_info_frame import GuideInfoFrame
from gui.form_frame import FormFrame
from gui.quest_list_frame import QuestListFrame
from gui.dialogs import CodeViewDialog, QuestHistoryDialog, show_action_types_dialog, confirm_new_guide

from models.guide import Guide
from models.quest import QuestHistory

from utils.data_loader import DataLoader
from utils.file_handler import FileHandler
from utils.lua_generator import LuaGenerator

class GuiaPhermuthCreator:
    """Clase principal de la aplicación GuiaPhermuth Quest Guide Creator."""
    
    def __init__(self, root):
        """
        Inicializa la aplicación.
        
        Args:
            root: Widget raíz de Tkinter
        """
        self.root = root
        self.root.title("GuiaPhermuth Quest Guide Creator")
        self.root.geometry("1000x800")
        
        # Inicializar modelos
        self.guide = Guide()
        self.quest_history = QuestHistory()
        
        # Variable para rastrear el paso que se está editando
        self.editing_step_index = None
        
        # Añadir protocolo para manejar cierre de la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Crear menú
        self.create_menu()
        
        # Crear widgets principales
        self.guide_info_frame = GuideInfoFrame(self.root)
        self.guide_info_frame.pack(fill="x", padx=10, pady=10)
        
        self.form_frame = FormFrame(
            self.root,
            on_add_step=self.add_step,
            on_clear_form=self.clear_form,
            on_generate_lua=self.generate_lua,
            on_delete_selected=self.delete_selected,
            on_move_up=lambda: self.move_step(-1),
            on_move_down=lambda: self.move_step(1)
        )
        self.form_frame.set_quest_changed_callback(self.quest_id_changed)
        
        # Establecer callback para obtener coordenadas
        self.form_frame.set_coords_callback(self.get_quest_coords)
        
        self.form_frame.pack(fill="x", padx=10, pady=10)
        
        self.quest_list_frame = QuestListFrame(
            self.root,
            on_edit_step=self.edit_step
        )
        self.quest_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cargar datos predefinidos
        self.load_predefined_data()

    def on_close(self):
        """Maneja el evento de cierre de la aplicación."""
        # Verificar si hay una edición en progreso
        if self.editing_step_index is not None:
            if not messagebox.askyesno("Edición en progreso",
                                    "Hay una edición en progreso. ¿Descartar los cambios y salir?"):
                return
        
        # Preguntar si desea guardar la guía antes de salir
        if self.guide.get_all_steps():
            if messagebox.askyesno("Guardar antes de salir",
                                "¿Deseas guardar la guía antes de salir?"):
                self.save_guide()
        
        # Cerrar la aplicación
        self.root.destroy()
    
    def create_menu(self):
        """Crea la barra de menú de la aplicación."""
        menubar = tk.Menu(self.root)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Guide", command=self.new_guide)
        file_menu.add_command(label="Save Guide", command=self.save_guide)
        file_menu.add_command(label="Load Guide", command=self.load_guide)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        file_menu.add_separator()
        file_menu.add_command(label="Load Last Autosave", command=self.load_last_autosave)
        file_menu.add_command(label="Force Autosave Now", command=self.force_autosave)
        
        # Menú de misiones
        quest_menu = tk.Menu(menubar, tearoff=0)
        quest_menu.add_command(label="View Quest History", command=self.view_quest_history)
        quest_menu.add_command(label="Export Quest Database", command=self.export_quest_db)
        quest_menu.add_command(label="Import Quest Database", command=self.import_quest_db)
        
        # Menú de ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Action Types", command=self.show_action_types)
        
        # Añadir menús a la barra de menú
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Quests", menu=quest_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def load_predefined_data(self):
        """Carga los datos predefinidos para los combos."""
        # Cargar tipos de acciones
        action_types = DataLoader.load_action_types()
        self.form_frame.set_action_types(action_types)
        
        # Cargar listas de clases, zonas y razas
        self.form_frame.set_class_list(DataLoader.load_class_list())
        self.form_frame.set_zone_list(DataLoader.load_zone_list())
        self.form_frame.set_race_list(DataLoader.load_race_list())
    
    def add_step(self, step_data):
        """
        Añade o actualiza un paso en la guía.
        
        Args:
            step_data (dict): Datos del paso a añadir o actualizar
        """
        # Validar campos requeridos
        if not step_data['action'] or not step_data['quest_name']:
            messagebox.showerror("Error", "Action and Quest Name are required fields")
            return
        
        index_to_select = None
        
        if self.editing_step_index is not None:
            # Estamos editando un paso existente
            # Actualizar en el modelo Guide
            self.guide.update_step(self.editing_step_index, step_data)
            
            # Guardamos el índice para seleccionarlo después
            index_to_select = self.editing_step_index
            
            # Restablecer el índice de edición
            self.editing_step_index = None
            
            # Cambiar la UI al modo de adición
            self.form_frame.set_edit_mode(False)
        else:
            # Añadir nuevo paso al modelo Guide
            self.guide.add_step(step_data)
            # Seleccionaremos el último paso
            index_to_select = len(self.guide.get_all_steps()) - 1
        
        # Actualizar historial de misiones (en ambos casos)
        quest_id = step_data['quest_id']
        if quest_id:
            self.quest_history.add_quest(
                quest_id, 
                step_data['quest_name'],
                step_data['action'],
                step_data.get('coord_x'),
                step_data.get('coord_y')
            )
        
        # Actualizar vista
        self.quest_list_frame.refresh(self.guide.get_all_steps())

        # Después de refrescar la lista, quitar el destacado de edición
        self.quest_list_frame.highlight_editing_row(None)
        
        # Seleccionar el paso que acabamos de añadir/actualizar
        if index_to_select is not None:
            self.quest_list_frame.select_by_index(index_to_select)
        
        # Limpiar formulario
        self.clear_form()
        
        # Sugerir siguiente acción si aplica
        if quest_id:
            next_action = self.quest_history.suggest_next_action(quest_id)
            if next_action:
                self.form_frame.set_next_action(next_action)
        
        # Autoguardar
        self.autosave()
    
    def get_quest_coords(self, quest_id, action):
        """
        Obtiene coordenadas para una misión y acción específicas.
        
        Args:
            quest_id (str): ID de la misión
            action (str): Tipo de acción
            
        Returns:
            tuple: Coordenadas (x, y) o (None, None) si no existen
        """
        return self.quest_history.get_quest_coords(quest_id, action)
    
    def clear_form(self):
        """Limpia el formulario y cancela cualquier edición en progreso."""
        self.form_frame.clear_form()
        
        # Si estábamos editando, cancelar la edición
        if self.editing_step_index is not None:
            self.editing_step_index = None
            self.form_frame.update_add_button_text("Add Step")
    
    def generate_lua(self):
        """Genera y muestra el código Lua."""
        # Si hay una edición en progreso, advertir al usuario
        if self.editing_step_index is not None:
            if not messagebox.askyesno("Edición en progreso",
                                    "Hay una edición en progreso. ¿Deseas continuar sin guardar los cambios?"):
                return
        
        # Verificar que hay pasos para generar
        if not self.guide.get_all_steps():
            messagebox.showerror("Error", "No quest steps to generate")
            return
        
        # Obtener metadatos de la guía
        zone, level_range, next_zone, faction = self.guide_info_frame.get_metadata()
        
        # Generar nombre de la guía
        if zone and level_range:
            guide_name = f"{zone} ({level_range})"
            if next_zone and '-' in level_range:
                next_zone_name = f"{next_zone} ({level_range.split('-')[1]}-XX)"
            else:
                next_zone_name = next_zone
        else:
            guide_name = "Custom Guide"
            next_zone_name = next_zone if next_zone else "nil"
        
        # Generar código Lua
        lua_code = LuaGenerator.generate_lua(
            self.guide.get_all_steps(),
            guide_name,
            next_zone_name,
            faction
        )
        
        # Mostrar el código generado
        dialog = CodeViewDialog(
            self.root,
            "Generated Lua Code",
            lua_code,
            on_copy=lambda code: self.root.clipboard_clear() or self.root.clipboard_append(code),
            on_save=lambda code: FileHandler.save_lua_to_file(code, zone, level_range),
            on_close=lambda: None
        )
    
    def delete_selected(self):
        """Elimina el paso seleccionado."""
        # Si estamos editando, preguntar si quiere cancelar la edición primero
        if self.editing_step_index is not None:
            if not messagebox.askyesno("Edición en progreso",
                                    "Hay una edición en progreso. ¿Descartar los cambios?"):
                return
            
            # Cancelar la edición
            self.editing_step_index = None
            self.form_frame.set_edit_mode(False)
            self.clear_form()
        
        selected_index = self.quest_list_frame.get_selected_index()
        if selected_index is None:
            return
        
        # Confirmar eliminación
        if not messagebox.askyesno("Confirmar eliminación",
                                "¿Estás seguro de que deseas eliminar este paso?"):
            return
        
        # Eliminar del modelo
        self.guide.remove_step(selected_index)
        
        # Actualizar vista
        self.quest_list_frame.refresh(self.guide.get_all_steps())
        
        # Autoguardar
        self.autosave()
    
    def move_step(self, direction):
        """
        Mueve un paso hacia arriba o hacia abajo en la guía.
        
        Args:
            direction (int): Dirección de movimiento (-1 para arriba, 1 para abajo)
        """
        # Si estamos editando y se intenta mover otro paso, advertir al usuario
        if self.editing_step_index is not None:
            messagebox.showwarning("Edición en progreso",
                                "Por favor, termina la edición actual antes de mover pasos.")
            return
        
        selected_index = self.quest_list_frame.get_selected_index()
        if selected_index is None:
            return
        
        # Mover en el modelo
        new_index = self.guide.move_step(selected_index, direction)
        if new_index is None:
            return
        
        # Actualizar vista
        self.quest_list_frame.refresh(self.guide.get_all_steps())
        
        # Seleccionar el ítem movido
        self.quest_list_frame.select_by_index(new_index)
        
        # Autoguardar
        self.autosave()
    
    def edit_step(self, event):
        """
        Maneja el evento para editar un paso.
        
        Args:
            event: Evento que desencadenó la edición
        """
        # Verificar si ya estamos editando algo
        if self.editing_step_index is not None:
            # Preguntar al usuario si quiere descartar la edición actual
            if not messagebox.askyesno("Edición en progreso", 
                                    "Ya estás editando un paso. ¿Descartar los cambios actuales?"):
                return
        
        selected_index = self.quest_list_frame.get_selected_index()
        if selected_index is None:
            return
        
        # Obtener datos del paso
        step_data = self.guide.get_step(selected_index)
        if not step_data:
            return
        
        # Establecer datos en el formulario
        self.form_frame.set_form_data(step_data)
        
        # Guardar el índice del paso que estamos editando
        self.editing_step_index = selected_index
        
        # Cambiar la UI al modo de edición
        self.form_frame.set_edit_mode(True)
        
        # Seleccionar y destacar visualmente el paso que se está editando
        self.quest_list_frame.select_by_index(selected_index)
        self.quest_list_frame.highlight_editing_row(selected_index)

    def clear_form(self):
        """Limpia el formulario y cancela cualquier edición en progreso."""
        self.form_frame.clear_form()
        
        # Si estábamos editando, cancelar la edición
        if self.editing_step_index is not None:
            self.editing_step_index = None
            self.form_frame.set_edit_mode(False)

        # Quitar el destacado de edición
        self.quest_list_frame.highlight_editing_row(None)
    
    def quest_id_changed(self, quest_id):
        """
        Maneja el evento de cambio en el ID de misión.
        
        Args:
            quest_id (str): ID de la misión cambiada
        """
        # Verificar si está en el historial
        if quest_id and self.quest_history.has_quest(quest_id):
            # Auto-completar nombre de la misión
            quest_name = self.quest_history.get_quest_name(quest_id)
            if quest_name:
                self.form_frame.quest_name_var.set(quest_name)
            
            # Sugerir siguiente acción
            next_action = self.quest_history.suggest_next_action(quest_id)
            if next_action:
                self.form_frame.set_next_action(next_action)
    
    def new_guide(self):
        """Crea una nueva guía."""
        # Si hay una edición en progreso, preguntar si quiere descartarla
        if self.editing_step_index is not None:
            if not messagebox.askyesno("Edición en progreso",
                                    "Hay una edición en progreso. ¿Descartar los cambios?"):
                return
            
            # Cancelar la edición
            self.editing_step_index = None
            self.form_frame.set_edit_mode(False)
        
        if not confirm_new_guide(self.root):
            return
        
        # Limpiar modelos
        self.guide.clear()
        
        # Limpiar formularios
        self.guide_info_frame.set_metadata("", "", "", "Horde")
        self.form_frame.clear_form()
        
        # Actualizar vista
        self.quest_list_frame.refresh([])
    
    def save_guide(self):
        """Guarda la guía actual."""
        if not self.guide.get_all_steps():
            messagebox.showerror("Error", "No quest steps to save")
            return
        
        # Actualizar metadatos de la guía
        zone, level_range, next_zone, faction = self.guide_info_frame.get_metadata()
        self.guide.set_metadata(zone, level_range, next_zone, faction)
        
        # Crear diccionario con todos los datos
        guide_data = self.guide.to_dict()
        guide_data["quest_history"] = self.quest_history.get_all_quests()
        
        # Guardar a archivo
        FileHandler.save_guide(guide_data)
    
    def load_guide(self):
        """Carga una guía desde un archivo."""
        # Si hay una edición en progreso, preguntar si quiere descartarla
        if self.editing_step_index is not None:
            if not messagebox.askyesno("Edición en progreso",
                                    "Hay una edición en progreso. ¿Descartar los cambios?"):
                return
            
            # Cancelar la edición
            self.editing_step_index = None
            self.form_frame.set_edit_mode(False)
        
        guide_data = FileHandler.load_guide()
        if not guide_data:
            return
        
        # Cargar en modelos
        self.guide.from_dict(guide_data)
        
        # Cargar historial si está disponible
        if "quest_history" in guide_data:
            self.quest_history.update_from_dict(guide_data["quest_history"])
        
        # Actualizar vistas
        metadata = guide_data.get("metadata", {})
        self.guide_info_frame.set_metadata(
            metadata.get("zone", ""),
            metadata.get("level_range", ""),
            metadata.get("next_zone", ""),
            metadata.get("faction", "Horde")
        )
        
        self.quest_list_frame.refresh(self.guide.get_all_steps())
    
    def autosave(self):
        """Guarda automáticamente el estado actual."""
        # Actualizar metadatos de la guía
        zone, level_range, next_zone, faction = self.guide_info_frame.get_metadata()
        self.guide.set_metadata(zone, level_range, next_zone, faction)
        
        # Crear diccionario con todos los datos
        guide_data = self.guide.to_dict()
        guide_data["quest_history"] = self.quest_history.get_all_quests()
        
        # Guardar a archivo de autoguardado
        FileHandler.autosave(guide_data)
    
    def force_autosave(self):
        """Fuerza un autoguardado manual."""
        self.autosave()
        messagebox.showinfo("Autosave", "Guide autosaved successfully.")
    
    def load_last_autosave(self):
        """Carga el último autoguardado disponible."""
        # Si hay una edición en progreso, preguntar si quiere descartarla
        if self.editing_step_index is not None:
            if not messagebox.askyesno("Edición en progreso",
                                    "Hay una edición en progreso. ¿Descartar los cambios?"):
                return
            
            # Cancelar la edición
            self.editing_step_index = None
            self.form_frame.set_edit_mode(False)
        
        guide_data = FileHandler.load_last_autosave()
        if not guide_data:
            return
        
        # Cargar en modelos
        self.guide.from_dict(guide_data)
        
        # Cargar historial si está disponible
        if "quest_history" in guide_data:
            self.quest_history.update_from_dict(guide_data["quest_history"])
        
        # Actualizar vistas
        metadata = guide_data.get("metadata", {})
        self.guide_info_frame.set_metadata(
            metadata.get("zone", ""),
            metadata.get("level_range", ""),
            metadata.get("next_zone", ""),
            metadata.get("faction", "Horde")
        )
        
        self.quest_list_frame.refresh(self.guide.get_all_steps())
    
    def view_quest_history(self):
        """Muestra el historial de misiones."""
        if not self.quest_history.get_all_quests():
            messagebox.showinfo("Quest History", "No quests in history yet.")
            return
        
        # Mostrar diálogo de historial
        dialog = QuestHistoryDialog(
            self.root,
            self.quest_history.get_all_quests(),
            on_use_selected=self.use_selected_quest
        )
    
    def use_selected_quest(self, quest_id, quest_name):
        """
        Utiliza la misión seleccionada del historial.
        
        Args:
            quest_id (str): ID de la misión
            quest_name (str): Nombre de la misión
        """
        # Establecer ID y nombre en el formulario
        self.form_frame.quest_id_var.set(quest_id)
        self.form_frame.quest_name_var.set(quest_name)
        
        # Sugerir siguiente acción
        next_action = self.quest_history.suggest_next_action(quest_id)
        if next_action:
            self.form_frame.set_next_action(next_action)
    
    def export_quest_db(self):
        """Exporta la base de datos de misiones."""
        FileHandler.export_quest_db(self.quest_history.get_all_quests())
    
    def import_quest_db(self):
        """Importa una base de datos de misiones."""
        imported_db = FileHandler.import_quest_db()
        if imported_db:
            self.quest_history.update_from_dict(imported_db)
    
    def show_about(self):
        """Muestra información sobre la aplicación."""
        messagebox.showinfo(
            "About",
            "GuiaPhermuth Quest Guide Creator\n"
            "A tool to create quest guides for the GuiaPhermuth addon."
        )
    
    def show_action_types(self):
        """Muestra información sobre los tipos de acciones."""
        action_types = DataLoader.load_action_types()
        show_action_types_dialog(self.root, action_types)