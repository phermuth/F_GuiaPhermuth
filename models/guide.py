class Guide:
    """Clase para representar una guía completa."""
    
    def __init__(self):
        """Inicializa una nueva guía vacía."""
        # Metadatos de la guía
        self.zone = ""
        self.level_range = ""
        self.next_zone = ""
        self.faction = "Horde"  # Facción predeterminada
        
        # Pasos de la guía
        self.quest_steps = []
    
    def add_step(self, step_data):
        """
        Agrega un paso a la guía.
        
        Args:
            step_data (dict): Datos del paso a agregar
        """
        self.quest_steps.append(step_data)
    
    def remove_step(self, index):
        """
        Elimina un paso de la guía.
        
        Args:
            index (int): Índice del paso a eliminar
            
        Returns:
            bool: True si el paso se eliminó correctamente, False en caso contrario
        """
        if 0 <= index < len(self.quest_steps):
            self.quest_steps.pop(index)
            return True
        return False
    
    def move_step(self, index, direction):
        """
        Mueve un paso hacia arriba o hacia abajo en la guía.
        
        Args:
            index (int): Índice del paso a mover
            direction (int): Dirección de movimiento (-1 para arriba, 1 para abajo)
            
        Returns:
            int or None: Nuevo índice del paso o None si no se pudo mover
        """
        if not self.quest_steps:
            return None
            
        new_index = index + direction
        if 0 <= new_index < len(self.quest_steps):
            # Intercambiar pasos
            self.quest_steps[index], self.quest_steps[new_index] = self.quest_steps[new_index], self.quest_steps[index]
            return new_index
        return None
    
    def get_step(self, index):
        """
        Obtiene un paso de la guía.
        
        Args:
            index (int): Índice del paso a obtener
            
        Returns:
            dict or None: Datos del paso o None si el índice es inválido
        """
        if 0 <= index < len(self.quest_steps):
            return self.quest_steps[index]
        return None
    
    def get_all_steps(self):
        """
        Obtiene todos los pasos de la guía.
        
        Returns:
            list: Lista de pasos de la guía
        """
        return self.quest_steps
    
    def update_step(self, index, step_data):
        """
        Actualiza un paso existente.
        
        Args:
            index (int): Índice del paso a actualizar
            step_data (dict): Nuevos datos del paso
            
        Returns:
            bool: True si el paso se actualizó correctamente, False en caso contrario
        """
        if 0 <= index < len(self.quest_steps):
            self.quest_steps[index] = step_data
            return True
        return False
    
    def clear(self):
        """Limpia todos los pasos de la guía."""
        self.quest_steps = []
    
    def set_metadata(self, zone, level_range, next_zone, faction):
        """
        Establece los metadatos de la guía.
        
        Args:
            zone (str): Zona de la guía
            level_range (str): Rango de niveles
            next_zone (str): Zona siguiente
            faction (str): Facción (Horde, Alliance, Both)
        """
        self.zone = zone
        self.level_range = level_range
        self.next_zone = next_zone
        self.faction = faction
    
    def get_guide_name(self):
        """
        Obtiene el nombre de la guía basado en los metadatos.
        
        Returns:
            str: Nombre de la guía
        """
        if self.zone and self.level_range:
            return f"{self.zone} ({self.level_range})"
        return "Custom Guide"
    
    def get_next_zone_name(self):
        """
        Obtiene el nombre de la zona siguiente basado en los metadatos.
        
        Returns:
            str: Nombre de la zona siguiente o "nil" si no hay zona siguiente
        """
        if self.next_zone and '-' in self.level_range:
            level_max = self.level_range.split('-')[1]
            return f"{self.next_zone} ({level_max}-XX)"
        return "nil"
    
    def to_dict(self):
        """
        Convierte la guía a un diccionario para serialización.
        
        Returns:
            dict: Diccionario con datos de la guía
        """
        return {
            "metadata": {
                "zone": self.zone,
                "level_range": self.level_range,
                "next_zone": self.next_zone,
                "faction": self.faction
            },
            "steps": self.quest_steps
        }
    
    def from_dict(self, guide_data):
        """
        Carga la guía desde un diccionario.
        
        Args:
            guide_data (dict): Diccionario con datos de la guía
        """
        if not guide_data:
            return
            
        # Cargar metadatos
        metadata = guide_data.get("metadata", {})
        self.zone = metadata.get("zone", "")
        self.level_range = metadata.get("level_range", "")
        self.next_zone = metadata.get("next_zone", "")
        self.faction = metadata.get("faction", "Horde")
        
        # Cargar pasos
        self.quest_steps = guide_data.get("steps", [])