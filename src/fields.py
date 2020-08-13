from PyQt5 import QtWidgets, QtGui, QtCore

from typing import List

import os

from station import Station


class ComboBoxField(QtWidgets.QComboBox):
    """Выпадающий список станций"""
    def __init__(
        self,
        name: str,
        stations: List[Station],
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.name = name
        self.stations = stations

        self.label = QtWidgets.QLabel(
            "<center>{}</center>".format(
                self.name
            )
        )

        self.model = QtGui.QStandardItemModel()

        # Делаем первый элемент заголовком
        header = QtGui.QStandardItem("---- Выбор станций ----")
        header.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
        header.setSelectable(False)
        self.model.setItem(0, 0, header)

        for station in self.stations:
            item = QtGui.QStandardItem(station.name)
            item.setFlags(
                QtCore.Qt.ItemIsUserCheckable |
                QtCore.Qt.ItemIsEnabled
            )

            item.setData(
                QtCore.Qt.Unchecked,
                QtCore.Qt.CheckStateRole
            )

            item.setData(
                station,
                role=QtCore.Qt.UserRole + 1
            )

            self.model.appendRow(item)

        self.setModel(self.model)

    def get_stations(self) -> List[Station]:
        """Получить список выбранных пунктов"""
        chosen_stations = []

        for i in range(self.model.rowCount()):
            if self.model.item(i).checkState() == 2:
                chosen_stations.append(
                    self.model.item(i).data(
                        role=QtCore.Qt.UserRole + 1
                    )
                )

        return chosen_stations


class DirectoryField(QtWidgets.QLineEdit):
    """Поле для выбора текущего каталога"""
    def __init__(
        self,
        name: str,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.name = name

        self.label = QtWidgets.QPushButton(self.name)

        self.label.clicked.connect(lambda: self.set_folder())

    def set_folder(self) -> None:
        """Открываем диалоговое окно для выбора каталога"""
        self.setText(QtWidgets.QFileDialog.getExistingDirectory())

    def get_data(self) -> str:
        """Получаем указанную директорию"""
        if os.path.isdir(self.text()):
            return self.text()
        else:
            raise NotADirectoryError


class NumberField(QtWidgets.QDoubleSpinBox):
    """Поле для ввода численных данных"""
    def __init__(
        self,
        name: str,
        default: float,
        min_value: float,
        max_value: float,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.name = name
        self.min_value = min_value
        self.max_value = max_value

        self.label = QtWidgets.QLabel(
            "<center>{}</center>".format(
                self.name
            )
        )

        # Зацикливаем значения от max до min
        self.setWrapping(True)
        self.setRange(
            self.min_value,
            self.max_value
        )

        self.setValue(default)

    def get_data(self) -> float:
        """Получить данные с элемента"""
        return self.value()
