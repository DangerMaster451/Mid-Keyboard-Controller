import pygame.midi
from piano import Piano

class Midi():
    def __init__(self):
        pygame.midi.init()
        device_id = pygame.midi.get_default_input_id()
        self.midi_in = pygame.midi.Input(device_id)

    def check_midi(self, piano:Piano) -> None:
        if self.midi_in.poll():   
            events = self.midi_in.read(5)
            for event in events:
                e = MidiEvent(event)
                if e.event_type == 144:
                    for key in piano.piano_keys:
                        if key.midi_key == e.key_pressed:
                            piano.itemconfig(key.rect, fill="gray80")
                if e.event_type == 128:
                    for key in piano.piano_keys:
                        if key.midi_key == e.key_pressed:
                            piano.itemconfig(key.rect, fill=key.fill_color)

class MidiEvent():
    def __init__(self, event):
        self.event_type = event[0][0]
        self.key_pressed = event[0][1]
        self.velocity = event[0][2]