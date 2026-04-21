#
# Copyright (c) 2026 Fidel Moreno Miranda
#
# :Module: code_cleaner.py
# :Description: Utility functions to clean, optimize and make Python
#               files more professional.
#
# :Author: Fidel Moreno Miranda <fidelm02@gmail.com>
#

# Standard modules
from typing import Dict, List, Optional, Tuple
import datetime
import os
import re
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

import ai_helper


def remove_empty_spaces(file_path: str) -> None:
    """
    Remove trailing whitespace from each line in the file.

    Args:
        file_path: Path to the Python file to clean.

    Return:
        None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = [line.rstrip() + '\n' for line in lines]

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)


def remove_multiple_blank_lines(file_path: str, max_blanks: int = 2) -> None:
    """
    Reduce consecutive blank lines to a maximum number (PEP8: max 2).

    Args:
        file_path: Path to the Python file to clean.
        max_blanks: Maximum number of consecutive blank lines allowed.

    Return:
        None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace 3+ consecutive newlines with max_blanks newlines
    pattern = r'\n{' + str(max_blanks + 1) + r',}'
    replacement = '\n' * max_blanks
    cleaned_content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)


def normalize_blank_lines(file_path: str) -> None:
    """
    Normalize blank lines to follow Flake8/PEP8 rules.

    Rules enforced:
    - 2 blank lines before top-level class/function definitions (E302)
    - 1 blank line between methods in a class (E301)
    - No blank lines between decorator and function/class (E304)
    - Max 2 consecutive blank lines anywhere (E303)
    - 1 blank line before nested class/function definitions (E306)

    Args:
        file_path: Path to the Python file to clean.

    Return:
        None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if not lines:
        return

    new_lines = []
    i = 0

    while i < len(lines):
        current_line = lines[i]
        stripped = current_line.strip()

        # Get current indentation level
        indent_level = len(current_line) - len(current_line.lstrip())
        is_top_level = indent_level == 0

        # Check if current line is a decorator
        is_decorator = stripped.startswith('@')

        # Check if current line is a class or function definition
        is_class = stripped.startswith('class ')
        is_func = stripped.startswith('def ')
        is_def = is_class or is_func

        # Check if this is inside a class (method/property)
        is_method = is_def and indent_level > 0

        # Count blank lines before current line
        blank_count = 0
        j = i - 1
        while j >= 0 and lines[j].strip() == '':
            blank_count += 1
            j -= 1

        # Find the previous non-blank line
        prev_non_blank_idx = j

        # Determine required blank lines
        required_blanks = 0

        # Check if we have a previous non-blank line
        prev_is_decorator = False
        if prev_non_blank_idx >= 0:
            prev_stripped = lines[prev_non_blank_idx].strip()
            prev_is_decorator = prev_stripped.startswith('@')

        # Determine required blank lines based on current line type
        # Special case: decorator followed by def/class (E304 - no blank lines)
        if is_def and prev_is_decorator:
            required_blanks = 0
        # Decorator at start of class methods (E301 - needs 1 blank line before decorator)
        elif is_decorator and indent_level > 0:
            # This is a decorator for a method - need 1 blank line before it (E301)
            # unless the previous line is also a decorator
            if not prev_is_decorator:
                required_blanks = 1
        # Top-level class definitions (E302 - 2 blank lines)
        elif is_class and is_top_level:
            required_blanks = 2
        # Top-level function definitions (E302 - 2 blank lines)
        elif is_func and is_top_level:
            required_blanks = 2
        # Method/nested function definitions (E306 - 1 blank line)
        elif is_method:
            required_blanks = 1
        # For regular code lines, preserve existing blank lines (up to max 2)
        elif stripped != '':
            # Preserve blank lines within code blocks, but limit to max 2 (E303)
            required_blanks = min(blank_count, 2)

        # Add the required blank lines
        for _ in range(required_blanks):
            new_lines.append('\n')

        # Add current line to new_lines (skip if it's a blank line - already handled)
        if stripped != '':
            new_lines.append(current_line)

        i += 1

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def ensure_final_newline(file_path: str) -> None:
    """
    Ensure file ends with a single newline (PEP8 requirement).

    Args:
        file_path: Path to the Python file to clean.

    Return:
        None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if content and not content.endswith('\n'):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content + '\n')


