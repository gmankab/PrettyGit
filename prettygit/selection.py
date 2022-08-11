#!/bin/python

from rich import pretty
from rich.console import Console
from pynput import keyboard
import subprocess
import sys

pretty.install()
console = Console()
print = console.print
run = subprocess.getstatusoutput
Key = keyboard.Key


class Selection:
    def __init__(
        self,
        items: list | tuple,
        styles: list | tuple = [],
        choosen: int = 0,
    ) -> None:
        self.items = items
        self.choosen = choosen
        self.len = len(items)
        if not styles:
            styles = [None] * len(self.items)
        self.styles = styles

    def print(self):
        if self.choosen < 0:
            self.choosen = self.len - 1
        elif self.choosen >= self.len:
            self.choosen = 0
        print()
        for index, item in enumerate(self.items):
            if index == self.choosen:
                item = f'[blue]➜[/blue]  [reverse]{item}[/reverse]'
            else:
                item = f'    {item}'
            print(
                item,
                style = self.styles[index]
            )
        print()

    def update(self):
        up_one = '\x1b[1A'
        erase_line = '\x1b[2K'
        sys.stdout.write(
            erase_line + (
                up_one + erase_line
            ) * (
                self.len + 2
            )
        )
        self.print()

    def choose(self):
        def on_press(pressed_key):
            match pressed_key:
                case Key.esc:
                    self.choosen = None
                    return False
                case Key.enter:
                    return False
                case Key.up:
                    self.choosen -= 1
                case Key.down:
                    self.choosen += 1
            self.update()

        run('stty -echo')
        self.print()
        with keyboard.Listener(
            on_press=on_press,
        ) as listener:
            listener.join()
        input()
        run('stty echo')

        if self.choosen is None:
            return None
        else:
            return self.items[self.choosen]
