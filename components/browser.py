from .component import Component
from fl_controller_framework.api.fl_browser import FLBrowser
from fl_controller_framework.controls.button import ButtonControl
from fl_controller_framework.controls.jog_control import JogControl


class BrowserNavigationComponent(Component):
    def __init__(self, name: str = "BrowserNavigationComponent"):
        super(BrowserNavigationComponent, self).__init__(name=name)
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

    def show_modal(self, title: str, message: str):
        self.global_event_object.notify_listeners("screen_modal", title, message)
