
# created by anan, 2006-11-25
# TODO

import wx
import time
import wx.lib.anchors as anchors

from cardinfo import *
from cardinfolib import *

app = None
lib = None

def load_lib():
    global lib
    if lib is None:
        lib = CardInfoLib()
        lib.load()

class ListWindow(wx.Window):
    def __init__(self, parent, ID, title):
        wx.Window.__init__(self, parent, ID)
        self.p = parent
        #self.panel = wx.Panel (self, -1)
        
        load_lib()
        
        self.create_controls()
        
    def create_controls(self):
        #self.panel.SetAutoLayout(True)
        
        list = self.list = wx.ListCtrl (self, -1, size=wx.DefaultSize, style=wx.LC_REPORT)
        self.populate_list()
        
        #list.SetConstraints( anchors.LayoutAnchors(list, False, False, True, True))
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        
        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
#        sizer.Add (list, 0, wx.ALL, 2)
        
#        self.panel.SetSizerAndFit (sizer)
        #self.SetClientSize (self.panel.GetSize())
        
    def populate_list(self):
        self.list.InsertColumn (0, "id")
        self.list.InsertColumn (1, "name")
        self.list.InsertColumn (2, "image")
        
        self.populate_list_items()
        
        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        
    def populate_list_items(self):
        for key, data in lib.lib.items():
            self.insert_item (str(key), data.name, data.image, key)
            #temp = wx.ListItem()
            #temp.SetText(str(key))
            #index = self.list.InsertItem (temp)
            #self.list.SetStringItem (index, 1, data.name)
            #self.list.SetItemData (index, key)
        
        
    def update_list(self):
        self.list.DeleteAllItems()
        self.populate_list_items()
        
    def insert_item(self, text1, text2, text3, item_data=None):
        temp = wx.ListItem()
        temp.SetText(text1)
        index = self.list.InsertItem(temp)
        self.list.SetStringItem (index, 1, text2)
        self.list.SetStringItem (index, 2, text3)
        if item_data is not None: self.list.SetItemData (index, item_data)
        
    def OnSize(self, event):
        #w, h = self.GetClientSizeTuple()
        w, h = event.GetSize()
        self.list.SetDimensions (0, 0, w, h)
        
    def OnDoubleClick(self, event):
        #text = self.list.GetItem(self.list.GetFirstSelected(), 1).GetText()
        #self.insert_item("OnDoubleClick", text)
        
        dlg = ModifyDialog(self, -1, "Modify", self.list.GetItem(self.list.GetFirstSelected()).GetData())
        dlg.ShowModal()
        dlg.Destroy()
        self.update_list()
    
    def OnItemDelete(self, event):
        self.insert_item("OnItemDelete", "")

class AddWindow(wx.Window):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER):
        wx.Window.__init__(self, parent, ID)
        self.panel = wx.Panel (self, -1)
        
        load_lib()
        
        self.create_controls()
        self.new_card()
        
    def create_controls(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        gbs = self.gbs = wx.GridBagSizer(4,2)
        gbs.SetHGap (10)
        gbs.SetVGap (5)
        
        st = wx.StaticText (self.panel, -1, 'id:')
        gbs.Add (st, (0,0), flag=wx.ALIGN_RIGHT)
        self.st_id = wx.StaticText (self.panel, -1, '')
        gbs.Add (self.st_id, (0,1))
        
        st = wx.StaticText (self.panel, -1, 'Name:')
        gbs.Add (st, (1,0), flag=wx.ALIGN_RIGHT)
        tc = self.card_name = wx.TextCtrl (self.panel, -1, 'test')
        gbs.Add (tc, (1,1))
        
        st = wx.StaticText (self.panel, -1, 'Image:')
        gbs.Add (st, (2,0), flag=wx.ALIGN_RIGHT)
        tc = self.card_image = wx.TextCtrl (self.panel, -1, 'card001.jpg')
        gbs.Add (tc, (2,1))
        
        btn = wx.Button (self.panel, -1, "Add")
        btn.SetDefault()
        gbs.Add (btn, (3,0), (1,2), wx.ALIGN_CENTER|wx.ALL, 5)
        self.Bind (wx.EVT_BUTTON, self.OnAdd, btn)
        
        sizer.Add (gbs, 0, wx.ALL, 10)
        
        self.panel.SetSizerAndFit(sizer)
        self.SetClientSize(self.panel.GetSize())
        
    def OnAdd(self, event):
        card = CardInfo()
        card.id = self.card_id
        card.name = self.card_name.GetValue()
        card.image = self.card_image.GetValue()
        lib.add (card)
        lib.save()
        self.new_card()
        
    def new_card(self):
        self.card_id = lib.new_id()
        self.st_id.SetLabel (str(self.card_id))
        self.card_name.SetValue('')

class MyFrame(wx.Frame):
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        
        load_lib()
        self.card_id = lib.new_id()
        
        self.create_controls()
        
    def OnCloseWindow(self):
        self.Destroy()
        app.ProcessIdle()
        app.Exit()
        
    def create_controls(self):
        nb = self.nb = wx.Notebook(self, -1, size=(0,0),pos=(0,0),style=wx.NB_FIXEDWIDTH)
        
        self.page_list_win = self.addPanelPage (nb, ListWindow, "LIST")
        self.addPanelPage (nb, AddWindow, "ADD")
        
        nb.Bind (wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.SetClientSize ((300,400))
        
    def addPanelPage (self, nb, win_class, title):
        p = wx.Panel (nb, -1, size=wx.DefaultSize)
        win = win_class(p, -1, title)
        p.win = win
        p.SetSize (nb.GetSize())
        
        def OnCPSize(evt, win=win):
            win.SetSize (evt.GetSize())
            
        p.Bind (wx.EVT_SIZE, OnCPSize)
        nb.AddPage(p, title)
        return win
    
    def OnPageChanged(self, event):
        if event.GetSelection() == 0:
            self.page_list_win.update_list()
        event.Skip()

class MyApp(wx.App):
    def OnInit(self):
        win = MyFrame(None, -1, "OurGathering Library Maker")
        win.Show(True)
        self.SetTopWindow(win)
        
        global app
        app = self
        
        return True

if __name__ == '__main__':
    MyApp(False).MainLoop()