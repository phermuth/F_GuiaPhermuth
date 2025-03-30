import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import os
import json

class GuiaPhermuthCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("GuiaPhermuth Quest Guide Creator")
        self.root.geometry("1000x800")
        
        # Data storage
        self.quest_steps = []
        self.current_zone = ""
        self.next_zone = ""
        self.faction = "Horde"  # Default faction
        
        # Variables
        self.action_var = tk.StringVar(value="A")
        self.quest_name_var = tk.StringVar()
        self.quest_id_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.coords_var = tk.StringVar()  # Keep for compatibility
        self.coord_x_var = tk.StringVar()  # New X coordinate
        self.coord_y_var = tk.StringVar()  # New Y coordinate
        self.class_var = tk.StringVar()
        self.zone_var = tk.StringVar()
        self.race_var = tk.StringVar()
        self.obj_id_var = tk.StringVar()
        
        # Quest guide metadata
        self.guide_zone_var = tk.StringVar()
        self.guide_level_range_var = tk.StringVar()
        self.guide_next_zone_var = tk.StringVar()
        self.guide_faction_var = tk.StringVar(value="Horde")
        
        # Create the UI
        self.create_menu()
        self.create_guide_info_frame()
        self.create_form_frame()
        self.create_quest_list_frame()
        
        # Load default data
        self.load_action_types()
        self.load_class_list()
        self.load_zone_list()
        self.load_race_list()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Guide", command=self.new_guide)
        file_menu.add_command(label="Save Guide", command=self.save_guide)
        file_menu.add_command(label="Load Guide", command=self.load_guide)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "GuiaPhermuth Quest Guide Creator\nA tool to create quest guides for the GuiaPhermuth addon."))
        help_menu.add_command(label="Action Types", command=self.show_action_types)
        
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def create_guide_info_frame(self):
        frame = ttk.LabelFrame(self.root, text="Guide Information")
        frame.pack(fill="x", padx=10, pady=10)
        
        # Zone and level range
        zone_frame = ttk.Frame(frame)
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
        
    def create_form_frame(self):
        frame = ttk.LabelFrame(self.root, text="Quest Step Information")
        frame.pack(fill="x", padx=10, pady=10)
        
        # Action and Quest Name
        row1 = ttk.Frame(frame)
        row1.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(row1, text="Action:").pack(side="left", padx=5)
        self.action_combo = ttk.Combobox(row1, textvariable=self.action_var, width=5)
        self.action_combo.pack(side="left", padx=5)
        
        # Action description label
        self.action_desc_label = ttk.Label(row1, text="", font=("", 8, "italic"))
        self.action_desc_label.pack(side="left", padx=5)
        
        # Binding for action combo to update description
        self.action_combo.bind("<<ComboboxSelected>>", self.update_action_description)
        
        ttk.Label(row1, text="Quest Name:").pack(side="left", padx=5)
        ttk.Entry(row1, textvariable=self.quest_name_var, width=40).pack(side="left", padx=5)
        
        ttk.Label(row1, text="Quest ID:").pack(side="left", padx=5)
        ttk.Entry(row1, textvariable=self.quest_id_var, width=8).pack(side="left", padx=5)
        
        # Note
        row2 = ttk.Frame(frame)
        row2.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(row2, text="Note:").pack(side="left", padx=5)
        ttk.Entry(row2, textvariable=self.note_var, width=80).pack(side="left", padx=5, expand=True, fill="x")
        
        # Coordinates, Class, Zone
        row3 = ttk.Frame(frame)
        row3.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(row3, text="Coordinates:").pack(side="left", padx=5)
        
        # New coordinate input with X and Y separated
        coord_frame = ttk.Frame(row3)
        coord_frame.pack(side="left", padx=5)
        
        # X coordinate
        ttk.Label(coord_frame, text="X:").pack(side="left")
        self.coord_x_var = tk.StringVar()
        ttk.Entry(coord_frame, textvariable=self.coord_x_var, width=7).pack(side="left", padx=2)
        
        # Y coordinate
        ttk.Label(coord_frame, text="Y:").pack(side="left", padx=2)
        self.coord_y_var = tk.StringVar()
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
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(button_frame, text="Add Step", command=self.add_step).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Generate Lua", command=self.generate_lua).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Move Up", command=lambda: self.move_step(-1)).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Move Down", command=lambda: self.move_step(1)).pack(side="right", padx=5)
    
    def create_quest_list_frame(self):
        frame = ttk.LabelFrame(self.root, text="Quest Steps")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for quest steps
        columns = ("step", "action", "quest", "questid", "note", "coords", "class", "race", "zone", "objid")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Define column headings
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
        
        # Set column widths
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
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double click event to edit item
        self.tree.bind("<Double-1>", self.edit_step)
    
    def load_action_types(self):
        # Action types: A=Accept, C=Complete, T=Turnin, etc.
        actions = {
            "A": "Accept Quest - Accept a new quest from an NPC",
            "C": "Complete Quest - Fulfill quest objectives (kill mobs, collect items, etc.)",
            "T": "Turn in Quest - Return to quest giver to complete quest",
            "K": "Kill Mob - Kill a specific monster or NPC",
            "R": "Run to Location - Travel to a specific location",
            "H": "Use Hearthstone - Use hearthstone to return to your inn",
            "h": "Set Hearthstone - Set your hearthstone at an innkeeper",
            "G": "Grind - Kill mobs to gain XP until a specific level",
            "F": "Fly to Location - Use a flight path to travel",
            "f": "Get Flight Point - Discover a new flight master",
            "N": "Note - General information or instruction",
            "B": "Buy Item - Purchase an item from a vendor",
            "b": "Take Boat/Zeppelin - Use boat or zeppelin transport",
            "U": "Use Item - Use a specific item in your inventory",
            "P": "Pet Skill - Learn or use a hunter pet skill",
            "D": "Die and Respawn - Intentionally die to save time",
            "MAP": "Look at Map - Check the map for a location"
        }
        
        self.action_types = actions
        self.action_combo['values'] = list(actions.keys())
        
        # Update the description for the default action
        self.update_action_description()
        
    def update_action_description(self, event=None):
        action = self.action_var.get()
        if action in self.action_types:
            self.action_desc_label.config(text=self.action_types[action])
        else:
            self.action_desc_label.config(text="")
    
    def load_class_list(self):
        classes = [
            "", "Warrior", "Paladin", "Hunter", "Rogue", 
            "Priest", "Shaman", "Mage", "Warlock", "Druid"
        ]
        self.class_combo['values'] = classes
    
    def load_zone_list(self):
        zones = [
            "", "Durotar", "Mulgore", "Tirisfal Glades", "Elwynn Forest", 
            "Dun Morogh", "Teldrassil", "The Barrens", "Silverpine Forest", 
            "Westfall", "Loch Modan", "Darkshore", "Redridge Mountains", 
            "Stonetalon Mountains", "Ashenvale", "Thousand Needles",
            "Hillsbrad Foothills", "Arathi Highlands", "Stranglethorn Vale",
            "Orgrimmar", "Thunder Bluff", "Undercity", "Stormwind", "Ironforge",
            "Darnassus"
        ]
        self.zone_combo['values'] = zones
    
    def load_race_list(self):
        races = [
            "", "Human", "Dwarf", "NightElf", "Gnome", 
            "Orc", "Troll", "Tauren", "Undead"
        ]
        self.race_combo['values'] = races
    
    def add_step(self):
        # Validate required fields
        if not self.action_var.get() or not self.quest_name_var.get():
            messagebox.showerror("Error", "Action and Quest Name are required fields")
            return
        
        # Combine X and Y coordinates if provided
        coords = ""
        if self.coord_x_var.get() and self.coord_y_var.get():
            coords = f"{self.coord_x_var.get()}, {self.coord_y_var.get()}"
        
        # Gather data from form
        step_data = {
            'action': self.action_var.get(),
            'quest_name': self.quest_name_var.get(),
            'quest_id': self.quest_id_var.get(),
            'note': self.note_var.get(),
            'coords': coords,
            'coord_x': self.coord_x_var.get(),
            'coord_y': self.coord_y_var.get(),
            'class': self.class_var.get(),
            'race': self.race_var.get(),
            'zone': self.zone_var.get(),
            'obj_id': self.obj_id_var.get()
        }
        
        # Add to data structure
        self.quest_steps.append(step_data)
        
        # Add to treeview
        step_num = len(self.quest_steps)
        self.tree.insert("", "end", values=(
            step_num,
            step_data['action'],
            step_data['quest_name'],
            step_data['quest_id'],
            step_data['note'],
            step_data['coords'],
            step_data['class'],
            step_data['race'],
            step_data['zone'],
            step_data['obj_id']
        ))
        
        # Clear form for next entry
        self.clear_form()
    
    def clear_form(self):
        # Reset form fields but keep the action
        action = self.action_var.get()
        self.quest_name_var.set("")
        self.quest_id_var.set("")
        self.note_var.set("")
        self.coords_var.set("")
        self.coord_x_var.set("")
        self.coord_y_var.set("")
        self.class_var.set("")
        self.race_var.set("")
        self.zone_var.set("")
        self.obj_id_var.set("")
        self.action_var.set(action)  # Restore the action
    
    def edit_step(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        # Get the selected item values
        item = selected_items[0]
        values = self.tree.item(item, "values")
        
        # Populate form with selected item's data
        idx = int(values[0]) - 1
        step_data = self.quest_steps[idx]
        
        self.action_var.set(step_data['action'])
        self.quest_name_var.set(step_data['quest_name'])
        self.quest_id_var.set(step_data['quest_id'])
        self.note_var.set(step_data['note'])
        
        # Handle coordinates - split them if they exist
        if 'coord_x' in step_data and 'coord_y' in step_data:
            self.coord_x_var.set(step_data['coord_x'])
            self.coord_y_var.set(step_data['coord_y'])
        elif step_data['coords']:
            coords_parts = step_data['coords'].split(',')
            if len(coords_parts) == 2:
                self.coord_x_var.set(coords_parts[0].strip())
                self.coord_y_var.set(coords_parts[1].strip())
        
        self.class_var.set(step_data['class'])
        self.race_var.set(step_data['race'])
        self.zone_var.set(step_data['zone'])
        self.obj_id_var.set(step_data['obj_id'])
        
        # Delete the old entry
        self.delete_selected()
    
    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        for item in selected_items:
            values = self.tree.item(item, "values")
            idx = int(values[0]) - 1
            self.quest_steps.pop(idx)
            self.tree.delete(item)
        
        # Renumber the remaining items
        self.refresh_treeview()
    
    def move_step(self, direction):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        item = selected_items[0]
        values = self.tree.item(item, "values")
        idx = int(values[0]) - 1
        
        # Calculate new index
        new_idx = idx + direction
        if new_idx < 0 or new_idx >= len(self.quest_steps):
            return  # Out of bounds
        
        # Swap positions
        self.quest_steps[idx], self.quest_steps[new_idx] = self.quest_steps[new_idx], self.quest_steps[idx]
        
        # Refresh treeview
        self.refresh_treeview()
        
        # Select the moved item
        for item in self.tree.get_children():
            if int(self.tree.item(item, "values")[0]) == new_idx + 1:
                self.tree.selection_set(item)
                self.tree.see(item)
                break
    
    def refresh_treeview(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Repopulate with updated data
        for i, step in enumerate(self.quest_steps):
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
    
    def generate_lua(self):
        if not self.quest_steps:
            messagebox.showerror("Error", "No quest steps to generate")
            return
        
        # Make zone and level range optional
        if self.guide_zone_var.get() and self.guide_level_range_var.get():
            # Generate guide name
            guide_name = f"{self.guide_zone_var.get()} ({self.guide_level_range_var.get()})"
            if self.guide_next_zone_var.get() and '-' in self.guide_level_range_var.get():
                next_zone = f"{self.guide_next_zone_var.get()} ({self.guide_level_range_var.split('-')[1]}-XX)"
            else:
                next_zone = "nil"
        else:
            # Use placeholders if not provided
            guide_name = "Custom Guide"
            next_zone = "nil"
            
        faction = self.guide_faction_var.get()
        
        # Start building Lua code
        lua_code = f'GuiaPhermuth:RegisterGuide("{guide_name}", "{next_zone}", "{faction}",function()\n\n'
        lua_code += 'return [[\n\n'
        
        # Add quest steps
        for step in self.quest_steps:
            line = f"{step['action']} {step['quest_name']}"
            
            # Add QID if provided
            if step['quest_id']:
                line += f" |QID|{step['quest_id']}|"
            
            # Add note if provided
            if step['note']:
                line += f" |N|{step['note']}"
                
                # Add coordinates if provided
                if step['coords']:
                    line += f" ({step['coords']})"
                
                line += "|"
            
            # Add class restriction if provided
            if step['class']:
                line += f" |C|{step['class']}|"
            
            # Add race restriction if provided
            if step['race']:
                line += f" |R|{step['race']}|"
            
            # Add zone if provided
            if step['zone']:
                line += f" |Z|{step['zone']}|"
            
            # Add object ID if provided
            if step['obj_id']:
                line += f" |OBJ|{step['obj_id']}|"
            
            lua_code += line + "\n"
        
        # End Lua code
        lua_code += '\n]]\nend)\n'
        
        # Show generated code in a new window
        self.show_generated_code(lua_code)
    
    def show_generated_code(self, code):
        code_window = tk.Toplevel(self.root)
        code_window.title("Generated Lua Code")
        code_window.geometry("800x600")
        
        # Text widget for code
        text_widget = tk.Text(code_window, wrap="none")
        text_widget.pack(fill="both", expand=True)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(text_widget, orient="vertical", command=text_widget.yview)
        x_scrollbar = ttk.Scrollbar(text_widget, orient="horizontal", command=text_widget.xview)
        text_widget.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        
        # Insert code
        text_widget.insert("1.0", code)
        
        # Add buttons
        button_frame = ttk.Frame(code_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Copy to Clipboard", 
                  command=lambda: self.root.clipboard_clear() or self.root.clipboard_append(code)).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Save to File", 
                  command=lambda: self.save_to_file(code)).pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Close", 
                  command=code_window.destroy).pack(side="right", padx=5)
    
    def save_to_file(self, code):
        # Create filename based on guide info if available
        if self.guide_zone_var.get() and self.guide_level_range_var.get():
            default_filename = self.guide_level_range_var.get().replace("-", "_") + "_" + self.guide_zone_var.get().replace(" ", "_") + ".lua"
        else:
            default_filename = "guia_phermuth_guide.lua"
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".lua",
            filetypes=[("Lua files", "*.lua"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            messagebox.showinfo("Success", f"Guide saved to {filename}")
    
    def new_guide(self):
        if messagebox.askyesno("New Guide", "This will clear all current quest steps. Continue?"):
            self.quest_steps = []
            self.guide_zone_var.set("")
            self.guide_level_range_var.set("")
            self.guide_next_zone_var.set("")
            self.guide_faction_var.set("Horde")
            self.clear_form()
            self.refresh_treeview()
    
    def save_guide(self):
        if not self.quest_steps:
            messagebox.showerror("Error", "No quest steps to save")
            return
        
        # Create a dictionary with all guide data
        guide_data = {
            "metadata": {
                "zone": self.guide_zone_var.get(),
                "level_range": self.guide_level_range_var.get(),
                "next_zone": self.guide_next_zone_var.get(),
                "faction": self.guide_faction_var.get()
            },
            "steps": self.quest_steps
        }
        
        # Ask for filename
        if self.guide_zone_var.get() and self.guide_level_range_var.get():
            default_filename = self.guide_level_range_var.get().replace("-", "_") + "_" + self.guide_zone_var.get().replace(" ", "_") + ".json"
        else:
            default_filename = "guia_phermuth_data.json"
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(guide_data, f, indent=2)
            messagebox.showinfo("Success", f"Guide data saved to {filename}")
    
    def load_guide(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                guide_data = json.load(f)
            
            # Load metadata
            metadata = guide_data.get("metadata", {})
            self.guide_zone_var.set(metadata.get("zone", ""))
            self.guide_level_range_var.set(metadata.get("level_range", ""))
            self.guide_next_zone_var.set(metadata.get("next_zone", ""))
            self.guide_faction_var.set(metadata.get("faction", "Horde"))
            
            # Load steps
            self.quest_steps = guide_data.get("steps", [])
            self.refresh_treeview()
            
            messagebox.showinfo("Success", f"Guide loaded from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load guide: {str(e)}")
    
    def show_action_types(self):
        action_info = "Action Types:\n\n"
        for code, desc in self.action_types.items():
            action_info += f"{code} - {desc}\n"
        
        messagebox.showinfo("Action Types", action_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = GuiaPhermuthCreator(root)
    root.mainloop()