# Nnexx Convert .ui to SGTK PyQT

This extension adds a right-click context menu to `.ui` and `.py` files in the Explorer, allowing you to run Python scripts to convert them into SGTK PyQT format and clean Python code according to PEP 8 / Flake8 standards.

## Features

### 1. Convert .ui to SGTK PyQT ✨
- Right-click any `.ui` file in the Explorer
- Select **"Convert .ui to SGTK PyQT"**
- Automatic conversion to SGTK PyQT format

### 2. Clean Python Files 🧹 (NEW - Enhanced!)
- Right-click any `.py` file in the Explorer or open in editor
- Select **"Clean Python file"** or use the editor command
- Automatically fixes:
  - ✅ Adds/updates Boxel Studio header
  - ✅ Organizes imports into categories
  - ✅ **Normalizes blank lines (Flake8 E30x)** ← NEW!
  - ✅ Removes trailing whitespace
  - ✅ Reduces excessive blank lines
  - ✅ Ensures final newline

#### Flake8 Rules Enforced

The code cleaner now enforces all PEP 8 blank line rules:

| Error | Rule | What It Does |
|-------|------|-------------|
| **E301** | 1 blank line between methods | Adds space between class methods |
| **E302** | 2 blank lines before top-level def/class | Separates module-level definitions |
| **E303** | Max 2 consecutive blank lines | Removes excessive blank lines |
| **E304** | No blank line after decorator | Ensures decorator binds to function |
| **E305** | 2 blank lines after top-level def/class | Same as E302 (applied when needed) |
| **E306** | 1 blank line before nested def/class | Organizes nested definitions |

## Usage

### Convert UI Files
1. Right-click a `.ui` file in the Explorer
2. Select **"Convert .ui to SGTK PyQT"**
3. Script executes automatically

### Clean Python Files

#### Option 1: From File Explorer
1. Right-click a `.py` file in the Explorer
2. Select **"Clean Python file"**
3. File will be cleaned and automatically reloaded

#### Option 2: From Editor
1. Open a `.py` file in the editor
2. Right-click in the editor and select **"Clean Python file from Editor"**
3. File will be cleaned and automatically reloaded

#### Before Cleaning
```python
import os
def function_one():
    pass
def function_two():
    pass

class MyClass:
    def method_one(self):
        pass
    def method_two(self):
        pass
```

#### After Cleaning
```python
import os


def function_one():
    pass


def function_two():
    pass


class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass
```

## Install

1. Copy this folder to your VS Code extensions directory:
   - **Windows**: `%USERPROFILE%\.vscode\extensions\`
   - **macOS/Linux**: `~/.vscode/extensions/`

2. Restart VS Code

## Documentation

### Quick Start
📖 **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Cheat sheet and common examples

### Detailed Guides
📖 **[FLAKE8_RULES.md](FLAKE8_RULES.md)** - Complete Flake8 E30x rule explanations  
📖 **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical implementation details  
📖 **[TEST_CASES.md](TEST_CASES.md)** - Before/after examples and test cases

## Configuration

### Smart File Detection
- **Unsaved changes**: If a file has unsaved edits, you'll be asked for confirmation before cleaning
- **Automatic reload**: File is automatically reloaded after cleaning
- **Warnings only**: Only warnings are displayed (no success popup)

### Python Requirements
- Python 3.6 or higher
- Standard library only (no additional packages required)

## How It Works

### Code Cleaner Pipeline
```
1. Add/update Boxel Studio header
2. Organize imports (Standard, Third-party, Boxel)
3. Normalize blank lines (Flake8 E301-E306)  ← NEW
4. Remove trailing whitespace
5. Reduce excessive blank lines (max 2)
6. Ensure file ends with newline
7. Check for long lines and unused imports
8. Report any warnings to user
```

## Advanced: Verify with Flake8

If you have Flake8 installed, you can verify the cleaning:

```bash
# Install Flake8
pip install flake8

# Check only blank line rules (E30x)
flake8 your_file.py --select=E30

# Check all rules
flake8 your_file.py

# After cleaning, should show no E30x errors
```

## Python File Structure Expected

The cleaner works best with standard Python files containing:
- Module docstrings
- Imports (organized into groups)
- Top-level functions and classes
- Nested functions and classes

## Error Handling

If cleaning fails:
1. ❌ File won't be modified
2. 📧 Error message will be displayed
3. 💾 Original file remains unchanged

## Troubleshooting

### "No file is currently open"
Make sure you have a `.py` file open in the editor when using the editor command.

### "File has unsaved changes"
Save your file or confirm in the dialog to proceed with cleaning (unsaved changes will be lost).

### Flake8 still shows errors after cleaning
- Some Flake8 errors (E5xx, W6xx, etc.) are not handled by this cleaner
- Use `flake8 --select=E30` to check only blank line rules
- Run the cleaner again if output formatting changed

## Version History

### v2.0.0 (January 27, 2026)
- ✨ Added Flake8 blank line normalization (E301-E306)
- ✨ Improved unsaved changes detection
- 🐛 Fixed duplicate import section headers
- 📖 Removed success confirmation dialog
- 📚 Added comprehensive documentation

### v1.0.0 (Previous)
- Initial release with UI conversion and basic file cleaning

## License

See [LICENSE](LICENSE) file for details.

## Author

**Fidel Moreno Miranda**  
Boxel Studio

---

**Last Updated**: January 27, 2026