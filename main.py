import tkinter as tk
import pygame.midi as midi

class Key():
    def __init__(self, canvas, x:int, width:int, height:int, fill_color:str, outline_color:str, midi_key:int):
        self.width = width
        self.height = height
        self.left_x = x
        self.left_y = 0
        self.right_x = x+self.width
        self.right_y = self.height
        self.canvas = canvas
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.rect:int
        self.midi_key = midi_key

    def on_enter(self, event):
        self.canvas.itemconfig(self.rect, fill="gray80")
    
    def on_leave(self, event):
        self.canvas.itemconfig(self.rect, fill=self.fill_color)

class Piano(tk.Canvas):
    def __init__(self, root:tk.Tk) -> None:
        self.total_keys = 37
        self.root = root
        self.key_width = 25
        self.width = self.getWidth()
        self.height = 150
        self.piano_keys:list[Key] = []
        super().__init__(self.root, width=self.width, height=self.height, bg="gray99")

        self.place_keys()

    def getWidth(self) -> int:
        return round((self.total_keys-2) * 0.63) * self.key_width + 4

    def place_keys(self) -> None:
        for i in range(self.total_keys):
            midi_key = i+48
            if len(self.piano_keys) == 0:
                key = Key(self, 2, self.key_width, self.height, "white", "black", midi_key)
            elif i % 12 in [1,3,6,8,10]:
                key = Key(self, self.piano_keys[i-1].right_x - round(self.key_width/2), self.key_width, round(self.height/2), "black", "white", midi_key)
            else:
                if self.piano_keys[i-1].fill_color == "black":
                    key = Key(self, self.piano_keys[i-2].right_x, self.key_width, self.height, "white", "black", midi_key)
                else:
                    key = Key(self, self.piano_keys[i-1].right_x, self.key_width, self.height, "white", "black", midi_key)
            self.piano_keys.append(key)

        for index, key in enumerate(self.piano_keys):
            if key.fill_color == "black":
                self.piano_keys.pop(index)
                self.piano_keys.append(key)

        for key in self.piano_keys:
            key.rect = self.create_rectangle(key.left_x, key.left_y, key.right_x, key.right_y, fill=key.fill_color, outline=key.outline_color)
            self.tag_bind(key.rect, "<Enter>", key.on_enter)
            self.tag_bind(key.rect, "<Leave>", key.on_leave)

class MidiEvent():
    def __init__(self, event):
        self.event_type = event[0][0]
        self.key_pressed = event[0][1]
        self.velocity = event[0][2]

root = tk.Tk()
piano = Piano(root)

root.title("MIDI Keyboard Controller")
root.geometry("1200x600")
root.config(bg="gray80")
root.resizable(False, False)

midi.init()
device_id = midi.get_default_input_id()
midi_in = midi.Input(device_id)

piano.pack(padx=0, pady=10, side=tk.BOTTOM)


def check_midi() -> None:
    if midi_in.poll():   
        events = midi_in.read(5)
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
    root.after(100,check_midi)

root.after(0, check_midi)

root.mainloop()
