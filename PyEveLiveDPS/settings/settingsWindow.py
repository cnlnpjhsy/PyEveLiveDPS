"""
Makes a Settings window
which acceps user input, and validates it in 'doSettings'
"""

import tkinter as tk
import tkinter.font as tkFont
import tkinter.colorchooser as colorchooser
import sys
import copy
import os
from settings.generalSettingsFrame import GeneralSettingsFrame
from settings.lineSettingsFrame import LineSettingsFrame
from settings.labelSettingsFrame import LabelSettingsFrame
from settings.detailSettingsFrame import DetailSettingsFrame
from settings.fleetSettingsFrame import FleetSettingsFrame
from peld import settings

class SideBar(tk.Frame):
    images = {"数据追踪": "lines.png",
              "数据标签": "labels.png",
              "按飞行员显示": "pilotDetails.png",
              "舰队窗口": "fleet.png"
             }
    
    def __init__(self, parent, mainWindow, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.mainWindow = mainWindow
        self.update_idletasks()
        tk.Frame(self, height="0", width=self.winfo_reqwidth()).grid(row="0", column="0")
        
        self.counter = 0
        
    def addOption(self, title, function):
        button = tk.Radiobutton(self, text=title, command=lambda:function(title), 
                                indicatoron=0, value=self.counter,
                                selectcolor="#00FFFF", bg="#FFFFFF",
                                compound="top")
        font = tkFont.Font(font=button['font'])
        font.config(weight='bold')
        button['font'] = font
        button.grid(row=self.counter, column="0", sticky="ew")
        if self.counter == 0:
            button.select()
            
        try:
            chosenImage = self.images[title]
        except KeyError:
            chosenImage = "gear.png"
            
        try:
            image = tk.PhotoImage(file=sys._MEIPASS + '\\images\\' + chosenImage)
            button.configure(image=image)
            button.image = image
        except Exception:
            try:
                path = os.path.join('PyEveLiveDPS', 'images', chosenImage)
                image = tk.PhotoImage(file=path)
                button.configure(image=image)
                button.image = image
            except Exception as e:
                pass
                
        self.counter += 1

class SettingsWindow(tk.Toplevel):
    def __init__(self, mainWindow):
        tk.Toplevel.__init__(self)
        
        self.mainWindow = mainWindow
        self.graph = mainWindow.getGraph()
        
        self.wm_attributes("-topmost", True)
        self.wm_title("PyEveLiveDPS 设置")
        try:
            self.iconbitmap(sys._MEIPASS + '\\app.ico')
        except Exception:
            try:
                self.iconbitmap("app.ico")
            except Exception:
                pass
        self.geometry("550x600")
        self.update_idletasks()
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        generalFrame = GeneralSettingsFrame(self, self.mainWindow, relief="groove", borderwidth=1)
        generalFrame.grid(row="0", column="1", columnspan="10", rowspan="90", sticky="wens")
        
        linesFrame = LineSettingsFrame(self, self.mainWindow, relief="groove", borderwidth=1)
        linesFrame.grid(row="0", column="1", columnspan="10", rowspan="90", sticky="wens")
        linesFrame.grid_remove()
        
        labelsFrame = LabelSettingsFrame(self, self.mainWindow, relief="groove", borderwidth=1)
        labelsFrame.grid(row="0", column="1", columnspan="10", rowspan="90", sticky="wens")
        labelsFrame.grid_remove()
        
        detailsFrame = DetailSettingsFrame(self, self.mainWindow, relief="groove", borderwidth=1)
        detailsFrame.grid(row="0", column="1", columnspan="10", rowspan="90", sticky="wens")
        detailsFrame.grid_remove()
        
        fleetFrame = FleetSettingsFrame(self, self.mainWindow, relief="groove", borderwidth=1)
        fleetFrame.grid(row="0", column="1", columnspan="10", rowspan="90", sticky="wens")
        fleetFrame.grid_remove()
        
        self.options = [["总体设定", generalFrame], ["数据追踪", linesFrame], ["数据标签", labelsFrame],
                        ["按飞行员显示", detailsFrame], ["舰队窗口", fleetFrame]]
        
        self.sideBar = SideBar(self, self.mainWindow, bg="white", width="125", relief="groove", borderwidth=1)
        self.sideBar.grid(row="0", column="0", rowspan="90", sticky="nsew", padx="1", pady="1")
        for option,frame in self.options:
            self.sideBar.addOption(option, self.switchTab)
        
        tk.Frame(self, height="20", width="10").grid(row="99", column="1", columnspan="5")
        
        buttonFrame = tk.Frame(self)
        buttonFrame.grid(row="100", column="0", columnspan="5")
        okButton = tk.Button(buttonFrame, text="  应用  ", command=self.doSettings)
        okButton.grid(row="0", column="0")
        tk.Frame(buttonFrame, height="1", width="30").grid(row="0", column="1")
        cancelButton = tk.Button(buttonFrame, text="  取消  ", command=self.destroy)
        cancelButton.grid(row="0", column="2")
        
        tk.Frame(self, height="20", width="10").grid(row="101", column="1", columnspan="5")
        
    def switchTab(self, title):
        for option, frame in self.options:
            if option == title:
                frame.grid()
                if option == "数据标签":
                    self.geometry("1100x600")
                elif option == "数值追踪":
                    self.geometry("900x600")
                else:
                    self.geometry("550x600")
            else:
                frame.grid_remove()
            
            
        
    def doSettings(self):
        if settings.lowCPUMode:
            if not tk.messagebox.askokcancel("你确定吗？", "在低CPU占用舰队模式中，设置" + 
                                         "将会在舰队模式关闭后才会被应用。\n\n" + 
                                         "It will also remove most of your settings."):
                return
        settingsToApply = {}
        for option, frame in self.options:
            returnValue = frame.doSettings()
            if returnValue == None:
                return
            settingsToApply.update(returnValue)
        
        settings.setSettings(**settingsToApply)
        
        self.mainWindow.animator.changeSettings()
        
        self.destroy()