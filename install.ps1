# install.ps1

echo "[*] Installing environment with uv.`n"
uv sync
echo "`n---------------------------------`n"


echo "[*] Initializing databases.`n"
$output = uv run init_db.py
if ($output -eq "[-] PASSWORD ERROR") {
    Write-Host "[-] Passwords do not match!"
    Write-Host "[!] Installation Failed!!!"
    exit 1
}
echo "`n---------------------------------`n"


echo "[*] Building executables.`n"

if (Test-Path "dist") {
    Remove-Item -Recurse -Force dist        # Clean build
}

uv run pyinstaller -F linker.py --uac-admin --manifest admin.manifest
uv run pyinstaller -F hiding.py
uv run pyinstaller -F recovery.py
echo "`n---------------------------------`n"


echo "[*] Removing unnecessary files.`n"
rm *.spec
rm -r build/
echo "`n---------------------------------`n"
Write-Host "[+] Installation completed successfully."
