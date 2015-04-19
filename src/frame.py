import wx
import logWin
import leftPanel
import mainPanel

class MainFrame(wx.Frame):

    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, title = title, size = size)

        self._setupStatusBar()
        self._setupWindow()
        self._setupToolBar()

        self.Show()

    def _setupLeftPanel(self):
        self.leftPanel = wx.Window(self.vSplitter)
        self.elementTree = leftPanel.ElementTree(self.leftPanel)

    def _setupMainPanel(self):
        self.mainPanel = wx.Window(self.vSplitter)
        self.view = mainPanel.RobotView(self.mainPanel)
        wx.StaticText(self.mainPanel, -1, "My right Panel")
        self.mainPanel.SetBackgroundColour("#000000")

    def _setupConsolePanel(self):
        self.consolePanel = wx.Window(self.hSplitter)
        self.console = logWin.ConsoleWin(self.consolePanel)
        self.console.log('console log output.')

    def _setupSplitter(self):
        self.hSplitter = wx.SplitterWindow(self)
        self.vSplitter = wx.SplitterWindow(self.hSplitter)

    def _setupWindow(self):
        self._setupSplitter()
        self._setupLeftPanel()
        self._setupMainPanel()
        self._setupConsolePanel()
        self.vSplitter.SplitVertically(self.leftPanel, self.mainPanel, 150)
        self.hSplitter.SplitHorizontally(self.vSplitter, self.consolePanel, 500)

    def _setupStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('statusbar already.')

    def _setupToolBar(self):
        self.toolbar = self.CreateToolBar()
        open = self.toolbar.AddLabelTool(wx.NewId(), 'hi', wx.Bitmap('../resource/icons/folder-26.png'))
        save = self.toolbar.AddLabelTool(wx.NewId(), 'hi', wx.Bitmap('../resource/icons/save-26.png'))
        self.toolbar.AddSeparator()
        play = self.toolbar.AddLabelTool(wx.NewId(), 'hi', wx.Bitmap('../resource/icons/play-26.png'))
        stop = self.toolbar.AddLabelTool(wx.NewId(), 'hi', wx.Bitmap('../resource/icons/pause-26.png'))
        restart = self.toolbar.AddLabelTool(wx.NewId(), 'hi', wx.Bitmap('../resource/icons/refresh-26.png'))
        slower = self.toolbar.AddLabelTool(wx.NewId(), 'hi', wx.Bitmap('../resource/icons/rewind-26.png'))
        faster = self.toolbar.AddLabelTool(wx.NewId(), 'hi', wx.Bitmap('../resource/icons/fast_forward-26.png'))
        self.toolbar.Realize()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None,title='Robot Arm Simulator', size=(800,600))
    app.MainLoop()