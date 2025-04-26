@echo off

SET hiding_path=%~dp0dist\hiding.exe
SET recovery_path=%~dp0dist\recovery.exe

echo.
echo "[*] Adding registry entries for Hide File (Create lnk File) and Recover File (Extract File)..."
echo.

reg add "HKEY_CLASSES_ROOT\*\shell\Hide File" /t REG_SZ /v "" /d "Hide File (Create lnk File)" /f
reg add "HKEY_CLASSES_ROOT\*\shell\Hide File\command" /t REG_SZ /v "" /d "\"%hiding_path%\" --file_path \"%%1\"" /f

reg add "HKEY_CLASSES_ROOT\Lnkfile\shell\Recover File" /t REG_SZ /v "" /d "Recover File (Extract File)" /f
reg add "HKEY_CLASSES_ROOT\Lnkfile\shell\Recover File\command" /t REG_SZ /v "" /d "\"%recovery_path%\" --link_file_path \"%%1\"" /f

reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\Recover All" /t REG_SZ /v "" /d "Recover All (Extract All Files)" /f
reg add "HKEY_CLASSES_ROOT\Directory\Background\shell\Recover All\command" /t REG_SZ /v "" /d "\"%recovery_path%\" --all" /f

pause 