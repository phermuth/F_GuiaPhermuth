import tkinter as tk
from tkinter import ttk

class QuestListFrame:
    """Frame para la lista de pasos de la guía."""
    
    def __init__(self, parent, on_edit_step):
        """
        Inicializa el frame de la lista de pasos.
        
        Args:
            parent: Widget padre donde se colocará este frame
            on_edit_step: Función callback para editar un paso
        """
        # Crear frame principal
        self.frame = ttk.LabelFrame(parent, text="Quest Steps")
        
        # Definir columnas del treeview
        columns = ("step", "action", "quest", "questid", "note", "coords", "class", "race", "zone", "objid")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        # Establecer cabeceras de columnas
        self.tree.heading("step", text="#")
        self.tree.heading("action", text="Action")
        self.tree.heading("quest", text="Quest Name")
        self.tree.heading("questid", text="QID")
        self.tree.heading("note", text="Note")
        self.tree.heading("coords", text="Coords")
        self.tree.heading("class", text="Class")
        self.tree.heading("race", text="Race")
        self.tree.heading("zone", text="Zone")
        self.tree.heading("objid", text="ObjID")
        
        # Establecer anchos de columnas
        self.tree.column("step", width=30, anchor="center")
        self.tree.column("action", width=50, anchor="center")
        self.tree.column("quest", width=200)
        self.tree.column("questid", width=50, anchor="center")
        self.tree.column("note", width=200)
        self.tree.column("coords", width=100, anchor="center")
        self.tree.column("class", width=80, anchor="center")
        self.tree.column("race", width=80, anchor="center")
        self.tree.column("zone", width=100)
        self.tree.column("objid", width=50, anchor="center")
        
        # Añadir barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar treeview y barra de desplazamiento
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Vincular evento de doble clic para editar paso
        self.tree.bind("<Double-1>", on_edit_step)

        # Configurar estilos de tags
        self.tree.tag_configure("editing", background="#FFFFCC")
    
    def pack(self, **kwargs):
        """
        Empaqueta el frame en su contenedor padre.
        
        Args:
            **kwargs: Argumentos para el método pack
        """
        self.frame.pack(**kwargs)
    
    def refresh(self, quest_steps):
        """
        Actualiza el treeview con los pasos actuales de la guía.
        
        Args:
            quest_steps (list): Lista de pasos de la guía
        """
        # Limpiar elementos existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Repoblar con datos actualizados
        for i, step in enumerate(quest_steps):
            self.tree.insert("", "end", values=(
                i + 1,
                step['action'],
                step['quest_name'],
                step['quest_id'],
                step['note'],
                step['coords'],
                step['class'],
                step['race'],
                step['zone'],
                step['obj_id']
            ))
    
    def get_selected_index(self):
        """
        Obtiene el índice del paso seleccionado.
        
        Returns:
            int or None: Índice del paso seleccionado o None si no hay selección
        """
        selected_items = self.tree.selection()
        if not selected_items:
            return None
        
        item = selected_items[0]
        values = self.tree.item(item, "values")
        return int(values[0]) - 1  # Restar 1 porque la UI muestra índices desde 1
    
    def select_by_index(self, index):
        """
        Selecciona un paso por su índice.
        
        Args:
            index (int): Índice del paso a seleccionar
        """
        # El índice en la UI es +1 respecto al índice en la lista
        ui_index = index + 1
        
        # Buscar el ítem con ese índice
        for item in self.tree.get_children():
            if int(self.tree.item(item, "values")[0]) == ui_index:
                self.tree.selection_set(item)
                self.tree.see(item)
                break

    def highlight_editing_row(self, index):
        """
        Destaca visualmente la fila que se está editando.
        
        Args:
            index (int): Índice del paso que se está editando
        """
        # Restaurar el estilo normal para todas las filas
        for item in self.tree.get_children():
            self.tree.item(item, tags=())
        
        # Si se proporciona un índice válido, aplicar estilo de edición
        if index is not None:
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                if values and int(values[0]) - 1 == index:  # Ajuste por índice UI vs índice real
                    self.tree.item(item, tags=("editing",))
                    break
        
        # Definir el estilo para filas en edición (color de fondo amarillo claro)
        self.tree.tag_configure("editing", background="#FFFFCC")