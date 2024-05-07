from tkinter import *
from tkinter import ttk
from src.data import Data
from src.AllTask.controller import Controller


class AllTaskGUI(Controller):
    """
    Diese Klasse stellt eine GUI zur Anzeige aller Aufgaben dar. Sie erbt von der Controller-Klasse
    und ermöglicht die Verwaltung und Anzeige von Aufgaben sowie die Interaktion des Benutzers mit diesen Aufgaben.
    """
    def __init__(self, root: Tk, tree: ttk.Treeview):
        """
        Initialisiert eine neue Instanz der KLasse.
        :param root: Das Tk-Objekt, das als Elternfenster für den Timer fungiert.
        :param tree: Ein Treeview-Objekt, das die Aufgabenliste aus dem main.py darstellt.
        """
        self.__top_level = Toplevel(master=root)
        self.__canvas = Canvas(master=self.__top_level, scrollregion=(0, 0, 700, 700))
        self.__main_frame = Frame(master=self.__canvas)
        self.__data = Data.load_json_file()
        self.__widgets_list = {}
        self.__max_width = 0
        self.__font = ("Arial", 12)

        self.__setup_window()
        super().__init__(self.__widgets_list, self.__max_width, tree, self.__top_level, root)

    def __setup_window(self):
        """
        Konfiguriert das Hauptfenster der GUI mit Titel, Fokus und das Scrollverhalten. Erstellt die Scrollleiste,
        Widgets und passt die Fenstergröße an.
        """
        self.__top_level.title("Alle Aufgaben")
        self.__top_level.focus_force()
        self.__canvas.bind_all("<MouseWheel>", self.__on_mouse_wheel)
        self.__create_scrollbar()
        self.__create_widgets()
        self.__resize_window()

    def __on_mouse_wheel(self, event: Event):
        """
        Behandelt das Scrollen mit dem Mausrad. Es wird überprüft, ob das richtige Fenster aktiv ist in dem
        gescrollt werden soll.
        :param event: Ein Ereignisobjekt, das die Mausereignisse enthält.
        """
        if self.__canvas and self.__top_level.winfo_exists():
            self.__canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def __resize_window(self):
        """
        Passt die Größe des Fensters an die enthaltenen Elemente an.
        """
        width = self.__main_frame.winfo_reqwidth() + 21
        height = self.__main_frame.winfo_reqheight() + 21

        if height < 281:
            height = 281
        elif height > 561:
            height = 540

        self.__top_level.geometry(f"{width}x{height}")

    def __create_widgets(self):
        """
        Erstellt die GUI Elemente für jede Aufgabe und platziert sie im Hauptfenster. Nach der Erstellung wird
        die Größe des Labels für den Namen na das Größte angepasst.
        """
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

        self.__canvas.update_idletasks()
        self.__canvas.configure(scrollregion=self.__canvas.bbox(ALL))

    def __create_scrollbar(self):
        """
        Erstellt und konfiguriert die Scrollleisten.
        """
        scrollbar_x = Scrollbar(master=self.__top_level)
        scrollbar_y = Scrollbar(master=self.__top_level)
        self.__canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        scrollbar_x.configure(orient=HORIZONTAL, command=self.__canvas.xview)
        scrollbar_y.configure(orient=VERTICAL, command=self.__canvas.yview)
        scrollbar_x.pack(fill=X, side=BOTTOM, expand=False)
        scrollbar_y.pack(fill=Y, side=RIGHT, expand=False)
        self.__canvas.pack(fill=BOTH, expand=TRUE)
        self.__canvas.create_window(0, 0, window=self.__main_frame, anchor=NW)

    def __widget(self, finished: bool, color: str, name: str, value: list):
        """
        Erstellt ein Element für eine einzelne Aufgabe. Am Ende wird die maximale Breite des Labels für den Text
        überprüft und angepasst.
        :param finished: Ein Boolean, der angibt, ob die Aufgabe abgeschlossen ist oder nicht.
        :param color: Die Hintergrundfarbe des Elements.
        :param name: Der Name der Aufgabe.
        :param value: Eine Liste mit den Pomodori Wert und dem Erstellerdatum.
        """
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
        """
        Startet die Anwendung wo alle Aufgaben angezeigt werden.
        """
        self.__top_level.mainloop()
