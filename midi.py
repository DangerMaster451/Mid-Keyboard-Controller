import pygame.midi

pygame.midi.init()

device_id = pygame.midi.get_default_input_id()
midi_in = pygame.midi.Input(device_id)
while True:
    events = midi_in.read(5)
    if events != []:
        print(events)
