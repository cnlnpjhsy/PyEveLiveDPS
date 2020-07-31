import tkinter as tk
import tkinter.font as tkFont
from peld import settings

class GeneralSettingsFrame(tk.Frame):
    def __init__(self, parent, mainWindow, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.mainWindow = mainWindow
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)
        self.configure(pady=10)
        tk.Frame(self, height="0", width="1").grid(row="0", column="0")
        tk.Frame(self, height="0", width="1").grid(row="0", column="4")
        self.counter = 0
        
        checkboxValue = tk.BooleanVar()
        checkboxValue.set(settings.getGraphDisabled())
        self.graphDisabled = tk.Checkbutton(self, text="完全禁用图象", variable=checkboxValue)
        self.graphDisabled.var = checkboxValue
        self.graphDisabled.grid(row=self.counter, column="1", columnspan="2")
        descriptor = tk.Label(self, text="数据标签将仍被显示")
        font = tkFont.Font(font=descriptor['font'])
        font.config(slant='italic')
        descriptor['font'] = font
        descriptor.grid(row=self.counter+1, column="1", columnspan="2")
        tk.Frame(self, height="20", width="10").grid(row=self.counter+2, column="1", columnspan="5")
        self.counter += 3
        
        self.secondsVar = tk.StringVar()
        self.secondsVar.set(settings.getSeconds())
        self.addSetting(self.secondsVar, "每求一次数据平均值的时间间隔（秒）:", 
                        "建议将此值设定为高于你武器射速的数值。")
        
        self.intervalVar = tk.StringVar()
        self.intervalVar.set(settings.getInterval())
        self.addSetting(self.intervalVar, "更新图象与数据标签的时间间隔（毫秒）:", 
                        "该值越低，电脑CPU的占用越高。")
        
        self.transparencyVar = tk.StringVar()
        self.transparencyVar.set(settings.getCompactTransparency())
        self.addSetting(self.transparencyVar, "紧凑模式下的窗口透明度:", 
                        "100为完全可见，0为完全不可见。")
        
        
    def addSetting(self, var, labelText, descriptorText):
        centerFrame = tk.Frame(self)
        centerFrame.grid(row=self.counter, column="1", columnspan="2")
        label = tk.Label(centerFrame, text=labelText)
        label.grid(row=self.counter, column="1", sticky="e")
        entry = tk.Entry(centerFrame, textvariable=var, width=10)
        entry.grid(row=self.counter, column="2", sticky="w")
        descriptor = tk.Label(self, text=descriptorText)
        font = tkFont.Font(font=descriptor['font'])
        font.config(slant='italic')
        descriptor['font'] = font
        descriptor.grid(row=self.counter+1, column="1", columnspan="2")
        tk.Frame(self, height="20", width="10").grid(row=self.counter+2, column="1", columnspan="5")
        self.counter += 3
        
    def doSettings(self):
        try:
            secondsSetting = int(self.secondsVar.get())
        except ValueError:
            tk.messagebox.showerror("错误", "请输入一个数值（秒）来求平均DPS")
            return
        if (secondsSetting < 2 or secondsSetting > 600):
            tk.messagebox.showerror("错误", "请输入一个介于2-600的数值（秒）来求平均DPS")
            return  
        
        try:
            intervalSetting = int(self.intervalVar.get())
        except ValueError:
            tk.messagebox.showerror("错误", "请输入一个数值（毫秒）来更新图象")
            return
        if (intervalSetting < 10 or intervalSetting > 1000):
            tk.messagebox.showerror("错误", "请输入一个介于10-1000的数值（毫秒）来更新图象")
            return
        
        if ((secondsSetting*1000)/intervalSetting <= 10):
            tk.messagebox.showerror("错误", "(求平均值的时间间隔（秒）*1000)/(更新图象的时间间隔) 必须大于10。\n" +
                                   "如果该值小于10，数据将不足以绘出准确图象。")
            return
        
        if ((secondsSetting*1000)/intervalSetting < 20):
            okCancel = tk.messagebox.askokcancel("继续？", "(求平均值的时间间隔（秒）*1000)/(更新图象的时间间隔) 小于20。\n" +
                                   "这是被允许的，但建议你增大 求平均值的时间间隔（秒）或减小 更新图象的时间间隔 来提高图象准确度。\n"
                                   "是否仍要保留这些设置？")
            if not okCancel:
                return
            
        if (intervalSetting < 50):
            okCancel = tk.messagebox.askokcancel("继续？", "将更新图象的时间间隔设置为低于50ms会极大增加电脑CPU的负荷。"
                                                 "是否仍要保留这些设置？")
            if not okCancel:
                return
            
        if (secondsSetting/intervalSetting > 1):
            okCancel = tk.messagebox.askokcancel("继续？", "(求平均值的时间间隔（秒）*1000)/(更新图象的时间间隔) 大于1000。\n" +
                                   "这是被允许的，但建议你减小 更新图象的时间间隔 来提高性能。\n"
                                   "若你将 求平均值的时间间隔 设置得很高时，没有必要将 更新图象的时间间隔 设置得如此低。\n"
                                   "是否仍要保留这些设置？")
            if not okCancel:
                return
            
        try:
            compactTransparencySetting = int(self.transparencyVar.get())
        except ValueError:
            tk.messagebox.showerror("错误", "请输入紧凑模式下的窗口透明度")
            return
        if (compactTransparencySetting < 1 or compactTransparencySetting > 100):
            tk.messagebox.showerror("错误", "请输入一个介于1-100的紧凑模式下的窗口透明度")
            return  
        
        return {"seconds": secondsSetting, "interval": intervalSetting, 
                "compactTransparency": compactTransparencySetting, "graphDisabled": self.graphDisabled.var.get()}