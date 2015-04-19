import wx

class ElementTree:

    def __init__(self, parent):

        self.elementTree = wx.TreeCtrl(parent, -1, style=wx.TR_DEFAULT_STYLE)
        self.elementInfo = wx.Panel(parent, -1)
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.elementTree, 1, flag = wx.EXPAND)
        hBox.Add(self.elementInfo, 0, flag = wx.EXPAND)
        # hBox.SetMinSize(self.elementInfo, 100)
        parent.SetSizerAndFit(hBox)
        root = self.elementTree.AddRoot('Root item')

        for i in range(10):
            self.elementTree.AppendItem(root, 'Item %d'%(i+1))

        self.elementTree.ExpandAll()