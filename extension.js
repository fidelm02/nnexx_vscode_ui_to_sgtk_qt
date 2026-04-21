const vscode = require('vscode');
const path = require('path');
const cp = require('child_process');

// Reloads an on-disk file in VS Code if it's already open.
async function refreshFileInEditor(filePath) {
    try {
        const doc = await vscode.workspace.openTextDocument(vscode.Uri.file(filePath));
        await vscode.window.showTextDocument(doc, { preview: false });
        await vscode.commands.executeCommand('workbench.action.files.revert');
    } catch (err) {
        console.error('Failed to refresh document after cleaning:', err);
    }
}

// Check if a file is open and has unsaved changes
async function checkUnsavedChanges(filePath) {
    const openEditors = vscode.window.visibleTextEditors;
    const editor = openEditors.find(e => e.document.fileName === filePath);
    
    if (editor && editor.document.isDirty) {
        const choice = await vscode.window.showWarningMessage(
            `This file has unsaved changes. Do you want to proceed with cleaning?\nUnsaved edits will be lost when the file is reloaded.`,
            { modal: true },
            'Proceed',
            'Cancel'
        );
        return choice === 'Proceed';
    }
    return true;
}

function activate(context) {
    let disposable = vscode.commands.registerCommand('nnexx.convertUiToSgtk', (uri) => {
        const filePath = uri.fsPath; // Get the file system path
        

        // Validate if the file is a .ui file
        if (!filePath.endsWith('.ui')) {
            vscode.window.showErrorMessage('Please right-click on a .ui file.');
            return;
        }
        vscode.window.showInformationMessage(`Converting: ${filePath}`);
        const { exec } = require('child_process');

        // Path to the placeholder Python script
        const pythonScript = path.join(context.extensionPath, 'converter.py');

        exec(`python ${pythonScript} "${filePath}"`, (error, stdout, stderr) => {
            if (error) {
                vscode.window.showInformationMessage(`Converting: ${filePath}`);(`exec error: ${error}`);
                return;
            }
            console.log(`Python output: ${stdout}`);
            if (stderr) {
                vscode.window.showInformationMessage(`Converting: ${filePath}`);(`Python error: ${stderr}`);
            }
        });

        vscode.window.showInformationMessage(`Process complete: ${filePath}`);
    });

    context.subscriptions.push(disposable);

    context.subscriptions.push(vscode.commands.registerCommand('nnexx.removeEmptySpaces', (uri) => {
        const filePath = uri.fsPath;

        // Validate if the file is a .py file
        if (!filePath.endsWith('.py')) {
            vscode.window.showErrorMessage('Please right-click on a .py file.');
            return;
        }

        // Check for unsaved changes
        checkUnsavedChanges(filePath).then(canProceed => {
            if (!canProceed) {
                return;
            }

            vscode.window.showInformationMessage(`Cleaning Python file: ${filePath}`);

            // Path to the Python cleaning script
            const pythonScript = path.join(context.extensionPath, 'python', 'code_cleaner.py');

            const { exec } = require('child_process');
            exec(`python "${pythonScript}" "${filePath}"`, (error, stdout, stderr) => {
                if (error) {
                    vscode.window.showErrorMessage(`Error cleaning file: ${error.message}`);
                    return;
                }
                
                try {
                    // Parse the JSON output from Python
                    const result = JSON.parse(stdout);
                    console.log('Cleaning result:', result);
                    
                    // Display warnings if any
                    if (result.warnings.length > 0) {
                        const warnings = result.warnings.join('\n• ');
                        vscode.window.showWarningMessage(`Cleaning completed with warnings:\n• ${warnings}`);
                    }
                } catch (parseError) {
                    console.error('Failed to parse Python output:', stdout);
                    vscode.window.showErrorMessage(`Error parsing results: ${parseError.message}`);
                }
                
                if (stderr) {
                    console.error('Python stderr:', stderr);
                }

                refreshFileInEditor(filePath);
            });
        });
    }));

    context.subscriptions.push(vscode.commands.registerCommand('nnexx.removeEmptySpacesEditor', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No file is currently open.');
            return;
        }

        const filePath = editor.document.fileName;

        // Validate if the file is a .py file
        if (!filePath.endsWith('.py')) {
            vscode.window.showErrorMessage('This command only works with .py files.');
            return;
        }

        // Check for unsaved changes
        checkUnsavedChanges(filePath).then(canProceed => {
            if (!canProceed) {
                return;
            }

            vscode.window.showInformationMessage(`Cleaning Python file: ${filePath}`);

            // Path to the Python cleaning script
            const pythonScript = path.join(context.extensionPath, 'python', 'code_cleaner.py');

            const { exec } = require('child_process');
            exec(`python "${pythonScript}" "${filePath}"`, (error, stdout, stderr) => {
                if (error) {
                    vscode.window.showErrorMessage(`Error cleaning file: ${error.message}`);
                    return;
                }
                
                try {
                    // Parse the JSON output from Python
                    const result = JSON.parse(stdout);
                    console.log('Cleaning result:', result);
                    
                    // Display warnings if any
                    if (result.warnings.length > 0) {
                        const warnings = result.warnings.join('\n• ');
                        vscode.window.showWarningMessage(`Cleaning completed with warnings:\n• ${warnings}`);
                    }
                } catch (parseError) {
                    console.error('Failed to parse Python output:', stdout);
                    vscode.window.showErrorMessage(`Error parsing results: ${parseError.message}`);
                }
                
                if (stderr) {
                    console.error('Python stderr:', stderr);
                }

                refreshFileInEditor(filePath);
            });
        });
    }));
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};