from tkinter import *
from tkinter import messagebox
from datetime import date, datetime
from tkcalendar import *
from Database import *
from MainWindowSingleton import *

def CreateTaskWindow():
    def DisableButton():
        typeDropdown.configure(state="disabled")        
        dueDateButton.config(state=DISABLED)
        confirmButton.config(state=DISABLED)
        backButton.config(state=DISABLED)
        
    def EnableButton():
        typeDropdown.configure(state="active")             
        dueDateButton.config(state=NORMAL)
        confirmButton.config(state=NORMAL)
        backButton.config(state=NORMAL)
        
    def CheckDailyOrCustom(*args):
        if typeVariable.get() == "Custom":
            dueDateButton.config(state=NORMAL)
            dueDateButton.config(text="Due Date")
            
        elif typeVariable.get() == "Daily":
            dueDateButton.config(state=DISABLED)
            dueDateButton.config(text="Daily")

    def UpdateButtonText():
        dueDateButton.config(text=selectedDate)
        
    def OpenCalendar():
        def onDateSelect():
            nonlocal selectedDate 
            selectedDate = cal.get_date()
            UpdateButtonText()
            EnableButton()
            top.destroy()

        typeDropdown.configure(state="disabled")  
        dueDateButton.config(state=DISABLED)
        confirmButton.config(state=DISABLED)
        
        top = Toplevel(window)
        top.title("Select Due Date")
        
        windowWidth = 250
        windowHeight = 275
        x = (top.winfo_screenwidth()//2)-(windowWidth//2)
        y = (top.winfo_screenheight()//2)-(windowHeight//2)
        
        top.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

        cal = Calendar(top, selectmode='day', year=selectedYear, month=selectedMonth, day=selectedDay, date_pattern='yyyy-mm-dd')
        cal.pack(padx=20, pady=20)

        selectButton = Button(top, text="Select Due Date", command=onDateSelect)
        selectButton.pack(pady=10)
        
    def Confirm():
        title = titleEntry.get("1.0", "end-1c").strip()
        note = noteEntry.get("1.0", "end-1c").strip()
        
        if not title or not note:
            DisableButton()
            messagebox.showerror("Error", "All fields are required.")
            EnableButton()
            if typeVariable.get() == "Daily":
                dueDateButton.config(state=DISABLED)
            return
        
        if typeVariable.get() == "Custom":
            if dueDateButton.cget("text") == "Due Date":
                DisableButton()
                messagebox.showerror("Error", "All fields are required.")
                EnableButton()
                return            
            
            if datetime.strptime(selectedDate, '%Y-%m-%d').date() < date.today():
                DisableButton()
                messagebox.showerror("Error", "Please choose a valid date.")
                EnableButton()
                return
            
            CreateRecord('Custom_Task', {'userID': userID, 'title': title, 'note': note, 'difficulty': difficultyVariable.get(), 'dueDate': selectedDate, 'createdDate': date.today()})
            
        elif typeVariable.get() == "Daily":
            CreateRecord('Daily_Task', {'userID': userID, 'title': title, 'note': note, 'difficulty': difficultyVariable.get(), 'createdDate': date.today()})
        
        DisableButton()        
        messagebox.showinfo("Success", "Task created!")
        EnableButton()

        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def Back():
        window.destroy()
        from Task import TaskWindow
        TaskWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()    
        app.OnClose()
    
    selectedDate = date.today()
        
    selectedYear = selectedDate.year
    selectedMonth = selectedDate.month
    selectedDay = selectedDate.day

    window = Toplevel()
    
    windowWidth = 300
    windowHeight = 350
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
        
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("User Create Task")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('CreateTaskWindow', window)
    
    app = Singleton.getMainWindowInstance()
    
    userID = app.user[0]
    # username = app.user[1]
    # password = app.user[2]
    # birthdate = app.user[3]
    # lastLogin = app.user[4]
    # isReminder = app.user[5]
    # intervalHour = app.user[6]

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

    frame7 = Frame(window)
    frame7.pack(fill=BOTH, expand=1)

    frame8 = Frame(window)
    frame8.pack(fill=BOTH, expand=1)

    Label(frame1, text="Title").pack(side=LEFT, padx=10)
    titleEntry = Text(frame2, height=3, width=40)
    titleEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)

    Label(frame3, text="Note").pack(side=LEFT, padx=10)
    noteEntry = Text(frame4, height=3, width=40)
    noteEntry.pack(side=LEFT, padx=10, fill=BOTH, expand=1)
    
    Label(frame5, text="Difficulty").pack(side=LEFT, padx=10)
    
    difficultyOption = ["Easy", "Medium", "Hard", "Extreme"]
    
    difficultyVariable = StringVar()

    difficultyVariable.set(difficultyOption[0])

    difficultyDropdownOption = OptionMenu(frame5, difficultyVariable, *difficultyOption)
    difficultyDropdownOption.pack(side=RIGHT, padx=10)

    Label(frame6, text="Type").pack(side=LEFT, padx=10)
        
    typeOption = ["Custom", "Daily"]

    typeVariable = StringVar()

    typeVariable.set(typeOption[0])

    typeDropdown = OptionMenu(frame6, typeVariable, *typeOption)
    typeDropdown.pack(side=RIGHT, padx=10)

    typeVariable.trace_add("write", CheckDailyOrCustom)

    Label(frame7, text="Due Date").pack(side=LEFT, padx=10)
    dueDateButton = Button(frame7, text="Due Date", command=OpenCalendar)
    dueDateButton.pack(side=RIGHT, padx=10)
    
    frame8Left = Frame(frame8)
    frame8Left.pack(side=LEFT, expand=True)

    frame8Right = Frame(frame8)
    frame8Right.pack(side=LEFT, expand=True)

    confirmButton = Button(frame8Left, text="Confirm", command=Confirm)
    confirmButton.pack(side=LEFT, anchor=E, pady=5) 

    backButton = Button(frame8Right, text="Back", command=Back)
    backButton.pack(side=RIGHT, anchor=W, pady=5) 

    window.mainloop()