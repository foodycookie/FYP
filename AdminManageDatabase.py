from tkinter import *
from tkinter import messagebox
from datetime import date, datetime
from library.tkcalendar import *
from Database import *
from MainWindowSingleton import *

def AdminManageUserDataWindow(selectedResult):
    def IsPositiveValue(value):
        try:
            number = float(value)
            return number > 0
        except ValueError:
            return False
        
    def DisableButton():
        birthdateButton.config(state=DISABLED)
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        birthdateButton.config(state=NORMAL)
        updateButton.config(state=NORMAL)
        deleteButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        
    def UpdateButtonText():
        birthdateButton.config(text=selectedDate)
        
    def OpenCalendar():
        def onDateSelect():
            nonlocal selectedDate 
            selectedDate = cal.get_date()
            UpdateButtonText()
            EnableButton()
            top.destroy()
        
        birthdateButton.config(state=DISABLED)
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)

        top = Toplevel(window)
        top.title("Select Birthdate")

        cal = Calendar(top, selectmode='day', year=selectedYear, month=selectedMonth, day=selectedDay, date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)

        selectButton = Button(top, text="Select Birthdate", command=onDateSelect)
        selectButton.pack(pady=10)
        
    def Update():
        newUsername = usernameEntry.get().strip()
        newPassword = passwordEntry.get().strip()
        newIntervalHour = intervalHourEntry.get().strip()
        
        if not newUsername or not newIntervalHour:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return
        
        if not IsPositiveValue(newIntervalHour) :
            DisableButton()
            messagebox.showerror("Error", "Please choose a positive number.")
            EnableButton()
            return
        
        result = FetchRecord('User', columns=['userID'], where_clause='username = ?', params=(newUsername,))
        
        if result and newUsername != username:
            DisableButton()
            messagebox.showerror("Error", "Username already exists.")
            EnableButton()
            return
        
        if newPassword:
            hashedPassword = hashingString(newPassword)
        if birthdateButton.cget("text") != "Select New Birthdate":
            hashedBirthdate = hashingString(selectedDate)
        
        renameUsernameDropdownSelectedValue = breakReminderDropdownOption.get()
        
        if renameUsernameDropdownSelectedValue == "On":
            renameUsernameDropdownSelectedValue = 1
        elif renameUsernameDropdownSelectedValue == "Off":
            renameUsernameDropdownSelectedValue = 0
            
        if not newPassword and birthdateButton.cget("text") == "Select New Birthdate":
            UpdateRecord('User', {'username': newUsername, 'isReminder': renameUsernameDropdownSelectedValue, 'intervalHour': newIntervalHour}, 'userID = ?', (userID,))
        
        elif not newPassword:
            UpdateRecord('User', {'username': newUsername, 'birthdate': hashedBirthdate, 'isReminder': renameUsernameDropdownSelectedValue, 'intervalHour': newIntervalHour}, 'userID = ?', (userID,))
            
        elif birthdateButton.cget("text") == "Select New Birthdate":
            UpdateRecord('User', {'username': newUsername, 'password': hashedPassword, 'isReminder': renameUsernameDropdownSelectedValue, 'intervalHour': newIntervalHour}, 'userID = ?', (userID,))
        
        else:    
            UpdateRecord('User', {'username': newUsername, 'password': hashedPassword, 'birthdate': hashedBirthdate, 'isReminder': renameUsernameDropdownSelectedValue, 'intervalHour': newIntervalHour}, 'userID = ?', (userID,))
        
        DisableButton()
        messagebox.showinfo("Success", "User updated!")
        EnableButton()

        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Delete():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to delete this user?")
        
        if askUserYesNoBool:
            DeleteRecord('User', 'userID = ?', (userID,))
    
            messagebox.showinfo("Success", "User deleted!")
        
            window.destroy()
            from AdminPage import AdminWindow
            AdminWindow()
            
        else:
            EnableButton()
            
    def Back():
        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()
        app.OnClose()
        
    userID = selectedResult[0]
    username = selectedResult[1]
    # password = selectedResult[2]
    # birthdate = selectedResult[3] 
    lastLogin = selectedResult[4]  
    isReminder = selectedResult[5] 
    intervalHour = selectedResult[6]  
    
    selectedDate = date.today()
        
    selectedYear = selectedDate.year
    selectedMonth = selectedDate.month
    selectedDay = selectedDate.day

    window = Toplevel()
    
    windowWidth = 500
    windowHeight = 500
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Manage User Data")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('AdminManageUserDataWindow', window)

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
    
    frame9 = Frame(window)
    frame9.pack(padx=5, fill=BOTH, expand=1)
    
    Label(frame1, text="User ID").pack(side=LEFT, padx=10)
    Label(frame1, text=userID).pack(side=RIGHT, padx=10)

    Label(frame2, text="Username").pack(side=LEFT, padx=10)
    
    usernameForEntry = StringVar()
    usernameForEntry.set(username)
    
    usernameEntry = Entry(frame2, textvariable=usernameForEntry)
    usernameEntry.pack(side=RIGHT, padx=10)

    Label(frame3, text="Password").pack(side=LEFT, padx=10)
    passwordEntry = Entry(frame3)
    passwordEntry.pack(side=RIGHT, padx=10)

    Label(frame4, text="Birthdate").pack(side=LEFT, padx=10)
    birthdateButton = Button(frame4, text="Select New Birthdate", command=OpenCalendar)
    birthdateButton.pack(side=RIGHT, padx=10)

    Label(frame5, text="Last Login").pack(side=LEFT, padx=10)
    if lastLogin == None:
        Label(frame5, text="None").pack(side=RIGHT, padx=10)
    Label(frame5, text=lastLogin).pack(side=RIGHT, padx=10)
    
    offOnOptions = ["Off", "On"]

    Label(frame6, text="Break Reminder").pack(side=LEFT, padx=5)
    
    breakReminderDropdownOption = StringVar()
    
    if isReminder == 0:
        breakReminderDropdownOption.set(offOnOptions[0])
    elif isReminder == 1:
        breakReminderDropdownOption.set(offOnOptions[1])
    
    breakReminderDropdown = OptionMenu(frame6, breakReminderDropdownOption, *offOnOptions)
    breakReminderDropdown.pack(side=RIGHT, padx=10)

    Label(frame7, text="Interval Hours Between Break Reminders").pack(side=LEFT, padx=5)
    
    intervalHourForEntry = StringVar()
    intervalHourForEntry.set(intervalHour)
    
    intervalHourEntry = Entry(frame7, textvariable=intervalHourForEntry)
    intervalHourEntry.pack(side=RIGHT, padx=10)

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
    
    if username == "Admin":
        birthdateButton.config(state=DISABLED)
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)
        
    Label(frame9, text="Password and birthdate are optional.").pack(side=LEFT, padx=10)

    window.mainloop()
    
