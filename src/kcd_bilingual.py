import argparse
from collections import defaultdict
import xml.etree.ElementTree as ET
import zipfile

class BilingualPatcher:
    def __init__(self, files_to_process=None):
        self.stats = defaultdict(int)
        self.errors = []
        self.separator = " / "
        self.missing_entries = []
        # Default files to process if not specified
        self.files_to_process = files_to_process or [
            'text_ui_dialog.xml',   # Dialogues
            'text_ui_quest.xml',    # Quests
            'text_ui_tutorials.xml', # Tutorials
            'text_ui_soul.xml',     # Stats/Effects
            'text_ui_items.xml',    # Items
            'text_ui_menus.xml'     # Menus
        ]

    def _extract_data(self, pak_path, text_position):
        """Extracts texts from specified cell position in XML files"""
        data = {}
        with zipfile.ZipFile(pak_path, 'r') as zf:
            for file_info in zf.infolist():
                if file_info.filename in self.files_to_process:
                    with zf.open(file_info) as f:
                        tree = ET.parse(f)
                        content = {}
                        for row in tree.findall('.//Row'):
                            cells = row.findall('Cell')
                            if len(cells) > 2:  # Always use cell 2
                                entry_id = cells[0].text
                                text = cells[2].text or "MISSING"
                                content[entry_id] = text
                        data[file_info.filename] = content
        return data

    def _merge_data(self, first_data, second_data, eng_data):
        """Merges texts from different language files"""
        merged = defaultdict(list)
        all_files = set(first_data.keys()) | set(second_data.keys())
        
        for file_path in all_files:
            first_entries = first_data.get(file_path, {})
            second_entries = second_data.get(file_path, {})
            eng_entries = eng_data.get(file_path, {})
            
            all_ids = set(first_entries.keys()) | set(second_entries.keys())
            
            for entry_id in all_ids:
                primary_text = first_entries.get(entry_id, "MISSING")
                secondary_text = second_entries.get(entry_id, "MISSING")
                eng_text = eng_entries.get(entry_id, "MISSING")
                
                # Special handling for menus
                if file_path == 'text_ui_menus.xml':
                    words_count = len(primary_text.split()) if primary_text != "MISSING" else 0
                    if words_count < 3:
                        combined_text = primary_text
                    else:
                        # Always try to use secondary language first
                        combined_text = f"{primary_text} {self.separator} {secondary_text}" if secondary_text != "MISSING" else primary_text
                else:
                    # For all other files, prioritize secondary language over English
                    combined_text = f"{primary_text} {self.separator} {secondary_text}" if secondary_text != "MISSING" else f"{primary_text} {self.separator} {eng_text}"
                    if secondary_text == "MISSING":
                        self.stats['replaced_with_eng'] += 1
                
                merged[file_path].append((
                    entry_id,
                    primary_text,
                    combined_text
                ))
                self.stats['total'] += 1
                if primary_text == "MISSING": self.stats['missing_first'] += 1
                if secondary_text == "MISSING": self.stats['missing_second'] += 1
        return merged

    def _create_pak(self, data, output_path):
        """Creates output PAK file with merged texts"""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in self.files_to_process:
                if file_path in data:
                    root = ET.Element("Table")
                    for entry in data[file_path]:
                        row = ET.SubElement(root, "Row")
                        ET.SubElement(row, "Cell").text = entry[0]  # ID
                        ET.SubElement(row, "Cell").text = entry[1]  # Primary language
                        ET.SubElement(row, "Cell").text = entry[2]  # Combined text
                    zf.writestr(file_path, ET.tostring(root, encoding='utf-8'))
                    print(f"✓ Saved: {file_path}")

    def process(self, first_pak, second_pak, eng_pak, output_pak):
        """Main processing method"""
        try:
            first_data = self._extract_data(first_pak, 1)
            second_data = self._extract_data(second_pak, 1)
            eng_data = self._extract_data(eng_pak, 1)
            
            merged = self._merge_data(first_data, second_data, eng_data)
            self._create_pak(merged, output_pak)
            
            print("\n📊 Statistics:")
            print(f"Total entries: {self.stats['total']}")
            print(f"Missing in first language: {self.stats['missing_first']}")
            print(f"Missing in second language: {self.stats['missing_second']}")
            print(f"Replaced with English: {self.stats['replaced_with_eng']}")
            
            return True
        except Exception as e:
            print(f"\n❌ Error!\n- Error: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Create bilingual text files for Kingdom Come: Deliverance')
    parser.add_argument('first_pak', help='Primary language PAK file')
    parser.add_argument('second_pak', help='Secondary language PAK file')
    parser.add_argument('eng_pak', help='English PAK file (fallback)')
    parser.add_argument('-o', '--output', required=True, help='Output PAK file')
    parser.add_argument('-f', '--files', nargs='+', help='Specific files to process')
    
    args = parser.parse_args()
    
    patcher = BilingualPatcher(args.files)
    success = patcher.process(args.first_pak, args.second_pak, args.eng_pak, args.output)
    exit(0 if success else 1)

if __name__ == '__main__':
    main()