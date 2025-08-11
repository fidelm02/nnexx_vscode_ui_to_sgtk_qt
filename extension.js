const vscode = require('vscode');
const path = require('path');
const cp = require('child_process');

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
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};