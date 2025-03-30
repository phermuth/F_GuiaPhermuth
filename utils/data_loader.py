import json
import os

class DataLoader:
    """Clase para cargar datos predefinidos desde archivos JSON."""
    
    @staticmethod
    def get_resource_path(filename):
        """
        Obtiene la ruta completa a un archivo de recursos.
        
        Args:
            filename (str): Nombre del archivo en la carpeta resources
            
        Returns:
            str: Ruta completa al archivo
        """
        # Ruta base del proyecto (donde está main.py)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'resources', filename)
    
    @staticmethod
    def load_json_resource(filename):
        """
        Carga un archivo JSON desde la carpeta de recursos.
        
        Args:
            filename (str): Nombre del archivo JSON (sin la ruta)
            
        Returns:
            dict or list: Datos cargados desde el archivo JSON
        """
        resource_path = DataLoader.get_resource_path(filename)
        
        try:
            with open(resource_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading resource {filename}: {str(e)}")
            # Devolver valores predeterminados según el tipo de recurso
            if filename == 'action_types.json':
                return {"A": "Accept Quest"}
            elif filename in ['zone_list.json', 'class_list.json', 'race_list.json']:
                return [""]
            return {}

    @staticmethod
    def load_action_types():
        """Carga los tipos de acciones desde el archivo JSON."""
        return DataLoader.load_json_resource('action_types.json')
    
    @staticmethod
    def load_zone_list():
        """Carga la lista de zonas desde el archivo JSON."""
        return DataLoader.load_json_resource('zone_list.json')
    
    @staticmethod
    def load_class_list():
        """Carga la lista de clases desde el archivo JSON."""
        return DataLoader.load_json_resource('class_list.json')
    
    @staticmethod
    def load_race_list():
        """Carga la lista de razas desde el archivo JSON."""
        return DataLoader.load_json_resource('race_list.json')