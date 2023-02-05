SET hiding_path=%~dp0dist\hiding.exe
SET recovery_path=%~dp0dist\recovery.exe

reg add "HKEY_CLASSES_ROOT\*\shell\runas" /t REG_SZ /v "" /d "Hide File" /f
reg add "HKEY_CLASSES_ROOT\*\shell\runas\command" /t REG_SZ /v "" /d "\"%hiding_path%\" --hidefile \"%%1\"" /f

reg add "HKEY_CLASSES_ROOT\*\shell\Recover File (Extract File)" /t REG_SZ /v "" /d "" /f
reg add "HKEY_CLASSES_ROOT\*\shell\Recover File (Extract File)\command" /t REG_SZ /v "" /d "\"%recovery_path%\" --recoverfile \"%%3\"" /f

pause