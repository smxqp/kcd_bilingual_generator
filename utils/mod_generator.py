"""
Mod Generator Module
Handles creation of bilingual localization files for Kingdom Come: Deliverance
"""

# Creating mod structure
from pathlib import Path
from kcd_bilingual import BilingualPatcher

class ModGenerator:
    def __init__(self):
        self.patcher = None
        self.base_dir = self.get_app_dir()
    
    def get_app_dir(self):
        """Get application directory"""
        import sys
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent
        else:
            return Path(__file__).parent.parent
    
    def generate(self,
                game_path: Path,
                primary_lang: str,
                secondary_lang: str,
                selected_files: list) -> bool:
        """Generate bilingual mod files"""
        try:
            # Create Localization directory next to EXE
            loc_path = self.base_dir / "Localization"
            loc_path.mkdir(parents=True, exist_ok=True)
            
            # Process files
            self.patcher = BilingualPatcher(selected_files)
            success = self.patcher.process(
                str(game_path / "Localization" / f"{primary_lang}_xml.pak"),
                str(game_path / "Localization" / f"{secondary_lang}_xml.pak"),
                str(game_path / "Localization" / "English_xml.pak"),
                str(loc_path / f"{primary_lang}_xml.pak")
            )
            
            return success
            
        except Exception as e:
            print(f"Mod generation failed: {e}")
            return False 