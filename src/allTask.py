from tkinter import *
from tkinter import ttk
from data import Data


class AllTask:
    def __init__(self, root: Tk, tree: ttk.Treeview):
        self.__top_level = Toplevel(master=root)
        self.__top_level.title("Alle Aufgaben")
        self.__tree = tree
        self.__data = Data.return_json_data()
        self.__name_label = []
        self.__max_width = 0

        self.__create_widgets()

    def __create_widgets(self):
        finished = self.__data["finished"]
        not_finished = self.__data["not finished"]
        index = 0

        for name in not_finished:
            color = "#90ee90" if index % 2 == 0 else "#eeee90"
            index += 1
            value = not_finished[name]
            self.__widget(False, color, name, value)

        for name in finished:
            color = "#90ee90" if index % 2 == 0 else "#eeee90"
            index += 1
            value = finished[name]
            self.__widget(True, color, name, value)

        for label in self.__name_label:
            label.config(width=self.__max_width + 10)

    def __widget(self, finished: bool, color: str, name: str, value: list):
        font = ("Arial", 12)
        frame = Frame(master=self.__top_level, background=color)

        checkbox = Checkbutton(master=frame, background=color, padx=5, command=lambda n=name: self.__change_stat(n))
        name_label = Label(master=frame, text=name, background=color, font=font, relief=GROOVE, height=2)
        pomodoro_label = Label(master=frame, text=value[0], background=color, font=font, relief=GROOVE,
                               height=2, width=3, padx=5)
        date_label = Label(master=frame, text=value[1], background=color, font=font, relief=GROOVE, height=2, padx=5)
        delete_button = Button(master=frame, text="Löschen", font=font, command=lambda n=name: self.__delete(n))
        edit_button = Button(master=frame, text="Bearbeiten", font=font, command=lambda n=name: self.__edit(n))

        if finished:
            checkbox.select()

        checkbox.grid(row=0, column=0)
        name_label.grid(row=0, column=1)
        pomodoro_label.grid(row=0, column=2)
        date_label.grid(row=0, column=3)
        delete_button.grid(row=0, column=4, padx=5)
        edit_button.grid(row=0, column=5, padx=5)
        frame.pack(pady=5)

        self.__name_label.append(name_label)

        if len(name) > self.__max_width:
            self.__max_width = len(name)

    def __change_stat(self, name: str):
        if name in self.__data["not finished"]:
            tag = "c1"
            for child in self.__tree.get_children():
                task_name = self.__tree.item(child)["values"][0]
                task_tag = self.__tree.item(child)["tags"]

                if name == task_name:
                    self.__tree.delete(child)
                    continue

                if tag != task_tag:
                    self.__tree.item(child, tags=tag)

                if tag == "c1":
                    tag = "c2"
                else:
                    tag = "c1"

            self.__data["finished"][name] = self.__data["not finished"][name]
            self.__data["not finished"].pop(name)
        else:
            len_data = len(self.__data["not finished"])
            value = self.__data["finished"][name]
            tag = "c1" if len_data % 2 == 0 else "c2"
            self.__tree.insert(parent="", index=END, values=(name, value[0], value[1]), tags=tag)

            self.__data["not finished"][name] = self.__data["finished"][name]
            self.__data["finished"].pop(name)

        Data.save_json(self.__data)

    def __delete(self, name: str):
        # todo
        pass

    def __edit(self, name: str):
        # todo
        pass

    def run(self):
        self.__top_level.focus_force()
        self.__top_level.mainloop()
