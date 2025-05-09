class QuestHistory:
    """Clase para gestionar el historial de misiones."""
    
    def __init__(self):
        """Inicializa un nuevo historial de misiones vacío."""
        self.quest_history = {}
    
    def add_quest(self, quest_id, quest_name, action, coords_x=None, coords_y=None, quest_class=None):
        """
        Agrega o actualiza una misión en el historial.
        
        Args:
            quest_id (str): ID de la misión
            quest_name (str): Nombre de la misión
            action (str): Acción realizada (A, C, T, etc.)
            coords_x (str, optional): Coordenada X. Defaults to None.
            coords_y (str, optional): Coordenada Y. Defaults to None.
            quest_class (str, optional): Clase asociada a la misión. Defaults to None.
        """
        if not quest_id:
            return
            
        if quest_id not in self.quest_history:
            # Crear nuevo registro de misión
            self.quest_history[quest_id] = {
                'name': quest_name,
                'actions_used': [action],
                'coords': {},
                'class': quest_class
            }
        else:
            # Actualizar nombre de la misión
            self.quest_history[quest_id]['name'] = quest_name
            
            # Agregar acción si no está ya
            if action not in self.quest_history[quest_id]['actions_used']:
                self.quest_history[quest_id]['actions_used'].append(action)
            
            # Actualizar clase si se proporciona y no existía antes
            if quest_class and not self.quest_history[quest_id].get('class'):
                self.quest_history[quest_id]['class'] = quest_class
        
        # Guardar coordenadas para esta acción si se proporcionan
        if coords_x and coords_y:
            if 'coords' not in self.quest_history[quest_id]:
                self.quest_history[quest_id]['coords'] = {}
            
            self.quest_history[quest_id]['coords'][action] = {
                'x': coords_x,
                'y': coords_y
            }
    
    def get_quest_name(self, quest_id):
        """
        Obtiene el nombre de una misión del historial.
        
        Args:
            quest_id (str): ID de la misión
            
        Returns:
            str: Nombre de la misión o cadena vacía si no existe
        """
        if quest_id in self.quest_history:
            return self.quest_history[quest_id]['name']
        return ""
    
    def get_quest_class(self, quest_id):
        """
        Obtiene la clase asociada a una misión del historial.
        
        Args:
            quest_id (str): ID de la misión
            
        Returns:
            str: Clase de la misión o None si no existe o no tiene clase asociada
        """
        if quest_id in self.quest_history and 'class' in self.quest_history[quest_id]:
            return self.quest_history[quest_id]['class']
        return None
    
    def get_quest_coords(self, quest_id, action=None):
        """
        Obtiene las coordenadas para una misión específica y acción.
        Si no se especifica acción, intenta obtener coordenadas relevantes.
        Por ejemplo, para 'T' buscará coordenadas de 'A' si no existen para 'T'.
        
        Args:
            quest_id (str): ID de la misión
            action (str, optional): Acción específica. Defaults to None.
            
        Returns:
            tuple: Par (coord_x, coord_y) o (None, None) si no hay datos
        """
        if not quest_id or quest_id not in self.quest_history:
            return None, None
        
        if 'coords' not in self.quest_history[quest_id]:
            return None, None
        
        coords_data = self.quest_history[quest_id]['coords']
        
        # Si se especificó acción, intentar obtener coordenadas para esa acción
        if action and action in coords_data:
            return coords_data[action]['x'], coords_data[action]['y']
        
        # Para 'T', usar coordenadas de 'A' si existen
        if action == 'T' and 'A' in coords_data:
            return coords_data['A']['x'], coords_data['A']['y']
        
        # Si no se encontraron coordenadas específicas, retornar None
        return None, None
    
    def suggest_next_action(self, quest_id):
        """
        Sugiere la siguiente acción para una misión basándose en su historial.
        
        Args:
            quest_id (str): ID de la misión
            
        Returns:
            str: Acción sugerida o None si no hay sugerencia
        """
        if not quest_id or quest_id not in self.quest_history:
            return None
        
        actions_used = self.quest_history[quest_id]['actions_used']
        
        # Flujo típico de misión: A -> C -> T
        if 'A' in actions_used and 'C' not in actions_used:
            return 'C'
        elif 'C' in actions_used and 'T' not in actions_used:
            return 'T'
        
        return None
    
    def has_quest(self, quest_id):
        """
        Verifica si una misión está en el historial.
        
        Args:
            quest_id (str): ID de la misión
            
        Returns:
            bool: True si la misión está en el historial, False en caso contrario
        """
        return quest_id in self.quest_history
    
    def get_all_quests(self):
        """
        Obtiene todas las misiones del historial.
        
        Returns:
            dict: Historial completo de misiones
        """
        return self.quest_history
    
    def update_from_dict(self, quest_history_dict):
        """
        Actualiza el historial desde un diccionario.
        
        Args:
            quest_history_dict (dict): Diccionario con datos de historial
        """
        if quest_history_dict:
            self.quest_history.update(quest_history_dict)
    
    def clear(self):
        """Limpia el historial de misiones."""
        self.quest_history = {}