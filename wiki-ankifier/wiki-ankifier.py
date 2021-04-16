#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Dennis Irrgang"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"

import re
import tkinter as tk
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.ankify_button = tk.Button(self)
        self.ankify_button["text"] = "Ankify!"
        self.ankify_button["command"] = self.ankify
        self.ankify_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.input_box = tk.Text()
        self.input_box.pack()

        self.output_box = tk.Text()
        self.output_box.pack()

    def ankify(self):
        """ Main entry point of the app """
        

        inputText = self.input_box.get("1.0", tk.END)

        imgRegex = re.compile('\\)<.*?>')
        mathJaxOpen = re.compile(re.escape('{\displaystyle'))
        mathJaxClose = re.compile(re.escape('}<'))

        test = re.sub(mathJaxOpen, '\({\\\\displaystyle', re.sub(mathJaxClose, '}\)<', inputText))

        removedImgs = re.sub(imgRegex, ")", test)

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert("1.0", removedImgs)



if __name__ == "__main__":
    """ This is executed when run from the command line """
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
