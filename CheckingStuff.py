from datetime import datetime, date, timedelta
import time
import sqlite3
from tkinter import messagebox
from Database import *
from MainWindowSingleton import *
from WindowManager import *

def CheckLevelUp():
    app = Singleton.getMainWindowInstance()
    
    if app.user and app.user[1] == "Admin":
        return

    elif app.user:        
        userID = app.user[0]
        # username = app.user[1]
        # password = app.user[2]
        # birthdate = app.user[3]
        # lastLogin = app.user[4]
        # isReminder = app.user[5]
        # intervalHour = app.user[6]

        companionStat = FetchRecord('Companion', columns=['companionID', 'level', 'friendshipPoint', 'friendshipPointNext', 'friendshipPointMultiplier'], where_clause='userID = ?', params=(userID,))[0] 

        companionID = companionStat[0]
        level = companionStat[1]
        friendshipPoint = companionStat[2]
        friendshipPointNext = companionStat[3]
        friendshipPointMultiplier = companionStat[4]
        
        if friendshipPoint < 0:
            friendshipPoint = 0
            
            messagebox.showwarning("Negative Friendship", "Your current friendship point has been set to 0!")

            app.ChangeAnimation("angry")
            
            if level >= 50:
                app.UseDialogBox("I’m heartbroken by what’s happened. I believed in you, and this feels like a big letdown.")
                
            elif level >= 40 and level < 50:
                app.UseDialogBox("I’m truly disappointed. I know you’re capable of more, and I’m hurt by this.")
                
            elif level >= 30 and level < 40:
                app.UseDialogBox("I’m really disappointed in you. I know you could have done better.")
                
            elif level >= 20 and level < 30:
                app.UseDialogBox("I’m disappointed. I really thought you’d come through on this.")
                
            elif level >= 10 and level < 20:
                app.UseDialogBox("I’m a bit let down. I thought you had this handled.")
                
            elif level < 10:
                app.UseDialogBox("I thought you’d do better. Guess I was wrong.")
        
        while friendshipPoint >= friendshipPointNext:
            level += 1
            friendshipPoint -= friendshipPointNext
            friendshipPointNext = round(10 * (level ** 2))
            
            messagebox.showinfo("Level Up!", f"You are now level '{level}'!")
            
            app.ChangeAnimation("happy")
            
            if level >= 50:
                app.UseDialogBox("This is such a huge achievement! I’m bursting with pride and excitement for you.")
                
            elif level >= 40 and level < 50:
                app.UseDialogBox("This is fantastic! Your hard work has really paid off. Let’s celebrate!")
                
            elif level >= 30 and level < 40:
                app.UseDialogBox("You’ve done something amazing! I’m thrilled for you.")
                
            elif level >= 20 and level < 30:
                app.UseDialogBox("That’s fantastic news! You worked hard for this, didn’t you?")
                
            elif level >= 10 and level < 20:
                app.UseDialogBox("Hey, that’s quite an achievement! You’re on a roll.")
                
            elif level < 10:
                app.UseDialogBox("Well, this is a pleasant surprise.")
            
            if WindowExists("TaskWindow"):
                messagebox.showinfo("Refresh", f"Task Window will close now to refresh")
                RemoveWindow("TaskWindow")
                
        if level >= 50 and friendshipPointMultiplier < 6:
            friendshipPointMultiplier = 6
            messagebox.showinfo("Milestone", f"You reached the final milstone (Level 50)! You will gain friendship point faster than before!")
            
            app.ChangeAnimation("happy")
            
            app.UseDialogBox("You’ve done something truly incredible. I’m honored to be with you through all of it and celebrate together!")
            
        elif level >= 40 and level < 50 and friendshipPointMultiplier < 5:
            friendshipPointMultiplier = 5
            messagebox.showinfo("Milestone", f"You reached the fourth milstone (Level 40)! You will gain friendship point faster than before!")
            
            app.ChangeAnimation("happy")
            
            app.UseDialogBox("You did an amazing job! I’m so happy for you and proud of what you’ve accomplished.")
            
        elif level >= 30 and level < 40 and friendshipPointMultiplier < 4:
            friendshipPointMultiplier = 4
            messagebox.showinfo("Milestone", f"You reached the third milstone (Level 30)! You will gain friendship point faster than before!")
            
            app.ChangeAnimation("happy")
            
            app.UseDialogBox("Wow, you really knocked it out of the park! I’m so proud of you.")
            
        elif level >= 20 and level < 30 and friendshipPointMultiplier < 3:
            friendshipPointMultiplier = 3
            messagebox.showinfo("Milestone", f"You reached the second milstone (Level 20)! You will gain friendship point faster than before!")
            
            app.ChangeAnimation("happy")
            
            app.UseDialogBox("I knew you had it in you! Great job on reaching this milestone.")
            
        elif level >= 10 and level < 20 and friendshipPointMultiplier < 2:
            friendshipPointMultiplier = 2
            messagebox.showinfo("Milestone", f"You reached the first milstone (Level 10)! You will gain friendship point faster than before!")
            
            app.ChangeAnimation("happy")
            
            app.UseDialogBox("Well done! That’s a nice milestone you’ve hit.")
                
        UpdateRecord('Companion',  {'level': level, 'friendshipPoint': friendshipPoint, 'friendshipPointNext': friendshipPointNext, 'friendshipPointMultiplier': friendshipPointMultiplier}, 'companionID = ?', (companionID,))
            
    else:
        return
        
