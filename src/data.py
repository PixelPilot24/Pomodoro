import json
import os.path


class Data:
    __file_name = "pomodoro.json"
    __json_data = {
        "finished": {},
        "not finished": {}
    }

    @classmethod
    def save_json(cls, data: dict):
        file = open(cls.__file_name, "w")
        json.dump(data, file)

    @classmethod
    def load_json_file(cls) -> dict:
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
        return cls.__json_data

    @classmethod
    def save_data(cls, finished: bool, name: str, data: list):
        if finished:
            cls.__json_data["not finished"].pop(name)
            cls.__json_data["finished"][name] = data
        else:
            cls.__json_data["not finished"][name] = data

        cls.save_json(cls.__json_data)
