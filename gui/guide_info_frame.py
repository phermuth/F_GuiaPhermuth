import tkinter as tk
from tkinter import ttk

class GuideInfoFrame:
    """Frame para la información general de la guía."""
    
    def __init__(self, parent):
        """
        Inicializa el frame de información de la guía.
        
        Args:
            parent: Widget padre donde se colocará este frame
        """
        # Variables
        self.guide_zone_var = tk.StringVar()
        self.guide_level_range_var = tk.StringVar()
        self.guide_next_zone_var = tk.StringVar()
        self.guide_faction_var = tk.StringVar(value="Horde")
        
        # Crear frame principal
        self.frame = ttk.LabelFrame(parent, text="Guide Information")
        
        # Zona y rango de niveles
        zone_frame = ttk.Frame(self.frame)
        zone_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(zone_frame, text="Zone:").pack(side="left", padx=5)
        ttk.Entry(zone_frame, textvariable=self.guide_zone_var, width=20).pack(side="left", padx=5)
        
        ttk.Label(zone_frame, text="Level Range:").pack(side="left", padx=5)
        ttk.Entry(zone_frame, textvariable=self.guide_level_range_var, width=10).pack(side="left", padx=5)
        
        ttk.Label(zone_frame, text="Next Zone:").pack(side="left", padx=5)
        ttk.Entry(zone_frame, textvariable=self.guide_next_zone_var, width=20).pack(side="left", padx=5)
        
        ttk.Label(zone_frame, text="Faction:").pack(side="left", padx=5)
        faction_combo = ttk.Combobox(zone_frame, textvariable=self.guide_faction_var, width=10)
        faction_combo['values'] = ('Horde', 'Alliance', 'Both')
        faction_combo.pack(side="left", padx=5)
    
    def pack(self, **kwargs):
        """
        Empaqueta el frame en su contenedor padre.
        
        Args:
            **kwargs: Argumentos para el método pack
        """
        self.frame.pack(**kwargs)
    
    def get_metadata(self):
        """
        Obtiene los metadatos de la guía.
        
        Returns:
            tuple: (zone, level_range, next_zone, faction)
        """
        return (
            self.guide_zone_var.get(),
            self.guide_level_range_var.get(),
            self.guide_next_zone_var.get(),
            self.guide_faction_var.get()
        )
    
    def set_metadata(self, zone, level_range, next_zone, faction):
        """
        Establece los metadatos de la guía.
        
        Args:
            zone (str): Zona de la guía
            level_range (str): Rango de niveles
            next_zone (str): Zona siguiente
            faction (str): Facción (Horde, Alliance, Both)
        """
        self.guide_zone_var.set(zone)
        self.guide_level_range_var.set(level_range)
        self.guide_next_zone_var.set(next_zone)
        self.guide_faction_var.set(faction)