def RunCheckLevelUp():
    while True:
        CheckLevelUp()
        time.sleep(1)
        
def CompareCustomDueDate():
    app = Singleton.getMainWindowInstance()
    
    if app.user and app.user[1] == "Admin":
        return

    elif app.user:
        userID = app.user[0]
        # username = app.user[1]
        # password = app.user[2]
        # birthdate = app.user[3]
        # lastLogin = app.user[4]
        # isReminder = app.user[5]
        # intervalHour = app.user[6]

        companionStat = FetchRecord('Companion', columns=['companionID', 'level', 'friendshipPoint', 'friendshipPointNext', 'friendshipPointMultiplier'], where_clause='userID = ?', params=(userID,))[0] 

        companionID = companionStat[0]
        level = companionStat[1]
        friendshipPoint = companionStat[2]
        # friendshipPointNext = companionStat[3]
        friendshipPointMultiplier = companionStat[4]
        
        conn = sqlite3.connect('Task.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT Custom_Task.customTaskID, Custom_Task.title, Custom_Task.difficulty, Custom_Task.dueDate
        FROM Custom_Task
        LEFT JOIN Completed_Custom_Task 
        ON Custom_Task.customTaskID = Completed_Custom_Task.customTaskID
        WHERE Completed_Custom_Task.customTaskID IS NULL;
        ''')
        incompleteCustomTasks = cursor.fetchall()

        conn.close()
        
        currentDate = date.today()

        for incompleteCustomTask in incompleteCustomTasks:
            customTaskID, title, difficulty, dueDateString = incompleteCustomTask
            dueDate = datetime.strptime(dueDateString, '%Y-%m-%d').date()

            if dueDate < currentDate:
                if WindowExists("UserEditCustomTaskWindow"):
                    RemoveWindow("UserEditCustomTaskWindow")
                
                messagebox.showwarning("Task Overdue!", f"Task '{title}' is overdue!")
                
                app.ChangeAnimation("angry")
            
                if level >= 50:
                    app.UseDialogBox("I’m genuinely heartbroken that you didn’t keep your promise. I know you have the strength to do better, and I’m here for you.")
                    
                elif level >= 40 and level < 50:
                    app.UseDialogBox("I’m feeling let down because you didn’t keep your promise. I know you’re capable, and it’s hard to see you not follow through.")
                    
                elif level >= 30 and level < 40:
                    app.UseDialogBox("I’m really hurt that you didn’t keep your promise. I thought we were on the same page.")
                    
                elif level >= 20 and level < 30:
                    app.UseDialogBox("I really believed you’d do it. Not keeping your promise feels like a letdown.")
                    
                elif level >= 10 and level < 20:
                    app.UseDialogBox("I was really hoping you’d follow through. It’s a bit let down that you didn’t.")
                    
                elif level < 10:
                    app.UseDialogBox("You said you’d do that, but it looks like you didn’t. That’s unfortunate.")
                
                CreateRecord('Completed_Custom_Task', {'customTaskID': customTaskID, 'completedDate': currentDate, 'isOverdue': 1})
                
                if difficulty == "Easy":
                    friendshipPoint -= (20 * friendshipPointMultiplier)
                elif difficulty == "Medium":
                    friendshipPoint -= (60 * friendshipPointMultiplier)
                elif difficulty == "Hard":
                    friendshipPoint -= (180 * friendshipPointMultiplier)
                elif difficulty == "Extreme":
                    friendshipPoint -= (540 * friendshipPointMultiplier)
                
        UpdateRecord('Companion',  {'friendshipPoint': friendshipPoint}, 'companionID = ?', (companionID,))
        
    else:
        return

def RunCompareCustomDueDate():
    while True:
        CompareCustomDueDate()
        time.sleep(1)
        
def CompareDailyDueDate():  
    app = Singleton.getMainWindowInstance()
    
    if app.user and app.user[1] == "Admin":
        return

    elif app.user:
        userID = app.user[0]
        # username = app.user[1]
        # password = app.user[2]
        # birthdate = app.user[3]
        # lastLogin = app.user[4]
        # isReminder = app.user[5]
        # intervalHour = app.user[6]
        
        currentDate = date.today()
        yesterdayDate = currentDate - timedelta(days=1)
        
        companionStat = FetchRecord('Companion', columns=['companionID', 'level', 'friendshipPoint', 'friendshipPointNext', 'friendshipPointMultiplier'], where_clause='userID = ?', params=(userID,))[0] 

        companionID = companionStat[0]
        level = companionStat[1]
        friendshipPoint = companionStat[2]
        # friendshipPointNext = companionStat[3]
        friendshipPointMultiplier = companionStat[4]
        
        conn = sqlite3.connect('Task.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT Daily_Task.dailyTaskID, Daily_Task.title, Daily_Task.difficulty
        FROM Daily_Task
        LEFT JOIN Completed_Daily_Task 
        ON Daily_Task.dailyTaskID = Completed_Daily_Task.dailyTaskID
        AND Completed_Daily_Task.completedDate = ?
        WHERE Completed_Daily_Task.completedDailyTaskID IS NULL
        AND Daily_Task.createdDate != ?;
        ''', (yesterdayDate, currentDate))
        incompleteYesterdayDailyTasks = cursor.fetchall()
        
        conn.close()

        for incompleteYesterdayDailyTask in incompleteYesterdayDailyTasks:
            if WindowExists("UserEditDailyTaskWindow"):
                RemoveWindow("UserEditDailyTaskWindow")
                    
            dailyTaskID, title, difficulty = incompleteYesterdayDailyTask

            messagebox.showwarning("Task Overdue!", f"Task '{title}' is overdue!")
            
            app.ChangeAnimation("angry")
            
            if level >= 50:
                app.UseDialogBox("You mean so much to me, and seeing you break a promise is really upsetting. I know you can do better, and I’m here to support you in making it right.")
                
            elif level >= 40 and level < 50:
                app.UseDialogBox("It’s painful to see you not honor a promise you made to yourself. I believe in you, and I’m disappointed.")
                
            elif level >= 30 and level < 40:
                app.UseDialogBox("This isn’t like you. I’m genuinely disappointed that you didn’t stick to what you said you’d do.")
                
            elif level >= 20 and level < 30:
                app.UseDialogBox("I’m quite disappointed. You made a promise and didn’t keep it. What’s going on?")
                
            elif level >= 10 and level < 20:
                app.UseDialogBox("I noticed you didn’t stick to what you promised. I thought you were committed.")
                
            elif level < 10:
                app.UseDialogBox("Oh, so you didn’t follow through? That’s a shame.")
            
            CreateRecord('Completed_Daily_Task', {'dailyTaskID': dailyTaskID, 'completedDate': yesterdayDate, 'isOverdue': 1})

            if difficulty == "Easy":
                friendshipPoint -= (10 * friendshipPointMultiplier)
            elif difficulty == "Medium":
                friendshipPoint -= (30 * friendshipPointMultiplier)
            elif difficulty == "Hard":
                friendshipPoint -= (90 * friendshipPointMultiplier)
            elif difficulty == "Extreme":
                friendshipPoint -= (270 * friendshipPointMultiplier)
        
        UpdateRecord('Companion',  {'friendshipPoint': friendshipPoint}, 'companionID = ?', (companionID,))
        
    else:
        return

