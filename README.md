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

<br/>

<br/>

## C&C Server Commander (v2020.07.22)

### Table of Contents

> [GCP Tab](#GCP-Tab)
>
> - [Main Window](#Main-Window)
> - [GCP Tab Buttons](#GCP-Tab-Buttons)
>   - [Set IP (Open) : `pBtnSetGCPip`](#pBtnSetGCPip)
>   - Open : `pBtnGCP_OpenTargetList`
>   - Send CMD : `pBtnGCP_cmd`
>   - Collect : `pBtnGCP_collect`
>   - Watch : `pBtnGCP_watch`
>   - Copy : `pBtnGCP_copy`

<br/>

### GCP Tab

- ##### Main Window

![img](https://user-images.githubusercontent.com/41619898/88138535-d73bcc80-cc28-11ea-8e15-dd0337461888.png)

- ##### GCP Tab Buttons

  ```python
  ...
  
  # GCP Tab Func.
  self.pBtnSetGCPip.clicked.connect(self.pBtnSetGCPip_function)
  self.pBtnGCP_OpenTargetList.clicked.connect(self.pBtnGCP_OpenTargetList_function)
  self.pBtnGCP_cmd.clicked.connect(self.pBtnGCP_cmd_function)
  self.pBtnGCP_collect.clicked.connect(self.pBtnGCP_collect_function)
  self.pBtnGCP_watch.clicked.connect(self.pBtnGCP_watch_function)
  self.pBtnGCP_copy.clicked.connect(self.pBtnGCP_copy_function)
  
  ...
  ```

  <a name="pBtnSetGCPip"></a>

  - ##### Set IP (Open) : `pBtnSetGCPip`

  Load IP List text file path with `easygui`, Set `ip_list = []` elements

  ```python
  # file_open_easygui.py
  # fileopenbox: fileopenbox returns the name of a file
  
  import easygui
  
  def OpenWinFileExplorer():
      multiSearchFilePath = easygui.fileopenbox()
      return multiSearchFilePath
  ```

  ```python
  ...
  
      # Share
      ip_list = []
  
  ...
  
  def pBtnSetGCPip_function(self):
          print("GCP IP List Set Buttun Pressed.")
  
          # Load file path with easygui & Load IP List
          filePath = fopen.OpenWinFileExplorer()
          self.gcp_ipListPath.setText(filePath)
          print(self.gcp_ipListPath.text())
          try:
              ip_text = open(self.gcp_ipListPath.text(), "r", encoding='utf8')
          except IOError:
              print("No File.")
              return 0
          self.ip_list = ip_text.read().strip().split("\n")
          print("IP List: ", self.ip_list)
          
  ...
  ```

  Then, use the `Tkinter` to check the list of applied IPs to the user.

  ```python
  		tkWindow = Tk()     # show IP List with Tk
          tkWindow.geometry("220x200")
          tkWindow.title("IP LIST")
          labeltxt = "Number of Collectors: "+str(len(self.ip_list))
          tkLabel = Label(tkWindow, text=labeltxt)
          tkLabel.pack()
          ipListBox = Listbox(tkWindow)
          for i in range(0, len(self.ip_list)):
              ipListBox.insert(i+1, self.ip_list[i])
          ipListBox.pack(side="left", fill="both", expand=True)
          tkWindow.mainloop()
  ```

  <a name="pBtnGCP_OpenTargetList"></a>

  - **Open : `pBtnGCP_OpenTargetList`**

  <a name="pBtnGCP_cmd"></a>

  - **Send CMD : `pBtnGCP_cmd`**

  <a name="pBtnGCP_collect"></a>

  - **Collect : `pBtnGCP_collect`**

  <a name="pBtnGCP_watch"></a>

  - **Watch : `pBtnGCP_watch`**

  <a name="pBtnGCP_copy"></a>

  - **Copy : `pBtnGCP_copy`**

<br/>