def AdminManageCompanionDataWindow(selectedResult):    
    def IsPositiveValue(value):
        try:
            number = float(value)
            return number > 0
        except ValueError:
            return False
        
    def IsPositiveAndZeroValue(value):
        try:
            number = float(value)
            return number >= 0
        except ValueError:
            return False
        
    def DisableButton():
        updateButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        updateButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        
    def Update():
        newLevel = levelEntry.get().strip()
        newFriendshipPoint = friendshipPointEntry.get().strip()
        newFriendshipPointNext = friendshipPointNextEntry.get().strip()
        newFriendshipPointMultiplier = friendshipPointMultiplierEntry.get().strip()
        
        if not newLevel or not newFriendshipPoint or not newFriendshipPointNext or not newFriendshipPointMultiplier:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return
        
        if not IsPositiveValue(newLevel) or not IsPositiveAndZeroValue(newFriendshipPoint) or not IsPositiveValue(newFriendshipPointNext) or not IsPositiveValue(newFriendshipPointMultiplier):
            DisableButton()
            messagebox.showerror("Error", "Please choose a positive number.")
            EnableButton()
            return
            
        UpdateRecord('Companion', {'level': newLevel, 'friendshipPoint': newFriendshipPoint, 'friendshipPointNext': newFriendshipPointNext, 'friendshipPointMultiplier': newFriendshipPointMultiplier}, 'companionID = ?', (companionID,))
        
        DisableButton()
        messagebox.showinfo("Success", "Companion updated!")
        EnableButton()

        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
            
    def Back():
        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()
        app.OnClose()
        
    userID = selectedResult[0]
    username = selectedResult[1]
    # password = selectedResult[2]
    # birthdate = selectedResult[3] 
    # lastLogin = selectedResult[4]  
    # isReminder = selectedResult[5] 
    # intervalHour = selectedResult[6]
    
    companionID = selectedResult[7]
    # userID = selectedResult[8]
    level = selectedResult[9]
    friendshipPoint = selectedResult[10] 
    friendshipPointNext = selectedResult[11]  
    friendshipPointMultiplier = selectedResult[12]  

    window = Toplevel()
    
    windowWidth = 500
    windowHeight = 500
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Manage Companion Data")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('AdminManageCompanionDataWindow', window)

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
    
    Label(frame1, text="Companion ID").pack(side=LEFT, padx=10)
    Label(frame1, text=companionID).pack(side=RIGHT, padx=10)
    
    Label(frame2, text="User ID").pack(side=LEFT, padx=10)
    Label(frame2, text=userID).pack(side=RIGHT, padx=10)

    Label(frame3, text="Username").pack(side=LEFT, padx=10)
    Label(frame3, text=username).pack(side=RIGHT, padx=10)
    
    Label(frame4, text="Friendship Level").pack(side=LEFT, padx=10)
    
    levelForEntry = StringVar()
    levelForEntry.set(level)
    
    levelEntry = Entry(frame4, textvariable=levelForEntry)
    levelEntry.pack(side=RIGHT, padx=10)
    
    Label(frame5, text="Current Friendship Point").pack(side=LEFT, padx=10)
    
    friendshipPointForEntry = StringVar()
    friendshipPointForEntry.set(friendshipPoint)
    
    friendshipPointEntry = Entry(frame5, textvariable=friendshipPointForEntry)
    friendshipPointEntry.pack(side=RIGHT, padx=10)
    
    Label(frame6, text="Friendship Point To Next Level").pack(side=LEFT, padx=10)
    
    friendshipPointNextForEntry = StringVar()
    friendshipPointNextForEntry.set(friendshipPointNext)
    
    friendshipPointNextEntry = Entry(frame6, textvariable=friendshipPointNextForEntry)
    friendshipPointNextEntry.pack(side=RIGHT, padx=10)
    
    Label(frame7, text="Friendship Point Multiplier").pack(side=LEFT, padx=10)
    
    friendshipPointMultiplierForEntry = StringVar()
    friendshipPointMultiplierForEntry.set(friendshipPointMultiplier)
    
    friendshipPointMultiplierEntry = Entry(frame7, textvariable=friendshipPointMultiplierForEntry)
    friendshipPointMultiplierEntry.pack(side=RIGHT, padx=10)
    
    frame8Left = Frame(frame8)
    frame8Left.pack(side=LEFT, expand=True)

    frame8Right = Frame(frame8)
    frame8Right.pack(side=LEFT, expand=True)

    updateButton = Button(frame8Left, text="Update", command=Update)
    updateButton.pack(anchor=W, padx=10, pady=10)

    backButton = Button(frame8Right, text="Back", command=Back)
    backButton.pack(anchor=E, padx=10, pady=10)
        
    window.mainloop()
    
