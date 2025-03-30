#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from gui.app import GuiaPhermuthCreator

def main():
    """Punto de entrada principal de la aplicación."""
    root = tk.Tk()
    app = GuiaPhermuthCreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()