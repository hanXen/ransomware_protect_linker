echo "[*] Installing environment with uv.`n" + 
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
echo ""
uv run pyinstaller -F linker.py
uv run pyinstaller -F hiding.py
uv run pyinstaller -F recovery.py
echo "`n---------------------------------`n"


echo "[*] Removing unnecessary files.`n"
echo ""
rm *.spec
rm -r build/
echo "`n---------------------------------`n"
