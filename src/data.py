import json
import os.path


class Data:
    """
    Diese Klasse dient der Verwaltung der JSON Datei für die Anwendung.
    """
    __file_name = "pomodoro.json"
    __json_data = {
        "finished": {},
        "not finished": {}
    }

    @classmethod
    def save_json(cls, data: dict):
        """
        Diese Methode speichert die übergebenen Daten in der JSON-Datei.
        :param data: Eine Dictionary mit den zu speichernden Daten.
        """
        file = open(cls.__file_name, "w")
        json.dump(data, file)

    @classmethod
    def load_json_file(cls) -> dict:
        """
        Diese Methode lädt die Daten aus der JSON-Datei und gibt sie zurück. Wenn die Datei nicht vorhanden ist,
        wird eine neue Datei mit den Standarddaten erstellt.
        :return: Ein Dictionary mit den geladenen Daten.
        """
        if os.path.isfile(cls.__file_name):
            file = open(cls.__file_name, "r")
            data = json.load(file)
            cls.__json_data = data

            return data
        else:
            cls.save_json(cls.__json_data)

            return cls.__json_data

    @classmethod
    def return_json_data(cls) -> dict:
        """
        Diese Methode gibt das aktuelle Dictionary mit den gespeicherten Daten zurück.
        :return: Ein Dictionary mit den gespeicherten Daten.
        """
        return cls.__json_data
