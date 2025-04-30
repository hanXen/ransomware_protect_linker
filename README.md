# ransomware_protect_linker
Welcome to the official repository for the implementation of methods and algorithms presented in our research paper:

### 📄 **Hiding in the Crowd: Ransomware Protection by Adopting Camouflage and Hiding Strategy With the Link File**

- 📌 Authors: Soohan Lee _et al._   
- 📌 Published in: IEEE ACCESS  
- 🔗 [Read the Full Paper Here](https://doi.org/10.1109/ACCESS.2023.3309879)

---

### **⭐ Key Concept**

**The main idea**: _Most ransomware does not target system files like `.exe` or `.dll`, or system file directories (e.g., `Program Files`, `Windows`)._ By camouflaging files with these types of extensions and hiding them in system file directories, we can safeguard valuable data from ransomware attacks in a cost-effective manner.

To solve usability challenges, we use Windows shortcut files (a.k.a. link files) to provide seamless access to hidden files.

---

## 🛠️ Usage

### Install
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

2. Verify application paths in [app_path.json](./db/app_path.json)

    - Ensure the application paths specified in `app_path.json` are correct, especially for commercial software like **Microsoft Word**, **Excel**, **PowerPoint**, and **Adobe Acrobat**.

    - To set up our default environment, install **MS Office**, **Adobe Acrobat**, **7-Zip**, and **VLC Media Player** or configure `app_path.json` with your preferred applications.

        - If the application path specified in `app_path.json` does not actually exist, the corresponding extension will not be supported automatically when performing the hiding task.

    - Alternatively, you can remove any application entries from `app_path.json` if you do not need to support them.

3. Build the project

    ```powershell
    powershell -exec bypass -f install.ps1
    ```

4. (Optional) Set up Windows context menu for quick access to file hiding and recovery (**Run as Administrator**)

    ```powershell
    Set-RightClick.bat
    ```

---

### Run

- The executables are built in the `dist` directory.

- Make sure that `hiding.exe`, `linker.exe`, `recovery.exe` are in the dist directory.

    ```powershell
    cd dist
    ```

1. **Hiding Files  (Run as Administrator):**

    - Hide all files from the testbed directory (for proof-of-concept purpose)

        ```powershell
        hiding.exe --testbed
        ```

        By default, in the proof-of-concept, all hidden files are stored in the following directory: `C:\\Windows\\Help\\Windows\\IndexStore\\en-US`.


    - Hide a specific file (or you can just right-click the file and select `'Hide File'`) 

        ```powershell
        hiding.exe --file_path [filename]
        ```

2. **Recovery:**

    - Recover all hidden files

        ```powershell
        recovery.exe --all
        ```

    - Recover a specific hidden file (or you can just right-click the shortcut and select `'Recover File (Extract File)'`)

        ```powershell
        recovery.exe --file_hash [hash]
        ```

---

### Uninstall 

- Recover all hidden files

    ```powershell
    recovery.exe --all
    ```

- Remove file hiding and recovery options from the Windows context menu (**Run as Administrator**)

    ```powershell
    Remove-RightClick.bat
    ```

---

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

### Key Points:
- This source code may be used for **academic, educational, and research purposes only**.
- You are free to **share** and **adapt** this project for **non-commercial purposes**.
- If you modify or build upon this project, you must share your contributions under the **same license** (CC BY-NC-SA 4.0).
- You must give appropriate **credit** to the original work.

For more details, please see the [LICENSE](./LICENSE) file or visit the [official license page](https://creativecommons.org/licenses/by-nc-sa/4.0/).
