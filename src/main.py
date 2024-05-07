from tkinter import *
from tkinter import ttk
from data import Data
from newTask import NewTask
from src.AllTask.allTask import AllTaskGUI
from pomodoroTimer import Timer


class MainGUI:
    def __init__(self):
        self.__root = Tk()
        self.__tree_frame = Frame(master=self.__root)
        self.__tree_frame.pack(fill=BOTH)
        self.__tree = ttk.Treeview(master=self.__tree_frame, columns=["c1", "c2", "c3"], show='headings', height=5)
        self.__data = Data().load_json_file()

        self.__initialize_window()

    def __initialize_window(self):
        self.__root.title("Pomodoro")
        self.__max_width = 0

        self.__create_scrollbar()
        self.__create_menubar()
        self.__create_list()
        self.__create_start()
        self.__resize_window()

    def __create_scrollbar(self):
        scrollbar_y = Scrollbar(master=self.__tree_frame, orient=VERTICAL, command=self.__tree.yview)
        scrollbar_y.pack(fill=Y, side=RIGHT)

        self.__tree.configure(yscrollcommand=scrollbar_y.set)

    def __resize_window(self):
        self.__tree.configure(height=10)
        self.__root.update_idletasks()
        width_first_column = 100 if self.__max_width < 100 else self.__max_width
        width = width_first_column + 240
        height = self.__root.winfo_height()
        self.__root.geometry(f"{width}x{height}")

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
        AllTaskGUI(self.__root, self.__tree).run()

    def __new_task(self):
        NewTask(self.__root, self.__tree, self.__max_width).run()

    def __create_list(self):
        self.__font = ("Arial", 12)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14))

        self.__tree.heading(column="# 1", text="Name")
        self.__tree.heading(column="# 2", text="Pomodori", anchor=CENTER)
        self.__tree.heading(column="# 3", text="Datum", anchor=CENTER)

        self.__tree.column(column="# 1", minwidth=100, width=100)
        self.__tree.column(column="# 2", stretch=NO, width=100, anchor=CENTER)
        self.__tree.column(column="# 3", stretch=NO, width=120, anchor=CENTER)

        self.__tree.tag_configure("c1", background="#90ee90", font=self.__font)
        self.__tree.tag_configure("c2", background="#eeee90", font=self.__font)

        finished_data = self.__data["not finished"]
        index = 0

        for name in finished_data:
            pomodori = finished_data[name][0]
            date = finished_data[name][1]
            tag = "c1" if index % 2 == 0 else "c2"
            self.__tree.insert(parent="", index=END, values=(name, pomodori, date), tags=tag)

            length = len(name) * 8 + 15

            if self.__max_width < length:
                self.__max_width = length

            index += 1

        self.__tree.column(column="# 1", width=self.__max_width)
        self.__tree.bind_all("<Button-1>", self.__handle_link)
        self.__tree.pack(fill=BOTH)

    def __handle_link(self, event: Event):
        selected_item = self.__tree.identify_row(event.y)

        if selected_item != "":
            name = self.__tree.item(selected_item)["values"][0]
            self.__name_label.configure(text=f"Aufgabe: {name}")

    def __create_start(self):
        frame = Frame(master=self.__root, relief=GROOVE, borderwidth=2, padx=5, pady=5)
        self.__name_label = Label(master=frame, text="Aufgabe: ", font=self.__font, anchor=CENTER)
        start_button = Button(master=frame, text="Auswählen", font=self.__font, padx=5, pady=5,
                              command=self.__start_timer)

        self.__name_label.pack(padx=5, pady=5)
        start_button.pack(padx=5, pady=5)
        frame.pack(pady=5)

    def __start_timer(self):
        text = self.__name_label.cget("text")
        name = text.split(" ")[1]
        self.__data = Data.load_json_file()
        not_finished = True if name in self.__data["not finished"] else False

        if name != "" and not_finished:
            Timer(self.__root, name, self.__tree).run()
        elif not not_finished:
            self.__name_label.configure(text="Aufgabe: ")

    def run(self):
        self.__root.mainloop()


if __name__ == '__main__':
    MainGUI().run()
