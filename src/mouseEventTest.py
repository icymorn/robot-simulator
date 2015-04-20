import wx
class myFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetBackgroundColour('Black')
        
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseRightUp)
        self.Bind(wx.EVT_LEFT_DCLICK , self.OnMouseLeftDClick)
        self.Bind(wx.EVT_RIGHT_DCLICK , self.OnMouseRightDClick)
        self.Bind(wx.EVT_MOTION , self.OnMouseMove) 

        self.Bind(wx.EVT_MOTION , self.OnMouseMove) 
        self.Bind(wx.EVT_MOTION , self.OnMouseMove) 

        self.Bind(wx.EVT_ENTER_WINDOW , self.OnMouseEnter) 
        self.Bind(wx.EVT_LEAVE_WINDOW , self.OnMouseLeave)
        self.Bind(wx.EVT_MOUSEWHEEL , self.OnMouseWheel)
 
    def OnMouseMove(self, event):
        pos = event.GetPosition()
        self.SetTitle( 'OnMouseMove' + str(pos))
    def OnMouseLeftDown(self, event):
        pos = event.GetPosition()
        self.SetTitle( 'OnMouseLeftDown' + str(pos))
    def OnMouseRightDown(self, event):
        pos = event.GetPosition()
        self.SetTitle( 'OnMouseRightDown' + str(pos))
    def OnMouseLeftUp(self, event):
        pos = event.GetPosition()
        self.SetTitle( 'OnMouseLeftUp' + str(pos))
    def OnMouseRightUp(self, event):
        pos = event.GetPosition()
        self.SetTitle( 'OnMouseRightUp' + str(pos))
    def OnMouseLeftDClick(self, event):
        pos = event.GetPosition()
        self.deviceContext.SetPen(wx.Pen(wx.WHITE, 8))
        self.deviceContext.DrawCircle(pos[0],pos[1], 2)
    def OnMouseRightDClick(self, event):
        pos = event.GetPosition()
        self.deviceContext.SetPen(wx.Pen(wx.RED, 8))        
        self.deviceContext.DrawCircle(pos[0],pos[1], 2)
    def OnMouseWheel(self, event):
        pos = event.GetWheelRotation()

        print 'OnMouseWheel' + str(pos)                 
    def OnMouseEnter(self, event):
        pos = event.GetPosition()
        print 'OnMouseEnter' + str(pos)
    def OnMouseLeave(self, event):
        pos = event.GetPosition()
        print 'OnMouseLeave' + str(pos)          
    def OnPaint(self, event=None):
        self.deviceContext = wx.PaintDC(self)
        self.deviceContext.Clear()

app = wx.App(False)
frame = myFrame(None, "MouseEvents")
frame.Show()
app.MainLoop()