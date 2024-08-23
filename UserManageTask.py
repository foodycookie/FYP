from tkinter import *
from tkinter import messagebox
from datetime import date, datetime
from library.tkcalendar import *
from Database import *
from MainWindowSingleton import *
    
def UserEditCustomTaskWindow(selectedCustomTask):
    def DisableButton():
        dueDateButton.config(state=DISABLED)
        checkOffButton.config(state=DISABLED)
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        dueDateButton.config(state=NORMAL)
        checkOffButton.config(state=NORMAL)
        updateButton.config(state=NORMAL)
        deleteButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        
    def UpdateButtonText():
        dueDateButton.config(text=selectedDate)
        
    def OpenCalendar():
        def onDateSelect():
            nonlocal selectedDate 
            selectedDate = cal.get_date()
            selectedDate = datetime.strptime(selectedDate, "%Y-%m-%d").date()
            UpdateButtonText()
            EnableButton()
            top.destroy()
        
        dueDateButton.config(state=DISABLED)
        checkOffButton.config(state=DISABLED)
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)

        top = Toplevel(window)
        top.title("Select Due Date")

        cal = Calendar(top, selectmode='day', year=selectedYear, month=selectedMonth, day=selectedDay, date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)

        selectButton = Button(top, text="Select Due Date", command=onDateSelect)
        selectButton.pack(pady=10)
        
    def CheckOff():
        companionStat = FetchRecord('Companion', columns=['companionID', 'level', 'friendshipPoint', 'friendshipPointNext', 'friendshipPointMultiplier'], where_clause='userID = ?', params=(userID,))[0] 

        companionID = companionStat[0]
        # level = companionStat[1]
        friendshipPoint = companionStat[2]
        # friendshipPointNext = companionStat[3]
        friendshipPointMultiplier = companionStat[4]
            
        if difficulty == "Easy":
            friendshipPoint += (20 * friendshipPointMultiplier)
        elif difficulty == "Medium":
            friendshipPoint += (60 * friendshipPointMultiplier)
        elif difficulty == "Hard":
            friendshipPoint += (180 * friendshipPointMultiplier)
        elif difficulty == "Extreme":
            friendshipPoint += (540 * friendshipPointMultiplier)
        
        UpdateRecord('Companion',  {'friendshipPoint': friendshipPoint}, 'companionID = ?', (companionID,))
        
        CreateRecord('Completed_Custom_Task', {'customTaskID': customTaskID, 'completedDate': date.today(), 'isOverdue': 0})
        
        DisableButton()
        messagebox.showinfo("Success", "You completed a task!")
        EnableButton()
        
        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def Update():
        title = titleEntry.get("1.0", "end-1c").strip()
        note = noteEntry.get("1.0", "end-1c").strip()
        
        if not title or not note:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return
        
        if selectedDate < date.today():
            DisableButton()
            messagebox.showerror("Error", "Please choose a valid date.")
            EnableButton()
            return
    
        UpdateRecord('Custom_Task', {'title': title, 'note': note, 'difficulty': difficultyVariable.get(), 'dueDate': selectedDate}, 'customTaskID = ?', (customTaskID,))
        
        DisableButton()
        messagebox.showinfo("Success", "Task updated!")
        EnableButton()

        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def Delete():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to delete the task?")
        
        if askUserYesNoBool:
            DeleteRecord('Custom_Task', 'customTaskID = ?', (customTaskID,))
            
            messagebox.showinfo("Success", "Task deleted!")
        
            window.destroy()
            from Task import TaskWindow
            TaskWindow()
            
        else:
            EnableButton()
            
    def Back():
        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def Quit():
        RemoveMainWindow("MainWindow")
        
    customTaskID = selectedCustomTask[0]
    title = selectedCustomTask[1]
    note = selectedCustomTask[2]
    difficulty = selectedCustomTask[3] 
    dueDate = selectedCustomTask[4]  
    
    selectedDate = datetime.strptime(dueDate, "%Y-%m-%d").date()
        
    selectedYear = selectedDate.year
    selectedMonth = selectedDate.month
    selectedDay = selectedDate.day

    window = Toplevel()
    
    windowWidth = 360
    windowHeight = 360
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("User Edit Custom Task")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('UserEditCustomTaskWindow', window)
    
    app = Singleton.getMainWindowInstance()
    
    userID = app.user[0]
    # username = app.user[1]
    # password = app.user[2]
    # birthdate = app.user[3]
    # lastLogin = app.user[4]
    # isReminder = app.user[5]
    # intervalHour = app.user[6]

    frame1 = Frame(window)
    frame1.pack(padx=5, fill=BOTH, expand=1)

    frame2 = Frame(window)
    frame2.pack(padx=5, fill=BOTH, expand=1)

    frame3 = Frame(window)
    frame3.pack(padx=5, fill=BOTH, expand=1)

    frame4 = Frame(window)
    frame4.pack(padx=5, fill=BOTH, expand=1)

    frame5 = Frame(window)
    frame5.pack(padx=5, fill=BOTH, expand=1)

    frame6 = Frame(window)
    frame6.pack(padx=5, fill=BOTH, expand=1)

    frame7 = Frame(window)
    frame7.pack(padx=5, fill=BOTH, expand=1)

    frame8 = Frame(window)
    frame8.pack(padx=5, fill=BOTH, expand=1)
    
    Label(frame1, text="Title").pack(side=LEFT, padx=10)
    titleEntry = Text(frame2, height=3, width=40)
    titleEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    titleEntry.insert("1.0", title)

    Label(frame3, text="Note").pack(side=LEFT, padx=10)
    noteEntry = Text(frame4, height=3, width=40)
    noteEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    noteEntry.insert("1.0", note)
    
    Label(frame5, text="Difficulty").pack(side=LEFT, padx=10)
    
    difficultyOption = ["Easy", "Medium", "Hard", "Extreme"]
    
    difficultyVariable = StringVar()

    if difficulty == "Easy":
        difficultyVariable.set(difficultyOption[0])
    elif difficulty == "Medium":
        difficultyVariable.set(difficultyOption[1])
    elif difficulty == "Hard":
        difficultyVariable.set(difficultyOption[2])
    elif difficulty == "Extreme":
        difficultyVariable.set(difficultyOption[3])

    difficultyDropdownOption = OptionMenu(frame5, difficultyVariable, *difficultyOption)
    difficultyDropdownOption.pack(side=RIGHT, padx=10)
    
    Label(frame6, text="Due Date").pack(side=LEFT, padx=10)
    dueDateButton = Button(frame6, text=dueDate, command=OpenCalendar)
    dueDateButton.pack(side=RIGHT, padx=10)
    
    checkOffButton = Button(frame7, text="Check Off", command=CheckOff)
    checkOffButton.pack(fill=BOTH, expand=1, padx=30, pady=10)

    frame8Left = Frame(frame8)
    frame8Left.pack(side=LEFT, expand=True)

    frame8Middle = Frame(frame8)
    frame8Middle.pack(side=LEFT, expand=True)

    frame8Right = Frame(frame8)
    frame8Right.pack(side=LEFT, expand=True)

    updateButton = Button(frame8Left, text="Update", command=Update)
    updateButton.pack(anchor=W, padx=10, pady=10)

    deleteButton = Button(frame8Middle, text="Delete", command=Delete)
    deleteButton.pack(anchor=CENTER, padx=10, pady=10)

    backButton = Button(frame8Right, text="Back", command=Back)
    backButton.pack(anchor=E, padx=10, pady=10)

    window.mainloop()
    
