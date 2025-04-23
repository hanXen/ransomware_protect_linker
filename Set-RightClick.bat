@echo off
SET hiding_path=%~dp0dist\hiding.exe
SET recovery_path=%~dp0dist\recovery.exe

echo. & echo [*]Adding registry entries for Hide File and Recover File (Extract File)... & echo.

reg add "HKEY_CLASSES_ROOT\*\shell\Hide File" /t REG_SZ /v "" /d "Hide File" /f
reg add "HKEY_CLASSES_ROOT\*\shell\Hide File\command" /t REG_SZ /v "" /d "\"%hiding_path%\" --file_path \"%%1\"" /f

reg add "HKEY_CLASSES_ROOT\lnkfile\shell\Recover File (Extract File)" /t REG_SZ /v "" /d "" /f
reg add "HKEY_CLASSES_ROOT\lnkfile\shell\Recover File (Extract File)\command" /t REG_SZ /v "" /d "\"%recovery_path%\" --link_file_path \"%%1\"" /f

pause