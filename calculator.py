import tkinter as tk
import customtkinter as ctk
import subprocess
import re
import os

# default colors
base = '#262940'
accent = '#4D5382'
hover = '#C6CAED'

class Button(ctk.CTkButton):
    def __init__(self, parent, text, row, column, command):
        # Create and style the buttons.
        super().__init__(
            parent,
            text = text,
            font=('Lato', 50),
            corner_radius = 20,
            border_width = 10,

            fg_color = accent,
            bg_color = base,
            border_color = base,
            hover_color = base,
            text_color = hover,

            command = command
        )
        
        # Default button for the numbers and operations.
        if text != '=':
            self.grid(row=row, column=column, sticky = 'nsew', ipadx = 10, ipady = 10,)
        else:
            self.grid(row=row, column=column, columnspan=2, sticky = 'nsew', ipadx = 10, ipady = 10,)

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.set_size()
        self.resizable(False, False)
        #fg_color = base
        #bg_color = base

        output = tk.StringVar(value = '')
        display = tk.StringVar(value = '')
        
        self.create_layout()
        self.create_widgets(display, output)

        self.add_kbd_keys(display, output)

        self.mainloop()

    # Determine and set the proper size of the calculator given the screen resolution
    def set_size(self):
        # Get the screen resolution
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        # Calculate the window size
        window_width = int(width * 0.225)
        window_height = int(height * 0.55)

        # Set the calculator size
        self.geometry(f"{window_width}x{window_height}")

    # Create the grid layout.
    def create_layout(self):
        # Grid Setup
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

    # Create the display and button widgets
    def create_widgets(self, display, output):
        # This label is the display label
        ctk.CTkLabel(
                self,
                fg_color = base,
                text_color = hover,
                font=('Lato', 75),
                textvariable = display,
            ).grid(row=0, column=0, columnspan=6, sticky = 'nsew')

        # Create each of the buttons
        Button(self, 'AC', 1, 0, lambda: self.reset(display, output))
        Button(self, '+/-', 1, 1, lambda: display.set(-display.get()))
        Button(self, '%', 1, 2, lambda: self.operation(display, output, '%'))
        Button(self, '/', 1, 3, lambda: self.operation(display, output, '/'))
        Button(self, '7', 2, 0, lambda: display.set(display.get() + '7'))
        Button(self, '8', 2, 1, lambda: display.set(display.get() + '8'))
        Button(self, '9', 2, 2, lambda: display.set(display.get() + '9'))
        Button(self, 'x', 2, 3, lambda: self.operation(display, output, '*'))
        Button(self, '4', 3, 0, lambda: display.set(display.get() + '4'))
        Button(self, '5', 3, 1, lambda: display.set(display.get() + '5'))
        Button(self, '6', 3, 2, lambda: display.set(display.get() + '6'))
        Button(self, '-', 3, 3, lambda: self.operation(display, output, '-',))
        Button(self, '1', 4, 0, lambda: display.set(display.get() + '1'))
        Button(self, '2', 4, 1, lambda: display.set(display.get() + '2'))
        Button(self, '3', 4, 2, lambda: display.set(display.get() + '3'))
        Button(self, '+', 4, 3, lambda: self.operation(display, output, '+'))
        Button(self, '0', 5, 0, lambda: display.set(display.get() + '0'))
        Button(self, '.', 5, 1, lambda: self.operation(display, output, '.'))
        Button(self, '=', 5, 2, lambda: self.operation(display, output, '='))

    # Clear the display and the string to calculate
    def reset(self, display, output):
        display.set('')
        output.set('')

    # Adds the operation character to the string to calculate. If the operation is '=', then finalize the string and perform the calculation
    def operation(self, display, output, op):
        if op == '=':
            output.set(output.get() + str(display.get()))
            self.equals(display, output)
        elif op == '.':
            display.set(display.get() + '.')
        else:
            output.set(output.get() + str(display.get()) + op)
            display.set('')

    # Uses eva (CLI-tool) to calculate the result.
    def equals(self, display, output):
        command = ['eva', str(output.get())]
        result = subprocess.run(command, capture_output = True, text = True)

        # remove all commas from the result
        result.stdout = re.sub(r',', '', result.stdout)

        self.reset(display, output)
        display.set(self.format(float(result.stdout)))

    def format(self, display):
        tmp = int(display)
        if abs(tmp - display) > 0:
            return display 
        else:
            return tmp

    # Add keyboard support for numbers and operations
    def add_kbd_keys(self, display, output):
        self.bind('0', lambda event: display.set(display.get() + '0'))
        self.bind('1', lambda event: display.set(display.get() + '1'))
        self.bind('2', lambda event: display.set(display.get() + '2'))
        self.bind('3', lambda event: display.set(display.get() + '3'))
        self.bind('4', lambda event: display.set(display.get() + '4'))
        self.bind('5', lambda event: display.set(display.get() + '5'))
        self.bind('6', lambda event: display.set(display.get() + '6'))
        self.bind('7', lambda event: display.set(display.get() + '7'))
        self.bind('8', lambda event: display.set(display.get() + '8'))
        self.bind('9', lambda event: display.set(display.get() + '9'))
        self.bind('-', lambda event: self.operation(display, output, '-'))
        self.bind('+', lambda event: self.operation(display, output, '+'))
        self.bind('*', lambda event: self.operation(display, output, '*'))
        self.bind('%', lambda event: self.operation(display, output, '%'))
        self.bind('/', lambda event: self.operation(display, output, '/'))
        self.bind('.', lambda event: self.operation(display, output, '.'))
        self.bind('<Return>', lambda event: self.operation(display, output, '='))
        self.bind('<BackSpace>', lambda event: display.set(display.get()[:-1]))

def theme(theme):
    global base
    global accent
    global hover
    # obtain the user's home directory
    home = os.path.expanduser('~')

    # Read in the colors from the config file
    with open(home + '/.config/' + theme, 'r') as f:
        for line in f:
            if line.startswith('base'):
                base = re.search(r'#[0-9A-Fa-f]{6}', line).group(0)
            elif line.startswith('accent'):
                accent = re.search(r'#[0-9A-Fa-f]{6}', line).group(0)
            elif line.startswith('hover'):
                hover = re.search(r'#[0-9A-Fa-f]{6}', line).group(0)

theme('theme/active.theme')
Calculator()
