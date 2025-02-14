# GUI styles and scaling management

import tkinter as tk
from tkinter import ttk

class StyleManager:
    """Manage GUI styles and scaling for the application.
    
    Attributes:
        scaling (float): UI scaling factor for high-DPI displays
        fonts (dict): Dictionary of preconfigured fonts
        base_padding (int): Scaled base padding value
        large_padding (int): Scaled large padding value
    """
    
    DEFAULT_FONT = "Segoe UI"
    BASE_FONT_SIZES = {
        'title': 14,
        'header': 11,
        'normal': 10,
        'small': 9
    }
    PADDING = {
        'base': 5,
        'large': 10
    }
    SAFE_FONTS = ("Segoe UI", "Helvetica", "Arial", "sans-serif")

    def __init__(self, scaling):
        self.scaling = scaling
        self.setup_styles()
    
    def setup_styles(self):
        """Configure styles with DPI scaling"""
        style = ttk.Style()
        
        # Calculate font sizes
        title_size = int(self.BASE_FONT_SIZES['title'] * self.scaling)
        header_size = int(self.BASE_FONT_SIZES['header'] * self.scaling)
        normal_size = int(self.BASE_FONT_SIZES['normal'] * self.scaling)
        small_size = int(self.BASE_FONT_SIZES['small'] * self.scaling)
        
        # Configure padding (scaled)
        self.base_padding = int(self.PADDING['base'] * self.scaling)
        self.large_padding = int(self.PADDING['large'] * self.scaling)
        
        # Define fonts
        self.fonts = {
            'title': (self.SAFE_FONTS, title_size, "bold"),
            'header': (self.SAFE_FONTS, header_size, "bold"),
            'normal': (self.SAFE_FONTS, normal_size),
            'small': (self.SAFE_FONTS, small_size),
            'button': (self.SAFE_FONTS, normal_size),
            'generate': (self.SAFE_FONTS, header_size, "bold")
        }
        
        # Configure all widget styles
        style.configure("Title.TLabel",
                       font=self.fonts['title'],
                       padding=self.large_padding)
        
        style.configure("Header.TLabel",
                       font=self.fonts['header'],
                       padding=self.base_padding)
        
        style.configure("Normal.TLabel",
                       font=self.fonts['normal'],
                       padding=self.base_padding)
        
        style.configure("Small.TLabel",
                       font=self.fonts['small'],
                       padding=self.base_padding)
        
        # Frame styles
        style.configure("TLabelframe",
                       font=self.fonts['normal'],
                       padding=self.base_padding)
        
        style.configure("TLabelframe.Label",
                       font=self.fonts['header'])
        
        # Button styles
        style.configure("TButton",
                       font=self.fonts['button'],
                       padding=self.base_padding)
        
        style.configure("Generate.TButton",
                       font=self.fonts['generate'],
                       padding=self.large_padding)
        
        # Combobox styles
        style.configure("TCombobox",
                       font=self.fonts['normal'],
                       padding=self.base_padding)
        
        # Entry styles
        style.configure("TEntry",
                       font=self.fonts['normal'],
                       padding=self.base_padding)
        
        # Checkbutton styles
        style.configure("TCheckbutton",
                       font=self.fonts['normal'],
                       padding=self.base_padding)
    
    def create_tooltip(self, widget, text):
        """Attach a tooltip to a widget with proper scaling"""
        tooltip = None  # Сохраняем ссылку для предотвращения GC
        
        def hide_tooltip(_):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        
        def show_tooltip(event):
            nonlocal tooltip
            if tooltip: 
                return
            
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            
            # Scale position offset
            offset = int(10 * self.scaling)
            tooltip.wm_geometry(f"+{event.x_root+offset}+{event.y_root+offset}")
            
            # Scale padding
            padding = int(5 * self.scaling)
            label = ttk.Label(tooltip,
                            text=text,
                            style="Normal.TLabel",
                            padding=padding)
            label.pack()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', hide_tooltip)
        
        widget.bind('<Enter>', show_tooltip)
    
    def get_scaled_size(self, base_size):
        """Calculate scaled dimension based on DPI scaling factor.
        
        Args:
            base_size (int): Base size in pixels at 100% scaling
            
        Returns:
            int: Scaled size adjusted for current DPI
        """
        return int(base_size * self.scaling)
    
    def get_window_size(self):
        """Get default scaled window size"""
        BASE_WIDTH = 720
        BASE_HEIGHT = 480
        return (
            self.get_scaled_size(BASE_WIDTH),
            self.get_scaled_size(BASE_HEIGHT)
        ) 