#
# Copyright (c) Nneex enterprise
# Tools for VFX
#
# Dev. Fidel Moreno Miranda
# fidelm02@gmail.com
#

# Built-in modules
import datetime
import logging
import os
import subprocess
import sys

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
home_folder = os.path.expanduser("~")
file_handler = logging.FileHandler(
    os.path.join(home_folder, 'logs', 'VSCODE_UI_to_SGTK_Py_converter.log'))
logger.addHandler(file_handler)


def run_cmd_command(command: str):
    """
    Runs a Git command and returns its output.
    Raises an exception if the command fails.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            shell=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing command: {e.cmd}")
        logger.error(f"Stdout: {e.stdout}")
        logger.error(f"Stderr: {e.stderr}")
        raise


def main():
    """ Main function to convert a .ui file to a .py file using PyQt's
    pyuic6 tool.

    It takes the path to the .ui file as a command line argument.
    If the .ui file is in a specific folder structure, it will save the
    generated .py file in the corresponding folder.
    """
    if len(sys.argv) > 1:
        ui_path = sys.argv[1]

        # Check if a ui folder exists
        resources_folder = os.path.dirname(ui_path)
        main_app_folder = os.path.dirname(resources_folder)
        ui_folder = os.path.join(main_app_folder, "python", "app", "ui")
        if not os.path.exists(ui_folder):
            ui_py_path = ui_path.replace('.ui', '.py')
        else:
            # If the ui folder exists, save the python file in that folder
            ui_py_path = os.path.join(
                ui_folder,
                os.path.basename(ui_path).replace('.ui', '.py'))

        # Command to convert .ui file to .py file using pyuic6
        # Ensure that 'pyuic6.exe' is in your PATH or provide the full path to it
        cmd = f"pyuic6.exe -x {ui_path} -o {ui_py_path}"
        run_cmd_command(cmd)

        # Open the python file
        with open(ui_py_path, "r") as file:
            content = file.read()
            print(content)
        # Remove content first line
        content = "\n".join(content.split("\n")[1:])

        new_imports = (
            "import sgtk\n\n"
            "if hasattr(sgtk.platform.qt5, \"QtCore\"):\n"
            "    from sgtk.platform.qt5 import QtCore, QtGui, QtWidgets\n"
            "else:\n"
            "    from sgtk.platform.qt6 import QtCore, QtGui, QtWidgets\n\n"
            "# Make elements available\n"
            "for module in (QtCore, QtGui, QtWidgets):\n"
            "    for name, cls in module.__dict__.items():\n"
            "        if isinstance(cls, type):\n"
            "            globals()[name] = cls"
        )
        content = content.replace(
            "from PyQt6 import QtCore, QtGui, QtWidgets", new_imports)
        # Update the content
        with open(ui_py_path, "w") as file:
            now = datetime.datetime.now()
            file.write("# This file is auto-generated from UI_to_SGTK_Py.py\n")
            file.write(
                f"# Generated on: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(content)

        logger.info(f"Converted {ui_path} to {ui_py_path} successfully.")
    else:
        logger.error("No argument received by Python script.")


if __name__ == "__main__":
    main()
