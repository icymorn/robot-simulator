import wx
import time
class ConsoleWin():
    def __init__(self, parent):
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.console = wx.TextCtrl(parent, wx.ID_ANY, style = wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.console, 1, flag = wx.EXPAND)
        # parent.SetSizer(box)
        parent.SetSizerAndFit(box)

    def log(self, text):
        self.console.WriteText('>>> ' + time.strftime("%H:%M:%S  ", time.localtime())  + '  ' + text + '\n')