def AdminManageCustomTaskDataWindow(selectedResult):    
    def DisableButton():
        dueDateButton.config(state=DISABLED)
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        dueDateButton.config(state=NORMAL)
        updateButton.config(state=NORMAL)
        deleteButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        
    def UpdateButtonText():
        dueDateButton.config(text=selectedDate)
        
    def OpenCalendar():
        def onDateSelect():
            nonlocal selectedDate 
            selectedDate = cal.get_date()
            UpdateButtonText()
            EnableButton()
            top.destroy()
        
        dueDateButton.config(state=DISABLED)
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)

        top = Toplevel(window)
        top.title("Select Due Date")

        cal = Calendar(top, selectmode='day', year=selectedYear, month=selectedMonth, day=selectedDay, date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)

        selectButton = Button(top, text="Select Due Date", command=onDateSelect)
        selectButton.pack(pady=10)
        
    def Update():
        newTitle = titleEntry.get("1.0", "end-1c").strip()
        newNote = noteEntry.get("1.0", "end-1c").strip()
        newDifficulty = difficultyVariable.get()
        newDueDate = datetime.strptime(selectedDate, "%Y-%m-%d").date()
        
        if not newTitle or not newNote:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return
        
        if newDueDate < date.today():
            DisableButton()
            messagebox.showerror("Error", "Please choose a valid date.")
            EnableButton()
            return
            
        UpdateRecord('Custom_Task', {'title': newTitle, 'note': newNote, 'difficulty': newDifficulty, 'dueDate': newDueDate}, 'customTaskID = ?', (customTaskID,))
        
        DisableButton()
        messagebox.showinfo("Success", "Custom task updated!")
        EnableButton()

        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Delete():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to delete this custom task?")
        
        if askUserYesNoBool:
            DeleteRecord('Custom_Task', 'customTaskID = ?', (customTaskID,))
    
            messagebox.showinfo("Success", "Custom task deleted!")
        
            window.destroy()
            from AdminPage import AdminWindow
            AdminWindow()
            
        else:
            EnableButton()
            
    def Back():
        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()
        app.OnClose()
        
    userID = selectedResult[0]
    username = selectedResult[1]
    # password = selectedResult[2]
    # birthdate = selectedResult[3]
    # lastLogin = selectedResult[4]
    # isReminder = selectedResult[5]
    # intervalHour = selectedResult[6]

    customTaskID = selectedResult[7]
    # userID = selectedResult[8]
    title = selectedResult[9]
    note = selectedResult[10]
    difficulty = selectedResult[11]
    dueDate = selectedResult[12]
    createdDate = selectedResult[13]
    
    selectedDate = datetime.strptime(dueDate, "%Y-%m-%d").date()
        
    selectedYear = selectedDate.year
    selectedMonth = selectedDate.month
    selectedDay = selectedDate.day

    window = Toplevel()
    
    windowWidth = 500
    windowHeight = 500
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Manage Custom Task Data")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('AdminManageCustomTaskDataWindow', window)

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
    
    frame9 = Frame(window)
    frame9.pack(padx=5, fill=BOTH, expand=1)
    
    frame10 = Frame(window)
    frame10.pack(padx=5, fill=BOTH, expand=1)
    
    frame11 = Frame(window)
    frame11.pack(padx=5, fill=BOTH, expand=1)
    
    Label(frame1, text="User ID").pack(side=LEFT, padx=10)
    Label(frame1, text=userID).pack(side=RIGHT, padx=10)

    Label(frame2, text="Username").pack(side=LEFT, padx=10)
    Label(frame2, text=username).pack(side=RIGHT, padx=10)
    
    Label(frame3, text="Custom Task ID").pack(side=LEFT, padx=10)
    Label(frame3, text=customTaskID).pack(side=RIGHT, padx=10)
    
    Label(frame4, text="Title").pack(side=LEFT, padx=10)
    titleEntry = Text(frame5, height=3, width=40)
    titleEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    titleEntry.insert("1.0", title)

    Label(frame6, text="Note").pack(side=LEFT, padx=10)
    noteEntry = Text(frame7, height=3, width=40)
    noteEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    noteEntry.insert("1.0", note)
    
    Label(frame8, text="Difficulty").pack(side=LEFT, padx=10)
    
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

    difficultyDropdownOption = OptionMenu(frame8, difficultyVariable, *difficultyOption)
    difficultyDropdownOption.pack(side=RIGHT, padx=10)

    Label(frame9, text="Due Date").pack(side=LEFT, padx=10)
    dueDateButton = Button(frame9, text=selectedDate, command=OpenCalendar)
    dueDateButton.pack(side=RIGHT, padx=10)
    
    Label(frame10, text="Created Date").pack(side=LEFT, padx=10)
    Label(frame10, text=createdDate).pack(side=RIGHT, padx=10)

    frame11Left = Frame(frame11)
    frame11Left.pack(side=LEFT, expand=True)

    frame11Middle = Frame(frame11)
    frame11Middle.pack(side=LEFT, expand=True)

    frame11Right = Frame(frame11)
    frame11Right.pack(side=LEFT, expand=True)

    updateButton = Button(frame11Left, text="Update", command=Update)
    updateButton.pack(anchor=W, padx=10, pady=10)

    deleteButton = Button(frame11Middle, text="Delete", command=Delete)
    deleteButton.pack(anchor=CENTER, padx=10, pady=10)

    backButton = Button(frame11Right, text="Back", command=Back)
    backButton.pack(anchor=E, padx=10, pady=10)

    window.mainloop()
    