def validate_definition_spacing(file_path: str) -> None:
    """
    Validate and fix blank lines before class and function definitions.

    Ensures:
    - 2 blank lines before top-level class definitions (E302)
    - 2 blank lines before top-level function definitions (E302)
    - 1 blank line before method definitions in classes (E301)
    - 0 blank lines between decorator and definition (E304)

    This is a final validation step after all other cleaning operations.

    Args:
        file_path: Path to the Python file to validate.

    Return:
        None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if not lines:
        return

    new_lines = []
    i = 0

    while i < len(lines):
        current_line = lines[i]
        stripped = current_line.strip()

        # Determine indentation and line type
        indent_level = len(current_line) - len(current_line.lstrip())
        is_top_level = indent_level == 0
        is_decorator = stripped.startswith('@')
        is_class = stripped.startswith('class ')
        is_func = stripped.startswith('def ')
        is_definition = is_class or is_func

        # Count existing blank lines before this line
        blank_count = 0
        j = len(new_lines) - 1
        while j >= 0 and new_lines[j].strip() == '':
            blank_count += 1
            j -= 1

        # Check previous non-blank line
        prev_non_blank_idx = j
        prev_is_decorator = False
        prev_is_import = False
        prev_is_comment = False

        if prev_non_blank_idx >= 0:
            prev_stripped = new_lines[prev_non_blank_idx].strip()
            prev_is_decorator = prev_stripped.startswith('@')
            prev_is_import = prev_stripped.startswith('import ') or prev_stripped.startswith('from ')
            prev_is_comment = prev_stripped.startswith('#')

        # Determine required blank lines
        required_blanks = blank_count  # Default: keep existing

        if is_definition:
            # Definition right after decorator: no blank lines (E304)
            if prev_is_decorator:
                required_blanks = 0
            # Top-level class or function (E302): 2 blank lines
            elif is_top_level:
                # Skip if this is the first definition in file (after imports/header)
                if prev_non_blank_idx >= 0 and not (prev_is_import or prev_is_comment):
                    required_blanks = 2
                elif prev_is_import or prev_is_comment:
                    # After imports or comments, we want 2 blank lines
                    required_blanks = 2
            # Method in class (E301): 1 blank line
            else:
                if not prev_is_decorator:
                    required_blanks = 1
        elif is_decorator:
            # Decorator for a method (inside class): 1 blank line before it
            if indent_level > 0 and not prev_is_decorator:
                required_blanks = 1
            # Top-level decorator: 2 blank lines
            elif is_top_level and not prev_is_decorator:
                if prev_non_blank_idx >= 0 and not (prev_is_import or prev_is_comment):
                    required_blanks = 2

        # Remove excess blank lines
        while blank_count > required_blanks and new_lines:
            if new_lines[-1].strip() == '':
                new_lines.pop()
                blank_count -= 1
            else:
                break

        # Add missing blank lines
        while blank_count < required_blanks:
            new_lines.append('\n')
            blank_count += 1

        # Add current line
        new_lines.append(current_line)
        i += 1

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)


def sort_imports(file_path: str) -> None:
    """
    Sort and organize import statements into three groups:
    Standard library, Third-party, and Boxel (local) modules.

    Args:
        file_path: Path to the Python file to clean.

    Return:
        None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if not lines:
        return

    # Categorize imports
    standard_imports = []
    third_party_imports = []
    boxel_imports = []

    header_lines = []
    after_imports_lines = []

    in_header = True
    in_imports = False
    imports_done = False

    # Section header comments to skip
    section_headers = [
        '# Standard modules',
        '# Third-party modules',
        '# Boxel modules'
    ]

    for line in lines:
        stripped = line.strip()

        # Skip section header comments - we'll re-add them only if needed
        if stripped in section_headers:
            continue

        # Collect header (comments at the top)
        if in_header:
            if stripped.startswith('#') or stripped == '':
                header_lines.append(line)
                continue
            else:
                in_header = False

        # Process imports
        if not imports_done:
            if stripped.startswith('import ') or stripped.startswith('from '):
                in_imports = True
                # Categorize the import
                if stripped.startswith('from .'):
                    boxel_imports.append(line)
                elif any(pkg in stripped for pkg in ['sgtk', 'PySide', 'PyQt', 'Qt']):
                    third_party_imports.append(line)
                else:
                    # Extract module name
                    if stripped.startswith('import '):
                        module_name = stripped.split()[1].split('.')[0].split(',')[0]
                    else:  # from X import Y
                        module_name = stripped.split()[1].split('.')[0]

                    if ai_helper._is_standard_library(module_name):
                        standard_imports.append(line)
                    else:
                        third_party_imports.append(line)
            elif in_imports and stripped.startswith('#'):
                # Comment within imports section - skip to avoid duplicates
                continue
            elif in_imports and stripped == '':
                # Blank line during imports - continue
                continue
            elif in_imports and stripped:
                # First non-import, non-comment line after imports
                imports_done = True
                after_imports_lines.append(line)
            elif not in_imports and stripped:
                # Non-import line before any imports started
                after_imports_lines.append(line)
                imports_done = True
        else:
            after_imports_lines.append(line)

    # Sort imports alphabetically within each group
    standard_imports.sort()
    third_party_imports.sort()
    boxel_imports.sort()

    # Rebuild file with organized imports
    new_content = []

    # Add header
    if header_lines:
        new_content.extend(header_lines)

    # Add Standard modules section (only if we have standard imports)
    if standard_imports:
        new_content.append('\n')
        new_content.append('# Standard modules\n')
        new_content.extend(standard_imports)

    # Add Third-party modules section (only if we have third-party imports)
    if third_party_imports:
        # Add spacing before this section
        if standard_imports:
            new_content.append('\n')
            new_content.append('\n')
        else:
            new_content.append('\n')
        new_content.append('# Third-party modules\n')
        new_content.extend(third_party_imports)

    # Add Boxel modules section (only if we have local imports)
    if boxel_imports:
        # Add spacing before this section
        if standard_imports or third_party_imports:
            new_content.append('\n')
            new_content.append('\n')
        else:
            new_content.append('\n')
        new_content.append('# Boxel modules\n')
        new_content.extend(boxel_imports)

    # Add rest of file
    if after_imports_lines:
        # Add appropriate spacing before the rest of the code
        if standard_imports or third_party_imports or boxel_imports:
            new_content.append('\n')
            new_content.append('\n')
        new_content.extend(after_imports_lines)

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_content)


