from framework.component import Component
from framework.control import ControlBase
from framework.controls.button import ButtonControl
from mpc_studio_mk2.controls import Controls


class TransportComponent(Component):
    """This Component hold basic transport functionality. Instantiate this with your own ButtonControls as arguments."""
    def __init__(self, 
                 play_button: ButtonControl = None,
                 loop_recording: ButtonControl = None,
                 stop_button: ButtonControl = None,
                 record_button: ButtonControl = None,
                 overdub_button: ButtonControl = None,
                 seek_forward_button: ButtonControl = None,
                 seek_back_button: ButtonControl = None,
                 locate_button: ButtonControl = None,
                 tap_tempo_button: ButtonControl = None,
                 undo_button: ButtonControl = None,
                 shift_button: ButtonControl = None,
                 undo_shift_button: ButtonControl = None,
                 metronome_button: ButtonControl = None,
                 song_mode_button: ButtonControl = None,
                 quantize_button: ButtonControl = None,
                 beat_color_map: dict[int, str] = {
                     0:"OFF",
                     1: "BRIGHT",
                     2: "BRIGHT"
                 },
                 *a, **k):
        super(TransportComponent, self).__init__(
            name='TransportComponent', *a, **k)
        self.play_button: ButtonControl = play_button
        self.loop_recording: ButtonControl = loop_recording
        self.stop_button: ButtonControl = stop_button
        self.record_button: ButtonControl = record_button
        self.overdub_button: ButtonControl = overdub_button
        self.seek_forward_button: ButtonControl = seek_forward_button
        self.seek_back_button: ButtonControl = seek_back_button
        self.locate_button: ButtonControl = locate_button
        self.tap_tempo_button: ButtonControl = tap_tempo_button
        self.undo_button: ButtonControl = undo_button
        self.shift_button: ButtonControl = shift_button
        self.undo_shift_button: ButtonControl = undo_shift_button
        self.metronome_button: ButtonControl = metronome_button
        self.song_mode_button: ButtonControl = song_mode_button
        self.quantize_button: ButtonControl = quantize_button
        self.quantize_button: ButtonControl = quantize_button
        self.beat_color_map: ButtonControl = beat_color_map
        """This is a dictionary of skin color for each beat that FL Studio sends. When playing, FL Studio sends beats as integers, 0, 1, 2"""

    def change_song_position(self, direction: bool):
        delta = .1
        current_pos = self.fl.transport.getSongPos()
        new_pos = current_pos + delta if direction else current_pos - delta 
        self.fl.transport.setSongPos(new_pos)
   
    @Component.subscribe('quantize_button', 'pressed')
    def _on_quantize_button_pressed(self, pressed):
        if pressed:
            self.fl.channels.quickQuantize(self.fl.channels.selectedChannel())
            self.quantize_button.set_light("BRIGHT")
        else:
            self.quantize_button.set_light("DEFAULT")

    @Component.listens('ui.isLoopRecEnabled')
    def _on_isLoopRecEnabled(self, isLoopRecEnabled):
        self.loop_recording.set_light('BRIGHT') if isLoopRecEnabled == 1 else self.loop_recording.set_light('DEFAULT')

    @Component.subscribe('loop_recording', 'toggled')
    def _on_loop_recording_toggled(self, _):
        self.fl.transport.globalTransport(self.fl.midi.FPT_LoopRecord, 1)

    @Component.subscribe('song_mode_button', 'toggled')
    def _on_song_mode_button_toggled(self, _):
        self.fl.transport.setLoopMode()

    @Component.listens('transport.getLoopMode')
    def _on_loop_mode(self, loop_mode):
        if loop_mode == 1:
            self.song_mode_button.set_light('BRIGHT_2')
        else:
            self.song_mode_button.set_light('BRIGHT_1')
    @Component.subscribe('metronome_button', 'toggled')
    def _on_metronome_button_toggled(self, _):
        self.fl.transport.globalTransport(110, 2)

    @Component.listens('ui.isMetronomeEnabled')
    def _set_metronome_button(self, metronome_enabled):
        if metronome_enabled:
            self.metronome_button.set_light('BRIGHT_1')
        else:
            self.metronome_button.set_light('DEFAULT_1')

    @Component.subscribe('shift_button', 'pressed')
    def _on_shift_button_pressed(self, pressed: bool):
        if pressed:
            self.shift_button.set_light("BRIGHT_1")
        else:
            self.shift_button.set_light("DEFAULT")
            
    @Component.subscribe('undo_shift_button', 'pressed')
    def _on_undo_shift_button_pressed(self, pressed):
        self.fl.general.undoDown()

    @Component.subscribe('undo_button', 'pressed')
    def _on_undo_button_pressed(self, pressed):
        if pressed:
            self.fl.general.undoUp()
            self.undo_button.set_light('BRIGHT_1')
        else:
            self.undo_button.set_light('DEFAULT_1')

    @Component.subscribe('tap_tempo_button', 'pressed')
    def _on_tap_tempo_button_pressed(self, pressed):
        if pressed:
            self.fl.transport.globalTransport(106,1)
            self.tap_tempo_button.set_light('BRIGHT_1')
        else:
            self.tap_tempo_button.set_light('Default')

    @Component.listens('beat')
    def _on_beat(self, beat):
        self.play_button.set_light(self.beat_color_map[beat])
        
    @Component.subscribe('locate_button', 'pressed')
    def _on_locate_button_pressed(self, pressed):
        if pressed:
            self.locate_button.set_light('BRIGHT')
            self.fl.transport.setSongPos(0.0)
        else:
            self.locate_button.set_light('DEFAULT')

    @Component.subscribe('seek_forward_button', 'pressed')
    def _on_seek_forward_button_pressed(self, pressed):
        if pressed:
            self.seek_forward_button.set_light('BRIGHT')
            self.change_song_position(True)
        else:
            self.seek_forward_button.set_light('DEFAULT')

    @Component.subscribe('seek_back_button', 'pressed')
    def _on_seek_back_button_pressed(self, pressed):
        if pressed:
            self.seek_back_button.set_light('BRIGHT')
            self.change_song_position(False)
        else:
            self.seek_back_button.set_light('DEFAULT')     

    @Component.subscribe('overdub_button', 'pressed')
    def _on_overdub_button_pressed(self, pressed):
        if pressed:
            value = self.fl.transport.globalTransport(112, 2)

    @Component.subscribe('play_button', 'pressed')
    def _on_play_pressed(self, pressed):
        if pressed:
            self.fl.transport.start()

    @Component.subscribe('stop_button', 'pressed')
    def _on_stop_pressed(self, _):
        self.fl.transport.stop()

    @Component.subscribe('record_button', 'pressed')
    def _on_record_button_pressed(self, pressed):
        if pressed:
            self.fl.transport.record()

    @Component.listens('transport.isRecording')
    def _on_isRecording(self, isRecording):
        if isRecording == 1:
            self.record_button.set_light('BRIGHT')
        else:
            self.record_button.set_light('DEFAULT')

    @Component.listens('transport.isPlaying')
    def on_isPlaying(self, isPlaying):
        if isPlaying == 0:
            self.play_button.set_light('DEFAULT')
            self.stop_button.set_light('BRIGHT')
        else:
            self.play_button.set_light('BRIGHT')
            self.stop_button.set_light('DEFAULT')