def AdminManageDailyTaskDataWindow(selectedResult):    
    def DisableButton():
        updateButton.config(state=DISABLED)
        deleteButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        updateButton.config(state=NORMAL)
        deleteButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        
    def Update():
        newTitle = titleEntry.get("1.0", "end-1c").strip()
        newNote = noteEntry.get("1.0", "end-1c").strip()
        newDifficulty = difficultyVariable.get()
        
        if not newTitle or not newNote:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return
            
        UpdateRecord('Daily_Task', {'title': newTitle, 'note': newNote, 'difficulty': newDifficulty}, 'dailyTaskID = ?', (dailyTaskID,))
        
        DisableButton()
        messagebox.showinfo("Success", "Daily task updated!")
        EnableButton()

        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Delete():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to delete this daily task?")
        
        if askUserYesNoBool:
            DeleteRecord('Daily_Task', 'dailyTaskID = ?', (dailyTaskID,))
    
            messagebox.showinfo("Success", "Daily task deleted!")
        
            window.destroy()
            from AdminPage import AdminWindow
            AdminWindow()
            
        else:
            EnableButton()
            
    def Back():
        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()
        app.OnClose()
        
    userID = selectedResult[0]
    username = selectedResult[1]
    # password = selectedResult[2]
    # birthdate = selectedResult[3]
    # lastLogin = selectedResult[4]
    # isReminder = selectedResult[5]
    # intervalHour = selectedResult[6]

    dailyTaskID = selectedResult[7]
    # userID = selectedResult[8]
    title = selectedResult[9]
    note = selectedResult[10]
    difficulty = selectedResult[11]
    createdDate = selectedResult[12]

    window = Toplevel()
    
    windowWidth = 500
    windowHeight = 500
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Manage Daily Task Data")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('AdminManageDailyTaskDataWindow', window)

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
    
    frame9 = Frame(window)
    frame9.pack(padx=5, fill=BOTH, expand=1)
    
    frame10 = Frame(window)
    frame10.pack(padx=5, fill=BOTH, expand=1)
    
    Label(frame1, text="User ID").pack(side=LEFT, padx=10)
    Label(frame1, text=userID).pack(side=RIGHT, padx=10)

    Label(frame2, text="Username").pack(side=LEFT, padx=10)
    Label(frame2, text=username).pack(side=RIGHT, padx=10)
    
    Label(frame3, text="Daily Task ID").pack(side=LEFT, padx=10)
    Label(frame3, text=dailyTaskID).pack(side=RIGHT, padx=10)
    
    Label(frame4, text="Title").pack(side=LEFT, padx=10)
    titleEntry = Text(frame5, height=3, width=40)
    titleEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    titleEntry.insert("1.0", title)

    Label(frame6, text="Note").pack(side=LEFT, padx=10)
    noteEntry = Text(frame7, height=3, width=40)
    noteEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    noteEntry.insert("1.0", note)
    
    Label(frame8, text="Difficulty").pack(side=LEFT, padx=10)
    
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

    difficultyDropdownOption = OptionMenu(frame8, difficultyVariable, *difficultyOption)
    difficultyDropdownOption.pack(side=RIGHT, padx=10)
    
    Label(frame9, text="Created Date").pack(side=LEFT, padx=10)
    Label(frame9, text=userID).pack(side=RIGHT, padx=10)
    
    frame10Left = Frame(frame10)
    frame10Left.pack(side=LEFT, expand=True)

    frame10Middle = Frame(frame10)
    frame10Middle.pack(side=LEFT, expand=True)

    frame10Right = Frame(frame10)
    frame10Right.pack(side=LEFT, expand=True)

    updateButton = Button(frame10Left, text="Update", command=Update)
    updateButton.pack(anchor=W, padx=10, pady=10)

    deleteButton = Button(frame10Middle, text="Delete", command=Delete)
    deleteButton.pack(anchor=CENTER, padx=10, pady=10)

    backButton = Button(frame10Right, text="Back", command=Back)
    backButton.pack(anchor=E, padx=10, pady=10)

    window.mainloop()

