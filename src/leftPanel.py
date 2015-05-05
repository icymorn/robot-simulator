# -*- coding: utf-8 -*-
import wx
from loader import config

class ElementTree:
    instance = None

    def __init__(self, parent):
        if ElementTree.instance is None:
            ElementTree.instance = self

        self.elementTree = wx.TreeCtrl(parent, -1, style=wx.TR_DEFAULT_STYLE)
        self.elementInfo = wx.Panel(parent, -1)
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        hBox.Add(self.elementTree, 1, flag = wx.EXPAND)
        hBox.Add(self.elementInfo, 0, flag = wx.EXPAND)
        # hBox.SetMinSize(self.elementInfo, 100)
        parent.SetSizerAndFit(hBox)
        root = self.elementTree.AddRoot('Root item')

        itemArray = []
        for i in config.joint:
            itemArray.append(self.elementTree.AppendItem(root, 'd:{0:.2f} T:{0:.2f} r:{0:.2f} A:{0:.2f}'.format(i.d, i.theta, i.r, i.alpha)))

        self.items = itemArray

        self.elementTree.ExpandAll()