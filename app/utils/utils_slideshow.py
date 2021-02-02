#!/usr/bin/python

try:
    import tkinter as tk
    from tkinter.ttk import Combobox
except:
    import Tkinter as tk
    from ttk import Combobox

class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.bind('<KeyPress-Delete>', self.removeElement)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i
    
    def removeElement(self, event):
        if self.curIndex is not None:
            self.delete(self.curIndex)
            self.curIndex = self.nearest(event.y)


class DictCombobox(Combobox):
    """ A Tkinter combobox with a dictionary feature. """

    def __init__(self, master=None, cnf={}, **options):

        self.dict = None

        if 'values' in options:
            if isinstance(options.get('values'), dict):
                self.dict = options.get('values')
                options['values'] = self.dict.values()

        tk.Combobox.__init__(self, **options)

    # override "current" function of Combobox
    def current(self, newindex=None):
        if newindex is None:
            index = Combobox.current(self)
            keys = self.dict.keys()
            return keys[index]
        else:
            keys = self.dict.keys()
            current_index = 0
            for index, key in enumerate(keys):
                if key == newindex:
                    current_index = index
                    break
            return Combobox.current(self, current_index)

class CustomCombobox(Combobox):
    """ A Tkinter combobox with custom feature (current function overriden)."""

    def __init__(self, master=None, cnf={}, **options):

        self.list = None

        if 'values' in options:
            self.list = options['values']
            self.list.sort()
            options['values'] = self.list

        tk.Combobox.__init__(self, **options)

    # override "current" function of Combobox
    def current(self, newindex=None):
        if newindex is None:
            index = Combobox.current(self)
            return self.list[index]
        else:
            current_index = 0
            for index, value in enumerate(self.list):
                if value == newindex:
                    current_index = index
                    break
            return Combobox.current(self, current_index)
