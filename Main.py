import sqlite3
import threading
from datetime import datetime, timedelta
from tkinter import *
from Database import *
from CheckingStuff import *
from MainWindowSingleton import Singleton

def getUserWithClosestLastLogin():
    conn = sqlite3.connect('Task.db')
    cursor = conn.cursor()
    
    currentDate = datetime.now()
    threeDaysAgo = currentDate - timedelta(days=3)
    
    cursor.execute('''
        SELECT *
        FROM User 
        WHERE lastLogin IS NOT NULL AND lastLogin >= ?
        ORDER BY lastLogin DESC
        LIMIT 1
    ''', (threeDaysAgo.strftime('%Y-%m-%d'),))
    currentUser = cursor.fetchone()
    
    conn.close()
    
    if currentUser:
        return currentUser
    return None

def onLoginSuccess(currentUserID):
    app = Singleton.getMainWindowInstance()
       
    user = FetchRecord('User', columns=['*'], where_clause='userID = ?', params=(currentUserID,))

    app.user = user[0]
    
    if app.user and app.user[1] == "Admin":
        from AdminPage import AdminWindow
        AdminWindow()
        
        app.mainloop()

    elif app.user:        
        app = Singleton.getMainWindowInstance()

        companionStat = FetchRecord('Companion', columns=['level'], where_clause='userID = ?', params=(app.user[0],))[0] 

        level = companionStat[0]
        
        if level >= 50:
            app.UseDialogBox("Welcome back, my favorite person! Let’s make up for lost time.")
            
        elif level >= 40 and level < 50:
            app.UseDialogBox("You being here makes everything better. What have you been up to?")
            
        elif level >= 30 and level < 40:
            app.UseDialogBox("It’s great to see you again. I’ve missed you!")
            
        elif level >= 20 and level < 30:
            app.UseDialogBox("Welcome back! I’ve been looking forward to seeing you again.")
            
        elif level >= 10 and level < 20:
            app.UseDialogBox("Welcome back. Nice to see you.")
            
        elif level < 10:
            app.UseDialogBox("Oh, you’re back. Cool, I guess. Not that I missed you or anything.")
        
        app.deiconify()
    
def Main():
    InitializingDatabase()
    
    app = Singleton.getMainWindowInstance()
    
    app.user = getUserWithClosestLastLogin()
    
    thread1 = threading.Thread(target=RunCheckLevelUp)
    thread1.daemon = True
    thread1.start()
    
    thread2 = threading.Thread(target=RunCompareCustomDueDate)
    thread2.daemon = True
    thread2.start()
    
    thread3 = threading.Thread(target=RunCompareDailyDueDate)
    thread3.daemon = True
    thread3.start()
    
    thread4 = threading.Thread(target=RunReminder)
    thread4.daemon = True
    thread4.start()
    
    if app.user and app.user[1] == "Admin":
        app.withdraw()
        
        from AdminPage import AdminWindow
        AdminWindow()
        
        app.mainloop()
    
    elif app.user:
        def DialogBoxFadeIn(window, alpha=0):
            alpha += 0.1
            if alpha <= 1:
                window.attributes("-alpha", alpha)
                window.after(50, DialogBoxFadeIn, window, alpha)

        def DialogBoxFadeOut(window, alpha=1):
            alpha -= 0.1
            if alpha >= 0:
                window.attributes("-alpha", alpha)
                window.after(50, DialogBoxFadeOut, window, alpha)
            else:
                window.destroy()
            
        def UseDialogBox(text):
            dialogWindow = Toplevel()
            dialogWindow.overrideredirect(True)
            dialogWindow.attributes("-alpha", 0)
            
            maxCharactersPerLine = 50
            lines = textwrap.wrap(text, width=maxCharactersPerLine)
            
            fontSize = 10
            width = maxCharactersPerLine * fontSize
            height = 50 + (len(lines) - 1) * 20
            dialogWindow.geometry(f"{width}x{height}+{672 + (96 - width) // 2}+528")
            
            label = Label(dialogWindow, text='\n'.join(lines))
            label.pack()

            DialogBoxFadeIn(dialogWindow)
            
            dialogWindow.after(3000, DialogBoxFadeOut, dialogWindow)
        
        app = Singleton.getMainWindowInstance()

        companionStat = FetchRecord('Companion', columns=['level'], where_clause='userID = ?', params=(app.user[0],))[0] 

        level = companionStat[0]
        
        if level >= 50:
            UseDialogBox("Welcome back, my favorite person! Let’s make up for lost time.")
            
        elif level >= 40 and level < 50:
            UseDialogBox("You being here makes everything better. What have you been up to?")
            
        elif level >= 30 and level < 40:
            UseDialogBox("It’s great to see you again. I’ve missed you!")
            
        elif level >= 20 and level < 30:
            UseDialogBox("Welcome back! I’ve been looking forward to seeing you again.")
            
        elif level >= 10 and level < 20:
            UseDialogBox("Welcome back. Nice to see you.")
            
        elif level < 10:
            UseDialogBox("Oh, you’re back. Cool, I guess. Not that I missed you or anything.")
        
        app.mainloop()
        
    else:
        app.withdraw()
        
        from LoginAndEverything import LoginWindow
        LoginWindow()
        
        app.mainloop()

if __name__ == "__main__":
    Main()