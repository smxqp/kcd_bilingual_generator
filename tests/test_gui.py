import unittest
import tkinter as tk
from src.gui.main_window import BilingualModGUI

class TestBilingualModGUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.app = BilingualModGUI(cls.root)
    
    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()
    
    def test_initial_state(self):
        """Test initial GUI state"""
        # Check if main sections exist
        self.assertIsNotNone(self.app.header)
        self.assertIsNotNone(self.app.lang_section)
        self.assertIsNotNone(self.app.files_section)
        self.assertIsNotNone(self.app.output_section)
    
    def test_validation(self):
        """Test input validation"""
        # Should fail without game path
        self.app.game_path = None
        self.assertFalse(self.app.validate_selections())
        
        # Should fail with same languages
        self.app.game_path = "dummy_path"
        self.app.lang_section.primary_lang.set("English")
        self.app.lang_section.secondary_lang.set("English")
        self.assertFalse(self.app.validate_selections()) 