from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import os
from pathlib import Path
from MainWindowSingleton import *
from WindowManager import *
import pandas as pd

def TaskHistoryWindow():
    def DisableButton():
        backButton.config(state=DISABLED)
        taskHistoryGraphButton.config(state=DISABLED)
        exportButton.config(state=DISABLED)
        
    def EnableButton():
        backButton.config(state=NORMAL)
        taskHistoryGraphButton.config(state=NORMAL)
        exportButton.config(state=NORMAL)
        
    def Back():
        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def GetCompletedTask():
        conn = sqlite3.connect('Task.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM (
        SELECT Custom_Task.title, Custom_Task.note, Custom_Task.difficulty, Completed_Custom_Task.completedDate, Completed_Custom_Task.isOverdue, Custom_Task.createdDate, 'Custom' AS Type
        FROM Completed_Custom_Task
        JOIN Custom_Task ON Completed_Custom_Task.customTaskID = Custom_Task.customTaskID
        WHERE Custom_Task.userID = ?
        UNION
        SELECT Daily_Task.title, Daily_Task.note, Daily_Task.difficulty, Completed_Daily_Task.completedDate, Completed_Daily_Task.isOverdue,  Daily_Task.createdDate, 'Daily' AS Type
        FROM Completed_Daily_Task
        JOIN Daily_Task ON Completed_Daily_Task.dailyTaskID = Daily_Task.dailyTaskID
        WHERE Daily_Task.userID = ?
        ) AS completedTasks
        ORDER BY completedDate DESC;
        ''', (userID, userID,))
        completedTasks = cursor.fetchall()
        
        conn.close()
        
        return completedTasks
        
    def ExportToExcel():
        completedTasks = GetCompletedTask()
        
        columns = ['Title', 'Note', 'Difficulty', 'CompletedDate', 'IsOverdue', 'CreatedDate', 'Type']

        dataFrame = pd.DataFrame(completedTasks, columns=columns)
    
        if os.name == "nt":  # Windows
            downloads_path = Path(os.path.join(os.environ["USERPROFILE"], "Downloads"))
        else:  # Mac/Linux
            downloads_path = Path(os.path.join(os.path.expanduser("~"), "Downloads"))

        output_path = downloads_path / "CompletedTasks.xlsx"

        dataFrame.to_excel(output_path, index=False, engine="xlsxwriter")
        
        DisableButton()
        messagebox.showinfo("Export Success", "Export Successful in the Downloads Folder!")
        EnableButton()

    def SetupTreeview():
        columns = ["Title", "Note", "Difficulty", "Completed Date", "Is Overdue", "Created Date", "Type"]
        
        treeview["columns"] = columns
        
        treeview.column("#0", width=0, stretch=NO)
        
        for column in columns:
            treeview.column(column, anchor=CENTER, width=120)
            treeview.heading(column, text=column, anchor=CENTER)
        
    def InsertData():
        completedTasks = GetCompletedTask()
        
        for completedTask in completedTasks:
            treeview.insert("", "end", values=completedTask)
            
    def TaskHistoryGraph():
        window.destroy()
        from TaskHistoryGraph import TaskHistoryGraphWindow
        TaskHistoryGraphWindow()
            
    def Quit():
        app = Singleton.getMainWindowInstance()    
        app.OnClose()
    
    window = Toplevel()
    
    windowWidth = 945
    windowHeight = 600
    x = (window.winfo_screenwidth()//2) - (windowWidth//2)
    y = (window.winfo_screenheight()//2) - (windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Task History")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('TaskHistoryWindow', window)
    
    app = Singleton.getMainWindowInstance()
    userID = app.user[0]

    frame1 = Frame(window)
    frame1.pack(fill=BOTH, expand=1)
    
    frame2 = Frame(frame1)
    frame2.pack(fill=BOTH, expand=True, padx=5, pady=5)

    treeview = ttk.Treeview(frame2)
    treeview.pack(fill=BOTH, expand=True, side=LEFT)
    
    taskHistoryScrollbar = Scrollbar(frame2, orient='vertical', command=treeview.yview)
    taskHistoryScrollbar.pack(side=RIGHT, fill=Y)
    
    treeview.config(yscrollcommand=taskHistoryScrollbar.set)
    
    SetupTreeview()
    InsertData()

    frame3 = Frame(frame1, bg="white")
    frame3.pack(fill=X, padx=5, pady=5, side=BOTTOM)

    backButton = Button(frame3, text="Back", command=Back)
    backButton.pack(side=RIGHT, padx=20, pady=20)
    
    taskHistoryGraphButton = Button(frame3, text="Graph", command=TaskHistoryGraph)
    taskHistoryGraphButton.pack(side=RIGHT, padx=20, pady=20)
    
    exportButton = Button(frame3, text="Export to Excel", command=ExportToExcel)
    exportButton.pack(side=RIGHT, padx=20, pady=20)
    
    window.mainloop()