import tkinter as tk
from src.kcd_bilingual import BilingualPatcher
from src.gui import BilingualModGUI

def main():
    # Create root window
    root = tk.Tk()
    
    # Initialize and attach GUI
    BilingualModGUI(root)
    
    # Start main loop
    root.mainloop()

def refresh_ui(self):
    # Remove old widgets
    for widget in self.main_container.winfo_children():
        widget.destroy()
    
    # Reinitialize data
    self.languages = self.detect_available_languages()
    self.create_widgets()
    self.setup_status_bar()

if __name__ == "__main__":
    main()