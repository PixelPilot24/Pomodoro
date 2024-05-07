from tkinter import *
from tkinter import messagebox, ttk
from src.data import Data


class Controller:
    """
    Diese Klasse fungiert als Basissteuerung für die Benutzeroberfläche (GUI) zur Verwaltung von Aufgaben.
    Sie enthält Methoden zum Ändern des Status von Aufgaben, Löschen von Aufgaben, Bearbeiten von Aufgabendaten und
    Verwalten von GUI-Elementen.
    """
    def __init__(self, widgets_list: dict, max_width: int, tree: ttk.Treeview, top_level: Toplevel, root: Tk):
        """
        Initialisiert eine neue Instanz.
        :param widgets_list: Eine Dictionary für die Elemente für jede Aufgabe.
        :param max_width: Die maximale Breite der GUI, um sie bei Bedarf anzupassen.
        :param tree: Ein Treeview-Objekt, das die Aufgabenliste aus dem main.py darstellt.
        :param top_level: Das Tk-Objekt, das als Elternfenster dient.
        :param root: Das Tk-Objekt, das als Elternfenster für den Timer fungiert.
        """
        self.__root = root
        self.__widgets_list = widgets_list
        self.__data = Data.return_json_data()
        self.__max_width = max_width
        self.__tree = tree
        self.__top_level = top_level
        self.__font = ("Arial", 12)

    def _change_stat(self, name: str):
        """
        Ändert den Status einer Aufgabe zwischen "nicht abgeschlossen" und "abgeschlossen".
        :param name: Der Name der Aufgabe.
        """
        if name in self.__data["not finished"]:
            tag = "c1"
            for child in self.__tree.get_children():
                task_name = self.__tree.item(child)["values"][0]

                if name == str(task_name):
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
        """
        Ändert die Farbe der Zeilen.
        :param tag: Der tag der Farbe der Zeile.
        :param child: Der Name von der Zeile.
        :return: Gibt den richtigen tag, also die Farbe, der Zeile wieder.
        """
        task_tag = self.__tree.item(child)["tags"]

        if tag != task_tag:
            self.__tree.item(child, tags=tag)

        if tag == "c1":
            return "c2"
        else:
            return "c1"

    def _delete(self, name: str):
        """
        Löscht eine Aufgabe aus der Anzeige und aus den gespeicherten Daten.
        :param name: Der Name der Aufgabe.
        """
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

    def _edit_button(self, name: str):
        """
        Aktiviert den Bearbeitungsmodus für eine Aufgabe.
        :param name: Der Name der zu bearbeitenden Aufgabe.
        """
        self.__change_widget(name, name, True)

    def __save_button(self, name: str, new_name: str):
        """
        Speichert die geänderten Daten für eine bearbeitete Aufgabe.
        :param name: Der Name der ursprünglichen Aufgabe.
        :param new_name: Der neue Name der Aufgabe.
        """
        all_task = list(self.__data["finished"].keys()) + list(self.__data["not finished"].keys())
        exist = new_name in all_task

        if name == new_name:
            self.__cancel_button(name)
        elif exist:
            messagebox.showerror("Name", f"Der Name: {new_name} existiert bereits")
        else:
            widget = self.__widgets_list[name]
            current_list = "not finished" if name in self.__data["not finished"] else "finished"
            frame = widget[0]
            color = widget[2].cget("background")
            widget.pop(4)

            self.__change_widget(name, new_name, False)
            name_label = Label(master=frame, text=new_name, background=color, font=self.__font,
                               relief=GROOVE, height=2, width=self.__max_width)

            name_label.grid(row=0, column=1)

            widget.append(name_label)

            if self.__max_width < len(new_name) + 10:
                self.__max_width = len(new_name)

                for task_name in self.__widgets_list:
                    self.__widgets_list[task_name][4].config(width=self.__max_width + 10)

            self.__widgets_list[new_name] = widget
            self.__widgets_list.pop(name)

            self.__data[current_list][new_name] = self.__data[current_list][name]
            self.__data[current_list].pop(name)

            for child in self.__tree.get_children():
                if name == self.__tree.item(child)["values"][0]:
                    values = self.__tree.item(child)["values"][1:]
                    values.insert(0, new_name)
                    self.__tree.item(child, values=values)
                    break

            length = len(new_name) * 8 + 15

            if self.__max_width < length > 100:
                height = self.__root.winfo_height()
                self.__root.geometry(f"{length + 240}x{height}")

            Data.save_json(self.__data)

        self.__top_level.focus_force()

    def __change_widget(self, name: str, new_name: str, entry: bool):
        """
        Ändert die GUI-Elemente für eine bestimmte Aufgabe entsprechend dem Bearbeitungsmodus.
        :param name: Der Name der geändert werden soll.
        :param new_name: Der neue Name der Aufgabe.
        :param entry: Ein Boolean der angibt, ob dich die Aufgabe im Bearbeitungsmodus befindet.
        """
        widget = self.__widgets_list[name]
        frame = widget[0]
        color = widget[2].cget("background")
        current_list = "not finished" if name in self.__data["not finished"] else "finished"
        frame.winfo_children()[5].destroy()
        frame.winfo_children()[4].destroy()
        frame.winfo_children()[3].destroy()
        frame.winfo_children()[2].destroy()

        checkbox = Checkbutton(master=frame, background=color, padx=5, command=lambda: self._change_stat(new_name))
        delete_button = Button(master=frame, text="Löschen", font=self.__font,
                               command=lambda: self._delete(new_name))
        edit_button = Button(master=frame, text="Bearbeiten", font=self.__font,
                             command=lambda: self._edit_button(new_name))

        if entry:
            entry_name = Entry(master=frame, font=self.__font, width=self.__max_width + 9)
            delete_button.configure(text="Speichern", command=lambda: self.__save_button(name, entry_name.get()))
            edit_button.configure(text="Abbrechen", command=lambda: self.__cancel_button(name))

            entry_name.insert(0, name)

            entry_name.grid(row=0, column=1)

        if current_list == "finished":
            checkbox.select()

        checkbox.grid(row=0, column=0)
        delete_button.grid(row=0, column=4, padx=5)
        edit_button.grid(row=0, column=5, padx=5)

    def __cancel_button(self, name):
        """
        Bricht den Bearbeitungsmodus für eine bestimmte Aufgabe ab und behält die ursprünglichen Daten bei.
        :param name: Der Name der Aufgabe, für die der Bearbeitungsmodus abgebrochen werden soll.
        """
        widget = self.__widgets_list[name]
        frame = widget[0]
        color = widget[2].cget("background")

        self.__change_widget(name, name, False)
        name_label = Label(master=frame, text=name, background=color, font=self.__font,
                           relief=GROOVE, height=2, width=self.__max_width)

        name_label.grid(row=0, column=1)

        widget.pop(4)
        widget.append(name_label)

        for task_name in self.__widgets_list:
            self.__widgets_list[task_name][4].configure(width=self.__max_width + 10)
