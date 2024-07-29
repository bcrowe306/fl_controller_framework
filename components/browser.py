from .component import Component
from fl_controller_framework.api.fl_browser import FLBrowser
from fl_controller_framework.controls.button import ButtonControl
from fl_controller_framework.controls.jog_control import JogControl


class BrowserComponent(Component):
    """
    Represents a browser component in the FL Studio controller framework.

    This component provides functionality for navigating and interacting with the FL Studio browser.

    Attributes:
        jog_browser_node_control (JogControl): The jog control for navigating browser nodes.
        select_node_control (ButtonControl): The button control for selecting a browser node.
        back_button (ButtonControl): The button control for navigating back in the browser.
        previous_tab_control (ButtonControl): The button control for navigating to the previous browser tab.
        next_tab_control (ButtonControl): The button control for navigating to the next browser tab.
        escape_control (ButtonControl): The button control for escaping from the current browser view.
        preview_node_control (ButtonControl): The button control for previewing a browser node.
        jog_tabs (JogControl): The jog control for navigating browser tabs.
    """
    def __init__(self, name: str = "BrowserComponent"):
        super(BrowserComponent, self).__init__(name=name)
        self.jog_browser_node_control: JogControl = None
        self.select_node_control: ButtonControl = None
        self.back_button: ButtonControl = None
        self.previous_tab_control: ButtonControl = None
        self.next_tab_control: ButtonControl = None
        self.escape_control: ButtonControl = None
        self.preview_node_control: ButtonControl = None
        self.jog_tabs: JogControl = None

    @Component.subscribe("back_button", ButtonControl.Events.PRESSED)
    def _on_back_button_pressed(self, pressed):
        (
            self.back_button.set_light("DEFAULT")
            if pressed
            else self.back_button.set_light("DEFAULT")
        )

    @Component.subscribe("back_button", ButtonControl.Events.TOGGLED)
    def _on_back_button_toggled(self, _):
        FLBrowser.back()

    @Component.subscribe("next_tab_control", ButtonControl.Events.PRESSED)
    def _on_next_tab_control_pressed(self, pressed):
        (
            self.next_tab_control.set_light("ON")
            if pressed
            else self.next_tab_control.set_light("DEFAULT")
        )

    @Component.subscribe("next_tab_control", ButtonControl.Events.TOGGLED)
    def _on_next_tab_control_toggled(self, _):
        tab_name: str = FLBrowser.nextBrowserTab()
        self.show_modal("BROWSER TAB", tab_name)

    @Component.subscribe("previous_tab_control", ButtonControl.Events.PRESSED)
    def _on_previous_tab_control_pressed(self, pressed):
        (
            self.previous_tab_control.set_light("ON")
            if pressed
            else self.previous_tab_control.set_light("DEFAULT")
        )

    @Component.subscribe("previous_tab_control", ButtonControl.Events.TOGGLED)
    def _on_previous_tab_control_toggled(self, _):
        tab_name: str = FLBrowser.prevBrowserTab()
        self.show_modal("BROWSER TAB", tab_name)

    @Component.subscribe("jog_tabs", "inc")
    def _on_jog_tabs_toggled(self, _):
        self._on_next_tab_control_toggled(True)

    @Component.subscribe("jog_tabs", "dec")
    def _on_jog_tabs_toggled(self, _):
        self._on_previous_tab_control_toggled(True)

    @Component.subscribe("preview_node_control", ButtonControl.Events.TOGGLED)
    def _on_preview_node_control_toggled(self, _):
        self.fl.ui.setFocused(self.fl.midi.widBrowser)
        self.fl.ui.previewBrowserMenuItem()

    @Component.subscribe("preview_node_control", ButtonControl.Events.PRESSED)
    def _on_preview_node_control_pressed(self, isPressed: bool):
        if isPressed:
            self.preview_node_control.set_light("ON")
        else:
            self.preview_node_control.set_light("DEFAULT")

    @Component.subscribe("escape_control", ButtonControl.Events.TOGGLED)
    def _on_escape_control_toggled(self, _):
        FLBrowser.escape()

    @Component.subscribe("select_node_control", ButtonControl.Events.TOGGLED)
    def _on_select_node_control_toggled(self, _):
        FLBrowser.selectNode()

    @Component.subscribe("jog_browser_node_control", "inc")
    def _on_jog_browser_node_control_inc(self, _):
        browser_item_name: str = FLBrowser.nextBrowserNode()
        self.show_modal("Browser", browser_item_name)

    @Component.subscribe("jog_browser_node_control", "dec")
    def _on_jog_browser_node_control_dec(self, _):
        browser_item_name: str = FLBrowser.prevBrowserNode()
        self.show_modal("Browser", browser_item_name)

    def activate(self):
        FLBrowser.focus()
        return super().activate()
