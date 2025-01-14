import tkinter as tk
from Functions import VideoPlayer

root = tk.Tk()
root.title("Cinefy")
player = VideoPlayer(root)
root.mainloop()