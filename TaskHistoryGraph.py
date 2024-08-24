from tkinter import *
from datetime import datetime, timedelta
import sqlite3
from MainWindowSingleton import *
from WindowManager import *
import library.matplotlib.pyplot as plt
from library.matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def TaskHistoryGraphWindow():    
    def GetCompletedTaskNumber(startDate):
        endDate = startDate + timedelta(days=6)
        
        conn = sqlite3.connect("Task.db")
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT completedDate, COUNT(*) as count 
        FROM (
            SELECT Completed_Daily_Task.completedDate 
            FROM Completed_Daily_Task
            JOIN Daily_Task ON Completed_Daily_Task.dailyTaskID = Daily_Task.dailyTaskID
            WHERE Daily_Task.userID = ? AND Completed_Daily_Task.completedDate BETWEEN ? AND ?
            UNION ALL
            SELECT Completed_Custom_Task.completedDate 
            FROM Completed_Custom_Task
            JOIN Custom_Task ON Completed_Custom_Task.customTaskID = Custom_Task.customTaskID
            WHERE Custom_Task.userID = ? AND Completed_Custom_Task.completedDate BETWEEN ? AND ?
        )
        GROUP BY completedDate
        ''', (userID, startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d"), userID, startDate.strftime("%Y-%m-%d"), endDate.strftime("%Y-%m-%d")))
        completedTaskNumber = cursor.fetchall()
        
        conn.close()
        
        return completedTaskNumber

    def Graph(startDate):
        print("Creating graph...")
        
        completedTaskNumber = GetCompletedTaskNumber(startDate)
        
        datesNumbers = [startDate + timedelta(days=i) for i in range(7)]
        
        tasksNumber = {}
        for dateNumber in datesNumbers:
            tasksNumber[dateNumber.strftime("%Y-%m-%d")] = 0
        
        for row in completedTaskNumber:
            tasksNumber[row[0]] += row[1]
        
        figure, axis = plt.subplots()
        
        axis.bar(tasksNumber.keys(), tasksNumber.values())
        
        axis.set_xlabel("Date")
        axis.set_ylabel("Tasks Completed")
        axis.set_title(f"Tasks Completed from {startDate.strftime('%d/%m/%Y')} to {(startDate + timedelta(days=6)).strftime('%d/%m/%Y')}")
        
        axis.set_yticks(range(0, max(tasksNumber.values()) + 2))

        return figure

    def UpdateGraph():
        global currentWeekMonday
        
        figure = Graph(currentWeekMonday)
        
        for widget in frame2.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(figure, master=frame2)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def PreviousWeek():
        global currentWeekMonday
        currentWeekMonday -= timedelta(days=7)
        
        UpdateGraph()

    def NextWeek():
        global currentWeekMonday
        currentWeekMonday += timedelta(days=7)
        
        UpdateGraph()
        
    def Back():
        window.destroy()
        from TaskHistory import TaskHistoryWindow
        TaskHistoryWindow()
        
    def Quit():
        app = Singleton.getMainWindowInstance()    
        app.OnClose()
    
    window = Toplevel()
    
    windowWidth = 945
    windowHeight = 600
    x = (window.winfo_screenwidth()//2)-(windowWidth//2)
    y = (window.winfo_screenheight()//2)-(windowHeight//2)
    
    window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    window.configure(bg="#FFFFFF")
    window.title("Task History Graph")
    
    window.protocol("WM_DELETE_WINDOW", Quit)
    
    AddWindow('TaskHistoryGraphWindow', window)
    
    app = Singleton.getMainWindowInstance()
    
    userID = app.user[0]
    # username = app.user[1]
    # password = app.user[2]
    # birthdate = app.user[3]
    # lastLogin = app.user[4]
    # isReminder = app.user[5]
    # intervalHour = app.user[6]
    
    global currentWeekMonday
    
    currentWeekMonday = datetime.now() - timedelta(days=datetime.now().weekday())

    frame1 = Frame(window)
    frame1.pack(fill=BOTH, expand=1)

    frame2 = Frame(frame1)
    frame2.pack(fill=BOTH, expand=1)

    frame3 = Frame(frame1)
    frame3.pack(fill=X)
    
    previousWeekButton = Button(frame3, text="Previous Week", command=PreviousWeek)
    previousWeekButton.pack(side=LEFT, padx=20, pady=20)

    nextWeekButton = Button(frame3, text="Next Week", command=NextWeek)
    nextWeekButton.pack(side=LEFT, padx=20, pady=20)
    
    backButton = Button(frame3, text="Back", command=Back)
    backButton.pack(side=RIGHT, padx=20, pady=20)
    
    UpdateGraph()

    window.mainloop()