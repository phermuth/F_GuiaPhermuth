import tkinter as tk
from tkinter import ttk

class FormFrame:
    """Frame para el formulario de pasos de la guía."""
    
    def __init__(self, parent, on_add_step, on_clear_form, on_generate_lua, on_delete_selected, on_move_up, on_move_down):
        """
        Inicializa el frame del formulario.
        
        Args:
            parent: Widget padre donde se colocará este frame
            on_add_step: Función callback para añadir un paso
            on_clear_form: Función callback para limpiar el formulario
            on_generate_lua: Función callback para generar código Lua
            on_delete_selected: Función callback para eliminar paso seleccionado
            on_move_up: Función callback para mover paso hacia arriba
            on_move_down: Función callback para mover paso hacia abajo
        """
        # Variables
        self.action_var = tk.StringVar(value="A")
        self.quest_name_var = tk.StringVar()
        self.quest_id_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.coord_x_var = tk.StringVar()
        self.coord_y_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.zone_var = tk.StringVar()
        self.race_var = tk.StringVar()
        self.obj_id_var = tk.StringVar()
        
        # Almacenar callbacks
        self.on_add_step = on_add_step
        self.on_clear_form = on_clear_form
        self.on_generate_lua = on_generate_lua
        self.on_delete_selected = on_delete_selected
        self.on_move_up = on_move_up
        self.on_move_down = on_move_down
        
        # Diccionario para tipos de acciones
        self.action_types = {}
        
        # Crear frame principal
        self.frame = ttk.LabelFrame(parent, text="Quest Step Information")
        
        # Acción y Nombre de Misión
        row1 = ttk.Frame(self.frame)
        row1.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(row1, text="Action:").pack(side="left", padx=5)
        self.action_combo = ttk.Combobox(row1, textvariable=self.action_var, width=5)
        self.action_combo.pack(side="left", padx=5)
        
        # Etiqueta para descripción de acción
        self.action_desc_label = ttk.Label(row1, text="", font=("", 8, "italic"))
        self.action_desc_label.pack(side="left", padx=5)
        
        # Eventos para combo de acción
        self.action_combo.bind("<<ComboboxSelected>>", self.update_action_description)
        self.action_combo.bind("<<ComboboxSelected>>", self.action_changed, add="+")
        
        ttk.Label(row1, text="Quest ID:").pack(side="left", padx=5)
        self.quest_id_entry = ttk.Entry(row1, textvariable=self.quest_id_var, width=8)
        self.quest_id_entry.pack(side="left", padx=5)
        
        ttk.Label(row1, text="Quest Name:").pack(side="left", padx=5)
        self.quest_name_entry = ttk.Entry(row1, textvariable=self.quest_name_var, width=40)
        self.quest_name_entry.pack(side="left", padx=5)
        
        # Nota
        row2 = ttk.Frame(self.frame)
        row2.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(row2, text="Note:").pack(side="left", padx=5)
        ttk.Entry(row2, textvariable=self.note_var, width=80).pack(side="left", padx=5, expand=True, fill="x")
        
        # Coordenadas, Clase, Zona
        row3 = ttk.Frame(self.frame)
        row3.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(row3, text="Coordinates:").pack(side="left", padx=5)
        
        # Entradas de coordenadas X e Y separadas
        coord_frame = ttk.Frame(row3)
        coord_frame.pack(side="left", padx=5)
        
        # Coordenada X
        ttk.Label(coord_frame, text="X:").pack(side="left")
        ttk.Entry(coord_frame, textvariable=self.coord_x_var, width=7).pack(side="left", padx=2)
        
        # Coordenada Y
        ttk.Label(coord_frame, text="Y:").pack(side="left", padx=2)
        ttk.Entry(coord_frame, textvariable=self.coord_y_var, width=7).pack(side="left")
        
        ttk.Label(row3, text="Class:").pack(side="left", padx=5)
        self.class_combo = ttk.Combobox(row3, textvariable=self.class_var, width=10)
        self.class_combo.pack(side="left", padx=5)
        
        ttk.Label(row3, text="Race:").pack(side="left", padx=5)
        self.race_combo = ttk.Combobox(row3, textvariable=self.race_var, width=10)
        self.race_combo.pack(side="left", padx=5)
        
        ttk.Label(row3, text="Zone:").pack(side="left", padx=5)
        self.zone_combo = ttk.Combobox(row3, textvariable=self.zone_var, width=15)
        self.zone_combo.pack(side="left", padx=5)
        
        ttk.Label(row3, text="Object ID:").pack(side="left", padx=5)
        ttk.Entry(row3, textvariable=self.obj_id_var, width=8).pack(side="left", padx=5)
        
        # Botones
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill="x", padx=5, pady=10)
        
        self.add_button = ttk.Button(self.button_frame, text="Add Step", command=self.add_step)
        self.add_button.pack(side="left", padx=5)
        
        ttk.Button(self.button_frame, text="Clear Form", command=on_clear_form).pack(side="left", padx=5)
        
        # Botón para cancelar la edición (inicialmente oculto)
        self.cancel_edit_button = ttk.Button(self.button_frame, text="Cancel Edit", command=on_clear_form)
        # No empaquetamos todavía - se mostrará solo durante la edición
        
        ttk.Button(self.button_frame, text="Generate Lua", command=on_generate_lua).pack(side="right", padx=5)
        ttk.Button(self.button_frame, text="Delete Selected", command=on_delete_selected).pack(side="right", padx=5)
        ttk.Button(self.button_frame, text="Move Up", command=on_move_up).pack(side="right", padx=5)
        ttk.Button(self.button_frame, text="Move Down", command=on_move_down).pack(side="right", padx=5)
        
        # Configurar eventos
        self.quest_id_entry.bind("<FocusOut>", self.quest_id_changed)
        self.quest_id_entry.bind("<Return>", self.quest_id_changed)
        self.quest_name_entry.bind("<FocusOut>", self.quest_name_changed)
        self.quest_name_entry.bind("<Return>", self.quest_name_changed)
    
    def set_quest_changed_callback(self, callback):
        """
        Establece la función callback para cuando cambia el ID de misión.
        
        Args:
            callback: Función a llamar cuando cambia el ID de misión
        """
        self.quest_changed_callback = callback
    
    def set_coords_callback(self, callback):
        """
        Establece la función callback para obtener coordenadas de una misión.
        
        Args:
            callback: Función a llamar para obtener coordenadas
        """
        self.get_coords_callback = callback
    
    def pack(self, **kwargs):
        """
        Empaqueta el frame en su contenedor padre.
        
        Args:
            **kwargs: Argumentos para el método pack
        """
        self.frame.pack(**kwargs)
    
    def set_action_types(self, action_types):
        """
        Establece los tipos de acciones disponibles.
        
        Args:
            action_types (dict): Diccionario de tipos de acciones
        """
        self.action_types = action_types
        self.action_combo['values'] = list(action_types.keys())
        self.update_action_description()
    
    def set_class_list(self, classes):
        """
        Establece la lista de clases disponibles.
        
        Args:
            classes (list): Lista de clases
        """
        self.class_combo['values'] = classes
    
    def set_zone_list(self, zones):
        """
        Establece la lista de zonas disponibles.
        
        Args:
            zones (list): Lista de zonas
        """
        self.zone_combo['values'] = zones
    
    def set_race_list(self, races):
        """
        Establece la lista de razas disponibles.
        
        Args:
            races (list): Lista de razas
        """
        self.race_combo['values'] = races
    
    def update_action_description(self, event=None):
        """
        Actualiza la descripción de la acción seleccionada.
        
        Args:
            event: Evento que desencadenó la actualización (opcional)
        """
        action = self.action_var.get()
        if action in self.action_types:
            self.action_desc_label.config(text=self.action_types[action])
        else:
            self.action_desc_label.config(text="")
    
    def action_changed(self, event=None):
        """
        Maneja el evento de cambio en la acción.
        Si la acción cambia a "T" y hay un ID de misión, buscar coordenadas.
        
        Args:
            event: Evento que desencadenó el cambio (opcional)
        """
        # Verificar si tenemos el callback para obtener coordenadas
        if not hasattr(self, 'get_coords_callback'):
            return
        
        action = self.action_var.get()
        quest_id = self.quest_id_var.get().strip()
        
        # Si es una acción de entregar misión (T) y tenemos un ID, intentar recuperar coordenadas
        if action == 'T' and quest_id:
            self.try_load_quest_coords(quest_id, action)
    
    def quest_id_changed(self, event=None):
        """
        Maneja el evento de cambio en el ID de misión.
        
        Args:
            event: Evento que desencadenó el cambio (opcional)
        """
        if hasattr(self, 'quest_changed_callback'):
            quest_id = self.quest_id_var.get().strip()
            self.quest_changed_callback(quest_id)
            
            # Intentar cargar coordenadas si la acción actual es 'T'
            action = self.action_var.get()
            if action == 'T' and quest_id:
                self.try_load_quest_coords(quest_id, action)
    
    def try_load_quest_coords(self, quest_id, action):
        """
        Intenta cargar coordenadas para una misión y acción específicas.
        
        Args:
            quest_id (str): ID de la misión
            action (str): Tipo de acción
        """
        if hasattr(self, 'get_coords_callback'):
            # Llamar al callback para obtener coordenadas
            coord_x, coord_y = self.get_coords_callback(quest_id, action)
            
            # Si se encontraron coordenadas, establecerlas en el formulario
            if coord_x and coord_y:
                self.coord_x_var.set(coord_x)
                self.coord_y_var.set(coord_y)
    
    def quest_name_changed(self, event=None):
        """
        Maneja el evento de cambio en el nombre de misión.
        
        Args:
            event: Evento que desencadenó el cambio (opcional)
        """
        # Por ahora no hace nada, pero podría implementarse funcionalidad adicional
        pass
    
    def add_step(self):
        """Recopila los datos del formulario y llama al callback para añadir un paso."""
        # Combinar coordenadas X e Y si ambas están presentes
        coords = ""
        if self.coord_x_var.get() and self.coord_y_var.get():
            coords = f"{self.coord_x_var.get()}, {self.coord_y_var.get()}"
        
        # Recopilar datos del formulario
        step_data = {
            'action': self.action_var.get(),
            'quest_name': self.quest_name_var.get().strip(),
            'quest_id': self.quest_id_var.get().strip(),
            'note': self.note_var.get(),
            'coords': coords,
            'coord_x': self.coord_x_var.get(),
            'coord_y': self.coord_y_var.get(),
            'class': self.class_var.get(),
            'race': self.race_var.get(),
            'zone': self.zone_var.get(),
            'obj_id': self.obj_id_var.get()
        }
        
        # Llamar al callback con los datos
        self.on_add_step(step_data)
    
    def clear_form(self):
        """Limpia el formulario pero mantiene la acción actual."""
        action = self.action_var.get()
        self.quest_name_var.set("")
        self.quest_id_var.set("")
        self.note_var.set("")
        self.coord_x_var.set("")
        self.coord_y_var.set("")
        self.class_var.set("")
        self.race_var.set("")
        self.zone_var.set("")
        self.obj_id_var.set("")
        self.action_var.set(action)  # Restaurar la acción
    
    def set_form_data(self, step_data):
        """
        Establece los datos del formulario a partir de un paso.
        
        Args:
            step_data (dict): Datos del paso
        """
        self.action_var.set(step_data['action'])
        self.quest_name_var.set(step_data['quest_name'])
        self.quest_id_var.set(step_data['quest_id'])
        self.note_var.set(step_data['note'])
        
        # Manejar coordenadas
        if 'coord_x' in step_data and 'coord_y' in step_data and step_data['coord_x'] and step_data['coord_y']:
            self.coord_x_var.set(step_data['coord_x'])
            self.coord_y_var.set(step_data['coord_y'])
        elif step_data.get('coords'):
            coords_parts = step_data['coords'].split(',')
            if len(coords_parts) == 2:
                self.coord_x_var.set(coords_parts[0].strip())
                self.coord_y_var.set(coords_parts[1].strip())
        else:
            self.coord_x_var.set("")
            self.coord_y_var.set("")
        
        self.class_var.set(step_data['class'])
        self.race_var.set(step_data['race'])
        self.zone_var.set(step_data['zone'])
        self.obj_id_var.set(step_data['obj_id'])
    
    def set_next_action(self, action):
        """
        Establece la siguiente acción sugerida.
        
        Args:
            action (str): Acción a establecer
        """
        if action:
            self.action_var.set(action)
            self.update_action_description()
            
            # Verificar si debemos cargar coordenadas para esta nueva acción
            quest_id = self.quest_id_var.get().strip()
            if action == 'T' and quest_id:
                self.try_load_quest_coords(quest_id, action)

    def set_edit_mode(self, is_editing):
        """
        Cambia la interfaz entre modo de edición y modo de adición.
        
        Args:
            is_editing (bool): True si estamos en modo de edición, False en caso contrario
        """
        if is_editing:
            # Cambiar a modo de edición
            self.add_button.config(text="Update Step")
            # Mostrar botón de cancelar
            self.cancel_edit_button.pack(side="left", padx=5, after=self.add_button)
        else:
            # Cambiar a modo de adición
            self.add_button.config(text="Add Step")
            # Ocultar botón de cancelar
            self.cancel_edit_button.pack_forget()