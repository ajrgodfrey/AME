#!/usr/bin/env python3

"""
This module provides a very basic text editor and HTML reader 
so screen reader users can write and process markdown.
"""

# import base packages
import sys
import platform
import os
import codecs

# import third party packages
import markdown
import wx
from wx.html2 import WebView


class WebPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.browser = WebView.New(self)
        bsizer = wx.BoxSizer()
        bsizer.Add(self.browser, 1, wx.EXPAND)
        self.SetSizerAndFit(bsizer)


class MdPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        bsizer = wx.BoxSizer()
        bsizer.Add(self.control, 1, wx.EXPAND)
        self.SetSizerAndFit(bsizer)


class Window(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1920, 1080))
        self.dirname = ""
        self.filename = ""
        self.edited = False
        self.CreateStatusBar()
        fileMenu = wx.Menu()
        newMenu = fileMenu.Append(wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.onNew, newMenu)
        openMenu = fileMenu.Append(wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.onOpen, openMenu)
        importMenu = fileMenu.Append(wx.ID_ANY, "&Import other filetype\tCTRL+SHIFT+O")
        self.Bind(wx.EVT_MENU, self.onImport, importMenu)
        saveMenu = fileMenu.Append(wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.onSave, saveMenu)
        saveAsMenu = fileMenu.Append(wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.onSaveAs, saveAsMenu)
        exportMenu = fileMenu.Append(wx.ID_ANY, "&Export\tCTRL+E")
        self.Bind(wx.EVT_MENU, self.onExport, exportMenu)
        clipboardMenu = fileMenu.Append(
            wx.ID_ANY, "&Copy HTML to Clipboard\tCTRL+SHIFT+C"
        )
        self.Bind(wx.EVT_MENU, self.onClipboard, clipboardMenu)
        exitMenu = fileMenu.Append(wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnExit, exitMenu)
        viewMenu = wx.Menu()
        htmlMenu = viewMenu.Append(wx.ID_ANY, "&HTML\tCTRL+2")
        self.Bind(wx.EVT_MENU, self.onViewHtml, htmlMenu)
        markdownMenu = viewMenu.Append(wx.ID_ANY, "&Markdown\tCTRL+1")
        self.Bind(wx.EVT_MENU, self.onViewMarkdown, markdownMenu)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(viewMenu, "&View")
        self.SetMenuBar(menuBar)
        self.nb = wx.Notebook(self)
        self.mdPanel = MdPanel(self.nb)
        self.Bind(wx.EVT_TEXT, self.onEdited, self.mdPanel.control)
        self.nb.AddPage(self.mdPanel, "MarkDown")
        self.WebPanel = WebPanel(self.nb)
        self.nb.AddPage(self.WebPanel, "HTML")
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookChanged, self.nb)
        self.Bind(wx.EVT_CLOSE, self.onClose, self)
        bsizer = wx.BoxSizer()
        bsizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizerAndFit(bsizer)
        self.Show(True)
        self.Maximize(True)
        self.SetTitle("Untitled | Markdown Editor")
        if len(sys.argv) > 1:
            self.dirname = os.path.dirname(sys.argv[1])
            self.filename = os.path.basename(sys.argv[1])
            self.open()

    def open(self):
        f = open(os.path.join(self.dirname, self.filename), "r")
        self.mdPanel.control.ChangeValue(f.read())
        f.close()
        self.edited = False
        self.SetTitle(self.filename + " | Markdown Editor")
        self.nb.SetSelection(0)

    def shouldSave(self):
        dlg = wx.MessageDialog(
            None,
            "Recent change has not been saved.",
            "Save?",
            wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION,
        )
        dlg.SetYesNoLabels("Save", "Discard")
        res = dlg.ShowModal()
        if res == wx.ID_YES:
            if self.onSave(None) == wx.ID_CANCEL:
                return wx.ID_CANCEL
        return res


    def onOpen(self, e):
        if self.edited:
            if self.shouldSave() == wx.ID_CANCEL:
                return
        with wx.FileDialog(
            self,
            "Open",
            self.dirname,
            "",
            "*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.open()

    def onImport(self, e):
        if self.edited:
            if self.shouldSave() == wx.ID_CANCEL:
                return
        with wx.FileDialog(
            self,
            "Open",
            self.dirname,
            "",
            "*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.open()

    def onNew(self, e):
        if self.edited:
            if self.shouldSave() == wx.ID_CANCEL:
                return
        self.WebPanel.browser.SetPage("", "")
        self.mdPanel.control.SetValue("")
        self.edited = False
        self.nb.SetSelection(0)
        self.SetTitle("Untitled | Markdown Editor")

    def save(self):
        file = os.path.join(self.dirname, self.filename)
        output_file = codecs.open(file, "w", encoding="utf-8", errors="replace")
        content = self.mdPanel.control.GetValue()
        output_file.write(content)
        self.edited = False

    def onSave(self, e):
        if self.filename == "":
            return self.onSaveAs(e)
        else:
            self.save()

    def onSaveAs(self, e):
        with wx.FileDialog(
            self,
            "Save",
            self.dirname,
            "",
            "*.md",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return wx.ID_CANCEL
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.save()
            self.SetTitle(self.filename + " | Markdown Editor")

    def onExport(self, e):
        self.convert()
        with wx.FileDialog(
            self,
            "Export HTML",
            self.dirname,
            "",
            "*.html",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            file = os.path.join(dirname, filename)
            output_file = codecs.open(
                file, "w", encoding="utf-8", errors="xmlcharrefreplace"
            )
            htmlText = markdown.markdown(
                self.mdPanel.control.GetValue(), extensions=["extra"]
            )
            htmlOutput = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title></title>
</head>
<body>
{htmlText}
</body>
</html>
"""
            output_file.write(htmlOutput)

    def onClipboard(self, e):
        self.convert()
        htmlText = markdown.markdown(
            self.mdPanel.control.GetValue(), extensions=["extra"]
        )
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(htmlText))
            wx.TheClipboard.Close()

    def OnExit(self, e):
        if self.edited:
            if self.shouldSave() == wx.ID_CANCEL:
                return
        self.Close(True)

    def onClose(self, event):
        if event.CanVeto() and self.edited:
            if self.shouldSave() == wx.ID_CANCEL:
                event.Veto()
                return
        self.Destroy()

    def onEdited(self, e):
        self.edited = True

    def onViewHtml(self, e):
        self.nb.SetSelection(1)

    def onViewMarkdown(self, e):
        self.nb.SetSelection(0)

    def focus(self, focus):
        focus.SetFocus()
        if platform.system() == "Windows":
            robot = wx.UIActionSimulator()
            position = focus.GetPosition()
            position = focus.ClientToScreen(position)
            robot.MouseMove(position)
            robot.MouseClick()

    def OnNotebookChanged(self, e):
        focus = None
        if e.GetSelection() == 0:
            focus = self.mdPanel.control
        else:
            focus = self.WebPanel.browser
            self.convert()
        self.focus(focus)

    def convert(self):
        htmlText = markdown.markdown(
            self.mdPanel.control.GetValue(), extensions=["extra"]
        )
        self.WebPanel.browser.SetPage(htmlText, "")


app = wx.App(False)
frame = Window(None, title="Markdown Editor")
app.MainLoop()
