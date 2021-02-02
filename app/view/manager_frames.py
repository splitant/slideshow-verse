#!/usr/bin/python

try:
    import tkinter as tk
    import tkinter.filedialog
    import tkinter.messagebox
    from tkinter.ttk import Combobox
    from tkinter import font
    from tk_html_widgets import HTMLLabel
except:
    import Tkinter as tk
    from ttk import Combobox

from PIL import Image, ImageTk
from controller import controller_slideshow
from utils import utils_slideshow


class ManagerFrames(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.controller = controller_slideshow.ControllerSlideshow()
        self.frames = {}

        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.create_frames()

    def create_frames(self):
        for F in (HomepageFrame):
            page_name = F.__name__
            frame = F(parent=self.container, manager_frame=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('HomepageFrame')

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class HomepageFrame(tk.Frame):
    def __init__(self, parent, manager_frame):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.manager_frame = manager_frame
        
        self.controller = self.manager_frame.controller

        self.create_widgets()

    def create_widgets(self):
        self.pptx_verses = []
        
        font_label_form = font.Font(
            family='Helvetica', size=36, weight='bold')
        
        # Pptx file upload part.
        self.container_pptx_file = tk.Frame(self)
        self.pptx_file_var = tk.StringVar()
        self.pptx_file = tk.Entry(
            self.container_pptx_file, font=font_label_form, textvariable=self.pptx_file_var)
        self.pptx_file_button = tk.Button(self.container_pptx_file, font=font_label_form, text='Browse PPTX file',
                                                   fg='black', command=self.get_pptx_filename)

        self.pptx_file.grid(row=0, column=0, sticky='nesw', padx=5)
        self.pptx_file_button.grid(
            row=0, column=1, sticky='nesw', padx=5)

        # Comboboxes part.
        self.container_comboboxes = tk.Frame(self)
        self.container_comboboxes.grid_rowconfigure(0, weight=1)
        self.container_comboboxes.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        ## Combobox Version
        self.container_version = tk.Frame(self.container_comboboxes)
        self.label_version = tk.Label(self.container_version,
                            text='Version')
        self.version_var = tk.StringVar()
        self.version = utils_slideshow.DictCombobox(
            self.container_version, textvariable=self.version_var, font=font_label_form, state="readonly", values=self.controller.getBibleVersions())
        self.version.current('LSG')
        self.label_version.grid(
            row=0, column=0, sticky='nesw', pady=20, padx=20)
        self.version.grid(row=1, column=0, sticky='nesw', pady=20, padx=20)

        ## Combobox Book
        self.container_book = tk.Frame(self.container_comboboxes)
        self.label_book = tk.Label(self.container_book,
                                       text='Book')
        self.book_var = tk.StringVar()
        self.book = utils_slideshow.DictCombobox(
            self.container_book, textvariable=self.book_var, font=font_label_form, state="readonly", values=self.controller.getBibleBooks())
        self.book.current('genese')
        self.label_book.grid(row=0, column=1, sticky='nesw', pady=20, padx=20)
        self.book.grid(row=1, column=1, sticky='nesw', pady=20, padx=20)
        self.book.bind("<<ComboboxSelected>>", self.update_combo_chapter_verse)

        ## Combobox Chapter
        self.container_chapter = tk.Frame(self.container_comboboxes)
        self.label_chapter = tk.Label(self.container_chapter,
                                       text='Chapter')
        self.chapter_var = tk.StringVar()
        self.chapter = utils_slideshow.CustomCombobox(
            self.container_chapter, 
            textvariable=self.chapter_var, 
            font=font_label_form, 
            state="readonly", 
            values=self.controller.getBibleChaptersKeys(
                self.version_var.get(),
                self.book_var.get()
            )
        )
        self.chapter.current('1')
        self.label_chapter.grid(
            row=0, column=2, sticky='nesw', pady=20, padx=20)
        self.chapter.grid(row=1, column=2, sticky='nesw', pady=20, padx=20)
        self.chapter.bind("<<ComboboxSelected>>", self.update_combo_verse)

        ## Combobox Verse
        self.container_verse = tk.Frame(self.container_comboboxes)
        self.label_verse = tk.Label(self.container_verse,
                                      text='Verse')
        self.verse_var = tk.StringVar()
        self.verse = utils_slideshow.CustomCombobox(
            self.container_verse,
            textvariable=self.verse_var,
            font=font_label_form,
            state="readonly",
            values=self.controller.getBibleVersesKeys(
                self.version_var.get(),
                self.book_var.get(),
                self.chapter_var.get()
            )
        )
        self.verse.current('1')
        self.label_verse.grid(row=0, column=3, sticky='nesw', pady=20, padx=20)
        self.verse.grid(row=1, column=3, sticky='nesw', pady=20, padx=20)
        
        ## Button 'Add verse'
        self.button_add_verse = tk.Button(self.container_comboboxes, text='Add verse', font=font_label_form,
                                       fg='black', command=self.button_add_verse_command)
        self.button_add_verse.grid(
            row=0, column=4, sticky='nesw', pady=20, padx=20)

        # List verses part
        self.container_verses_list = tk.Frame(self)
        self.verses_list_var = tk.StringVar()
        self.verses_list_box = utils_slideshow.DragDropListbox(self.container_verses_list, listvariable=self.verses_list_var,
                                                                    height=25, width=50, borderwidth=2)
        self.verses_list_box.grid(row=0, column=0, sticky='nesw', padx=5)
                
        # Buttons part
        self.container_buttons = tk.Frame(self)
        self.container_buttons.grid_rowconfigure(0, weight=1)
        self.container_buttons.grid_columnconfigure((0, 1), weight=1)
        self.button_generate = tk.Button(self.container_buttons, text='Generate', font=font_label_form,
                                     fg='black', command=self.button_generate_command)
        self.button_reset = tk.Button(self.container_buttons, text='Reset', font=font_label_form,
                                         fg='black', command=self.button_reset_command)

        self.button_generate.grid(
            row=0, column=0, sticky='nesw', pady=20, padx=20)
        self.button_reset.grid(
            row=0, column=1, sticky='nesw', pady=20, padx=20)

    def get_pptx_filename(self):
        filename = tk.filedialog.askopenfilename(
            title='Select file',
            initialdir='.',
            filetypes=[
                ('PPTX files', '*.pptx'),
                ('All files', '*')
            ])
        self.pptx_file_var.set(filename)

    def update_combo_chapter_verse(self):
        self.chapter.config(values=self.controller.getBibleChaptersKeys(
            self.version_var.get(),
            self.book_var.get()
        ))
        self.chapter.current('1')

        self.update_combo_verse()

    def update_combo_verse(self):
        self.verse.config(values=self.controller.getBibleVersesKeys(
            self.version_var.get(), 
            self.book_var.get(),
            self.chapter_var.get()
        ))
        self.verse.current('1')

    def button_add_verse_command(self):
        version = self.version_var.get() 
        book = self.book_var.get()
        chapter = self.chapter_var.get()
        verse = self.verse_var.get()

        slug = version + '.' + book + '.' + chapter + '.' + verse

        if slug not in self.pptx_verses:
            self.pptx_verses.append(slug)
            data_verse = self.controller.getDataVerse(version, book, chapter, verse)
            # TODO : add data_verse into listbox
            self.verses_list_box.insert('end', slug)

        ## TODO: add item to dragndrop list
        pass

    def button_generate_command(self):
        ## TODO: Generate new pptx with verses. Maybe a new classe
        pass

    def button_reset_command(self):
        self.pptx_file.delete(0, 'end')

        self.version.config(values=self.controller.getBibleVersions())
        self.version.current('LSG')

        self.book.config(values=self.controller.getBibleBooks())
        self.book.current('genese')

        self.chapter.config(values=self.controller.getBibleChaptersKeys(
            self.version_var.get(),
            self.book_var.get()
        ))
        self.chapter.current('1')

        self.verse.config(values=self.controller.getBibleVersesKeys(
            self.version_var.get(),
            self.book_var.get(),
            self.chapter_var.get()
        ))
        self.verse.current('1')

    def button_exit_command(self):
        self.master.master.destroy()

class SettingsFrame(tk.Frame):
    def __init__(self, parent, manager_frame):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.manager_frame = manager_frame
        self.settings = self.manager_frame.controller.settings

        self.create_widgets()

    def create_widgets(self):
        font_label_setting = font.Font(
            family='Helvetica', size=22, weight='bold')

        self.container_background_picture = tk.Frame(self)
        self.background_picture_var = tk.StringVar()
        self.background_picture_var.set(self.settings.backgroundPicture)
        self.background_picture = tk.Entry(
            self.container_background_picture, font=font_label_setting, textvariable=self.source_file_var)
        self.background_picture_button = tk.Button(self.container_background_picture, font=font_label_setting, text='Browse background picture',
                                                   fg='black', command=self.get_filename_picture)

        self.background_picture.grid(row=0, column=0, sticky='nesw', padx=5)
        self.background_picture_button.grid(row=0, column=1, sticky='nesw', padx=5)

        self.container_layout_areas = tk.Frame(self)
        
        self.layout_area_list_var = tk.StringVar(
            value=self.settings.displayOrder)
        self.layout_area_list_box = utils_slideshow.DragDropListbox(self.container_layout_areas, listvariable=self.layout_area_list_var,
                                    height=25, width=50, borderwidth=2)

        self.layout_area_list_box.grid(row=0, column=0, sticky='nesw', padx=5)

        fonts = list(font.families())
        fonts.sort()
        
        self.font_var = tk.StringVar()
        self.fonts = utils_slideshow.CustomCombobox(
            self, textvariable=self.font_var, font=font_label_setting, state="readonly", values=fonts)
        self.fonts.current(self.settings.font)

        self.container_buttons = tk.Frame(self)
        self.button_save = tk.Button(self.container_buttons, font=font_label_setting, text="Save",
                                     fg="black", command=self.button_save_command)
        self.button_back = tk.Button(self.container_buttons, font=font_label_setting, text="Back",
                                     fg="black", command=self.button_back_command)

        self.button_save.grid(row=0, column=0, sticky='nesw', padx=5)
        self.button_back.grid(row=0, column=1, sticky='nesw', padx=5)

        self.container_background_picture.grid(
            row=0, column=0, sticky='w', pady=10, padx=20)
        self.container_layout_areas.grid(
            row=1, column=0, sticky='w', pady=10, padx=20)
        self.fonts.grid(row=2, column=0, sticky='w', pady=10, padx=20)
        self.container_buttons.grid(
            row=3, column=0, sticky='w', pady=10, padx=10)
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def button_save_command(self):
        error = self.validation()

        if len(error) > 0:
            tk.messagebox.showerror('Error', error)
        else:
            self.settings.backgroundPicture = self.background_picture_var.get()
            self.settings.displayOrder = self.layout_area_list_var.get()
            self.settings.font = self.font_var.get()
            self.settings.saveSettings()
            tk.messagebox.showinfo('Info', 'Settings updated.')

    def button_back_command(self):
        self.manager_frame.show_frame('HomepageFrame')

    def validation(self):
        if not self.background_picture_var.get():
            return 'Background picture entry must not empty !'

        return ''

    def get_filename_picture(self):
        filename = tk.filedialog.askopenfilename(
            title='Select file',
            initialdir='.',
            filetypes=[
                ('PNG files', '*.png'),
                ('JPEG files', ('*.jpg', '*.jpeg')),
                ('GIF files', '*.gif'),
                ('All files', '*')
            ])
        self.background_picture_var.set(filename)
