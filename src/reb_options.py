import os

from figures import Figure
from typing import List
from station import Station
from reb_event import Event


class REBOptions:
    """Клас для выборки данных"""

    START_WORD = "EVENT"
    STOP_WORD = "STOP"

    EMPTY_LINES = 3
    COORDS_COUNT = 2

    def __init__(
        self,
        figure: Figure,
        root_directory: str,
        stations: List[Station],
        range_name: str=None,
        result: str="result.txt"
    ) -> None:
        self.figure = figure
        self.root_directory = root_directory
        self.stations = stations
        self.range_name = range_name
        self.result = result

        self._valid_events = list()

    def get_events(self) -> List[Event]:
        return self._valid_events

    def _check_if_name_in_stations(
        self,
        name: str
    ) -> bool:
        """Проверяем, есть ли данное имя в списке станций"""
        for station in self.stations:
            if name == station.name:
                return True
        return False

    def _check_old_reb(
        self,
        filepath: str
    ) -> bool:
        """Проверяем, формат REB донесения в файле"""
        with open(filepath, "r") as file:
            for line in file.readlines():
                if self.START_WORD in line:
                    if len(line.split()) == 2:
                        return True
                    else:
                        return False

    def _process_old_reb(
        self,
        current_file: str
    ) -> List[Event]:
        """Набор правил, по которым разбираем старый REB текстовик"""
        start = False
        empty = 0
        valid_events = []
        current_data = ""
        current_lat = None
        current_long = None
        location = False
        loc_count = self.COORDS_COUNT
        valid_stations = []

        with open(current_file, "r") as file:
            for line in file.readlines():
                # Когда отрезок уже найден
                if start:
                    # Отсекаем косячные события без данных
                    if self.START_WORD in line:
                        start = True
                        current_data = line
                        location = False
                        loc_count = self.COORDS_COUNT
                        valid_stations = []
                        continue

                    # Если нашли STOP, то заканчиваем
                    if self.STOP_WORD in line:
                        current_data += "\n\n"
                        if valid_stations:
                            valid_events.append(
                                Event(
                                    current_data,
                                    current_lat,
                                    current_long
                                )
                            )
                        current_data = ""
                        current_lat = None
                        current_long = None
                        break

                    current_data += line

                    # Если строка пустая, то ищем конец
                    # if not line:  # Для пустой строки без знака переноса
                    if len(line) == 1 or len(line) == 2:  # Для строк с одним переносом
                        empty += 1

                        # Если нашли 3 пустых строки, то заканчиваем считывание
                        if empty == self.EMPTY_LINES:
                            empty = 0
                            start = False
                            if valid_stations:  # Если хотим, чтобы событие видели все станции
                            # if not a:  # Если хотим чтобы видна была хотя бы одна станция
                                valid_events.append(
                                    Event(
                                        current_data,
                                        current_lat,
                                        current_long
                                    )
                                )

                            current_data = ""
                            current_lat = None
                            current_long = None

                        continue

                    # Если строка непустая, то обрабатываем
                    else:
                        empty = 0

                        if not location:
                            if loc_count == 0:
                                location = True

                                latitude = float(line.split()[2])
                                longtitude = float(line.split()[3])

                                # Если событие не попало, то просто пропускаем его
                                if not self.figure.check_inside(
                                    latitude,
                                    longtitude
                                ):
                                    start = False
                                    current_data = ""
                                else:
                                    current_lat = latitude
                                    current_long = longtitude

                            else:
                                loc_count -= 1

                        else:
                            # Проверяем нужные нам станции
                            current_station = line.split()[0]
                            if self._check_if_name_in_stations(current_station):
                                valid_stations.append(current_station)

                # Если нашли начало отрезка, то начинаем считывать инфу
                elif self.START_WORD in line:
                    start = True
                    current_data = line
                    current_lat = None
                    current_long = None
                    location = False
                    loc_count = self.COORDS_COUNT
                    valid_stations = []

        return valid_events

    def _process_new_reb(
        self,
        current_file: str
    ) -> List[Event]:
        """Набор правил, по которым разбираем новый REB текстовик"""
        start = False
        empty = 0
        valid_events = []
        current_data = ""
        current_lat = None
        current_long = None
        location = False
        valid_stations = []

        with open(current_file, "r") as file:
            for line in file.readlines():
                # Когда отрезок уже найден
                if start:
                    # Отсекаем косячные события без данных
                    if self.START_WORD in line:
                        start = True
                        current_data = line
                        location = False
                        valid_stations = []
                        continue

                    # Если нашли STOP, то заканчиваем
                    if self.STOP_WORD in line:
                        current_data += "\n\n"
                        if valid_stations:
                            valid_events.append(
                                Event(
                                    current_data,
                                    current_lat,
                                    current_long
                                )
                            )
                        current_data = ""
                        current_lat = None
                        current_long = None
                        break

                    current_data += line

                    # Если строка пустая, то ищем конец
                    # if not line:  # Для пустой строки без знака переноса
                    if len(line) == 1 or len(line) == 2:  # Для строк с одним переносом
                        empty += 1

                        # Если нашли 3 пустых строки, то заканчиваем считывание
                        if empty == self.EMPTY_LINES:
                            empty = 0
                            start = False
                            if valid_stations:  # Если хотим, чтобы событие видели все станции
                            # if not a:  # Если хотим чтобы видна была хотя бы одна станция
                                valid_events.append(
                                    Event(
                                        current_data,
                                        current_lat,
                                        current_long
                                    )
                                )

                            current_data = ""
                            current_lat = None
                            current_long = None

                        continue

                    # Если строка непустая, то обрабатываем
                    else:
                        empty = 0

                        if not location:
                            if "Latitude" in line:
                                continue

                            location = True

                            latitude = float(line.split()[4])
                            longtitude = float(line.split()[5])

                            # Если событие не попало, то просто пропускаем его
                            if not self.figure.check_inside(
                                latitude,
                                longtitude
                            ):
                                start = False
                                current_data = ""
                            else:
                                current_lat = latitude
                                current_long = longtitude

                        else:
                            # Проверяем нужные нам станции
                            current_station = line.split()[0]
                            if self._check_if_name_in_stations(current_station):
                                valid_stations.append(current_station)

                # Если нашли начало отрезка, то начинаем считывать инфу
                elif self.START_WORD in line:
                    start = True
                    current_data = line
                    current_lat = None
                    current_long = None
                    location = False
                    valid_stations = []

        return valid_events

    def _process_file(self, filepath: str) -> None:
        """Определяем формат файла и обрабатываем его"""
        if self._check_old_reb(filepath):
            self._valid_events += self._process_old_reb(filepath)
        else:
            self._valid_events += self._process_new_reb(filepath)

    def process_directories(self) -> None:
        """Пробегается по папкам и обрабатывает каждую"""
        # Пробегаемся по всем папкам в директории
        for (dirname, _, files) in os.walk(self.root_directory):
            # Игнорируем файлы из текущей папки
            if dirname == ".":
                continue

            for filename in files:
                current_file = os.path.join(dirname, filename)

                if "txt" in current_file and "ims" not in current_file:
                    try:
                        self._process_file(current_file)

                        print(current_file + " - обработан")
                    except:
                        print(current_file + " - возникла ошибка при обработке!!!")
                else:
                    print(current_file + " - НЕ обработан")
