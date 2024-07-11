Dim objShell
Set objShell = WScript.CreateObject("WScript.Shell")

' Cambiar al directorio donde se encuentra el script de Python
Set objFSO = CreateObject("Scripting.FileSystemObject")
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = strPath

' Ejecutar el script de Python
objShell.Run "cmd /c python app.py", 1, True

' Limpiar
Set objShell = Nothing
Set objFSO = Nothing
