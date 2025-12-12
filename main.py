import tkinter as tk

class Key():
    def __init__(self, canvas, x:int, width:int, height:int, fill_color:str, outline_color:str):
        self.width = width
        self.height = height
        self.left_x = x
        self.left_y = 0
        self.right_x = x+self.width
        self.right_y = self.height
        self.canvas = canvas
        self.fill_color = fill_color
        self.outline_color = outline_color

class Piano(tk.Canvas):
    def __init__(self, root:tk.Tk) -> None:
        self.total_keys = 37
        self.root = root
        self.key_width = 25
        self.width = self.getWidth()
        self.height = 150
        super().__init__(self.root, width=self.width, height=self.height, bg="gray99")

        self.place_keys()

    def getWidth(self) -> int:
        return round((self.total_keys-2) * 0.63) * self.key_width + 4


    def place_keys(self) -> None:
        keys:list[Key] = []

        for i in range(self.total_keys):
            if len(keys) == 0:
                key = Key(self, 2, self.key_width, self.height, "white", "black")
            elif i % 12 in [1,3,6,8,10]:
                key = Key(self, keys[i-1].right_x - round(self.key_width/2), self.key_width, round(self.height/2), "black", "white")
            else:
                if keys[i-1].fill_color == "black":
                    key = Key(self, keys[i-2].right_x, self.key_width, self.height, "white", "black")
                else:
                    key = Key(self, keys[i-1].right_x, self.key_width, self.height, "white", "black")
            keys.append(key)

        for index, key in enumerate(keys):
            if key.fill_color == "black":
                keys.pop(index)
                keys.append(key)

        for key in keys:
            self.create_rectangle(key.left_x, key.left_y, key.right_x, key.right_y, fill=key.fill_color, outline=key.outline_color)


root = tk.Tk()
piano = Piano(root)

root.title("MIDI Keyboard Controller")
root.geometry("1200x600")
root.config(bg="gray80")
root.resizable(False, False)

piano.pack(padx=0, pady=10, side=tk.BOTTOM)

root.mainloop()