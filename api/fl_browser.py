import ui, transport

PME_System = 1 << 1
PME_System_Safe = 1 << 2
PME_PreviewNote = 1 << 3
PME_FromHost = 1 << 4
PME_FromMIDI = 1 << 5
PME_FromScript = 1 << 6

FPT_Escape = 81
FPT_Left = 42
FPT_Right = 43

class FLBrowser:
    widBrowser = 4

    @staticmethod
    def focus():
        visibleWindow = ui.getVisible(FLBrowser.widBrowser)
        focusedWindow = ui.getFocused(FLBrowser.widBrowser)
        if visibleWindow != 1:
            ui.showWindow(FLBrowser.widBrowser)
        if focusedWindow !=1:
            ui.setFocused(FLBrowser.widBrowser)

    @staticmethod
    def selectNode():
        FLBrowser.focus()
        nodeFileType = ui.getFocusedNodeFileType()
        if nodeFileType == -1:
            return
        elif nodeFileType == -100:
            ui.setFocused(FLBrowser.widBrowser)
            ui.toggleBrowserNode()
            # ui.enter()
            # self.fl.transport.globalTransport(
            #     80, 80, self.fl.midi.PME_System)

        elif ui.isInPopupMenu() == 1:
            ui.enter()
        else:
            ui.setFocused(FLBrowser.widBrowser)
            ui.selectBrowserMenuItem()

    @staticmethod
    def escape():
        FLBrowser.focus()
        transport.globalTransport(FPT_Escape, 1, PME_System | PME_FromMIDI)

    @staticmethod
    def nextBrowserNode(preview: bool = True) -> str:
        return FLBrowser.jogBrowserNode(1, preview)

    @staticmethod
    def prevBrowserNode(preview: bool = True) -> str:
        return FLBrowser.jogBrowserNode(-1, preview)

    @staticmethod
    def jogBrowserNode(direction: int, preview: bool = True) -> str:
        FLBrowser.focus()
        ui.jog(direction)
        browser_item_name: str = ui.getFocusedNodeCaption()
        if preview and not ui.isInPopupMenu():
            ui.previewBrowserMenuItem()
        return browser_item_name

    @staticmethod
    def nextBrowserTab() -> str:
        FLBrowser.focus()
        tab_name: str = ui.navigateBrowserTabs(FPT_Left)
        return tab_name

    @staticmethod
    def prevBrowserTab() -> str:
        FLBrowser.focus()
        tab_name: str = ui.navigateBrowserTabs(FPT_Right)
        return tab_name

    @staticmethod
    def jogBrowserTab(direction: int) -> str:
        tab_name: str
        if direction > 0:
            tab_name: str = FLBrowser.nextBrowserTab()
        elif direction < 0:
            tab_name: str = FLBrowser.prevBrowserTab()
        else:
            tab_name: str = ui.getFocusedNodeCaption()
        return tab_name

    @staticmethod
    def back():
        if ui.isInPopupMenu() == 1:
            transport.globalTransport(FPT_Escape, 1, PME_System | PME_FromMIDI)
        else:
            transport.globalTransport(FPT_Left, 1, PME_System | PME_FromMIDI )
