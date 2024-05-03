from tkinter import *
from tkinter import ttk
from data import Data
from newTask import NewTask
from allTask import AllTask


class MainGUI:
    def __init__(self):
        self.__root = Tk()
        self.__tree = ttk.Treeview(self.__root, columns=["c1", "c2", "c3"], show='headings', height=5)
        self.__data = Data().load_json_file()

        self.__initialize_window()

    def __initialize_window(self):
        self.__root.title("Pomodoro")

        self.__create_menubar()
        self.__create_list()
        self.__create_start()

    def __create_menubar(self):
        menubar = Menu(master=self.__root)
        option_menu = Menu(master=menubar, tearoff=0)
        option_menu.add_command(label="Neue Aufgabe", command=self.__new_task)
        option_menu.add_command(label="Alle Aufgaben", command=self.__all_task)
        option_menu.add_separator()
        option_menu.add_command(label="Schließen", command=lambda: exit())
        menubar.add_cascade(label="Datei", menu=option_menu)

        self.__root.config(menu=menubar)

    def __all_task(self):
        AllTask(self.__root, self.__tree).run()

    def __new_task(self):
        NewTask(self.__root, self.__tree).run()

    def __create_list(self):
        font = ("Arial", 12)
        font_head = ("Arial", 14)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=font_head)

        self.__tree.heading("# 1", text="Name")
        self.__tree.heading("# 2", text="Pomodori", anchor=CENTER)
        self.__tree.heading("# 3", text="Datum", anchor=CENTER)

        self.__tree.column("# 1", width=100, stretch=YES)
        self.__tree.column("# 2", width=100, anchor=CENTER)
        self.__tree.column("# 3", width=120, anchor=CENTER)

        self.__tree.tag_configure("c1", background="#90ee90", font=font)
        self.__tree.tag_configure("c2", background="#eeee90", font=font)

        finished_data = self.__data["not finished"]
        index = 0

        for name in finished_data:
            pomodori = finished_data[name][0]
            date = finished_data[name][1]
            tag = "c1" if index % 2 == 0 else "c2"
            self.__tree.insert(parent="", index=END, values=(name, pomodori, date), tags=tag)
            index += 1

        self.__tree.pack()

    def __create_start(self):
        # todo
        pass

    def run(self):
        self.__root.mainloop()


if __name__ == '__main__':
    MainGUI().run()
