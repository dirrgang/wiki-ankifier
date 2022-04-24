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

        # Concatenation of Math formulas
        inputText = re.sub(r'<\/math> (für alle) <math>',
                           r'\\quad \\text{für alle} \\quad ', inputText)

        # MathJax
        inputText = re.sub(
            r'\n:?\s*<math(?:(>| display="inline">))((.|\n)*?)<\/math>(.|)', r'\n$$\2\4$$', inputText)
        inputText = re.sub(
            r'<math(?:(>| display="inline">))\s*(.*?)\s*<\/math>', r'$\2$', inputText)
        inputText = re.sub(r'\n+', r'\n', inputText)

        # Categories
        inputText = re.sub(r'\[\[Kategorie:(.*?)\]\]', r'#\1', inputText)

        # Nowrap
        inputText = re.sub(r'{{nowrap\|(.*?)}}', r'\1', inputText)

        # Wikitable
        inputText = re.sub(
            r'{\| class="wikitable"((.|\n)*?)\|}', r'', inputText)

        # Infobox
        inputText = re.sub(r'{{Infobox ((.|\n)*?)}}', r'', inputText)

        # Language Indicators
        inputText = re.sub(r"{{(en|de).*?''(.*?)''}}", r"''\2''", inputText)

        # References
        inputText = re.sub(
            r'(<ref>|<ref name=".*?">).*?(<\/ref>)', r'', inputText)

        # Inline Code Formatting
        inputText = re.sub(r"<code>(.*?)<\/code>", r'`\1`', inputText)

        # Block Code Formatting
        inputText = re.sub(
            r'\<syntaxhighlight lang="(.*)".*?\>((.|\n)*?)\<\/syntaxhighlight\>', r'```\1\n\2\n```', inputText)

        # External URLs
        inputText = re.sub(r'\[(http.*?) (.*?)\]', r'[\2](\1)', inputText)

        # Lists
        inputText = re.sub(r'\n(\*)', r'\n* ', inputText)

        # Text Formatting
        inputText = re.sub(r"'''(.*?)'''", r'**\1**', inputText)
        inputText = re.sub(r"''(.*?)''", r'*\1*', inputText)
        inputText = re.sub(r"'(.*?)'", r'*\1*', inputText)

        # Language
        inputText = re.sub(r'{{lang\|..\|(.*?)}}', r'\1', inputText)

        # URL
        inputText = re.sub(r'{{\w+\|url.+?}}', r'', inputText)

        # Wiki-specific oddities
        inputText = re.sub(r'\\N', r'\\mathbb N', inputText)
        inputText = re.sub(r'\\Complex', r'\\mathbb C', inputText)
        inputText = re.sub(r'\\R(?!ightarrow)', r'\\mathbb R', inputText)
        inputText = re.sub(r'\\Z', r'\\mathbb Z', inputText)
        inputText = re.sub(r'\n# ', r'\n 1. ', inputText)

        # Headings
        for i in range(1, 5):
            OldFormat = i * '='
            NewFormat = i * '#'

            inputText = re.sub(rf'\n{OldFormat} (.*?) {OldFormat}',
                               rf"{NewFormat} \1", inputText)

        self.output(inputText)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    window = tk.Tk()
    window.title("Work damnit")
    app = Application(master=window)
    app.mainloop()
