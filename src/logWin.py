import wx
import time

instance = None

class ConsoleWin():

    def __init__(self, parent):
        global instance
        if instance is None:
            instance = self
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.console = wx.TextCtrl(parent, wx.ID_ANY, style = wx.TE_MULTILINE|wx.TE_READONLY)
        box.Add(self.console, 1, flag = wx.EXPAND)
        # parent.SetSizer(box)
        parent.SetSizerAndFit(box)

    def log(self, text):
        self.console.WriteText('>>> ' + time.strftime("%H:%M:%S  ", time.localtime())  + '  ' + text + '\n')