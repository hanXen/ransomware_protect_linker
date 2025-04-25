@echo off

echo.
echo "[*] Removing registry entries for Hide File (Create lnk File) and Recover File (Extract File)..." 
echo.

reg delete "HKEY_CLASSES_ROOT\*\shell\Hide File" /f
reg delete "HKEY_CLASSES_ROOT\*\shell\Hide File\command" /f

reg delete "HKEY_CLASSES_ROOT\*\shell\Recover File (Extract File)" /f
reg delete "HKEY_CLASSES_ROOT\*\shell\Recover File (Extract File)\command" /f
