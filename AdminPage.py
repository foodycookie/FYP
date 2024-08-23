from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from Database import *
from MainWindowSingleton import *
from WindowManager import *

currentData = "User"
results = None
dummyDataType = "User"
dataPerPage = 11
currentPage = 1
totalPage = 1

def AdminWindow():
    def UpdatePageButtonState():
        global currentPage, totalPage
        
        if currentPage > 1:
            previousPageButton.config(state=NORMAL)
        else:
            previousPageButton.config(state=DISABLED)
        
        if currentPage < totalPage:
            nextPageButton.config(state=NORMAL)
        else:
            nextPageButton.config(state=DISABLED)
        
    def UpdateDataList(dataType):
        global currentPage, totalPage, results, currentData, defaultText, results, dummyDataType
        
        if dummyDataType != dataType:
            currentPage = 1
            dummyDataType = dataType

        searchBoxEntry.delete(0, END)
        
        if dataType == "User":
            defaultText = "Search User ID or username"
            currentData = "User"
            results = FetchRecord('User', columns=['*'])
            
        elif dataType == "Companion":
            defaultText = "Search User ID or username"
            currentData = "Companion"
            
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Companion.level
            
            cursor.execute('''
            SELECT User.*, Companion.*
            FROM Companion
            JOIN User ON Companion.userID = User.userID;
            ''')
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "CustomTask":
            defaultText = "Search User ID or title"
            currentData = "CustomTask"
            
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Custom_Task.title, Custom_Task.createdDate
            
            cursor.execute('''
            SELECT User.*, Custom_Task.*
            FROM Custom_Task
            JOIN User ON Custom_Task.userID = User.userID;
            ''')
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "DailyTask":
            defaultText = "Search User ID or title"
            currentData = "DailyTask"
            
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Daily_Task.title, Daily_Task.createdDate
            
            cursor.execute('''
            SELECT User.*, Daily_Task.*
            FROM Daily_Task
            JOIN User ON Daily_Task.userID = User.userID;
            ''')
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "CompletedCustomTask":
            defaultText = "Search User ID or title"
            currentData = "CompletedCustomTask"
            
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Custom_Task.title, Completed_Custom_Task.completedDate
            
            cursor.execute('''
            SELECT User.*, Custom_Task.*, Completed_Custom_Task.*
            FROM Completed_Custom_Task
            JOIN Custom_Task ON Completed_Custom_Task.customTaskID = Custom_Task.customTaskID
            JOIN User ON Custom_Task.userID = User.userID;
            ''')
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "CompletedDailyTask":
            defaultText = "Search User ID or title"
            currentData = "CompletedDailyTask"
            
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Daily_Task.title, Completed_Daily_Task.completedDate
            
            cursor.execute('''
            SELECT User.*, Daily_Task.*, Completed_Daily_Task.*
            FROM Completed_Daily_Task
            JOIN Daily_Task ON Completed_Daily_Task.dailyTaskID = Daily_Task.dailyTaskID
            JOIN User ON Daily_Task.userID = User.userID;
            ''')
            results = cursor.fetchall()
            
            conn.close()
            
        searchBoxEntry.insert(0, defaultText)
        searchBoxEntry.config(fg='gray')
            
        scrollbar.config(command=listbox.yview)
        
        totalPage = (len(results) + dataPerPage - 1) // dataPerPage

        start = (currentPage - 1) * dataPerPage
        end = start + dataPerPage
        
        listbox.delete(0, END)
        
        if dataType == "User":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Last Login: {result[4]}")
            
        elif dataType == "Companion":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Companion Level: {result[9]}")
            
        elif dataType == "CustomTask":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Task Title: {result[9]}   |   Created Date: {result[13]}")
            
        elif dataType == "DailyTask":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Task Title: {result[9]}   |   Created Date: {result[12]}")
            
        elif dataType == "CompletedCustomTask":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Task Title: {result[9]}   |   Completed Date: {result[16]}")
            
        elif dataType == "CompletedDailyTask":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Task Title: {result[9]}   |   Completed Date: {result[15]}")
            
        UpdatePageButtonState()

    def NextPage(dataType):
        global currentPage, totalPage
        
        if currentPage < totalPage:
            currentPage += 1
            UpdateDataList(dataType)

    def PreviousPage(dataType):
        global currentPage
        
        if currentPage > 1:
            currentPage -= 1
            UpdateDataList(dataType)
            
    def SearchData(dataType):  
        global currentPage, totalPage, results
        
        currentPage = 1
        
        searchTerm = searchBoxEntry.get().strip()
        
        if dataType == "User":
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT *
            FROM User
            WHERE username LIKE ? OR CAST(userID AS TEXT) LIKE ?;
            ''', (f"%{searchTerm}%", f"%{searchTerm}%",))
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "Companion":
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Companion.level

            cursor.execute('''
            SELECT User.*, Companion.*
            FROM Companion
            JOIN User ON Companion.userID = User.userID
            WHERE User.username LIKE ? OR CAST(User.userID AS TEXT) LIKE ?;
            ''', (f"%{searchTerm}%", f"%{searchTerm}%",))
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "CustomTask":
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Custom_Task.title, Custom_Task.createdDate
            
            cursor.execute('''
            SELECT User.*, Custom_Task.*
            FROM Custom_Task
            JOIN User ON Custom_Task.userID = User.userID
            WHERE Custom_Task.title LIKE ? OR CAST(User.userID AS TEXT) LIKE ?;
            ''', (f"%{searchTerm}%", f"%{searchTerm}%",))
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "DailyTask":
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Daily_Task.title, Daily_Task.createdDate
            
            cursor.execute('''
            SELECT User.*, Daily_Task.*
            FROM Daily_Task
            JOIN User ON Daily_Task.userID = User.userID
            WHERE Daily_Task.title LIKE ? OR CAST(User.userID AS TEXT) LIKE ?;
            ''', (f"%{searchTerm}%", f"%{searchTerm}%",))
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "CompletedCustomTask":
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Custom_Task.title, Completed_Custom_Task.completedDate
            
            cursor.execute('''
            SELECT User.*, Custom_Task.*, Completed_Custom_Task.*
            FROM Completed_Custom_Task
            JOIN Custom_Task ON Completed_Custom_Task.customTaskID = Custom_Task.customTaskID
            JOIN User ON Custom_Task.userID = User.userID
            WHERE Custom_Task.title LIKE ? OR CAST(User.userID AS TEXT) LIKE ?;
            ''', (f"%{searchTerm}%", f"%{searchTerm}%",))
            results = cursor.fetchall()
            
            conn.close()
            
        elif dataType == "CompletedDailyTask":
            conn = sqlite3.connect('Task.db')
            cursor = conn.cursor()
            
            # SELECT User.userID, User.username, Daily_Task.title, Completed_Daily_Task.completedDate
            
            cursor.execute('''
            SELECT User.*, Custom_Task.*, Completed_Custom_Task.*
            FROM Completed_Daily_Task
            JOIN Daily_Task ON Completed_Daily_Task.dailyTaskID = Daily_Task.dailyTaskID
            JOIN User ON Daily_Task.userID = User.userID
            WHERE Daily_Task.title LIKE ? OR CAST(User.userID AS TEXT) LIKE ?;
            ''', (f"%{searchTerm}%", f"%{searchTerm}%",))
            results = cursor.fetchall()      
            
            conn.close()

        totalPage = (len(results) + dataPerPage - 1) // dataPerPage

        start = (currentPage - 1) * dataPerPage
        end = start + dataPerPage
        
        listbox.delete(0, END)
        
        if dataType == "User":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Last Login: {result[4]}")
            
        elif dataType == "Companion":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Companion Level: {result[9]}")
            
        elif dataType == "CustomTask":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Task Title: {result[9]}   |   Created Date: {result[13]}")
            
        elif dataType == "DailyTask":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Task Title: {result[9]}   |   Created Date: {result[12]}")
            
        elif dataType == "CompletedCustomTask":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Task Title: {result[9]}   |   Completed Date: {result[16]}")
            
        elif dataType == "CompletedDailyTask":
            for result in results[start:end]:
                listbox.insert(END, f"{dataType} - User ID: {result[0]}   |   Username: {result[1]}   |   Task Title: {result[9]}   |   Completed Date: {result[15]}")

        UpdatePageButtonState()
            
    def ResetSearchData(dataType):
        global currentPage
        
        currentPage = 1
        
        searchBoxEntry.delete(0, END)
        
        UpdateDataList(dataType)
        
    def ShowDataDetails(event, dataType):
        global results, currentPage
        
        index = (listbox.curselection()[0]) + ((currentPage - 1) * dataPerPage)
        selectedResult = results[index]
        
        if dataType == "User":
            window.destroy()
            from AdminManageDatabase import AdminManageUserDataWindow
            AdminManageUserDataWindow(selectedResult)
            
        elif dataType == "Companion":
            window.destroy()
            from AdminManageDatabase import AdminManageCompanionDataWindow
            AdminManageCompanionDataWindow(selectedResult)
            
        elif dataType == "CustomTask":
            window.destroy()
            from AdminManageDatabase import AdminManageCustomTaskDataWindow
            AdminManageCustomTaskDataWindow(selectedResult)
            
        elif dataType == "DailyTask":
            window.destroy()
            from AdminManageDatabase import AdminManageDailyTaskDataWindow
            AdminManageDailyTaskDataWindow(selectedResult)
            
        elif dataType == "CompletedCustomTask":
            window.destroy()
            from AdminManageDatabase import AdminManageCompletedCustomTaskDataWindow
            AdminManageCompletedCustomTaskDataWindow(selectedResult)
            
        elif dataType == "CompletedDailyTask":
            window.destroy()
            from AdminManageDatabase import AdminManageCompletedDailyTaskDataWindow
            AdminManageCompletedDailyTaskDataWindow(selectedResult)
        
    def Logout():
        logoutButton.config(state=DISABLED)
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
            
            app = Singleton.getMainWindowInstance()
            
            app.user = None

            from LoginAndEverything import LoginWindow
            window.destroy()
            Singleton.getMainWindowInstance().withdraw()
            LoginWindow()
            
        else:
            logoutButton.config(state=NORMAL)
            
    def Quit():
        app = Singleton.getMainWindowInstance()    
        app.OnClose()
        
    global defaultText
    defaultText = None
        
    window = Toplevel()
    
    windowWidth = 800
    windowHeight = 350
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Admin Panel")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow("AdminWindow", window)
    
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
    
    logoutButton = Button(frame1, text="Logout", command=Logout)
    logoutButton.pack(side=LEFT, padx=10)
    
    def setCurrentDataAndUpdateList(data):
        currentData = data
        UpdateDataList(currentData)
    
    showUserDataButton = ttk.Button(frame2, text="User", command=lambda: setCurrentDataAndUpdateList("User"))
    showUserDataButton.pack(side=LEFT, padx=(10,0))
    
    showCompanionDataButton = ttk.Button(frame2, text="Companion", command=lambda: setCurrentDataAndUpdateList("Companion"))
    showCompanionDataButton.pack(side=LEFT)

    showCustomTaskDataButton = ttk.Button(frame2, text="Custom Task", command=lambda: setCurrentDataAndUpdateList("CustomTask"))
    showCustomTaskDataButton.pack(side=LEFT)
    
    showDailyTaskDataButton = ttk.Button(frame2, text="Daily Task", command=lambda: setCurrentDataAndUpdateList("DailyTask"))
    showDailyTaskDataButton.pack(side=LEFT)
    
    showCompletedCustomTaskDataButton = ttk.Button(frame2, text="Completed Custom Task", command=lambda: setCurrentDataAndUpdateList("CompletedCustomTask"))
    showCompletedCustomTaskDataButton.pack(side=LEFT)
    
    showCompletedDailyTaskDataButton = ttk.Button(frame2, text="Completed Daily Task", command=lambda: setCurrentDataAndUpdateList("CompletedDailyTask"))
    showCompletedDailyTaskDataButton.pack(side=LEFT)
    
    def OnEntryClick(event, defaultText):
        if searchBoxEntry.get() == defaultText:
            searchBoxEntry.delete(0, END)
            searchBoxEntry.config(fg='black')

    def OnFocusOut(event, defaultText):
        if not searchBoxEntry.get():
            searchBoxEntry.insert(0, defaultText)
            searchBoxEntry.config(fg='gray')
            
    searchBoxEntry = Entry(frame3, width=100)
    searchBoxEntry.pack(side=LEFT, padx=10)
    
    searchBoxEntry.bind("<FocusIn>", lambda event: OnEntryClick(event, defaultText))
    searchBoxEntry.bind("<FocusOut>", lambda event: OnFocusOut(event, defaultText))
    
    searchButton = ttk.Button(frame3, text="Search", command=lambda: SearchData(currentData))
    searchButton.pack(side=LEFT, padx=(5, 0))
    
    resetButton = ttk.Button(frame3, text="Reset", command=lambda: ResetSearchData(currentData))
    resetButton.pack(side=LEFT, padx=(5, 10))

    scrollbar = Scrollbar(frame4, orient='vertical')
    scrollbar.pack(side=RIGHT, fill=Y, padx=10)

    listbox = Listbox(frame4, yscrollcommand=scrollbar.set)
    listbox.pack(side=LEFT, fill=BOTH, expand=True, padx=10)
    
    listbox.bind('<Double-1>', lambda event: ShowDataDetails(event, currentData))

    previousPageButton = ttk.Button(frame5, text="Previous", command=lambda: PreviousPage(currentData))
    previousPageButton.pack(side=LEFT, pady=5, padx=70)
    
    nextPageButton = ttk.Button(frame5, text="Next", command=lambda: NextPage(currentData))
    nextPageButton.pack(side=RIGHT, pady=5, padx=70)
    
    UpdateDataList(currentData)
    
    window.mainloop()