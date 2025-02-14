import winreg
from pathlib import Path
from typing import Optional, List
import logging

class GamePathFinder:
    def __init__(self):
        self.logger = logging.getLogger('GamePathFinder')
        self.logger.setLevel(logging.INFO)

        # Steam registry locations (HKLM)
        self.steam_registry_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        ]
        
        # GOG Galaxy registry locations
        self.gog_registry_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\GOG Galaxy"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\GOG Galaxy")
        ]
        
        self.gog_install_paths = [
            Path(r"C:\GOG Games\KingdomComeDeliverance"),
            Path(r"D:\GOG Games\KingdomComeDeliverance"),
            Path(r"E:\GOG Games\KingdomComeDeliverance"),
            Path.home() / "GOG Games/KingdomComeDeliverance",
            Path(r"C:\Program Files\KingdomComeDeliverance"),
            Path(r"C:\Program Files (x86)\KingdomComeDeliverance")
        ]
        
        self.standard_paths = [
            Path(r"C:\Program Files\KingdomComeDeliverance"),
            Path(r"C:\Program Files (x86)\KingdomComeDeliverance"),
            Path(r"D:\Program Files\KingdomComeDeliverance"),
            Path(r"D:\Program Files (x86)\KingdomComeDeliverance"),
            Path.home() / "Games/KingdomComeDeliverance"
        ]

        self.game_path = None

    def find_game_path(self) -> Optional[str]:
        """Find KCD installation path through various sources"""
        paths = []
        
        # 1. Steam search
        try:
            steam_path = self._get_steam_path()
            if steam_path:
                libraries = self._find_steam_libraries(steam_path)
                paths.extend(libraries)
        except Exception as e:
            pass

        # 2. GOG search
        try:
            gog_path = self._get_gog_path()
            if gog_path:
                paths.append(gog_path)
        except Exception as e:
            pass

        # 3. Check standard paths
        for std_path in self.standard_paths:
            if std_path.exists():
                paths.append(str(std_path))

        # Validate and return first valid path
        valid_paths = []
        for path in set(paths):
            data_path = Path(path) / "Data"
            if data_path.exists():
                valid_paths.append(path)
        
        return valid_paths[0] if valid_paths else None

    def _get_steam_path(self) -> Optional[str]:
        """Get Steam path from registry"""
        for hkey_root, key_path in self.steam_registry_keys:
            try:
                with winreg.OpenKey(hkey_root, key_path) as key:
                    path = winreg.QueryValueEx(key, "InstallPath")[0]
                    if path:
                        return path
            except WindowsError:
                continue
        return None
    
    def _find_steam_libraries(self, steam_path: str) -> List[str]:
        """Find all Steam library folders"""
        libraries = []
        default_library = Path(steam_path) / "steamapps" / "common" / "KingdomComeDeliverance"
        if default_library.exists():
            libraries.append(str(default_library))
        
        try:
            vdf_path = Path(steam_path) / "steamapps" / "libraryfolders.vdf"
            if vdf_path.exists():
                try:
                    with open(vdf_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        import re
                        paths = re.findall(r'"path"\s+"([^"]+)"', content)
                        for lib_path in paths:
                            kcd_path = Path(lib_path.replace("\\\\", "\\")) / "steamapps" / "common" / "KingdomComeDeliverance"
                            if kcd_path.exists():
                                libraries.append(str(kcd_path))
                except Exception as e:
                    self.logger.error(f"Error parsing Steam library VDF: {str(e)}", exc_info=True)
        except Exception as e:
            self.logger.error(f"Steam library error: {str(e)}", exc_info=True)
        return libraries
    
    def detect_languages(self, game_path: Optional[str]) -> List[str]:
        """Identify available game localizations by scanning PAK files"""
        languages = []
        
        if not game_path:
            return languages
        
        # Check both Data and Localization folders
        possible_paths = [
            Path(game_path) / "Data",
            Path(game_path) / "Localization",
            Path(game_path) / "Data" / "Localization"
        ]
        
        for data_path in possible_paths:
            if not data_path.exists():
                continue
            
            try:
                # Check for *_xml.pak files
                for file in data_path.glob("*_xml.pak"):
                    lang = file.stem.replace("_xml", "")
                    if lang not in languages:
                        languages.append(lang)
            except Exception as e:
                pass
        
        # Add English as default if no localization found
        if "English" not in languages and languages:
            languages.append("English")
        
        return sorted(languages)

    # GOG version search method
    def _get_gog_path(self) -> Optional[str]:
        """Locate GOG installation through multiple detection methods"""
        try:
            # Galaxy client registry-based detection
            if galaxy_path := self._get_galaxy_path():
                possible_galaxy_paths = [
                    galaxy_path / "Games" / "KingdomComeDeliverance",
                    galaxy_path.parent / "GOG Games" / "KingdomComeDeliverance"
                ]
                for path in possible_galaxy_paths:
                    if (path / "Data").exists():
                        return str(path)

            # Filesystem scan for common GOG paths
            for gog_path in self.gog_install_paths:
                if (gog_path / "Data").exists():
                    return str(gog_path)

        except Exception as e:
            self.logger.error(f"GOG search error: {str(e)}", exc_info=True)
        return None

    def _get_galaxy_path(self) -> Optional[Path]:
        """Get GOG Galaxy path from registry"""
        for hkey_root, key_path in self.gog_registry_keys:
            try:
                with winreg.OpenKey(hkey_root, key_path) as key:
                    path = winreg.QueryValueEx(key, "path")[0]
                    if path:
                        return Path(path.replace("\\", "/"))
            except WindowsError:
                continue
        return None

    def find_mods_folder(self, game_path: str) -> Path:
        return Path(game_path) / "Mods"