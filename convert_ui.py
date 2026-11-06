#!/usr/bin/env python3
"""
Convert .ui files to Python code using pyside6-uic
Usage: python convert_ui.py
"""

import os
import subprocess
import sys

def convert_ui_files():
    """Convert all .ui files in the ui/ directory to Python files"""
    
    ui_dir = "ui"
    output_dir = "src/ui"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all .ui files
    ui_files = []
    if os.path.exists(ui_dir):
        for file in os.listdir(ui_dir):
            if file.endswith('.ui'):
                ui_files.append(file)
    
    if not ui_files:
        print("No .ui files found in ui/ directory")
        return
    
    print(f"Found {len(ui_files)} .ui files to convert:")
    
    for ui_file in ui_files:
        ui_path = os.path.join(ui_dir, ui_file)
        py_file = ui_file.replace('.ui', '_ui.py')
        py_path = os.path.join(output_dir, py_file)
        
        print(f"Converting {ui_file} -> {py_file}")
        
        try:
            # Run pyside6-uic to convert .ui to .py
            result = subprocess.run([
                'pyside6-uic', ui_path, '-o', py_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"  ✓ Successfully converted {ui_file}")
            else:
                print(f"  ✗ Error converting {ui_file}: {result.stderr}")
                
        except FileNotFoundError:
            print(f"  ✗ pyside6-uic not found. Install with: pip install pyside6")
            break
        except Exception as e:
            print(f"  ✗ Error converting {ui_file}: {e}")
    
    print("\nConversion complete!")
    print(f"Python files saved to: {output_dir}/")
    print("\nTo use the converted files in your code:")
    print("from src.ui.main_window_ui import Ui_MainWindow")

if __name__ == "__main__":
    convert_ui_files()