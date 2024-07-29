# FL Studio Controller Framework
Framework to implement a MIDI controller in FL Studio using Python. It provides sets of classes and data structures that make the process simple to implement complex functionality from your MIDI controller.

## The Why?
Why create a framework, when Image line has already provided a Python API to Fl Studio? In my work of implementing more complex control surfaces such as Ableton Push2, MPC Studio Mk2, I realized that provided Fl Studio Python API left a lot to be desired. To make the most out these larger more complex controllers, you need to mimic UI design patterns used in other areas of technology to accomplish this in a way that is flexible, extensible, repeatable and easy to maintain.

Sifting through other examples of controllers implemented using the FL Studio Python API only, left me overwhelmed by the thousands of lines, single file, Python scripts. While they may provide the functionality needed for the moment, they are extremely hard to maintain, error prone, and difficult to reason about.

This framework is an attempt to answer that issue and make implementing controllers "easier". To do this, I decided to code the framework, as I implemented the MPC Studio Mk2. This gave me the opportunity to see where code was duplicated, and generalize the code to be used in the framework, no matter what controller is being implemented. The goal here is to provide functionality in a vendor/model agnostic way.

## The How
In have implemented many different MIDI Controllers in many different DAWs, and I've come to the conclusion that "they're all basically doing the same thing". It boils down to one design pattern... The observer pattern... All DAWs, and Midi controller manufactures are pretty much accomplishing the same thing.

The Observer pattern is a publish, subscribe method, where a message is published, and other entities can subscribe to the message and act on it. This is the meat and potatoes of what is happening in this framework. The MIDI controller is sending Midi msgs. We want to subscribe to those messages and perform some actions when they come. Also FL studio is publishing it's own message, we want to subscribe to those, and perform the desired actions. 

Using the Obersever pattern, combined with the State pattern, I've made a framework that abstracts away the implementation details, and allows you to define your controller in a more logical way.

### Overview:
Here is the basic structure of the framework.

##### Control Surface
It all starts with a [ControlSurface](https://bcrowe306.github.io/fl_controller_framework/fl_controller_framework.control_surface.ControlSurface.html). A ControlSurface represents your controller as a whole. The control surface has different Components on it. The Control Surface is also the first oject passed into the API, and interfaces with FL Studio's callback methods:

#### Component
A [Component](https://bcrowe306.github.io/fl_controller_framework/fl_controller_framework.components.component.Component.html) represents a grouping of functionality. Think of a Transport. The transport normally has multiple controls associated with it, but its normally grouped together in one section. You could define this as a TransportComponent. Components can be activated/deactivated. When they're activated/deactivate every control thats attached to them is activated/deactivated.

#### Control
A Component can have many [Controls](https://bcrowe306.github.io/fl_controller_framework/fl_controller_framework.controls.control.Control.html). A Control may represent the Buttons that make up the transport... PlayButton, RecordButton, StopButton, etc... [Buttons](https://bcrowe306.github.io/fl_controller_framework/fl_controller_framework.controls.button.ButtonControl.html) may not be the only type of control that exists on a Transport Component. You could have a Jog Wheel as part of the transport. It would be represented as a JogControl. All these controls would then make up your component...

Example:
```
ControlSurface:
    TransportComponent:
        PlayButton:
        StopButton:
        RecordButton:
        JogWheel:
```
Controls generate events that you can then use to implement whatever functionality you need. Most Midi controllers have the same type of common controls; Buttons, Pads, Faders, Knobs, Encoders, Jog Wheels, and Touch Strips. These are very common on Midi controllers, and each of these controls are already defined in the framework. This means all you need to do is define your control, add it to a component, and subscribe to it's events to implement any functionality you want. 

Control are automatically activated and deactivate when a component is activated/deactivated. This makes it trivial to implement multiple levels of functionality on the same Control.

#### Modes.
This brings us to the concept of [Modes](https://bcrowe306.github.io/fl_controller_framework/fl_controller_framework.components.modes.ModesComponent.html). Where this framework really shines is it's ability to easily and predictably implement modes. You may have times where you want the same set of controls to do something completely different, depending on the context. For example. You may want your jog wheel to adjust volume while the mixer panel is open, but when your in the channel rack view, you may want the same know to scroll through the different channels. You can do this with Modes.

Modes is a special type of component that enables you to group components together in different Modes. You get to define what they modes are, and how/when they are switched to a different mode. Modes can be switched by using a Control, or modes can be switched by responding to an event from the Host Application(Fl Studio).

Normally this kind of functionality is difficult to implement, but with this framework, it becomes trivial and common.

#### Conclusion
Using these building blocks, I was able to fully implement the MPC Studio Mk2, using all it's features to work with FL Studio. The beauty of this framework though is that it's not defined for one device but it will work with any controller that implements basic midi.

## Getting Started
The best place to get started is by using the [examples](https://github.com/bcrowe306/fl_controller_framework/tree/main/examples) folder. There is a whole project starter template that you can copy/paste and modify to your liking. There are also examples on how to define Controls. How to create your own Controls, Components, Skins. etc. There's also examples on how to send Sysex messages, and talk back to your controller.

The next place to go is the [FL Studio Framework Documentation](https://bcrowe306.github.io/fl_controller_framework/) . Much effort was made in documenting this framework. It's a work in progress, but I believe a well documented project will encourage adoption among developers. Examples are also necessary for a more thorough understanding. 

It is my plan to release a youtube series on implementing a controller in FL Studio using this framework. Stay tuned.
