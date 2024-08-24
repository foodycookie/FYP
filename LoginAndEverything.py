from tkinter import *
from tkinter import messagebox
from datetime import date
from library.tkcalendar import *
from Database import *
from MainWindowSingleton import *
from WindowManager import *

def LoginWindow():    
    def DisableButton():
        loginButton.config(state=DISABLED)
        registerPageButton.config(state=DISABLED)
        forgetPasswordButton.config(state=DISABLED)
        
    def EnableButton():
        loginButton.config(state=NORMAL)
        registerPageButton.config(state=NORMAL)
        forgetPasswordButton.config(state=NORMAL)
        
    def Login():
        username = usernameEntry.get().strip()
        password = passwordEntry.get().strip()
        hashedPassword = hashingString(password)
        
        if not username or not password:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return
        
        result = FetchRecord('User', columns=['password'], where_clause='username = ?', params=(username,))

        if result and result[0][0] == hashedPassword:
            currentUserID = (FetchRecord('User', columns=['userID'], where_clause='username = ?', params=(username,)))[0][0]
            
            UpdateRecord('User',  {'lastLogin': date.today()}, 'userID = ?', (currentUserID,))
            
            DisableButton()
            messagebox.showinfo("Success", "Login successful!")
            EnableButton()
            
            window.destroy()
            
            from Main import onLoginSuccess
            onLoginSuccess(currentUserID)
            
        else:
            DisableButton()
            messagebox.showerror("Error", "Invalid username or password")
            EnableButton()
    
    def JumpToRegister():
        window.destroy()
        RegisterWindow()
    
    def JumpToForgetPassword():
        window.destroy()
        ForgetPasswordWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()    
        app.OnClose()
        
    window = Toplevel()
    
    windowWidth = 300
    windowHeight = 150
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Login")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('LoginWindow', window)

    frame1 = Frame(window)
    frame1.pack(pady=10)

    frame2 = Frame(window)
    frame2.pack(pady=5)

    frame3 = Frame(window)
    frame3.pack(pady=5)

    frame4 = Frame(window)
    frame4.pack(pady=10)

    Label(frame1, text="Login").pack()

    Label(frame2, text="Username").pack(side=LEFT)
    usernameEntry = Entry(frame2)
    usernameEntry.pack(side=LEFT)

    Label(frame3, text="Password").pack(side=LEFT)
    passwordEntry = Entry(frame3, show='*')
    passwordEntry.pack(side=LEFT)
    
    loginButton = Button(frame4, text="Login", command=Login)
    loginButton.pack(side=LEFT, padx=5)
    
    registerPageButton = Button(frame4, text="Register Page", command=JumpToRegister)
    registerPageButton.pack(side=LEFT, padx=5)
    
    forgetPasswordButton = Button(frame4, text="Forget Password", command=JumpToForgetPassword)
    forgetPasswordButton.pack(side=LEFT, padx=5)
    
    quitButton = Button(frame4, text="Quit", command=Quit)
    quitButton.pack(side=LEFT, padx=5)

    window.mainloop()
    
