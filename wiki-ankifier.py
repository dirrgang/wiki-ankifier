#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Dennis Irrgang"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"

import re
import tkinter as tk
import pyperclip
from markdownify import markdownify as md


class Application(tk.Frame):
    def __init__(self, master: tk):
        super().__init__(master)
        self.master = master

        self.create_widgets()

    def create_widgets(self) -> None:
        self.frameButtons = tk.Frame()
        self.frameButtons.pack(fill=tk.X, ipadx=40, ipady=10, padx=10, pady=10)

        self.ankify_button = tk.Button(master=self.frameButtons)
        self.ankify_button["text"] = "Ankify!"
        self.ankify_button["command"] = self.ankify
        self.ankify_button.pack(side=tk.LEFT, ipadx=5, ipady=5)

        self.obsidianfy_button = tk.Button(master=self.frameButtons)
        self.obsidianfy_button["text"] = "Obsidianfy!"
        self.obsidianfy_button["command"] = self.obsidianfy
        self.obsidianfy_button.pack(side=tk.RIGHT, ipadx=5, ipady=5)

        self.frameExit = tk.Frame(width=50, height=50)
        self.frameExit.pack(fill=tk.X, ipadx=5, ipady=5)

        self.quit = tk.Button(self.frameExit, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack()

        # self.pack()

        # self.input_box = tk.Text()
        # self.input_box.pack()

    def output(self, text: str) -> None:
        # self.input_box.delete("1.0", tk.END)
        # self.input_box.insert("1.0", text)
        pyperclip.copy(text)

    def ankify(self):
        """ Main entry point of the app """
        # inputText = self.input_box.get("1.0", tk.END)
        inputText = pyperclip.paste()

        imgRegex = re.compile('\\)<.*?>')
        mathJaxOpen = re.compile(re.escape('{\displaystyle'))
        mathJaxClose = re.compile(re.escape('}<'))

        result = re.sub(
            mathJaxOpen, '\({\\\\displaystyle', re.sub(mathJaxClose, '}\)<', inputText))

        self.output(re.sub(imgRegex, ")", result))

    def obsidianfy(self):
        inputText = pyperclip.paste()

        inputText = re.sub(r'(:(| )|)<math(>|.+?>)\s?', r'$', inputText)
        inputText = re.sub(r'(<|\s?<)/math>', r'$', inputText)
        inputText = re.sub(r'(\<ref\>)|(\<\/ref\>)', r'', inputText)
        inputText = re.sub(r"'''", r'***', inputText)
        
        inputText = re.sub(r'\\N', r'\\mathbb N', inputText)
        inputText = re.sub(r'\\R', r'\\mathbb R', inputText)
        inputText = re.sub(r'\\Z', r'\\mathbb Z', inputText)

        inputText = re.split(r'(\[{2}.+?\]{2})', inputText)

        result = ""
        for obj in inputText:
            if obj[0:2] == "[[":
                if obj.count("|") > 0:
                    result += obj[obj.find("|")+1:-2]
                else:
                    result += obj[2:-2]
            else:
                result += obj
        inputText = result

        inputText = re.split(r'(={1,5}.+?={1,5}(\r|\n))', inputText)

        result = ""
        for obj in inputText:
            n = obj[0:5].count('=')
            if n >= 1:
                result += re.sub(r'=', r'#', obj, n)[:-n-1]
            else:
                result += obj

        self.output(result)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    window = tk.Tk()
    window.title("Work damnit")
    app = Application(master=window)
    app.mainloop()
