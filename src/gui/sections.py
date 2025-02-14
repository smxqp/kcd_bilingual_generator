# GUI sections components

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox

class BaseSection:
    def __init__(self, parent, style_manager):
        self.parent = parent
        self.styles = style_manager
        self.frame = None
    
    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            
            offset = self.styles.get_padding('base')
            tooltip.wm_geometry(f"+{event.x_root+offset}+{event.y_root+offset}")
            
            label = ttk.Label(
                tooltip,
                text=text,
                style="Small.TLabel",
                padding=self.styles.get_padding('small')
            )
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip)

class HeaderSection(BaseSection):
    def __init__(self, parent, style_manager, game_path):
        super().__init__(parent, style_manager)
        self.game_path = game_path
        self.create_section()
    
    def create_section(self):
        """Create top section with game path"""
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        ttk.Label(header_frame, 
                 text="Kingdom Come: Deliverance Bilingual Generator",
                 style="Title.TLabel").pack(anchor=tk.W)
        
        # Game path frame
        path_frame = ttk.LabelFrame(
            header_frame, 
            text="Game Location",
            padding=int(5 * self.styles.scaling)
        )
        path_frame.pack(fill=tk.X, pady=(5, 0))
        
        if self.game_path:
            # Path display with scaled font
            path_label = ttk.Label(
                path_frame, 
                text=str(Path(self.game_path).resolve()),
                font=self.styles.fonts['normal'],
                wraplength=int(600 * self.styles.scaling)
            )
            path_label.pack(side=tk.LEFT, padx=(int(5 * self.styles.scaling), 0), 
                          fill=tk.X, expand=True)
            
            self.change_btn = ttk.Button(
                path_frame,
                text="Change Location",
                command=None
            )
            self.change_btn.pack(side=tk.RIGHT, padx=int(5 * self.styles.scaling))
        else:

            ttk.Label(path_frame,
                     text="Game not found",
                     foreground="red",
                     style="Info.TLabel").pack(side=tk.LEFT, padx=(0, 5))
            
            # Create button but pack separately
            self.change_btn = ttk.Button(
                path_frame,
                text="Select Game",
                command=None
            )
            self.change_btn.pack(side=tk.RIGHT)


class LanguageSection:
    def __init__(self, parent, style_manager, languages):
        self.parent = parent
        self.styles = style_manager
        self.languages = languages
        self.create_section()
    
    def create_section(self):
        """Create language selection section"""
        lang_frame = ttk.LabelFrame(self.parent, text="Languages", 
                                  padding=int(5 * self.styles.scaling))
        lang_frame.pack(fill=tk.X)
        
        # Primary language
        ttk.Label(lang_frame,
                 text="Primary Language (e.g., Czech):",
                 style="Header.TLabel").pack(anchor=tk.W, pady=(0, 2))
        
        # Create combobox style with increased height
        combo_height = int(30 * self.styles.scaling)
        
        # Using ttk.Entry to set combobox height
        entry_style = ttk.Style()
        entry_style.configure(
            "Combo.TEntry",
            padding=int(8 * self.styles.scaling)
        )
        
        # Primary language combobox
        primary_frame = ttk.Frame(lang_frame)
        primary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.primary_lang = ttk.Combobox(
            primary_frame,
            values=self.languages,
            state="readonly",
            font=self.styles.fonts['normal'],
            height=10
        )
        self.primary_lang.pack(fill=tk.X, ipady=int(3 * self.styles.scaling))
        
        # Secondary language
        ttk.Label(lang_frame,
                 text="Secondary Language (e.g., Russian):",
                 style="Header.TLabel").pack(anchor=tk.W, pady=(0, 2))
        
        # Secondary language combobox
        secondary_frame = ttk.Frame(lang_frame)
        secondary_frame.pack(fill=tk.X)
        
        self.secondary_lang = ttk.Combobox(
            secondary_frame,
            values=self.languages,
            state="readonly",
            font=self.styles.fonts['normal'],
            height=10
        )
        self.secondary_lang.pack(fill=tk.X, ipady=int(3 * self.styles.scaling))
        
        # Set defaults if available
        if "Czech" in self.languages:
            self.primary_lang.set("Czech")
        if "Russian" in self.languages:
            self.secondary_lang.set("Russian")
        
        # Apply style to all comboboxes
        self.parent.option_add('*TCombobox*Listbox.font', self.styles.fonts['normal'])
        
        # Bind events for language selection
        self.primary_lang.bind('<<ComboboxSelected>>', self._on_primary_changed)
        self.secondary_lang.bind('<<ComboboxSelected>>', self._on_secondary_changed)
    
    def _on_primary_changed(self, event):
        """Handle primary language selection"""
        selected = self.primary_lang.get()
        if selected == self.secondary_lang.get():
            # Reset to previous value if same language selected
            messagebox.showwarning(
                "Invalid Selection",
                "Primary and secondary languages must be different!"
            )
            # Try to select Czech or first available language
            if "Czech" in self.languages and "Czech" != self.secondary_lang.get():
                self.primary_lang.set("Czech")
            else:
                # Find first available language that's not secondary
                for lang in self.languages:
                    if lang != self.secondary_lang.get():
                        self.primary_lang.set(lang)
                        break
    
    def _on_secondary_changed(self, event):
        """Handle secondary language selection"""
        selected = self.secondary_lang.get()
        if selected == self.primary_lang.get():
            # Reset to previous value if same language selected
            messagebox.showwarning(
                "Invalid Selection",
                "Primary and secondary languages must be different!"
            )
            # Try to select Russian or first available language
            if "Russian" in self.languages and "Russian" != self.primary_lang.get():
                self.secondary_lang.set("Russian")
            else:
                # Find first available language that's not primary
                for lang in self.languages:
                    if lang != self.primary_lang.get():
                        self.secondary_lang.set(lang)
                        break

    def get_languages(self):
        """Get selected languages"""
        return (self.primary_lang.get(), self.secondary_lang.get())
    
    def set_defaults(self):
        """Set default languages if available"""
        if "Czech" in self.languages:
            self.primary_lang.set("Czech")
        if "Russian" in self.languages:
            self.secondary_lang.set("Russian")

