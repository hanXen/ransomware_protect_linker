# ransomware_protect_linker
Welcome to the official repository for the implementation of methods and algorithms presented in our research paper:

### 📄 **"Hiding in the Crowd: Ransomware Protection by Adopting Camouflage and Hiding Strategy With the Link File"**
- 📌 Authors: Soohan Lee _et al._   
- 📌 Published in: IEEE ACCESS  
- 🔗 [Read the Full Paper Here](https://doi.org/10.1109/ACCESS.2023.3309879)

---

### **🧠 Key Concept**

**The main idea**: _Most ransomware does not target system files like `.exe` or `.dll`, or system file directories (e.g., Program Files, System32)._ By camouflaging files with these types of extensions and hiding them in system file directories, we can safeguard valuable data from ransomware attacks in a cost-effective manner.

To solve usability challenges, we use Windows shortcut files (a.k.a. link files) to provide seamless access to hidden files without compromising security.

---

## Usage

### Installation
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and sync:

    ```bash
    uv sync
    ```

2. Build the project:

    ```powershell
    powershell -exec bypass -f install.ps1
    Set-RightClick.bat (Run as Administrator)
    ```

---

### Run

1. **Hiding Files:**

    ```powershell
    # Hide All Files (from the testbed Directory) (Run as Administrator)
    hiding.exe --testbed

    # Hide a Specific File (or you can just right-click the file) (Run as Administrator)
    hiding.exe --file_path [filename]
    ```

2. **Recovery:**

    ```powershell
    # Recover All Files
    recovery.exe --all

    # Recover a Specific File (Extract) (or you can just right-click the file)
    recovery.exe --file_hash [hash]
    ```

---

### Remove Registry Entries

```powershell
> Remove-RightClick.bat (Run as Administrator)
