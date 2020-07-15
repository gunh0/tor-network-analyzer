import easygui

# fileopenbox: fileopenbox returns the name of a file

def OpenWinFileExplorer():
    multiSearchFilePath = easygui.fileopenbox()
    return multiSearchFilePath