def AdminManageCompletedCustomTaskDataWindow(selectedResult):
    def DisableButton():
        deleteButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        deleteButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        
    def Delete():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to delete this completed custom task?")
        
        if askUserYesNoBool:
            DeleteRecord('Completed_Custom_Task', 'completedCustomTaskID = ?', (completedCustomTaskID,))
    
            messagebox.showinfo("Success", "Completed custom task deleted!")
        
            window.destroy()
            from AdminPage import AdminWindow
            AdminWindow()
            
        else:
            EnableButton()
            
    def Back():
        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()
        app.OnClose()
        
    userID = selectedResult[0]
    username = selectedResult[1]
    # password = selectedResult[2]
    # birthdate = selectedResult[3]
    # lastLogin = selectedResult[4]
    # isReminder = selectedResult[5]
    # intervalHour = selectedResult[6]

    customTaskID = selectedResult[7]
    # userID = selectedResult[8]
    title = selectedResult[9]
    # note = selectedResult[10]
    difficulty = selectedResult[11]
    dueDate = selectedResult[12]
    createdDate = selectedResult[13]

    completedCustomTaskID = selectedResult[14]
    # customTaskID = selectedResult[15]
    completedDate = selectedResult[16]
    isOverdue = selectedResult[17]

    window = Toplevel()
    
    windowWidth = 500
    windowHeight = 500
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Manage Completed Custom Task Data")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('AdminManageCompletedCustomTaskDataWindow', window)

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
    
    frame9 = Frame(window)
    frame9.pack(padx=5, fill=BOTH, expand=1)
    
    frame10 = Frame(window)
    frame10.pack(padx=5, fill=BOTH, expand=1)
    
    frame11 = Frame(window)
    frame11.pack(padx=5, fill=BOTH, expand=1)
    
    frame12 = Frame(window)
    frame12.pack(padx=5, fill=BOTH, expand=1)
    
    Label(frame1, text="User ID").pack(side=LEFT, padx=10)
    Label(frame1, text=userID).pack(side=RIGHT, padx=10)

    Label(frame2, text="Username").pack(side=LEFT, padx=10)
    Label(frame2, text=username).pack(side=RIGHT, padx=10)
    
    Label(frame3, text="Custom Task ID").pack(side=LEFT, padx=10)
    Label(frame3, text=customTaskID).pack(side=RIGHT, padx=10)
    
    Label(frame4, text="Completed Custom Task ID").pack(side=LEFT, padx=10)
    Label(frame4, text=completedCustomTaskID).pack(side=RIGHT, padx=10)
    
    Label(frame5, text="Title").pack(side=LEFT, padx=10)
    titleEntry = Text(frame6, height=3, width=40)
    titleEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    titleEntry.insert("1.0", title)

    Label(frame7, text="Difficulty").pack(side=LEFT, padx=10)
    Label(frame7, text=difficulty).pack(side=RIGHT, padx=10)
    
    Label(frame8, text="Due Date").pack(side=LEFT, padx=10)
    Label(frame8, text=dueDate).pack(side=RIGHT, padx=10)
    
    Label(frame9, text="Created Date").pack(side=LEFT, padx=10)
    Label(frame9, text=createdDate).pack(side=RIGHT, padx=10)
    
    Label(frame10, text="Completed Date").pack(side=LEFT, padx=10)
    Label(frame10, text=completedDate).pack(side=RIGHT, padx=10)
    
    Label(frame11, text="Overdue").pack(side=LEFT, padx=10)
    if isOverdue == 0:
        Label(frame11, text="No").pack(side=RIGHT, padx=10)
    elif isOverdue == 1:
        Label(frame11, text="Yes").pack(side=RIGHT, padx=10)

    frame12Left = Frame(frame12)
    frame12Left.pack(side=LEFT, expand=True)

    frame12Right = Frame(frame12)
    frame12Right.pack(side=LEFT, expand=True)

    deleteButton = Button(frame12Left, text="Delete", command=Delete)
    deleteButton.pack(anchor=W, padx=10, pady=10)

    backButton = Button(frame12Right, text="Back", command=Back)
    backButton.pack(anchor=E, padx=10, pady=10)

    window.mainloop()