class FilesSection:
    def __init__(self, parent, style_manager):
        self.parent = parent
        self.styles = style_manager
        self.file_vars = {}
        self.create_section()
    
    def create_section(self):
        """Create files selection section with scaled fonts"""
        files_frame = ttk.LabelFrame(self.parent, text="Files to Process", 
                                   padding=int(5 * self.styles.scaling))
        files_frame.pack(fill=tk.X)
        
        # Create two columns for files
        left_files = ttk.Frame(files_frame)
        left_files.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        right_files = ttk.Frame(files_frame)
        right_files.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        default_files = [
            ('Dialogues', 'text_ui_dialog.xml'),
            ('Quests', 'text_ui_quest.xml'),
            ('Tutorials', 'text_ui_tutorials.xml'),
            ('Stats', 'text_ui_soul.xml'),
            ('Items', 'text_ui_items.xml'),
            ('Menus', 'text_ui_menus.xml')
        ]
        
        for i, (label, file) in enumerate(default_files):
            var = tk.BooleanVar(value=True)
            self.file_vars[file] = var
            
            # Choose column based on index
            parent_frame = left_files if i < 3 else right_files
            frame = ttk.Frame(parent_frame)
            frame.pack(fill=tk.X, pady=2)
            
            # Create checkbutton with scaled font
            cb = ttk.Checkbutton(frame, text=label, variable=var, style="TCheckbutton")
            cb.pack(side=tk.LEFT)
            
            # Add file name with scaled font
            ttk.Label(frame, 
                     text=f"({file})",
                     font=self.styles.fonts['small']).pack(side=tk.LEFT, padx=(5, 0))
            
            # Add tooltip
            self.styles.create_tooltip(cb, f"Process {file}")

    def get_selected_files(self):
        """Get list of selected files"""
        return [f for f, var in self.file_vars.items() if var.get()]

class OutputSection:
    def __init__(self, parent, style_manager, output_location):
        self.parent = parent
        self.styles = style_manager
        self.output_location = tk.StringVar(value=str(output_location))
        self.create_section()
    
    def create_section(self):
        """Create output settings section"""
        output_frame = ttk.LabelFrame(self.parent,
                                    text="Output Settings",
                                    padding=int(5 * self.styles.scaling))
        output_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Output location
        loc_frame = ttk.Frame(output_frame)
        loc_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(loc_frame,
                 text="Mod folder:",
                 style="Header.TLabel").pack(side=tk.LEFT)
        
        path_entry = ttk.Entry(loc_frame,
                             textvariable=self.output_location,
                             font=self.styles.fonts['normal'],
                             state="readonly")
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.browse_btn = ttk.Button(
            loc_frame,
            text="Browse",
            command=None
        )
        self.browse_btn.pack(side=tk.LEFT)
        
        # Generate button frame
        self.generate_frame = ttk.Frame(output_frame)
        self.generate_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Generate button
        self.generate_btn = ttk.Button(
            self.generate_frame,
            text="Create Bilingual Mod",
            command=None,
            style="Generate.TButton"
        )
        self.generate_btn.pack(fill=tk.X)
        
        # Processing label
        self.processing_label = ttk.Label(
            self.generate_frame,
            text="Creating mod...",
            style="Header.TLabel",
            anchor="center"
        )

    def get_output_location(self):
        """Get output location"""
        return Path(self.output_location.get())
    
    def set_generate_command(self, command):
        """Set command for generate button"""
        self.generate_btn.configure(command=command)
    
    def toggle_progress(self, show=True):
        """Show/hide progress bar"""
        if show:
            self.progress.pack(fill=tk.X, pady=(10, 0))
            self.progress.start()
        else:
            self.progress.stop()
            self.progress.pack_forget()

    def select_output_folder(self):
        """Select output folder"""
        folder = filedialog.askdirectory(
            title="Select Mods Folder",
            initialdir=self.output_location.get()
        )
        if folder:
            self.output_location.set(folder)

class StatusBar:
    def __init__(self, parent, style_manager):
        self.parent = parent
        self.styles = style_manager
        self.status_var = tk.StringVar()
        self.create_section()
    
    def create_section(self):
        """Create status bar"""
        self.status_bar = ttk.Label(
            self.parent,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            padding=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update("Ready")
    
    def update(self, message):
        """Update status bar message"""
        self.status_var.set(message)
        self.parent.update_idletasks() 