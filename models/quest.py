class QuestHistory:
    """Clase para gestionar el historial de misiones."""
    
    def __init__(self):
        """Inicializa un nuevo historial de misiones vacío."""
        self.quest_history = {}
    
    def add_quest(self, quest_id, quest_name, action):
        """
        Agrega o actualiza una misión en el historial.
        
        Args:
            quest_id (str): ID de la misión
            quest_name (str): Nombre de la misión
            action (str): Acción realizada (A, C, T, etc.)
        """
        if not quest_id:
            return
            
        if quest_id not in self.quest_history:
            self.quest_history[quest_id] = {
                'name': quest_name,
                'actions_used': [action]
            }
        else:
            # Actualizar nombre de la misión
            self.quest_history[quest_id]['name'] = quest_name
            
            # Agregar acción si no está ya
            if action not in self.quest_history[quest_id]['actions_used']:
                self.quest_history[quest_id]['actions_used'].append(action)
    
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