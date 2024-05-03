from datetime import date
from tkinter import *
from tkinter import ttk, messagebox
from data import Data


class NewTask:
    def __init__(self, root: Tk, tree: ttk.Treeview):
        self.__top_level = Toplevel(master=root)
        self.__top_level.geometry("250x150")
        self.__top_level.focus_force()
        self.__tree = tree

        self.__create_widgets()

    def __create_widgets(self):
        frame = Frame(master=self.__top_level)
        Label(master=frame, text="Name", font=("Arial", 10)).pack(anchor=W)
        self.__name_entry = Entry(master=frame, font=("Arial", 12))
        save_button = Button(master=frame, text="Speichern", command=self.__save_data, font=("Arial", 12))

        self.__name_entry.pack()
        save_button.pack(pady=10)
        frame.pack()

    def __save_data(self):
        name = self.__name_entry.get()
        today = date.today().strftime("%d.%m.%Y")
        data = Data.return_json_data()
        finished = data["finished"]
        not_finished = data["not finished"]
        tag = "c1" if len(not_finished) % 2 == 0 else "c2"
        name_existed = name in finished or name in not_finished

        if name == "":
            messagebox.showerror("Name", "Der Name darf nicht leer sein")
        elif name_existed:
            messagebox.showerror("Name", "Der Name existiert bereits")
        else:
            self.__tree.insert(parent="", index=END, values=(name, 0, today), tags=tag)
            self.__tree.update_idletasks()
            Data.save_data(False, name, [0, today])

        self.__top_level.focus_force()

    def run(self):
        self.__top_level.mainloop()
