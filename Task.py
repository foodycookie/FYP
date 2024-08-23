from tkinter import *
from datetime import date
import sqlite3
from Database import *
from MainWindowSingleton import *
from WindowManager import *

dataPerPage = 15
currentPageCustom = 1
currentPageDaily = 1
totalPagesCustom = 1
totalPagesDaily = 1

def TaskWindow():
    def UpdateCustomTaskList():
        global currentPageCustom, totalPagesCustom, incompleteCustomTasks
        
        conn = sqlite3.connect('Task.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT customTaskID, title, note, difficulty, dueDate, createdDate
        FROM Custom_Task
        WHERE userID = ? AND customTaskID NOT IN (
            SELECT customTaskID FROM Completed_Custom_Task
        )
        ORDER BY dueDate ASC;
        ''', (userID,))
        incompleteCustomTasks = cursor.fetchall()
        
        conn.close()
        
        customTaskScrollBar.config(command=customTaskListbox.yview)

        totalPagesCustom = (len(incompleteCustomTasks) + dataPerPage - 1) // dataPerPage

        start = (currentPageCustom - 1) * dataPerPage
        end = start + dataPerPage
        
        customTaskListbox.delete(0, END)
        
        for incompleteCustomTask in incompleteCustomTasks[start:end]:
            customTaskListbox.insert(END, f"[Custom] {incompleteCustomTask[1]}   |   {incompleteCustomTask[3]}   |   Due: {incompleteCustomTask[4]}")
            
        UpdatePageButtonState()

    def UpdateDailyTaskList():
        global currentPageDaily, totalPagesDaily, incompleteDailyTasks

        currentDate = date.today()
        
        conn = sqlite3.connect('Task.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Daily_Task.dailyTaskID, Daily_Task.title, Daily_Task.note, Daily_Task.difficulty, Daily_Task.createdDate
            FROM Daily_Task
            LEFT JOIN Completed_Daily_Task ON Daily_Task.dailyTaskID = Completed_Daily_Task.dailyTaskID
                AND Completed_Daily_Task.completedDate = ?
            WHERE userID = ? AND Completed_Daily_Task.completedDailyTaskID IS NULL;
        ''', (currentDate, userID,))
        incompleteDailyTasks = cursor.fetchall()
        
        conn.close()
        
        dailyTaskScrollBar.config(command=dailyTaskListbox.yview)
        
        totalPagesDaily = (len(incompleteDailyTasks) + dataPerPage - 1) // dataPerPage

        start = (currentPageDaily - 1) * dataPerPage
        end = start + dataPerPage
        
        dailyTaskListbox.delete(0, END)

        for incompleteDailyTask in incompleteDailyTasks[start:end]:
            dailyTaskListbox.insert(END, f"[Daily] {incompleteDailyTask[1]}   |   {incompleteDailyTask[3]}")
            
        UpdatePageButtonState()
        
    def ShowCustomTask():
        customTaskSearchBoxFrame.place(x=191.0, y=70.0, width=720.0, height=50.0)
        customTaskFrame.place(x=191.0, y=120.0, width=720.0, height=245.0)
        customTaskPageButtonFrame.place(x=191.0, y=365.0, width=720.0, height=50.0)
    
        dailyTaskSearchBoxFrame.place_forget()
        dailyTaskFrame.place_forget()
        dailyTaskPageButtonFrame.place_forget()
        
        UpdateCustomTaskList()
        
    def ShowDailyTask():
        dailyTaskSearchBoxFrame.place(x=191.0, y=70.0, width=720.0, height=50.0)
        dailyTaskFrame.place(x=191.0, y=120.0, width=720.0, height=245.0)
        dailyTaskPageButtonFrame.place(x=191.0, y=365.0, width=720.0, height=50.0)
        
        customTaskSearchBoxFrame.place_forget()
        customTaskFrame.place_forget()
        customTaskPageButtonFrame.place_forget()
    
        UpdateDailyTaskList()
        
    def UpdatePageButtonState():
        global currentPageCustom, totalPagesCustom, currentPageDaily, totalPagesDaily
        
        if currentPageCustom > 1:
            customTaskPreviousPageButton.config(state=NORMAL)
        else:
            customTaskPreviousPageButton.config(state=DISABLED)
        
        if currentPageCustom < totalPagesCustom:
            customTaskNextPageButton.config(state=NORMAL)
        else:
            customTaskNextPageButton.config(state=DISABLED)

        if currentPageDaily > 1:
            dailyTaskPreviousPageButton.config(state=NORMAL)
        else:
            dailyTaskPreviousPageButton.config(state=DISABLED)
        
        if currentPageDaily < totalPagesDaily:
            dailyTaskNextPageButton.config(state=NORMAL)
        else:
            dailyTaskNextPageButton.config(state=DISABLED)

    def GoToNextPageCustom():
        global currentPageCustom, totalPagesCustom
        
        if currentPageCustom < totalPagesCustom:
            currentPageCustom += 1
            UpdateCustomTaskList()

    def GoToPreviousPageCustom():
        global currentPageCustom
        
        if currentPageCustom > 1:
            currentPageCustom -= 1
            UpdateCustomTaskList()

    def GoToNextPageDaily():
        global currentPageDaily, totalPagesDaily
        
        if currentPageDaily < totalPagesDaily:
            currentPageDaily += 1
            UpdateDailyTaskList()

    def GoToPreviousPageDaily():
        global currentPageDaily
        
        if currentPageDaily > 1:
            currentPageDaily -= 1
            UpdateDailyTaskList()
        
    def SearchCustomTask():  
        global currentPageCustom, totalPagesCustom, incompleteCustomTasks
        
        currentPageCustom = 1
        
        searchTerm = customTaskSearchBoxEntry.get().strip()

        conn = sqlite3.connect('Task.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT customTaskID, title, note, difficulty, dueDate, createdDate
            FROM Custom_Task
            WHERE customTaskID NOT IN (
                SELECT customTaskID FROM Completed_Custom_Task
            )
            AND title LIKE ? AND userID = ?
            ORDER BY dueDate ASC;
        ''', (f"%{searchTerm}%", userID,))
        incompleteCustomTasks = cursor.fetchall()
        
        conn.close()

        totalPagesCustom = (len(incompleteCustomTasks) + dataPerPage - 1) // dataPerPage

        start = (currentPageCustom - 1) * dataPerPage
        end = start + dataPerPage
        
        customTaskListbox.delete(0, END)
        
        for incompleteCustomTask in incompleteCustomTasks[start:end]:
            customTaskListbox.insert(END, f"[Custom] {incompleteCustomTask[1]}   |   {incompleteCustomTask[3]}   |   {incompleteCustomTask[4]}")

        UpdatePageButtonState()
        
    def SearchDailyTask():
        global currentPageDaily, totalPagesDaily, incompleteDailyTasks
        
        currentPageDaily = 1
        
        currentDate = date.today()
        
        searchTerm = dailyTaskSearchBoxEntry.get().strip()

        conn = sqlite3.connect("Task.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Daily_Task.dailyTaskID, Daily_Task.title, Daily_Task.note, Daily_Task.difficulty, Daily_Task.createdDate
            FROM Daily_Task
            LEFT JOIN Completed_Daily_Task ON Daily_Task.dailyTaskID = Completed_Daily_Task.dailyTaskID
            AND Completed_Daily_Task.completedDate = ?
            WHERE Completed_Daily_Task.completedDailyTaskID IS NULL
            AND Daily_Task.title LIKE ? AND userID = ?;
        ''', (currentDate, f"%{searchTerm}%", userID))
        incompleteDailyTasks = cursor.fetchall()
        
        conn.close()

        totalPagesDaily = (len(incompleteDailyTasks) + dataPerPage - 1) // dataPerPage

        start = (currentPageDaily - 1) * dataPerPage
        end = start + dataPerPage
        
        dailyTaskListbox.delete(0, END)
        
        for incompleteDailyTask in incompleteDailyTasks[start:end]:
            dailyTaskListbox.insert(END, f"[Daily] {incompleteDailyTask[1]}   |   {incompleteDailyTask[3]}")

        UpdatePageButtonState()
            
    def ResetCustomTaskSearch():
        global currentPageCustom
        
        currentPageCustom = 1
        
        customTaskSearchBoxEntry.delete(0, END)
        
        UpdateCustomTaskList()
        
    def ResetDailyTaskSearch():
        global currentPageDaily
        
        currentPageDaily = 1
        
        dailyTaskSearchBoxEntry.delete(0, END)
        
        UpdateDailyTaskList()
        
    def ShowCustomTaskDetails(event):
        global incompleteCustomTasks, currentPageCustom
        
        index = (customTaskListbox.curselection()[0]) + ((currentPageCustom - 1) * dataPerPage)
        selectedCustomTask = incompleteCustomTasks[index]
        
        window.destroy()
        from UserManageTask import UserEditCustomTaskWindow
        UserEditCustomTaskWindow(selectedCustomTask)
        
    def ShowDailyTaskDetails(event):
        global incompleteDailyTasks, currentPageDaily
        
        index = dailyTaskListbox.curselection()[0] + ((currentPageDaily - 1) * dataPerPage)
        selectedDailyTask = incompleteDailyTasks[index]
        
        window.destroy()
        from UserManageTask import UserEditDailyTaskWindow
        UserEditDailyTaskWindow(selectedDailyTask)
        
    def OpenCreateTaskWindow():
        window.destroy()
        from CreateTask import CreateTaskWindow
        CreateTaskWindow()
        
    def TaskHistoryWindow():
        window.destroy()
        from TaskHistory import TaskHistoryWindow
        TaskHistoryWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()    
        app.OnClose()
    
    # def AddFriendship():
    #     global friendshipPoint
    #     friendshipPoint += (1000 * friendshipPointMultiplier)
                
    #     UpdateRecord('Companion',  {'friendshipPoint': friendshipPoint}, 'companionID = ?', (companionID,))
        
        
    # def MinusFriendship():
    #     global friendshipPoint
    #     friendshipPoint -= (1000 * friendshipPointMultiplier)
        
    #     UpdateRecord('Companion',  {'friendshipPoint': friendshipPoint}, 'companionID = ?', (companionID,))

    # def Refresh():
    #     window.destroy()
    #     TaskWindow()
        
    # global friendshipPoint, friendshipPointMultiplier
        
    window = Toplevel()
    
    windowWidth = 945
    windowHeight = 440
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Task")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('TaskWindow', window)

    canvas = Canvas(window, bg="#FFFFFF", height=396, width=945)
    canvas.place(x=0, y=0)
    
    app = Singleton.getMainWindowInstance()
    
    userID = app.user[0]
    # username = app.user[1]
    # password = app.user[2]
    # birthdate = app.user[3]
    # lastLogin = app.user[4]
    # isReminder = app.user[5]
    # intervalHour = app.user[6]
    
    companionStat = FetchRecord('Companion', columns=['companionID', 'level', 'friendshipPoint', 'friendshipPointNext', 'friendshipPointMultiplier'], where_clause='userID = ?', params=(userID,))[0] 

    # companionID = companionStat[0]
    level = companionStat[1]
    friendshipPoint = companionStat[2]
    friendshipPointNext = companionStat[3]
    friendshipPointMultiplier = companionStat[4]
    
    companionImage = PhotoImage(file="assets/CatSpriteSheetIcon.png")
    canvas.create_image(94.0, 94.0, image=companionImage)
    
    friendshipBarImage = PhotoImage(file="assets/FriendshipBar.png")
    canvas.create_image(94.0, 261.0, image=friendshipBarImage)
    
    heartShapeImage = PhotoImage(file="assets/HeartShape.png")
    canvas.create_image(93.0, 203.0, image=heartShapeImage)
    
    canvas.create_text(88.0, 190.0, anchor="nw", text=level, fill="#000000")

    canvas.create_text(65.0, 253.0, anchor="nw", text=f"{friendshipPoint} / {friendshipPointNext} (x{friendshipPointMultiplier})", fill="#000000")
    
    createTaskButton = Button(window, text="Create Task", command=OpenCreateTaskWindow)
    createTaskButton.place(x=31.0, y=300.0, width=126.0, height=30.0)
    
    showCustomTaskButton = Button(window, text="Show Custom Tasks", command=ShowCustomTask)
    showCustomTaskButton.place(x=341.0, y=40.0, width=150.0, height=30.0)
           
    showDailyTaskButton = Button(window, text="Show Daily Tasks", command=ShowDailyTask)
    showDailyTaskButton.place(x=191.0, y=40.0, width=150.0, height=30.0)

    customTaskSearchBoxFrame = Frame(window)
    customTaskSearchBoxFrame.place(x=191.0,  y=70.0, width=720.0, height=50.0)
    
    customTaskFrame = Frame(window)
    customTaskFrame.place(x=191.0, y=120.0, width=720.0, height=245.0)
    
    customTaskPageButtonFrame = Frame(window)
    customTaskPageButtonFrame.place(x=191.0, y=365.0, width=720.0, height=50.0)
    
    customTaskSearchBoxEntry = Entry(customTaskSearchBoxFrame, bg="light grey", width=100)
    customTaskSearchBoxEntry.pack(pady=5, side=LEFT, padx=5)
    
    customTaskSearchButton = Button(customTaskSearchBoxFrame, text="Search", command=SearchCustomTask)
    customTaskSearchButton.pack(pady=5, side=LEFT, padx=5)
    
    customTaskResetButton = Button(customTaskSearchBoxFrame, text="Reset", command=ResetCustomTaskSearch)
    customTaskResetButton.pack(pady=5, side=LEFT, padx=5)

    customTaskScrollBar = Scrollbar(customTaskFrame, orient='vertical')
    customTaskScrollBar.pack(side=RIGHT, fill=Y)

    customTaskListbox = Listbox(customTaskFrame, yscrollcommand=customTaskScrollBar.set, bg='light grey')
    customTaskListbox.pack(side=LEFT, fill=BOTH, expand=True)
    
    dailyTaskSearchBoxFrame = Frame(window)
    dailyTaskSearchBoxFrame.place(x=191.0, y=70.0, width=720.0, height=50.0)
    
    dailyTaskFrame = Frame(window)
    dailyTaskFrame.place(x=191.0, y=120.0, width=720.0, height=245.0)
    
    dailyTaskPageButtonFrame = Frame(window)
    dailyTaskPageButtonFrame.place(x=191.0, y=365.0, width=720.0, height=50.0)
    
    dailyTaskSearchBoxEntry = Entry(dailyTaskSearchBoxFrame, bg="light grey", width=100)
    dailyTaskSearchBoxEntry.pack(pady=5, side=LEFT, padx=5)
    
    dailyTaskSearchButton = Button(dailyTaskSearchBoxFrame, text="Search", command=SearchDailyTask)
    dailyTaskSearchButton.pack(pady=5, side=LEFT, padx=5)
    
    dailyTaskResetButton = Button(dailyTaskSearchBoxFrame, text="Reset", command=ResetDailyTaskSearch)
    dailyTaskResetButton.pack(pady=5, side=LEFT, padx=5)
    
    dailyTaskScrollBar = Scrollbar(dailyTaskFrame, orient='vertical')
    dailyTaskScrollBar.pack(side=RIGHT, fill=Y)

    dailyTaskListbox = Listbox(dailyTaskFrame, yscrollcommand=dailyTaskScrollBar.set, bg='light grey')
    dailyTaskListbox.pack(side=LEFT, fill=BOTH, expand=True)
        
    customTaskListbox.bind('<Double-1>', ShowCustomTaskDetails)
    dailyTaskListbox.bind('<Double-1>', ShowDailyTaskDetails)
    
    customTaskPreviousPageButton = Button(customTaskPageButtonFrame, text="Previous", command=GoToPreviousPageCustom)
    customTaskPreviousPageButton.pack(side=LEFT, pady=5, padx=40)
    
    customTaskNextPageButton = Button(customTaskPageButtonFrame, text="Next", command=GoToNextPageCustom)
    customTaskNextPageButton.pack(side=RIGHT, pady=5, padx=40)

    dailyTaskPreviousPageButton = Button(dailyTaskPageButtonFrame, text="Previous", command=GoToPreviousPageDaily)
    dailyTaskPreviousPageButton.pack(side=LEFT, pady=5, padx=40)
    
    dailyTaskNextPageButton = Button(dailyTaskPageButtonFrame, text="Next", command=GoToNextPageDaily)
    dailyTaskNextPageButton.pack(side=RIGHT, pady=5, padx=40)
    
    taskHistoryButton = Button(window, text="Task History", command=TaskHistoryWindow)
    taskHistoryButton.place(x=31.0, y=350.0, width=126.0, height=30.0)
    
    # addFriendshipButton = Button(window, text="Add Friendship", command=AddFriendship)
    # addFriendshipButton.place(x=31.0, y=400.0, width=126.0, height=30.0)
    
    # minusFriendshipButton = Button(window, text="Minus Friendship", command=MinusFriendship)
    # minusFriendshipButton.place(x=31.0, y=450.0, width=126.0, height=30.0)
    
    # refreshButton = Button(window, text="Refresh", command=Refresh)
    # refreshButton.place(x=31.0, y=500.0, width=126.0, height=30.0)
    
    ShowCustomTask()
    
    window.mainloop()    