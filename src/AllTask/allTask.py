from tkinter import *
from tkinter import ttk
from src.data import Data
from controller import Controller


class AllTaskGUI(Controller):
    # todo scrollbar hinzufügen
    def __init__(self, root: Tk, tree: ttk.Treeview):
        self.__top_level = Toplevel(master=root)
        self.__top_level.title("Alle Aufgaben")
        self.__main_frame = Frame(master=self.__top_level)
        self.__data = Data.return_json_data()
        self.__widgets_list = {}
        self.__max_width = 0
        self.__font = ("Arial", 12)

        self.__create_widgets()
        super().__init__(self.__widgets_list, self.__max_width, tree, self.__top_level, root)

    def __create_widgets(self):
        finished = self.__data["finished"]
        not_finished = self.__data["not finished"]
        index = 0

        for name in not_finished:
            color = "#90ee90" if index % 2 == 0 else "#eeee90"
            value = not_finished[name]
            self.__widget(False, color, name, value)
            index += 1

        for name in finished:
            color = "#90ee90" if index % 2 == 0 else "#eeee90"
            value = finished[name]
            self.__widget(True, color, name, value)
            index += 1

        for name in self.__widgets_list:
            self.__widgets_list[name][4].config(width=self.__max_width + 10)

        self.__main_frame.pack()

    def __widget(self, finished: bool, color: str, name: str, value: list):
        frame = Frame(master=self.__main_frame, background=color, relief=GROOVE)

        pomodoro_label = Label(master=frame, text=value[0], background=color, font=self.__font, relief=GROOVE,
                               height=2, width=3, padx=5)
        date_label = Label(master=frame, text=value[1], background=color, font=self.__font,
                           relief=GROOVE, height=2, padx=5)
        checkbox = Checkbutton(master=frame, background=color, padx=5, command=lambda: self._change_stat(name))
        name_label = Label(master=frame, text=name, background=color, font=self.__font, relief=GROOVE, height=2)
        delete_button = Button(master=frame, text="Löschen", font=self.__font,
                               command=lambda: self._delete(name))
        edit_button = Button(master=frame, text="Bearbeiten", font=self.__font,
                             command=lambda: self._edit_button(name))

        if finished:
            checkbox.select()

        pomodoro_label.grid(row=0, column=2)
        date_label.grid(row=0, column=3)
        checkbox.grid(row=0, column=0)
        name_label.grid(row=0, column=1)
        delete_button.grid(row=0, column=4, padx=5)
        edit_button.grid(row=0, column=5, padx=5)
        frame.pack(pady=5)

        self.__widgets_list[name] = [frame, checkbox, pomodoro_label, date_label, name_label]

        if len(name) > self.__max_width:
            self.__max_width = len(name)

    def run(self):
        self.__top_level.focus_force()
        self.__top_level.mainloop()
