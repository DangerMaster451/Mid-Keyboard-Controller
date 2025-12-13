import tkinter as tk
from piano import Piano
from midi import Midi, MidiEvent

root = tk.Tk()
piano = Piano(root)

midi = Midi()

root.title("MIDI Keyboard Controller")
root.geometry("1200x600")
root.config(bg="gray80")
root.resizable(False, False)

piano.pack(padx=0, pady=10, side=tk.BOTTOM)

def update():
    midi.check_midi(piano)
    root.after(100, update)

root.after(0, update)

root.mainloop()