def check_line_length(file_path: str, max_length: int = 79) -> List[Tuple[int, int, str]]:
    """
    Check for lines exceeding maximum length (PEP8: 79 characters).

    Args:
        file_path: Path to the Python file to check.
        max_length: Maximum allowed line length.

    Return:
        List of tuples (line_number, line_length, line_content) for
        lines exceeding max_length.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    violations: List[Tuple[int, int, str]] = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, start=1):
            # Remove newline for length check
            line_content = line.rstrip('\n')
            if len(line_content) > max_length:
                violations.append((line_num, len(line_content), line_content))

    return violations


def remove_unused_imports(file_path: str) -> List[str]:
    """
    Identify potentially unused imports (basic check).

    Args:
        file_path: Path to the Python file to analyze.

    Return:
        List of import statements that appear unused.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        lines = content.split('\n')

    unused: List[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('import '):
            # Extract module name
            module = stripped.replace('import ', '').split(' as ')[0].split(',')[0].strip()
            # Check if used in code
            if content.count(module) == 1:  # Only the import line
                unused.append(line)
        elif stripped.startswith('from '):
            # Extract imported names
            match = re.match(r'from\s+\S+\s+import\s+(.+)', stripped)
            if match:
                imports = match.group(1)
                for imp in imports.split(','):
                    name = imp.split(' as ')[-1].strip()
                    if content.count(name) == 1:  # Only the import line
                        unused.append(line)
                        break

    return unused


def clean_file(file_path: str, max_line_length: int = 79) -> dict:
    """
    Apply all cleaning operations to a Python file.

    Args:
        file_path: Path to the Python file to clean.
        max_line_length: Maximum allowed line length for checking.

    Return:
        Dictionary with cleaning results and any warnings.
    """
    results = {
        'file': file_path,
        'cleaned': False,
        'warnings': []
    }

    try:
        # Apply cleaning functions
        remove_empty_spaces(file_path)
        remove_multiple_blank_lines(file_path)
        ensure_final_newline(file_path)

        # Check for issues
        long_lines = check_line_length(file_path, max_line_length)
        if long_lines:
            results['warnings'].append(
                f"Found {len(long_lines)} lines exceeding {max_line_length} characters"
            )

        unused = remove_unused_imports(file_path)
        if unused:
            results['warnings'].append(
                f"Found {len(unused)} potentially unused imports"
            )

        results['cleaned'] = True

    except Exception as e:
        results['warnings'].append(f"Error during cleaning: {str(e)}")

    return results


def has_boxel_header(file_path: str) -> bool:
    """
    Check if a Python file has the Boxel Studio header.

    Args:
        file_path: Path to the Python file to check.

    Return:
        True if file has Boxel header, False otherwise.
    """
    if not os.path.isfile(file_path):
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            first_lines = ''.join(file.readlines()[:10])

        # Check for Boxel Studio copyright
        val_1 = 'Copyright (c)' in first_lines and 'Boxel Studio' in first_lines
        # Check for Autodesk copyright (legacy)
        val_2 = 'Copyright (c)' in first_lines
        return val_1 or val_2
    except Exception:
        return False


def add_boxel_header(file_path: str, description: Optional[str] = None) -> None:
    """
    Add Boxel Studio header to a Python file if it doesn't have one.

    Args:
        file_path: Path to the Python file.
        description: Optional description for the file. If None, will
                     be auto-generated.

    Return:
        None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    # Check if already has header
    if has_boxel_header(file_path):
        return

    # Read current content
    with open(file_path, 'r', encoding='utf-8') as file:
        original_content = file.read()

    # Generate description if not provided
    if description is None:
        description = ai_helper.generate_file_description(file_path)

    # Get filename
    filename = os.path.basename(file_path)

    # Get current year
    current_year = datetime.datetime.now().year

    # Create header
    header = f"""#
# Copyright (c) {current_year} Boxel Studio.
#
# :Module: {filename}
# :Description: {description}
#
# :Author: Fidel Moreno Miranda <fidel.moreno@boxelstudio.com>
#

"""

    # Remove any existing shebang or encoding declarations
    lines = original_content.split('\n')
    content_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#!') or 'coding:' in stripped or 'coding=' in stripped:
            content_start = i + 1
        elif stripped:
            break

    # Combine header with original content
    if content_start > 0:
        new_content = header + '\n'.join(lines[content_start:])
    else:
        new_content = header + original_content

    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)


def update_header_description(file_path: str, description: Optional[str] = None) -> None:
    """
    Update the description in an existing Boxel header.

    Args:
        file_path: Path to the Python file.
        description: New description. If None, will be auto-generated.

    Return:
        None
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not file_path.endswith('.py'):
        raise ValueError("The file must be a Python (.py) file.")

    # Generate description if not provided
    if description is None:
        description = ai_helper.generate_file_description(file_path)

    # Read file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace "Brief description." with actual description
    updated_content = re.sub(
        r'# :Description: Brief description\.',
        f'# :Description: {description}',
        content
    )

    # Write back
    if updated_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)


