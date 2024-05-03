from tkinter import *
from tkinter import ttk, messagebox
from data import Data


class AllTask:
    def __init__(self, root: Tk, tree: ttk.Treeview):
        self.__top_level = Toplevel(master=root)
        self.__top_level.title("Alle Aufgaben")
        self.__main_frame = Frame(master=self.__top_level)
        self.__tree = tree
        self.__data = Data.return_json_data()
        self.__widgets_list = {}
        self.__max_width = 0

        self.__create_widgets()

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
            self.__widgets_list[name][2].config(width=self.__max_width + 10)

        self.__main_frame.pack()

    def __widget(self, finished: bool, color: str, name: str, value: list):
        font = ("Arial", 12)
        frame = Frame(master=self.__main_frame, background=color)

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

        self.__widgets_list[name] = [frame, checkbox, name_label, pomodoro_label, date_label]

        if len(name) > self.__max_width:
            self.__max_width = len(name)

    def __change_stat(self, name: str):
        if name in self.__data["not finished"]:
            tag = "c1"
            for child in self.__tree.get_children():
                task_name = self.__tree.item(child)["values"][0]

                if name == task_name:
                    self.__tree.delete(child)
                    continue

                tag = self.__change_tag(tag, child)

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

    def __change_tag(self, tag: str, child: str) -> str:
        task_tag = self.__tree.item(child)["tags"]

        if tag != task_tag:
            self.__tree.item(child, tags=tag)

        if tag == "c1":
            return "c2"
        else:
            return "c1"

    def __delete(self, name: str):
        delete_bool = messagebox.askyesno("Löschen",
                                          f"Soll die Aufgabe: {name} wirklich gelöscht werden?")

        if delete_bool:
            current_list = "not finished" if name in self.__data["not finished"] else "finished"
            if current_list == "not finished":
                tag = "c1"

                for child in self.__tree.get_children():
                    if name == self.__tree.item(child)["values"][0]:
                        self.__tree.delete(child)
                        continue

                    tag = self.__change_tag(tag, child)

            self.__data[current_list].pop(name)
            self.__widgets_list[name][0].pack_forget()
            self.__widgets_list.pop(name)

            for i in range(len(self.__widgets_list)):
                task_name = list(self.__widgets_list.keys())[i]
                color = "#90ee90" if i % 2 == 0 else "#eeee90"

                for j in range(5):
                    self.__widgets_list[task_name][j].config(background=color)

            Data.save_json(self.__data)

        self.__top_level.focus_force()

    def __edit(self, name: str):
        # todo
        pass

    def run(self):
        self.__top_level.focus_force()
        self.__top_level.mainloop()
