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
import math
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

    def tokenReplace(self, input: str, regexpr: str, oldToken: str, newToken: str,  offsetl=0, offsetr=0):
        result = ""
        input = re.split(regexpr, input)

        for obj in input:
            n = math.floor (obj.count(oldToken) / 2)
            if obj[len(oldToken)] == oldToken:
                result += newToken*(n+offsetl) + obj[n:-n] + newToken*(n+offsetr)
            else:
                result += obj
        return result

    def obsidianfy(self):
        inputText = pyperclip.paste()

        inputText = re.sub(r'(:(| )|)<math(>|.+?>)\s?', r'$', inputText)
        inputText = re.sub(r'(<|\s?<)/math>', r'$', inputText)
        inputText = re.sub(r'(\<ref\>)|(\<\/ref\>)', r'', inputText)

        inputText = re.sub(r'\\N\b', r'\\mathbb N', inputText)
        inputText = re.sub(r'\\R\b', r'\\mathbb R', inputText)
        inputText = re.sub(r'\\Z\b', r'\\mathbb Z', inputText)
        inputText = re.sub(r'\\Q\b', r'\\mathbb Q', inputText)

        inputText = self.tokenReplace(
            inputText, r"(''+.*?''+)", r"'", r"*", -1, -1)
        inputText = self.tokenReplace(
            inputText, r'(={2,5}.+?={2,5})', r"=", r"#")


        # result = ""
        # inputText = re.split(r"(<math>(?:(?!\<\/)?:(.|\n))*?<\/math>)", inputText)

        # for obj in inputText:
        #     if obj.count(r'<math>') >= 1:
                
        #         temp = re.sub(r'<math>', r'$', re.sub(r'<\/math>', r'$', obj))
        #         result += temp
        #     else:
        #         result += obj

        # inputText = result
            
        self.output(inputText)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    window = tk.Tk()
    window.title("Work damnit")
    app = Application(master=window)
    app.mainloop()