def AdminManageCompletedDailyTaskDataWindow(selectedResult):    
    def DisableButton():
        deleteButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        deleteButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        
    def Delete():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to delete this completed daily task?")
        
        if askUserYesNoBool:
            DeleteRecord('Completed_Daily_Task', 'completedDailyTaskID = ?', (completedDailyTaskID,))
    
            messagebox.showinfo("Success", "Completed daily task deleted!")
        
            window.destroy()
            from AdminPage import AdminWindow
            AdminWindow()
            
        else:
            EnableButton()
            
    def Back():
        window.destroy()
        from AdminPage import AdminWindow
        AdminWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()
        app.OnClose()
        
    userID = selectedResult[0]
    username = selectedResult[1]
    # password = selectedResult[2]
    # birthdate = selectedResult[3]
    # lastLogin = selectedResult[4]
    # isReminder = selectedResult[5]
    # intervalHour = selectedResult[6]

    dailyTaskID = selectedResult[7]
    # userID = selectedResult[8]
    title = selectedResult[9]
    # note = selectedResult[10]
    difficulty = selectedResult[11]
    createdDate = selectedResult[12]

    completedDailyTaskID = selectedResult[13]
    # dailyTaskID = selectedResult[14]
    completedDate = selectedResult[15]
    isOverdue = selectedResult[16]

    window = Toplevel()
    
    windowWidth = 500
    windowHeight = 500
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Manage Completed Daily Task Data")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('AdminManageCompletedDailyTaskDataWindow', window)

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
    
    frame9 = Frame(window)
    frame9.pack(padx=5, fill=BOTH, expand=1)
    
    frame10 = Frame(window)
    frame10.pack(padx=5, fill=BOTH, expand=1)
    
    frame11 = Frame(window)
    frame11.pack(padx=5, fill=BOTH, expand=1)
    
    Label(frame1, text="User ID").pack(side=LEFT, padx=10)
    Label(frame1, text=userID).pack(side=RIGHT, padx=10)

    Label(frame2, text="Username").pack(side=LEFT, padx=10)
    Label(frame2, text=username).pack(side=RIGHT, padx=10)
    
    Label(frame3, text="Daily Task ID").pack(side=LEFT, padx=10)
    Label(frame3, text=dailyTaskID).pack(side=RIGHT, padx=10)
    
    Label(frame4, text="Completed Daily Task ID").pack(side=LEFT, padx=10)
    Label(frame4, text=completedDailyTaskID).pack(side=RIGHT, padx=10)
    
    Label(frame5, text="Title").pack(side=LEFT, padx=10)
    titleEntry = Text(frame6, height=3, width=40)
    titleEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    titleEntry.insert("1.0", title)

    Label(frame7, text="Difficulty").pack(side=LEFT, padx=10)
    Label(frame7, text=difficulty).pack(side=RIGHT, padx=10)
    
    Label(frame8, text="Created Date").pack(side=LEFT, padx=10)
    Label(frame8, text=createdDate).pack(side=RIGHT, padx=10)
    
    Label(frame9, text="Completed Date").pack(side=LEFT, padx=10)
    Label(frame9, text=completedDate).pack(side=RIGHT, padx=10)
    
    Label(frame10, text="Overdue").pack(side=LEFT, padx=10)
    if isOverdue == 0:
        Label(frame10, text="No").pack(side=RIGHT, padx=10)
    elif isOverdue == 1:
        Label(frame10, text="Yes").pack(side=RIGHT, padx=10)

    frame11Left = Frame(frame11)
    frame11Left.pack(side=LEFT, expand=True)

    frame11Right = Frame(frame11)
    frame11Right.pack(side=LEFT, expand=True)

    deleteButton = Button(frame11Left, text="Delete", command=Delete)
    deleteButton.pack(anchor=W, padx=10, pady=10)

    backButton = Button(frame11Right, text="Back", command=Back)
    backButton.pack(anchor=E, padx=10, pady=10)

    window.mainloop()