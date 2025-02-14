import unittest
from pathlib import Path
import json
import zipfile
from src.utils.mod_generator import ModGenerator

class TestModGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ModGenerator()
        self.test_dir = Path("test_data/mod_test")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Create fake game structure
        self.game_path = self.test_dir / "game"
        self.game_path.mkdir(exist_ok=True)
        (self.game_path / "Localization").mkdir(exist_ok=True)
        
        # Create dummy language files as zip archives
        loc_path = self.game_path / "Localization"
        self.create_dummy_pak(loc_path / "English_xml.pak")
        self.create_dummy_pak(loc_path / "Czech_xml.pak")
        self.create_dummy_pak(loc_path / "German_xml.pak")
    
    def create_dummy_pak(self, path):
        """Create a dummy PAK file with minimal XML content"""
        with zipfile.ZipFile(path, 'w') as zf:
            zf.writestr('text_ui_dialog.xml', 
                       '<Table><Row><Cell>Test</Cell></Row></Table>')
    
    def tearDown(self):
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    def test_mod_structure_creation(self):
        self.generator.generate(
            game_path=self.game_path,
            primary_lang="Czech",
            secondary_lang="German",
            selected_files=["text_ui_dialog.xml"]
        )
        
        # Check output structure
        loc_path = self.generator.base_dir / "Localization"
        self.assertTrue(loc_path.exists())
        
        # Verify generated files
        self.assertTrue((loc_path / "Czech_xml.pak").exists()) 