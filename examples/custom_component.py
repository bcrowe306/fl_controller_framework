from fl_controller_framework.components.component import Component
from fl_controller_framework.controls.button import ButtonControl
from fl_controller_framework.api.fl_class import eve

# Create a custom component that extends the base component class
class CustomComponent(Component):
    def __init__(self, name: str, auto_active: bool = True, *a, **k):

        # Call the parent class constructor
        super().__init__(name, auto_active, *a, **k)

        # Create any custom attributes
        self.selected_channel_index = 0

        # Attach Controls to the component. 
        # It is recommended to define and instantiate your controls elsewhere in code, so they can be reused.
        self.play_button = ButtonControl("play_button", 0, 45)
        self.stop_button = ButtonControl("stop_button", 0, 90)


    # Subscribing to the buttoncontrol events
    @Component.subscribe("play_button", "pressed")
    def on_play_button_pressed(self, isPressed:bool):
        if isPressed:
            # Set the light when playbutton is pressed
            self.play_button.set_light("On")

    # Listen to FL Studio events too!
    @Component.subscribe("channels.selectedChannel")
    def on_selected_channel_changed(self, channel_index:int):
        self.selected_channel_index = channel_index
        print(f"Selected channel index changed to {channel_index}")

    