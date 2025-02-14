import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import ctypes
import sv_ttk

from .styles import StyleManager
from .sections import HeaderSection, LanguageSection, FilesSection, OutputSection
from src.utils.path_finder import GamePathFinder
from src.utils.mod_generator import ModGenerator

class BilingualModGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kingdom Come: Deliverance Bilingual Generator")
        
        # Set window icon
        try:
            icon_path = Path(__file__).parent.parent / 'resources' / 'icon.ico'
            if icon_path.exists():
                self.root.iconbitmap(default=str(icon_path))
        except Exception as e:
            print(f"Error loading icon: {e}")
        
        # Enable Windows DPI scaling
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            self.scaling = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        except:
            self.scaling = self.root.winfo_fpixels('1i') / 72
        
        sv_ttk.set_theme("dark")
        self.style_manager = StyleManager(self.scaling)
        
        width, height = self.style_manager.get_window_size()
        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)
        
        self.path_finder = GamePathFinder()
        self.game_path = self.path_finder.find_game_path()
        self.languages = self.path_finder.detect_languages(self.game_path)
        self.mod_generator = ModGenerator()
        self.base_dir = self.get_app_dir()
        self.output_path = self.base_dir / "Localization"
        
        self.main_container = ttk.Frame(root, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True) 
        self.create_widgets()
        
        self.refresh_ui()
    
    def get_app_dir(self):
        """Get application directory"""
        import sys
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent
        else:
            return Path(__file__).parent.parent
    
    def create_widgets(self):
        self.header = HeaderSection(self.main_container, self.style_manager, self.game_path)
        self.header.change_btn.configure(command=self.select_game_folder)
        
        main_frame = ttk.Frame(self.main_container)
        main_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Split into two columns
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.lang_section = LanguageSection(left_frame, self.style_manager, self.languages)
        self.files_section = FilesSection(right_frame, self.style_manager)
        
        self.output_section = OutputSection(self.main_container, self.style_manager, self.output_path)
        self.output_section.browse_btn.configure(command=self.select_output_folder)
        self.output_section.generate_btn.configure(command=self.generate_mod)
        self.output_section.output_location.set(str(self.output_path))
        self.output_section.browse_btn.pack_forget()
    
    def select_game_folder(self):
        """Manual game folder selection"""
        path = filedialog.askdirectory(title="Select KCD Installation Folder")
        if path:
            data_path = Path(path) / "Data"
            if data_path.exists():
                self.game_path = path
                self.path_finder.game_path = path
                self.languages = self.path_finder.detect_languages(self.game_path)
                self.refresh_ui()
            else:
                messagebox.showerror("Error", "Invalid KCD installation")
    
    def select_output_folder(self):
        """Select output folder"""
        path = filedialog.askdirectory(title="Select Output Folder")
        if path:
            self.output_section.output_location.set(path)
    
    def generate_mod(self):
        """Generate the bilingual mod"""
        if not self.validate_selections():
            return
        
        # Show processing state
        self.output_section.generate_btn.pack_forget()
        self.output_section.processing_label.pack(fill=tk.X)
        self.root.update()
        
        try:
            success = self.mod_generator.generate(
                game_path=Path(self.game_path),
                primary_lang=self.lang_section.primary_lang.get(),
                secondary_lang=self.lang_section.secondary_lang.get(),
                selected_files=[f for f, var in self.files_section.file_vars.items() if var.get()]
            )
            
            # Restore button
            self.output_section.processing_label.pack_forget()
            self.output_section.generate_btn.pack(fill=tk.X)
            
            if success:
                messagebox.showinfo(
                    "Success", 
                    f"Mod generated successfully!\n\n"
                    f"Location: {self.mod_generator.base_dir}\n\n"
                    f"Installation:\n"
                    f"1. Copy the entire folder containing this application\n"
                    f"   to your KCD Mods directory\n"
                    f"2. Enable mod in KCD Launcher (Mods tab)\n\n"
                    f"Game Settings:\n"
                    f"1. Set 'Text Language' to {self.lang_section.primary_lang.get()}\n"
                    f"2. Apply changes to see bilingual text"
                )
            else:
                messagebox.showerror("Error", "Failed to generate mod")
                
        except Exception as e:
            self.output_section.processing_label.pack_forget()
            self.output_section.generate_btn.pack(fill=tk.X)
            messagebox.showerror("Error", str(e))
    
    def validate_selections(self):
        """Validate user selections"""
        if not self.game_path:
            messagebox.showerror("Error", "Game path not selected")
            return False
        
        if not self.output_section.output_location.get().strip():
            messagebox.showerror("Error", "Output location not selected")
            return False
        
        if not self.lang_section.primary_lang.get():
            messagebox.showerror("Error", "Primary language not selected")
            return False
        
        if not self.lang_section.secondary_lang.get():
            messagebox.showerror("Error", "Secondary language not selected")
            return False
        
        if self.lang_section.primary_lang.get() == self.lang_section.secondary_lang.get():
            messagebox.showerror("Error", "Primary and secondary languages must be different")
            return False
        
        selected_files = [f for f, var in self.files_section.file_vars.items() if var.get()]
        if not selected_files:
            messagebox.showerror("Error", "No files selected for processing")
            return False
        
        return True 

    def refresh_ui(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        self.languages = self.path_finder.detect_languages(self.game_path)
        self.create_widgets()