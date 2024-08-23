from tkinter import *
import textwrap
import hashlib
import sys
from WindowManager import *
from library.PIL import Image, ImageTk

def hashingString(string):
    return hashlib.sha256(string.encode()).hexdigest()

class Singleton:
    _instance = None

    @staticmethod
    def getMainWindowInstance():
        if Singleton._instance is None:
            Singleton()
        return Singleton._instance

    def __init__(self):
        Singleton._instance = MainWindow()
        
class SpriteAnimator:
    def __init__(self, parent, spriteSheetPath, row, frameCount, width, height, scale, delay):
        self.parent = parent
        self.sheet = Image.open(spriteSheetPath)
        self.row = row
        self.frameCount = frameCount
        self.width = width
        self.height = height
        self.scale = scale
        self.delay = delay

        self.sprites = self.GetRowSprites()
        self.spritesTk = [ImageTk.PhotoImage(sprite) for sprite in self.sprites]

        self.label = Label(parent, bg="white")
        self.label.pack()

        self.currentFrame = 0
        
        self.Animate()

    def GetRowSprites(self):
        sprites = []
        for i in range(self.frameCount):
            left = i * self.width
            upper = self.row * self.height
            right = left + self.width
            lower = upper + self.height
            
            sprite = self.sheet.crop((left, upper, right, lower))
            
            if self.scale != 1:
                sprite = sprite.resize((int(self.width * self.scale), int(self.height * self.scale)), Image.Resampling.LANCZOS)
                
            sprites.append(sprite)
            
        return sprites

    def Animate(self):
        self.label.config(image=self.spritesTk[self.currentFrame])

        self.currentFrame = (self.currentFrame + 1) % self.frameCount
        
        self.parent.after(self.delay, self.Animate)

