from station import Station
from PyQt5 import QtWidgets

from fields import ComboBoxField, DirectoryField

from typing import List


class InstrumentsContainer:
    """Включает в себя:
    
    - выпадающий список станций
    
    - выбор директории
    
    - кнопку запуска обработки"""

    STATIONS_FILE = "stations.json"

    def __init__(
        self,
        parent: QtWidgets.QMainWindow,
        resources_path: str
    ) -> None:
        self.parent = parent

        self.stations_box = ComboBoxField(
            "Станции",
            Station.load_from_json(resources_path + self.STATIONS_FILE)
        )

        self.directory_field = DirectoryField("Выбрать папку")

        self.start_button = QtWidgets.QPushButton("Начать обработку")

        self.populate_window()

    def get_directory(self) -> str:
        return self.directory_field.get_data()

    def get_stations(self) -> List[Station]:
        return self.stations_box.get_stations()

    def populate_window(self) -> None:
        """Заполняем окно элементами"""
        self.parent.add_widget(
            self.stations_box,
            6,
            0
        )

        self.parent.add_widget(
            self.directory_field,
            6,
            1
        )

        self.parent.l.addWidget(
            self.start_button,
            0,
            8,
            2,
            1
        )
