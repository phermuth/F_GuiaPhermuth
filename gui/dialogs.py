import tkinter as tk
from tkinter import ttk, messagebox

class CodeViewDialog:
    """Diálogo para mostrar código generado."""
    
    def __init__(self, parent, title, code, on_copy, on_save, on_close):
        """
        Inicializa el diálogo para mostrar código.
        
        Args:
            parent: Widget padre
            title (str): Título de la ventana
            code (str): Código a mostrar
            on_copy: Función para copiar código al portapapeles
            on_save: Función para guardar código a un archivo
            on_close: Función para cerrar el diálogo
        """
        self.parent = parent
        self.code = code
        self.on_copy = lambda: on_copy(code)
        self.on_save = lambda: on_save(code)
        self.on_close = on_close
        
        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("800x600")
        
        # Widget de texto para el código
        self.text_widget = tk.Text(self.window, wrap="none")
        self.text_widget.pack(fill="both", expand=True)
        
        # Añadir barras de desplazamiento
        y_scrollbar = ttk.Scrollbar(self.text_widget, orient="vertical", command=self.text_widget.yview)
        x_scrollbar = ttk.Scrollbar(self.text_widget, orient="horizontal", command=self.text_widget.xview)
        self.text_widget.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        
        # Insertar código
        self.text_widget.insert("1.0", code)
        
        # Añadir botones
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Copy to Clipboard", command=self.on_copy).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Save to File", command=self.on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Close", command=self.window.destroy).pack(side="right", padx=5)
        
        # Hacer el widget de texto de solo lectura
        self.text_widget.config(state="disabled")

class QuestHistoryDialog:
    """Diálogo para mostrar el historial de misiones."""
    
    def __init__(self, parent, quest_history, on_use_selected):
        """
        Inicializa el diálogo para el historial de misiones.
        
        Args:
            parent: Widget padre
            quest_history (dict): Historial de misiones
            on_use_selected: Función a llamar cuando se selecciona una misión
        """
        self.parent = parent
        self.quest_history = quest_history
        self.on_use_selected = on_use_selected
        
        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title("Quest History")
        self.window.geometry("800x500")
        
        # Crear treeview para el historial de misiones
        columns = ("id", "name", "actions", "class")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings")
        
        # Definir cabeceras de columnas
        self.tree.heading("id", text="Quest ID")
        self.tree.heading("name", text="Quest Name")
        self.tree.heading("actions", text="Actions Used")
        self.tree.heading("class", text="Class")
        
        # Establecer anchos de columnas
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=400)
        self.tree.column("actions", width=150, anchor="center")
        self.tree.column("class", width=100, anchor="center")
        
        # Añadir barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tree y scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Poblar con datos
        for quest_id, data in self.quest_history.items():
            actions_str = ", ".join(data['actions_used'])
            class_str = data.get('class', "")
            self.tree.insert("", "end", values=(quest_id, data['name'], actions_str, class_str))
            
        # Añadir botones
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Use Selected Quest", 
                command=self.use_selected_quest).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Close", 
                command=self.window.destroy).pack(side="right", padx=5)
    
    def use_selected_quest(self):
        """Utiliza la misión seleccionada del historial."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        # Obtener valores del ítem seleccionado
        item = selected_items[0]
        values = self.tree.item(item, "values")
        
        # Llamar al callback con el ID y nombre de la misión
        quest_id = values[0]
        quest_name = values[1]
        
        # Llamar al callback con el ID y nombre de la misión
        self.on_use_selected(quest_id, quest_name)
        
        # Cerrar la ventana
        self.window.destroy()

def show_action_types_dialog(parent, action_types):
    """
    Muestra un diálogo con información sobre los tipos de acciones.
    
    Args:
        parent: Widget padre
        action_types (dict): Diccionario de tipos de acciones
    """
    action_info = "Action Types:\n\n"
    for code, desc in action_types.items():
        action_info += f"{code} - {desc}\n"
    
    messagebox.showinfo("Action Types", action_info, parent=parent)

def confirm_new_guide(parent):
    """
    Solicita confirmación para crear una nueva guía.
    
    Args:
        parent: Widget padre
        
    Returns:
        bool: True si el usuario confirmó, False en caso contrario
    """
    return messagebox.askyesno("New Guide", "This will clear all current quest steps. Continue?", parent=parent)