# Kingdom Come: Deliverance Bilingual Generator

A tool for generating bilingual mods for Kingdom Come: Deliverance that allow you to play with two languages simultaneously, showing primary language text with secondary language translation in the game.

## Features

- User-friendly graphical interface
- Automatic game installation detection
- Support for all available game languages
- Selective text elements (dialogues, quests, tutorials, etc.)
- DPI-aware interface scaling

## Requirements

- Python 3.8 or higher
- Kingdom Come: Deliverance game installation
- Required Python packages:
  - tkinter
  - sv_ttk
  - kcd_bilingual

## Installation

1. Download the latest release from [GitHub Releases](https://github.com/smxqp/kcd_bilingual_generator/releases)

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python kcd_bilingual_windowed.py
```

2. Select languages:
   - Primary Language: The main game text language
   - Secondary Language: The translation that will appear with the main text

3. Choose which files to process:
   - Dialogues (text_ui_dialog.xml)
   - Quests (text_ui_quest.xml)
   - Tutorials (text_ui_tutorials.xml)
   - Stats (text_ui_soul.xml)
   - Items (text_ui_items.xml)
   - Menus (text_ui_menus.xml)

4. Select output location for the mod

5. Click "Generate Bilingual Mod"

## Installing the Generated Mod

1. Copy the generated 'kcd_bilingual_mod' folder to your game's Mods folder
2. Enable the mod in KCD Launcher (Mods tab)
3. In game settings:
   - Go to 'Game' tab
   - Set 'Text Language' to your selected primary language
   - Apply changes

## Development

### Running Tests

Run all tests
```bash 
python -m unittest discover tests/
```

Run specific test module
```bash
python -m unittest tests/test_path_finder.py
```

### Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. Game not detected:
   - Use "Select Game" button to manually locate the game installation

2. Languages not showing:
   - Ensure game installation is complete with all language packs

3. Mod not working:
   - Verify mod is enabled in KCD Launcher
   - Check if correct text language is selected in game settings

### Error Reporting

If you encounter any issues, please create an issue on GitHub with:
- Error message
- Steps to reproduce
- Your system information
- Game version

## Contact

For questions and support:
- Create an issue on GitHub