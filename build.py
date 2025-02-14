import PyInstaller.__main__
from pathlib import Path

def build_exe():
    base_path = Path(__file__).parent
    src_path = base_path / "src"
    resources_path = base_path / "resources"
    
    PyInstaller.__main__.run([
        str(src_path / 'kcd_bilingual_windowed.py'),
        '--name=KCD Bilingual Generator',
        '--onefile',
        '--noconsole',
        f'--add-data={base_path / "LICENSE"};.',
        f'--add-data={resources_path / "icon.ico"};resources',
        f'--icon={resources_path / "icon.ico"}',
        '--clean',
        '--windowed',
        '--workpath=build',
        '--distpath=dist',
        '--specpath=build'
    ])

if __name__ == "__main__":
    build_exe()