def clean_file_professional(file_path: str, max_line_length: int = 79) -> dict:
    """
    Apply all professional cleaning operations including header management.

    Args:
        file_path: Path to the Python file to clean.
        max_line_length: Maximum allowed line length for checking.

    Return:
        Dictionary with cleaning results and any warnings.
    """
    results = {
        'file': file_path,
        'cleaned': False,
        'warnings': [],
        'actions': []
    }

    try:
        # Add header if missing
        if not has_boxel_header(file_path):
            add_boxel_header(file_path)
            results['actions'].append('Added Boxel Studio header')
        else:
            # Update description if it's the default
            update_header_description(file_path)
            results['actions'].append('Updated header description')

        # Sort imports into categories
        sort_imports(file_path)
        results['actions'].append('Organized imports into categories')

        # Normalize blank lines according to Flake8/PEP8
        normalize_blank_lines(file_path)
        results['actions'].append('Normalized blank lines (Flake8 E30x)')

        # Apply standard cleaning
        remove_empty_spaces(file_path)
        results['actions'].append('Removed trailing whitespace')

        remove_multiple_blank_lines(file_path)
        results['actions'].append('Reduced excessive blank lines')

        ensure_final_newline(file_path)
        results['actions'].append('Ensured final newline')

        # Final validation: ensure correct spacing before definitions
        validate_definition_spacing(file_path)
        results['actions'].append('Validated definition spacing (E301, E302, E304)')

        # Check for issues
        long_lines = check_line_length(file_path, max_line_length)
        if long_lines:
            results['warnings'].append(
                f"Found {len(long_lines)} lines exceeding {max_line_length} characters"
            )

        unused = remove_unused_imports(file_path)
        if unused:
            results['warnings'].append(
                f"Found {len(unused)} potentially unused imports"
            )

        results['cleaned'] = True

    except Exception as e:
        results['warnings'].append(f"Error during cleaning: {str(e)}")

    return results

if __name__ == '__main__':
    import sys
    import json

    if len(sys.argv) < 2:
        print(json.dumps({
            'success': False,
            'error': 'Usage: python code_cleaner.py <file_path>'
        }))
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        results = clean_file_professional(file_path)
        print(json.dumps(results))
        sys.exit(0 if results.get('cleaned') else 1)
    except Exception as e:
        print(json.dumps({
            'success': False,
            'error': str(e),
            'file': file_path
        }))
        sys.exit(1)
