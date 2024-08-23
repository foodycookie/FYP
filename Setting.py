from tkinter import *
from tkinter import messagebox
from Database import *
from MainWindowSingleton import *
from WindowManager import *

def SettingWindow():
    def IsPositiveValue(value):
        try:
            number = float(value)
            return number > 0
        except ValueError:
            return False
        
    def DisableButton():
        resetFriendshipButton.config(state=DISABLED)
        logoutButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        confirmButton.config(state=DISABLED)
        
    def EnableButton():
        resetFriendshipButton.config(state=NORMAL)
        logoutButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        confirmButton.config(state=NORMAL)
    
    def ResetFriendship():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to reset?")
        
        if askUserYesNoBool:
            UpdateRecord('Companion',  {'level': 1, 'friendshipPoint': 0, 'friendshipPointNext': 10, 'friendshipPointMultiplier': 1}, 'companionID = ?', (userID,))
            messagebox.showwarning("Progress Reset!", "Your progress have been reset.")
            
        EnableButton()
        
    def Back():
        window.destroy()
        
    def Confirm():
        newUsername = renameUsernameEntry.get().strip()
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
        
        renameUsernameDropdownSelectedValue = breakReminderDropdownOption.get()
        
        if renameUsernameDropdownSelectedValue == "On":
            renameUsernameDropdownSelectedValue = 1
        elif renameUsernameDropdownSelectedValue == "Off":
            renameUsernameDropdownSelectedValue = 0
        
        UpdateRecord('User', {'username': newUsername, 'isReminder': renameUsernameDropdownSelectedValue, 'intervalHour': newIntervalHour}, 'userID = ?', (userID,))
        
        app = Singleton.getMainWindowInstance()
       
        user = FetchRecord('User', columns=['*'], where_clause='userID = ?', params=(userID,))

        app.user = user[0]
        
        DisableButton()
        messagebox.showwarning("Changes Made", "Your changes have been saved!")
        EnableButton()
    
        window.destroy()
        
    def Logout():
        DisableButton()
        askUserYesNoBool = messagebox.askyesno("Confirmation", "Are you sure you want to logout?")
        
        if askUserYesNoBool:
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            cursor.execute('''
            UPDATE User
            SET lastLogin = NULL;
            ''')
            
            conn.commit()
            conn.close()
            
            app.user = None

            from LoginAndEverything import LoginWindow
            window.destroy()
            Singleton.getMainWindowInstance().withdraw()
            LoginWindow()
            
        else:
            EnableButton()
            
    def Quit():
        app = Singleton.getMainWindowInstance()    
        app.OnClose()
        
    window = Toplevel()
    
    windowWidth = 370
    windowHeight = 500
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Setting")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('SettingWindow', window)
    
    app = Singleton.getMainWindowInstance()
    
    userID = app.user[0]
    username = app.user[1]
    # password = app.user[2]
    # birthdate = app.user[3]
    # lastLogin = app.user[4]
    isReminder = app.user[5]
    intervalHour = app.user[6]
    
    frame1 = Frame(window)
    frame1.pack(fill=BOTH, expand=1)
    
    frame2 = Frame(window)
    frame2.pack(fill=BOTH, expand=1)
    
    frame3 = Frame(window)
    frame3.pack(fill=BOTH, expand=1)
    
    frame4 = Frame(window)
    frame4.pack(fill=BOTH, expand=1)
    
    frame5 = Frame(window)
    frame5.pack(fill=BOTH, expand=1)
    
    frame6 = Frame(window)
    frame6.pack(fill=BOTH, expand=1)
    
    offOnOptions = ["Off", "On"]

    Label(frame1, text="Break reminder").pack(side=LEFT, padx=5)
    
    breakReminderDropdownOption = StringVar()
    
    if isReminder == 0:
        breakReminderDropdownOption.set(offOnOptions[0])
    elif isReminder == 1:
        breakReminderDropdownOption.set(offOnOptions[1])
    
    breakReminderDropdown = OptionMenu(frame1, breakReminderDropdownOption, *offOnOptions)
    breakReminderDropdown.pack(side=RIGHT, padx=10)

    Label(frame2, text="Interval hours between break reminders").pack(side=LEFT, padx=5)
    
    intervalHourForEntry = StringVar()
    intervalHourForEntry.set(intervalHour)
    
    intervalHourEntry = Entry(frame2, textvariable=intervalHourForEntry)
    intervalHourEntry.pack(side=RIGHT, padx=10)
    
    Label(frame3, text="Rename username").pack(side=LEFT, padx=5)
    
    usernameForEntry = StringVar()
    usernameForEntry.set(username)
    
    renameUsernameEntry = Entry(frame3, textvariable=usernameForEntry)
    renameUsernameEntry.pack(side=RIGHT, padx=10)

    Label(frame4, text="Reset friendship").pack(side=LEFT, padx=5)
    
    resetFriendshipButton = Button(frame4, text="Reset", command=ResetFriendship)
    resetFriendshipButton.pack(side=RIGHT, padx=10)
    
    Label(frame5, text="Logout").pack(side=LEFT, padx=5)
    
    logoutButton = Button(frame5, text="Logout", command=Logout)
    logoutButton.pack(side=RIGHT, padx=10)
    
    backButton = Button(frame6, text="Back", command=Back)
    backButton.pack(side=LEFT, padx=60)
    
    confirmButton = Button(frame6, text="Confirm", command=Confirm)
    confirmButton.pack(side=RIGHT, padx=60)
    
    window.mainloop()