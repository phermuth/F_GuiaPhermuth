class LuaGenerator:
    """Clase para generar código Lua a partir de los datos de la guía."""
    
    @staticmethod
    def generate_lua(quest_steps, guide_name, next_zone, faction):
        """
        Genera código Lua a partir de los datos de la guía.
        
        Args:
            quest_steps (list): Lista de pasos de la guía
            guide_name (str): Nombre de la guía
            next_zone (str): Zona siguiente
            faction (str): Facción (Horde, Alliance, Both)
            
        Returns:
            str: Código Lua generado
        """
        # Determinar el nombre de la guía y la zona siguiente
        if not guide_name:
            guide_name = "Custom Guide"
        
        if not next_zone or next_zone == "":
            next_zone = "nil"
        
        # Inicio del código Lua
        lua_code = f'GuiaPhermuth:RegisterGuide("{guide_name}", "{next_zone}", "{faction}",function()\n\n'
        lua_code += 'return [[\n\n'
        
        # Agregar pasos de la guía
        for step in quest_steps:
            line = f"{step['action']} {step['quest_name']}"
            
            # Agregar ID de misión si se proporciona
            if step['quest_id']:
                line += f" |QID|{step['quest_id']}|"
            
            # Agregar nota si se proporciona
            if step['note']:
                line += f" |N|{step['note']}"
                
                # Agregar coordenadas si se proporcionan
                if step['coords']:
                    line += f" ({step['coords']})"
                
                line += "|"
            
            # Agregar restricción de clase si se proporciona
            if step['class']:
                line += f" |C|{step['class']}|"
            
            # Agregar restricción de raza si se proporciona
            if step['race']:
                line += f" |R|{step['race']}|"
            
            # Agregar zona si se proporciona
            if step['zone']:
                line += f" |Z|{step['zone']}|"
            
            # Agregar ID de objeto si se proporciona
            if step['obj_id']:
                line += f" |OBJ|{step['obj_id']}|"
            
            lua_code += line + "\n"
        
        # Fin del código Lua
        lua_code += '\n]]\nend)\n'
        
        return lua_code