# Anonymous Network Analysis

### Tor Browser Reference Repo.

- https://github.com/devgunho/Network_Tracking_Project

<br/>

### Convert PyQt UI to python

```powershell
pyuic5 -x input.ui -o mian.py
```

<br/>

### pyinstaller

```
# pyinstaller --clean --onefile --noconsole --icon=icon/icon.ico
pyinstaller --clean --onefile --icon=icon/icon.ico main_window.py
```

```
a = Analysis(['main_window.py'],
             pathex=[],
             binaries=[],
             datas=[('CC_Server_GUI.ui', '.')],
             ...
```

```
pyinstaller --clean --onefile --icon=icon/icon.ico main_window.spec
```