class MainWindow(Tk): 
    def __init__(self, user=None):
        super().__init__()
        self.user = user
        
        windowWidth = 96
        windowHeight = 96
        x = (self.winfo_screenwidth()//2)-(windowWidth//2)
        y = (self.winfo_screenheight()//2)-(windowHeight//2)
    
        self.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        
        AddMainWindow('MainWindow', self)

        self.spriteAnimator = None
        self.currentAnimationID = None
        self.ChangeAnimation("idle2")
        
        self.bind("<ButtonPress-1>", self.StartDrag)
        self.bind("<B1-Motion>", self.Dragging)
        self.bind("<ButtonRelease-1>", self.StopDrag)
        
        self.bind("<Button-3>", self.OpenMenuPanel)
        
        self.bind("<Button-2>", self.OnClickSleep)
        
        self._offset_x = 0
        self._offset_y = 0
        
    def StartDrag(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def Dragging(self, event):
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f'+{x}+{y}')

    def StopDrag(self, event):
        self._offset_x = 0
        self._offset_y = 0
        
    def Task(self):
        RemoveAllWindow()
        from Task import TaskWindow
        TaskWindow()
        
    def Setting(self):
        RemoveAllWindow()
        from Setting import SettingWindow
        SettingWindow()
        
    def OnClose(self):
        sys.exit()
    
    def OpenMenuPanel(self, event):
        menuPanel = Menu(self, tearoff=0)
        menuPanel.add_command(label="Task", command=self.Task)
        menuPanel.add_command(label="Setting", command=self.Setting)
        menuPanel.add_separator()
        menuPanel.add_command(label="Quit", command=self.OnClose)
        menuPanel.post(event.x_root, event.y_root)
        
    def OnClickSleep(self, event):
        self.ChangeAnimation("sleep")
        
    def DialogBoxFadeIn(self, window, alpha=0):
        alpha += 0.1
        if alpha <= 1:
            window.attributes("-alpha", alpha)
            window.after(50, self.DialogBoxFadeIn, window, alpha)

    def DialogBoxFadeOut(self, window, alpha=1):
        alpha -= 0.1
        if alpha >= 0:
            window.attributes("-alpha", alpha)
            window.after(50, self.DialogBoxFadeOut, window, alpha)
        else:
            window.destroy()
        
    def UseDialogBox(self, text):
        dialogWindow = Toplevel(self)
        dialogWindow.overrideredirect(True)
        dialogWindow.attributes("-alpha", 0)
        
        maxCharactersPerLine = 50
        lines = textwrap.wrap(text, width=maxCharactersPerLine)
        
        fontSize = 10
        width = maxCharactersPerLine * fontSize
        height = 50 + (len(lines) - 1) * 20
        x = self.winfo_x() + (96 - width) // 2
        y = self.winfo_y() + self.winfo_height()
        
        if y + height > self.winfo_screenheight():
            y = self.winfo_screenheight() - height - 10
            
        dialogWindow.geometry(f"{width}x{height}+{x}+{y}")
        
        label = Label(dialogWindow, text='\n'.join(lines))
        label.pack()

        self.DialogBoxFadeIn(dialogWindow)
        
        dialogWindow.after(10000, self.DialogBoxFadeOut, dialogWindow)
        
    def clearSprite(self):
        if self.spriteAnimator:
            self.spriteAnimator.label.pack_forget()
            self.spriteAnimator = None

        if self.currentAnimationID is not None:
            self.after_cancel(self.currentAnimationID)
            self.currentAnimationID = None

    def sleep1(self):
        self.clearSprite()
        self.spriteAnimator = SpriteAnimator(self, spriteSheetPath="assets/main/CatSpriteSheet.png", row=0, frameCount=4, width=32, height=32, scale=3, delay=1000)
        self.currentAnimationID = self.after(4000, self.sleep2)

    def sleep2(self):
        self.clearSprite()
        self.spriteAnimator = SpriteAnimator(self, spriteSheetPath="assets/main/CatSpriteSheet.png", row=1, frameCount=7, width=32, height=32, scale=3, delay=1000)
        self.currentAnimationID = self.after(7000, self.sleep3)

    def sleep3(self):
        self.clearSprite()
        self.spriteAnimator = SpriteAnimator(self, spriteSheetPath="assets/main/CatSpriteSheet.png", row=2, frameCount=3, width=32, height=32, scale=3, delay=1000)
        self.currentAnimationID = self.after(3000, self.idle1)
        
    def idle1(self):
        self.clearSprite()
        self.spriteAnimator = SpriteAnimator(self, spriteSheetPath="assets/main/CatSpriteSheet.png", row=3, frameCount=4, width=32, height=32, scale=3, delay=500)
        self.currentAnimationID = self.after(2000, self.idle2)
        
    def idle2(self):
        self.clearSprite()
        self.spriteAnimator = SpriteAnimator(self, spriteSheetPath="assets/main/CatSpriteSheet.png", row=4, frameCount=8, width=32, height=32, scale=3, delay=500)
        self.currentAnimationID = self.after(4000, self.idle1)
        
    def happy(self):
        self.clearSprite()
        self.spriteAnimator = SpriteAnimator(self, spriteSheetPath="assets/main/CatSpriteSheet.png", row=5, frameCount=8, width=32, height=32, scale=3, delay=500)
        self.currentAnimationID = self.after(20000, self.idle1)
        
    def angry(self):
        self.clearSprite()
        self.spriteAnimator = SpriteAnimator(self, spriteSheetPath="assets/main/CatSpriteSheet.png", row=6, frameCount=7, width=32, height=32, scale=3, delay=500)
        self.currentAnimationID = self.after(17500, self.idle2)
        
    def ChangeAnimation(self, animation):
        if animation == "sleep":
            self.sleep1()
            
        elif animation == "idle1":
            self.idle1()
            
        elif animation == "idle2":
            self.idle2()
            
        elif animation == "happy":
            self.happy()
            
        elif animation == "angry":
            self.angry()