def UserEditDailyTaskWindow(selectedDailyTask):
    def DisableButton():
        checkOffButton.config(state=DISABLED)
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        checkOffButton.config(state=NORMAL)
        updateButton.config(state=NORMAL)
        deleteButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
             
    def CheckOff():
        companionStat = FetchRecord('Companion', columns=['companionID', 'level', 'friendshipPoint', 'friendshipPointNext', 'friendshipPointMultiplier'], where_clause='userID = ?', params=(userID,))[0] 

        companionID = companionStat[0]
        # level = companionStat[1]
        friendshipPoint = companionStat[2]
        # friendshipPointNext = companionStat[3]
        friendshipPointMultiplier = companionStat[4]
            
        if difficulty == "Easy":
            friendshipPoint += (10 * friendshipPointMultiplier)
        elif difficulty == "Medium":
            friendshipPoint += (30 * friendshipPointMultiplier)
        elif difficulty == "Hard":
            friendshipPoint += (90 * friendshipPointMultiplier)
        elif difficulty == "Extreme":
            friendshipPoint += (270 * friendshipPointMultiplier)
        
        UpdateRecord('Companion',  {'friendshipPoint': friendshipPoint}, 'companionID = ?', (companionID,))
        
        CreateRecord('Completed_Daily_Task', {'dailyTaskID': dailyTaskID, 'completedDate': date.today(), 'isOverdue': 0})
        
        DisableButton()
        messagebox.showinfo("Success", "You completed a task!")
        EnableButton()
        
        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def Update():
        title = titleEntry.get("1.0", "end-1c").strip()
        note = noteEntry.get("1.0", "end-1c").strip()
        
        if not title or not note:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return
    
        UpdateRecord('Daily_Task', {'title': title, 'note': note, 'difficulty': difficultyVariable.get()}, 'dailyTaskID = ?', (dailyTaskID,))

        DisableButton()
        messagebox.showinfo("Success", "Task updated!")
        EnableButton()

        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def Delete():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to delete the task?")
        
        if askUserYesNoBool:
            DeleteRecord('Daily_Task', 'dailyTaskID = ?', (dailyTaskID,))
            
            messagebox.showinfo("Success", "Task deleted!")
        
            window.destroy()
            from Task import TaskWindow
            TaskWindow()
            
        else:
            EnableButton()
            
    def Back():
        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()    
        app.OnClose()
        
    dailyTaskID = selectedDailyTask[0]
    title = selectedDailyTask[1]
    note = selectedDailyTask[2]
    difficulty = selectedDailyTask[3] 

    window = Toplevel()
    
    windowWidth = 360
    windowHeight = 340
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("User Edit Daily Task")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('UserEditDailyTaskWindow', window)
    
    app = Singleton.getMainWindowInstance()
    
    userID = app.user[0]
    # username = app.user[1]
    # password = app.user[2]
    # birthdate = app.user[3]
    # lastLogin = app.user[4]
    # isReminder = app.user[5]
    # intervalHour = app.user[6]

    frame1 = Frame(window)
    frame1.pack(padx=5, fill=BOTH, expand=1)
    
    frame2 = Frame(window)
    frame2.pack(padx=5, fill=BOTH, expand=1)

    frame3 = Frame(window)
    frame3.pack(padx=5, fill=BOTH, expand=1)

    frame4 = Frame(window)
    frame4.pack(padx=5, fill=BOTH, expand=1)

    frame5 = Frame(window)
    frame5.pack(padx=5, fill=BOTH, expand=1)

    frame6 = Frame(window)
    frame6.pack(padx=5, fill=BOTH, expand=1)

    frame7 = Frame(window)
    frame7.pack(padx=5, fill=BOTH, expand=1)
    
    Label(frame1, text="Title").pack(side=LEFT, padx=10)
    titleEntry = Text(frame2, height=3, width=40)
    titleEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    titleEntry.insert("1.0", title)

    Label(frame3, text="Note").pack(side=LEFT, padx=10)
    noteEntry = Text(frame4, height=3, width=40)
    noteEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    noteEntry.insert("1.0", note)
    
    Label(frame5, text="Difficulty").pack(side=LEFT, padx=10)
    
    difficultyOption = ["Easy", "Medium", "Hard", "Extreme"]
    
    difficultyVariable = StringVar()

    if difficulty == "Easy":
        difficultyVariable.set(difficultyOption[0])
    elif difficulty == "Medium":
        difficultyVariable.set(difficultyOption[1])
    elif difficulty == "Hard":
        difficultyVariable.set(difficultyOption[2])
    elif difficulty == "Extreme":
        difficultyVariable.set(difficultyOption[3])

    difficultyDropdownOption = OptionMenu(frame5, difficultyVariable, *difficultyOption)
    difficultyDropdownOption.pack(side=RIGHT, padx=10)
    
    checkOffButton = Button(frame7, text="Check Off", command=CheckOff)
    checkOffButton.pack(fill=BOTH, expand=1, padx=30, pady=10)

    frame7Left = Frame(frame7)
    frame7Left.pack(side=LEFT, expand=True)

    frame7Middle = Frame(frame7)
    frame7Middle.pack(side=LEFT, expand=True)

    frame7Right = Frame(frame7)
    frame7Right.pack(side=LEFT, expand=True)

    updateButton = Button(frame7Left, text="Update", command=Update)
    updateButton.pack(anchor=W, padx=10, pady=10)

    deleteButton = Button(frame7Middle, text="Delete", command=Delete)
    deleteButton.pack(anchor=CENTER, padx=10, pady=10)

    backButton = Button(frame7Right, text="Back", command=Back)
    backButton.pack(anchor=E, padx=10, pady=10)

    window.mainloop()