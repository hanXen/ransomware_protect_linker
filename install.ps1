# install.ps1

echo "[*] Installing environment with uv.`n"
uv sync
echo "`n---------------------------------`n"


echo "[*] Initializing databases.`n"
$output = uv run init_db.py
if ($output -eq "[-] PASSWORD ERROR") {
    Write-Host "`n[-] Passwords do not match or are empty!"
    Write-Host "[!] Installation Failed!!!"
    exit 1
}
elseif ($output -eq "[!] Keyboard Interrupt") {
    Write-Host "`n`n[-] Keyboard Interrupt!"
    Write-Host "[!] Installation Failed!!!"
    exit 1
}
echo "`n---------------------------------`n"


echo "[*] Building executables.`n"

if (Test-Path "dist") {
    Remove-Item -Recurse -Force dist
}

uv run pyinstaller -F hiding.py --uac-admin --manifest admin.manifest
uv run pyinstaller -F recovery.py --uac-admin --manifest admin.manifest
uv run pyinstaller -F linker.py --uac-admin --manifest admin.manifest
echo "`n---------------------------------`n"


echo "[*] Removing unnecessary files.`n"
rm *.spec
rm -r build/
echo "`n---------------------------------`n"

Write-Host "[+] Installation completed successfully."
