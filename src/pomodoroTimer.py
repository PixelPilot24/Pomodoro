import time
from threading import Thread
from tkinter import *
from tkinter import ttk
from data import Data
from pygame import mixer


class Timer:
    """
    Diese Klasse implementiert einen Pomodoro-Timer mit einer grafischen Benutzeroberfläche.
    """
    def __init__(self, root: Tk, name: str, tree: ttk.Treeview):
        """
        Initialisiert einen neuen Pomodoro-Timer.
        :param root: Das Tk-Objekt, das als Elternfenster für den Timer fungiert.
        :param name: Der Name der Aufgabe, für die der Timer gestartet wird.
        :param tree: Ein Treeview-Objekt, das die Aufgabenliste aus dem main.py darstellt.
        """
        self.__top_level = Toplevel(master=root, pady=10, padx=10)
        self.__top_level.focus_force()
        self.__top_level.title(name)
        self.__top_level.wm_attributes("-topmost", True)
        self.__top_level.wm_attributes("-toolwindow", True)
        self.__top_level.geometry("224x140")
        self.__name = name
        self.__tree = tree
        self.__thread = Thread()
        self.__rest = True

        self.__create_widgets()

    def __create_widgets(self):
        """
        Erstellt die grafischen Benutzeroberflächenelemente des Timers, einschließlich Labels, Buttons und Frame.
        """
        self.__max_seconds = 1500  # 25 Minuten
        self.__pomodori_counter = 0

        frame = Frame(master=self.__top_level)
        self.__pomodori_label = Label(master=frame, text=f"Pomodori hintereinander: {self.__pomodori_counter}",
                                      font=("Arial", 12))
        self.__text_label = Label(master=frame, text="Konzentriertes Arbeiten", font=("Arial", 14))
        self.__timer = Label(master=frame, text=self.__timer_text(self.__max_seconds), font=("Arial", 24))
        self.__start_button = Button(master=frame, text="Starten",
                                     command=lambda: self.__start_timer(self.__max_seconds))
        self.__restart_button = Button(master=frame, text="Neustart",
                                       command=lambda: self.__restart_timer(self.__max_seconds))

        self.__pomodori_label.pack(anchor=W)
        self.__text_label.pack()
        self.__timer.pack()
        self.__start_button.pack(side=LEFT)
        self.__restart_button.pack(side=RIGHT)
        frame.pack()

    @staticmethod
    def __timer_text(seconds: int) -> str:
        """
        Konvertiert die Sekunden in das Format "MM:SS" und gibt den resultierenden Text zurück.
        :param seconds: Die Anzahl der Sekunden, die umgewandelt werden sollen.
        :return: Eine Zeichenfolge im Format "MM:SS".
        """
        minute = seconds // 60
        second = seconds % 60

        return f"{int(minute):02d}:{int(second):02d}"

    def __start_timer(self, max_seconds: int):
        """
        Startet den Timer mit der angegebenen Anzahl von Sekunden in einem Thread.
        :param max_seconds: Die maximale Anzahl von Sekunden für den Timer.
        """
        if not self.__thread.is_alive():
            self.__start_button.configure(text="Pausieren", command=lambda: self.__pause_timer(max_seconds))
            self.__thread = Thread(target=self.__timer_thread, kwargs={"max_seconds": max_seconds})
            self.__thread.start()

    def __timer_thread(self, max_seconds: int):
        """
        Ein Hintergrundthread, der den Countdown des Timers durchführt.
        :param max_seconds: Die maximale Anzahl von Sekunden für den Timer.

        Wenn die Zeit abgelaufen ist, dann wird ein Sound abgespielt. Nach jedem Abschluss des Timers wird eine
        Pause gestartet und danach wieder der Timer.
        """
        mixer.init()
        mixer.music.load("../media/alarm.mp3")

        if mixer.music.get_busy():
            mixer.music.stop()

        self.__pause = False

        while max_seconds >= 0 and not self.__pause:
            if self.__timer.winfo_exists():
                self.__timer.configure(text=self.__timer_text(max_seconds))
                self.__timer.update_idletasks()
            else:
                break

            max_seconds -= 1
            time.sleep(1)

        if max_seconds == -1:
            mixer.music.play()

            if not mixer.music.get_busy():
                mixer.music.stop()

        if max_seconds == -1 and not self.__rest:
            self.__rest = True
            self.__update_timer("Konzentriertes Arbeiten", self.__max_seconds)
        elif max_seconds == -1 and self.__rest:
            self.__rest = False
            self.__pomodori_counter += 1
            rest_timer = 300  # 5 Minuten

            if self.__pomodori_counter % 4 == 0:
                rest_timer = 1200  # 20 Minuten

            self.__pomodori_label.configure(text=f"Pomodori hintereinander: {self.__pomodori_counter}")
            self.__update_timer("Pause", rest_timer)
            self.__save_pomodori()

    def __update_timer(self, text_label: str, timer_seconds: int):
        """
        Aktualisiert die Anzeige des Timers mit einem neuen Text und einer neuen Zeit.
        :param text_label: Der neue Text des Labels.
        :param timer_seconds: Die neue Anzahl von Sekunden für den Timer.
        """
        self.__text_label.configure(text=text_label)
        self.__timer.configure(text=self.__timer_text(timer_seconds))
        self.__start_button.configure(text="Starten", command=lambda: self.__start_timer(timer_seconds))
        self.__restart_button.configure(text="Neustarten", command=lambda: self.__restart_timer(timer_seconds))

    def __pause_timer(self, max_seconds: int):
        """
        Pausiert den Timer und ändert den Start-Button, um den Timer fortzusetzen.
        :param max_seconds: Die aktuelle Anzahl von Sekunden für den Timer.
        """
        self.__pause = True
        self.__start_button.configure(text="Starten", command=lambda: self.__start_timer(max_seconds))

    def __restart_timer(self, max_seconds: int):
        """
        Setzt den Timer zurück und ändert den Start-Button, um den Timer neu zu starten.
        :param max_seconds: Die aktuelle Anzahl von Sekunden für den Timer.
        """
        self.__pause = True
        self.__timer.configure(text=self.__timer_text(max_seconds))
        self.__start_button.configure(text="Starten", command=lambda: self.__start_timer(max_seconds))

    def __save_pomodori(self):
        """
        Aktualisiert die Anzahl der Pomodori für die aktuelle Aufgabe und speichert die Daten.
        """
        data = Data.load_json_file()
        data["not finished"][self.__name][0] += 1
        Data.save_json(data)

        for child in self.__tree.get_children():
            values = self.__tree.item(child)["values"]
            child_name = values[0]

            if self.__name == child_name:
                values[1] += 1
                self.__tree.item(child, values=values)
                break

    def run(self):
        """
        Startet die GUI des Timers. Nach dem loop wird überprüft, ob der Thread noch aktiv ist und wenn ja,
        dann wird dieser geschlossen.
        """
        self.__top_level.mainloop()

        if self.__thread.is_alive():
            self.__thread.join()
