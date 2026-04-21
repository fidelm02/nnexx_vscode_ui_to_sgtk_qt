#
# Copyright (c) 2026 Boxel Studio.
#
# :Module: ai_helper.py
# :Description: AI-assisted utilities for code analysis and documentation.
#
# :Author: Fidel Moreno Miranda <fidel.moreno@boxelstudio.com>
#

# Standard modules
import os
import re
from typing import Optional


def generate_file_description(file_path: str) -> str:
    """
    Generate a brief description of a Python file based on its content.

    Args:
        file_path: Path to the Python file to analyze.

    Return:
        A brief description of the file's purpose.
    """
    if not os.path.isfile(file_path):
        return "Brief description."
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract module docstring if present
        docstring_match = re.search(
            r'^"""(.+?)"""',
            content,
            re.MULTILINE | re.DOTALL
        )
        if docstring_match:
            docstring = docstring_match.group(1).strip()
            # Get first line of docstring
            first_line = docstring.split('\n')[0].strip()
            if first_line and len(first_line) < 100:
                return first_line
        
        # Look for class definitions to infer purpose
        class_matches = re.findall(r'class\s+(\w+)', content)
        if class_matches:
            if len(class_matches) == 1:
                return f"Implementation of {class_matches[0]} class."
            else:
                return (f"Implementation of {', '.join(class_matches[:2])} "
                       "and related classes.")
        
        # Look for main function patterns
        if 'def main(' in content or 'if __name__ == "__main__"' in content:
            return "Main script for execution."
        
        # Look for specific patterns
        if 'QtWidgets' in content or 'QWidget' in content:
            return "Qt-based user interface component."
        
        if 'def test_' in content or 'import pytest' in content:
            return "Unit tests for the module."
        
        # Count function definitions
        func_matches = re.findall(r'def\s+(\w+)', content)
        if len(func_matches) > 5:
            return "Utility functions and helper methods."
        elif len(func_matches) > 0:
            return f"Helper functions for {func_matches[0]} and related operations."
        
        # Fallback
        filename = os.path.basename(file_path)
        base_name = os.path.splitext(filename)[0]
        return f"Module for {base_name.replace('_', ' ')} functionality."
        
    except Exception:
        return "Brief description."


def extract_imports_info(file_path: str) -> dict:
    """
    Extract import information from a Python file.

    Args:
        file_path: Path to the Python file to analyze.

    Return:
        Dictionary with import categorization data.
    """
    if not os.path.isfile(file_path):
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        imports_data = {
            'standard': [],
            'third_party': [],
            'boxel': [],
            'header_end_line': 0
        }
        
        # Find where imports start (after header)
        in_header = True
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip header section
            if in_header:
                if stripped and not stripped.startswith('#'):
                    in_header = False
                    imports_data['header_end_line'] = i
            
            # Collect imports
            if stripped.startswith(('import ', 'from ')):
                if stripped.startswith('from .') or '/app/' in stripped:
                    imports_data['boxel'].append(line)
                elif 'sgtk' in stripped or 'PySide' in stripped or 'PyQt' in stripped:
                    imports_data['third_party'].append(line)
                else:
                    # Check if it's a standard library module
                    module_name = stripped.split()[1].split('.')[0]
                    if _is_standard_library(module_name):
                        imports_data['standard'].append(line)
                    else:
                        imports_data['third_party'].append(line)
        
        return imports_data
        
    except Exception:
        return {}


def _is_standard_library(module_name: str) -> bool:
    """
    Check if a module is part of Python's standard library.

    Args:
        module_name: Name of the module to check.

    Return:
        True if module is in standard library, False otherwise.
    """
    stdlib_modules = {
        'abc', 'argparse', 'ast', 'asyncio', 'base64', 'calendar',
        'collections', 'copy', 'csv', 'datetime', 'decimal', 'email',
        'enum', 'functools', 'glob', 'hashlib', 'http', 'importlib',
        'io', 'itertools', 'json', 'logging', 'math', 'multiprocessing',
        'os', 'pathlib', 'pickle', 'platform', 'pprint', 'queue',
        're', 'random', 'shutil', 'socket', 'sqlite3', 'string',
        'struct', 'subprocess', 'sys', 'tempfile', 'textwrap',
        'threading', 'time', 'traceback', 'typing', 'unittest',
        'urllib', 'uuid', 'warnings', 'weakref', 'xml', 'xmlrpc',
        'zipfile'
    }
    return module_name in stdlib_modules
