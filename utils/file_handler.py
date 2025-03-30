import json
import os
from datetime import datetime
from tkinter import filedialog, messagebox

class FileHandler:
    """Clase para manejar operaciones de archivos."""
    
    @staticmethod
    def get_autosave_dir():
        """
        Obtiene el directorio para guardar archivos de autoguardado.
        
        Returns:
            str: Ruta al directorio de autoguardado
        """
        # Ruta base del proyecto (donde está main.py)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        autosave_dir = os.path.join(base_dir, "autosave")
        
        # Crear directorio si no existe
        if not os.path.exists(autosave_dir):
            os.makedirs(autosave_dir)
            
        return autosave_dir
    
    @staticmethod
    def autosave(guide_data):
        """
        Guarda automáticamente el estado actual en un archivo temporal.
        
        Args:
            guide_data (dict): Datos de la guía a guardar
        """
        autosave_dir = FileHandler.get_autosave_dir()
        
        # Crear nombre de archivo basado en la zona y nivel, o usar timestamp
        metadata = guide_data.get('metadata', {})
        if metadata.get('zone') and metadata.get('level_range'):
            base_name = f"{metadata['level_range'].replace('-', '_')}_{metadata['zone'].replace(' ', '_')}"
        else:
            base_name = f"autosave_{datetime.now().strftime('%Y%m%d')}"
        
        filename = os.path.join(autosave_dir, f"{base_name}.autosave.json")
        
        # Añadir timestamp al guide_data
        guide_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Guardar en el archivo
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(guide_data, f, indent=2)
            print(f"Autosalvado completado: {filename}")
            return True
        except Exception as e:
            print(f"Error en autosalvado: {str(e)}")
            return False
    
    @staticmethod
    def load_last_autosave():
        """
        Carga el último archivo de autoguardado disponible.
        
        Returns:
            dict or None: Datos de la guía cargada o None si no hay autosaves
        """
        autosave_dir = FileHandler.get_autosave_dir()
        
        # Buscar el archivo de autoguardado más reciente
        autosave_files = [f for f in os.listdir(autosave_dir) if f.endswith('.autosave.json')]
        if not autosave_files:
            messagebox.showinfo("Autoguardado", "No hay archivos de autoguardado disponibles.")
            return None
        
        # Ordenar por fecha de modificación (más reciente primero)
        latest_file = max(
            [os.path.join(autosave_dir, f) for f in autosave_files],
            key=os.path.getmtime
        )
        
        # Cargar el archivo
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                guide_data = json.load(f)
            
            timestamp = guide_data.get("timestamp", "desconocido")
            messagebox.showinfo("Autoguardado", f"Guía cargada desde autoguardado\nÚltima modificación: {timestamp}")
            return guide_data
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el autoguardado: {str(e)}")
            return None
    
    @staticmethod
    def save_guide(guide_data):
        """
        Guarda los datos de la guía en un archivo JSON.
        
        Args:
            guide_data (dict): Datos de la guía a guardar
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        metadata = guide_data.get('metadata', {})
        
        # Determinar nombre de archivo predeterminado
        if metadata.get('zone') and metadata.get('level_range'):
            default_filename = f"{metadata['level_range'].replace('-', '_')}_{metadata['zone'].replace(' ', '_')}.json"
        else:
            default_filename = "guia_phermuth_data.json"
            
        # Solicitar nombre de archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if not filename:
            return False  # Usuario canceló la operación
        
        # Guardar en el archivo
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(guide_data, f, indent=2)
            messagebox.showinfo("Éxito", f"Datos de la guía guardados en {filename}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la guía: {str(e)}")
            return False
    
    @staticmethod
    def load_guide():
        """
        Carga los datos de una guía desde un archivo JSON.
        
        Returns:
            dict or None: Datos de la guía cargada o None si hubo un error
        """
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return None  # Usuario canceló la operación
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                guide_data = json.load(f)
            
            messagebox.showinfo("Éxito", f"Guía cargada desde {filename}")
            return guide_data
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la guía: {str(e)}")
            return None
    
    @staticmethod
    def save_lua_to_file(lua_code, guide_zone, guide_level_range):
        """
        Guarda el código Lua generado en un archivo.
        
        Args:
            lua_code (str): Código Lua a guardar
            guide_zone (str): Zona de la guía
            guide_level_range (str): Rango de niveles de la guía
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        # Crear nombre de archivo basado en la información de la guía
        if guide_zone and guide_level_range:
            default_filename = f"{guide_level_range.replace('-', '_')}_{guide_zone.replace(' ', '_')}.lua"
        else:
            default_filename = "guia_phermuth_guide.lua"
        
        # Solicitar nombre de archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".lua",
            filetypes=[("Lua files", "*.lua"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if not filename:
            return False  # Usuario canceló la operación
        
        # Guardar en el archivo
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(lua_code)
            messagebox.showinfo("Éxito", f"Guía guardada en {filename}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")
            return False
    
    @staticmethod
    def export_quest_db(quest_history):
        """
        Exporta la base de datos de misiones a un archivo JSON.
        
        Args:
            quest_history (dict): Historial de misiones a exportar
            
        Returns:
            bool: True si se exportó correctamente, False en caso contrario
        """
        if not quest_history:
            messagebox.showinfo("Exportar", "No hay misiones en el historial para exportar.")
            return False
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="guia_phermuth_quest_db.json"
        )
        
        if not filename:
            return False  # Usuario canceló la operación
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(quest_history, f, indent=2)
            messagebox.showinfo("Éxito", f"Base de datos de misiones exportada a {filename}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar la base de datos: {str(e)}")
            return False
    
    @staticmethod
    def import_quest_db():
        """
        Importa una base de datos de misiones desde un archivo JSON.
        
        Returns:
            dict or None: Base de datos importada o None si hubo un error
        """
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return None  # Usuario canceló la operación
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_db = json.load(f)
            
            messagebox.showinfo("Éxito", f"Base de datos de misiones importada desde {filename}\nImportadas {len(imported_db)} misiones.")
            return imported_db
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar la base de datos: {str(e)}")
            return None