def RunCompareDailyDueDate():
    while True:
        CompareDailyDueDate()
        time.sleep(1)
        
def RunReminder():
    while True:
        app = Singleton.getMainWindowInstance()
            
        if app.user and app.user[1] == "Admin":
            time.sleep(1)

        elif app.user:
            userID = app.user[0]
            # username = app.user[1]
            # password = app.user[2]
            # birthdate = app.user[3]
            # lastLogin = app.user[4]
            isReminder = app.user[5]
            intervalHour = app.user[6]
            
            companionStat = FetchRecord('Companion', columns=['level'], where_clause='userID = ?', params=(userID,))[0] 

            level = companionStat[0]
                
            intervalSecond = intervalHour * 60 * 60
            
            startTime = time.time()

            while isReminder == 1:
                if app.user and app.user[1] == "Admin":
                    break
                
                if app.user == None:
                    break
                
                if intervalHour != app.user[6]:
                    break
                    
                currentTime = time.time()
                
                if currentTime - startTime >= intervalSecond:
                    messagebox.showwarning("Reminder", f"You have been online for {intervalHour} hour(s)! Time to rest!")
                    
                    app.ChangeAnimation("sleep")
            
                    if level >= 50:
                        app.UseDialogBox("You mean so much to me, and I want you to be well. Please take a proper rest; you deserve it.")
                        
                    elif level >= 40 and level < 50:
                        app.UseDialogBox("We’ve worked so hard together. Now, it’s important that you take a break and take care of yourself.")
                        
                    elif level >= 30 and level < 40:
                        app.UseDialogBox("I care about your well-being. Please take a rest; you’ve earned it.")
                        
                    elif level >= 20 and level < 30:
                        app.UseDialogBox("I can tell you’re overdoing it. How about taking a break to recharge?")
                        
                    elif level >= 10 and level < 20:
                        app.UseDialogBox("I’ve noticed you’ve been pushing yourself. Maybe it’s time for a break?")
                        
                    elif level < 10:
                        app.UseDialogBox("You seem a bit tired. How about taking a short break?")
                    
                    startTime = currentTime
                else:
                    time.sleep(1)
                    
            time.sleep(1)
            
        else:
            time.sleep(1)