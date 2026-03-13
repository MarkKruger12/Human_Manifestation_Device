import os
import shutil
from pathlib import Path
import datetime

SOURCE_FOLDER = r"C:\Users\mkmdk\Book"
REAL_FOLDER = r"C:\Users\mkmdk\Sorted\Real"
POSSIBLE_FOLDER = r"C:\Users\mkmdk\Sorted\Possible"
SPECULATION_FOLDER = r"C:\Users\mkmdk\Sorted\Speculation"

REAL_HINTS = ['paper', 'published', 'patent', 'data', 'measurement', 'experiment', 'demo', 'product', 'doi', 'ieee']
POSSIBLE_HINTS = ['proposal', 'theory', 'model', 'simulation', 'sketch', 'draft', 'idea', 'notes']
SPECULATION_HINTS = ['consciousness', 'vacuum', 'zero point', 'free energy', 'spacetime', 'quantum mind']

class CrystalSorter:
    def __init__(self):
        self.stats = {'REAL': 0, 'POSSIBLE': 0, 'SPECULATION': 0, 'SKIPPED': 0}
        self.log = []
    
    def run(self):
        files = list(Path(SOURCE_FOLDER).rglob('*'))
        files = [f for f in files if f.is_file()]
        total = len(files)
        
        print(f"\nFound {total} files in your Book folder")
        print("Files will be COPIED to Sorted folders (originals stay in Book)\n")
        
        for i, filepath in enumerate(files):
            print(f"\n[{i+1}/{total}] {filepath.name}")
            print(f"Location: {filepath.parent}")
            
            guess = None
            name_lower = filepath.name.lower()
            for hint in REAL_HINTS:
                if hint in name_lower:
                    guess = "REAL"
            if not guess:
                for hint in POSSIBLE_HINTS:
                    if hint in name_lower:
                        guess = "POSSIBLE"
            if not guess:
                for hint in SPECULATION_HINTS:
                    if hint in name_lower:
                        guess = "SPECULATION"
            if guess:
                print(f"Suggestion: {guess}")
            
            choice = input("[r]eal, [p]ossible, [s]peculation, [space]kip, [q]uit: ").strip().lower()
            
            if choice == 'r':
                dest = REAL_FOLDER
                cat = 'REAL'
            elif choice == 'p':
                dest = POSSIBLE_FOLDER
                cat = 'POSSIBLE'
            elif choice == 's':
                dest = SPECULATION_FOLDER
                cat = 'SPECULATION'
            elif choice == 'q':
                break
            else:
                self.stats['SKIPPED'] += 1
                continue
            
            # Create destination folder if it doesn't exist
            os.makedirs(dest, exist_ok=True)
            
            # Create destination path
            dest_path = Path(dest) / filepath.name
            
            # Handle duplicate filenames
            if dest_path.exists():
                base = dest_path.stem
                ext = dest_path.suffix
                counter = 1
                while dest_path.exists():
                    new_name = f"{base}_{counter}{ext}"
                    dest_path = Path(dest) / new_name
                    counter += 1
            
            # COPY the file (not move)
            shutil.copy2(str(filepath), str(dest_path))
            print(f"✓ Copied to {cat}")
            self.stats[cat] += 1
            self.log.append(f"{filepath} -> {dest_path} ({cat})")
        
        print("\n" + "="*50)
        print("SORTING COMPLETE")
        print("="*50)
        print(f"REAL:        {self.stats['REAL']} files")
        print(f"POSSIBLE:    {self.stats['POSSIBLE']} files")
        print(f"SPECULATION: {self.stats['SPECULATION']} files")
        print(f"SKIPPED:     {self.stats['SKIPPED']} files")
        print(f"TOTAL:       {sum(self.stats.values())} files")
        print("\nOriginal files remain in Book folder")
        print(f"Log saved to Desktop")

if __name__ == "__main__":
    sorter = CrystalSorter()
    sorter.run()
    
    # Save log to Desktop
    log_path = Path.home() / "Desktop" / f"sorting_log_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    with open(log_path, 'w') as f:
        f.write("CRYSTAL COMPUTER SORTING LOG\n")
        f.write(f"Completed: {datetime.datetime.now()}\n")
        for entry in sorter.log:
            f.write(entry + "\n")