import unittest
from pathlib import Path
from src.utils.path_finder import GamePathFinder

class TestGamePathFinder(unittest.TestCase):
    def setUp(self):
        self.finder = GamePathFinder()
        self.test_game_path = Path("test_data/fake_game")
        self.test_game_path.mkdir(parents=True, exist_ok=True)
        (self.test_game_path / "Data").mkdir(exist_ok=True)
        (self.test_game_path / "Mods").mkdir()
        
    def tearDown(self):
        # Cleanup test directories
        import shutil
        if self.test_game_path.exists():
            shutil.rmtree(self.test_game_path)
    
    def test_find_mods_path(self):
        mods_path = Path(self.test_game_path) / "Mods"
        self.assertTrue(mods_path.exists())
    
    def test_detect_languages(self):
        # Create test language files
        loc_path = self.test_game_path / "Localization"
        loc_path.mkdir(exist_ok=True)
        
        test_langs = ["English", "Czech", "German"]
        for lang in test_langs:
            (loc_path / f"{lang}_xml.pak").touch()
        
        languages = self.finder.detect_languages(str(self.test_game_path))
        self.assertEqual(set(languages), set(test_langs)) 