def RegisterWindow():
    def DisableButton():
        birthdateButton.config(state=DISABLED)
        registerButton.config(state=DISABLED)
        loginPageButton.config(state=DISABLED)
        
    def EnableButton():
        birthdateButton.config(state=NORMAL)
        registerButton.config(state=NORMAL)
        loginPageButton.config(state=NORMAL)
        
    def Register():
        username = usernameEntry.get().strip()
        password = passwordEntry.get().strip()
        confirmPassword = confirmPasswordEntry.get().strip()
        birthdate = selectedDate

        if not username or not password or not confirmPassword or birthdateButton.cget("text") == "Birthdate":
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return
        
        if password != confirmPassword:
            DisableButton()
            messagebox.showerror("Error", "Passwords do not match.")
            EnableButton()
            return
        
        result = FetchRecord('User', columns=['userID'], where_clause='username = ?', params=(username,))
        
        if result:
            DisableButton()
            messagebox.showerror("Error", "Username already exists.")
            EnableButton()
            return
        
        hashedPassword = hashingString(password)
        hashedBirthdate = hashingString(birthdate)
        
        CreateRecord('User', {'username': username, 'password': hashedPassword, 'birthdate': hashedBirthdate, 'lastLogin': None, 'isReminder': 1, 'intervalHour': 3})
        
        userID = (FetchRecord('User', columns=['userID'], where_clause="username = ?", params=(username,)))[0][0]
        
        CreateRecord('Companion', {'userID': userID, 'level': 1, 'friendshipPoint': 0, 'friendshipPointNext': 10, 'friendshipPointMultiplier': 1})
        
        DisableButton()
        messagebox.showinfo("Success", "Registration successful.")
        EnableButton()
        
        window.destroy()
        LoginWindow()

    def Back():
        window.destroy()
        LoginWindow()
        
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
        registerButton.config(state=DISABLED)

        top = Toplevel(window)
        top.title("Select Birthdate")
        
        windowWidth = 250
        windowHeight = 275
        x = (top.winfo_screenwidth()//2)-(windowWidth//2)
        y = (top.winfo_screenheight()//2)-(windowHeight//2)
        
        top.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

        cal = Calendar(top, selectmode='day', year=selectedYear, month=selectedMonth, day=selectedDay, date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)

        selectButton = Button(top, text="Select Birthdate", command=onDateSelect)
        selectButton.pack(pady=10)
        
    def Quit():
        RemoveMainWindow("MainWindow")
        
    selectedDate = date.today()
    
    selectedYear = selectedDate.year
    selectedMonth = selectedDate.month
    selectedDay = selectedDate.day
        
    window = Toplevel()
    
    windowWidth = 250
    windowHeight = 215
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Register")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('RegisterWindow', window)
    
    frame1 = Frame(window)
    frame1.pack(pady=10)

    frame2 = Frame(window)
    frame2.pack(pady=5)

    frame3 = Frame(window)
    frame3.pack(pady=5)

    frame4 = Frame(window)
    frame4.pack(pady=5)

    frame5 = Frame(window)
    frame5.pack(pady=5)
    
    frame6 = Frame(window)
    frame6.pack(pady=10)

    Label(frame1, text="Register").pack()

    Label(frame2, text="Username").pack(side=LEFT)
    usernameEntry = Entry(frame2)
    usernameEntry.pack(side=LEFT)

    Label(frame3, text="Password").pack(side=LEFT)
    passwordEntry = Entry(frame3, show='*')
    passwordEntry.pack(side=LEFT)
    
    Label(frame4, text="Confirm Password").pack(side=LEFT)
    confirmPasswordEntry = Entry(frame4, show='*')
    confirmPasswordEntry.pack(side=LEFT)
    
    birthdateButton = Button(frame5, text="Birthdate", command=OpenCalendar)
    birthdateButton.pack(side=LEFT, padx=5)

    registerButton = Button(frame6, text="Register", command=Register)
    registerButton.pack(side=LEFT, padx=5)

    loginPageButton = Button(frame6, text="Back", command=Back)
    loginPageButton.pack(side=LEFT, padx=5)
    
    window.mainloop()
    
def ForgetPasswordWindow():
    global birthdate
    
    def DisableButton():
        birthdateButton.config(state=DISABLED)
        confirmButton.config(state=DISABLED)
        loginPageButton.config(state=DISABLED)
        
    def EnableButton():
        birthdateButton.config(state=NORMAL)
        confirmButton.config(state=NORMAL)
        loginPageButton.config(state=NORMAL)
        
    def ResetPassword():
        username = usernameEntry.get().strip()
        birthdate = selectedDate
        newPassword = newPasswordEntry.get().strip()
        confirmNewPassword = confirmNewPasswordEntry.get().strip()

        if not username or birthdateButton.cget("text") == "Your Birthdate" or not newPassword or not confirmNewPassword:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            return

        if newPassword != confirmNewPassword:
            DisableButton()
            messagebox.showerror("Error", "Passwords do not match.")
            EnableButton()
            return

        hashedBirthdate = hashingString(birthdate)
        hashedPassword = hashingString(newPassword)
        
        result = FetchRecord('User', columns=['userID'], where_clause="username = ? AND birthdate = ?", params=(username, hashedBirthdate,))

        if result is None:
            DisableButton()
            messagebox.showerror("Error", "Invalid username or birthdate")
            EnableButton()
            return
        
        UpdateRecord('User', {'password': hashedPassword}, 'username = ? AND birthdate = ?', (username, hashedBirthdate,))

        DisableButton()
        messagebox.showinfo("Success", "Password updated.")
        EnableButton()
        
        window.destroy()
        LoginWindow()

    def Back():
        window.destroy()
        LoginWindow()
        
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
        confirmButton.config(state=DISABLED)

        top = Toplevel(window)
        top.title("Select Birthdate")
        
        windowWidth = 250
        windowHeight = 275
        x = (top.winfo_screenwidth()//2)-(windowWidth//2)
        y = (top.winfo_screenheight()//2)-(windowHeight//2)
        
        top.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

        cal = Calendar(top, selectmode='day', year=selectedYear, month=selectedMonth, day=selectedDay, date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)

        selectButton = Button(top, text="Select Birthdate", command=onDateSelect)
        selectButton.pack(pady=10)
        
    def Quit():
        RemoveMainWindow("MainWindow")
        
    selectedDate = date.today()
    
    selectedYear = selectedDate.year
    selectedMonth = selectedDate.month
    selectedDay = selectedDate.day
        
    window = Toplevel()
    
    windowWidth = 270
    windowHeight = 215
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Forget Password")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('ForgetPasswordWindow', window)
        
    frame1 = Frame(window)
    frame1.pack(pady=10)

    frame2 = Frame(window)
    frame2.pack(pady=5)

    frame3 = Frame(window)
    frame3.pack(pady=5)

    frame4 = Frame(window)
    frame4.pack(pady=5)

    frame5 = Frame(window)
    frame5.pack(pady=5)
    
    frame6 = Frame(window)
    frame6.pack(pady=10)

    Label(frame1, text="Reset Password").pack()

    Label(frame2, text="Username").pack(side=LEFT)
    usernameEntry = Entry(frame2)
    usernameEntry.pack(side=LEFT)
    
    birthdateButton = Button(frame3, text="Your Birthdate", command=OpenCalendar)
    birthdateButton.pack(side=LEFT, padx=5)

    Label(frame4, text="New Password").pack(side=LEFT)
    newPasswordEntry = Entry(frame4, show='*')
    newPasswordEntry.pack(side=LEFT)
    
    Label(frame5, text="Confirm New Password").pack(side=LEFT)
    confirmNewPasswordEntry = Entry(frame5, show='*')
    confirmNewPasswordEntry.pack(side=LEFT)

    confirmButton = Button(frame6, text="Confirm", command=ResetPassword)
    confirmButton.pack(side=LEFT, padx=5)

    loginPageButton = Button(frame6, text="Back", command=Back)
    loginPageButton.pack(side=LEFT, padx=5)
    
    window.mainloop()