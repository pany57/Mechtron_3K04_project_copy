# PaceMaker Device Controllrt Monitor

PC based software to monitor and controll pacemaker. Build by python.

## Quick Start
Download ZIP (Win only)
1. Download in the release link
2. Unzip file
3. Click `DCM.exe` to run

Run with original code
1. Install Python 3 and Library listed below if not have it.
2. Download original code.
3. Run `main.py` (cd to this folder and run `python main.py`)

## Feature
- User Interface
    - Input Box and Button for modify
    - Output Box for monitor
- Login and Register
    - Register new identical user (Max 10)
    - Login with registered user
- Control Panel
    - Edit mode
    - Edit parameters
    - Save parameters in local file
    - Reset parameters to default value
    - Reset parameters to current pacemaker’s parameters
    - Upload parameters to pacemaker
    - Logout
- Monitor Panel
    - Testing Panel (will be removed at v1.0 version)
      - Test connect device
      - Test unconnected device
      - Test new device approach
    - Real-time e-diagram monito
      - Start Egram
      - Stop Egram
    - User Profile
      - Display user’s information
    - Device (Pacemaker) Information
      - Device connectivity status
      - Device current parameter
      - Battery status
      - Device connecting request
      - Device connection lost inform

## Released
Download DCM 0.1 **Windows** version from [Github Release](https://github.com/GJSK-Novice/Mechtron-3K04-Lab/releases/download/v0.1/DCM.v0.1.zip)


## Useage
### Python Library
- PYQT5
- PYQTgraph
- PySerial
- NumPy
- json
- jsonlines
- hashlib
- os
- sys
- datatime

Only for development (No need to download for running the program)
- PyInstaller
- PYQT5-tools

### Folder Structure
```
DCM/
├─ ui/
├─ utils/
├─ view/
├─ controller/
├─ model/
├─ appData/
├─ .gitignore
├─ main.py
├─ main.spec
├─ README.md
```
- ui: Designer User Interface .ui files, not for python program
- view: User Interface
- controller: Controller of Views
- model: class or object model
- utils: any other relevent modules
- main.spec: pyinstaller config
- appData: database
