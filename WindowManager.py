from tkinter import *

windows = {}
main = {}

def AddWindow(name, window):
    windows[name] = window

def RemoveWindow(name):
    if name in windows and windows[name].winfo_exists():
        windows[name].destroy()
        del windows[name]

def RemoveAllWindow():
    for name in list(windows.keys()):
        RemoveWindow(name)
        
def AddMainWindow(name, window):
    main[name] = window

def RemoveMainWindow(name):
    if name in main and main[name].winfo_exists():
        main[name].destroy()
        del main[name]
        
def WindowExists(name):
    if name in windows and windows[name].winfo_exists():
        return True
    elif name in main and main[name].winfo_exists():
        return True
    return False