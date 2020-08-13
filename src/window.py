from PyQt5 import QtWidgets, QtCore, QtGui

from cartopy.crs import PlateCarree

from globe_map import GlobeMap

from containers import InstrumentsContainer

from figures import Figure

from figure_buttons import RectangleButton, EllipseButton

from reb_options import REBOptions

import os
import subprocess
import argparse


class CustomGridLayout(QtWidgets.QGridLayout):
    """Создаем собственные настройки для выравнивания"""
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.setSpacing(10)


class MainWindow(QtWidgets.QMainWindow):
    """Главное окно программы"""
    MAP_UPDATE_FREQ = 100  # Количество милесекунд между обновлениями
    def __init__(
        self,
        window_title: str,
        layout_class: QtWidgets.QLayout,
        argv: argparse.Namespace,
        resources_path: str,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.window_title = window_title
        self.argv = argv
        self.resources_path = resources_path

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Устанавливаем имя окна
        self.setWindowTitle(self.window_title)

        # Генерируем меню в верхней части окна
        self._create_menu()

        # Настраиваем выравнивание окна
        self._create_layout(layout_class)

        self.map = GlobeMap(
            self,
            PlateCarree(),
            self.argv.light,
            self.resources_path
        )

        self.current_figure = None

        self.ellipse()

        self.instruments = InstrumentsContainer(self, self.resources_path)

        self.reb_options = None

        self.events = list()

        self.event_names_visible = True

        self.instruments.start_button.clicked.connect(
            lambda: self._start_processing()
        )

        self._connect_map_update()

        self.showMaximized()

    def _start_processing(self) -> None:
        """Начинаем парсинг файлов"""
        try:
            self.reb_options = REBOptions(
                self.current_figure.get_figure(),
                self.instruments.get_directory(),
                self.instruments.get_stations()
            )

            self._deactivate()

            self.reb_options.process_directories()

            self.events = self.reb_options.get_events()

            self._write_to_file()

            self.map.update(
                self.instruments.get_stations(),
                self.current_figure.get_figure(),
                self.events,
                self.event_names_visible
            )

        except NotADirectoryError:
            QtWidgets.QMessageBox.critical(
                self,
                "Не указана папка",
                "Укажите корректную папку"
            )

    def _write_to_file(self) -> None:
        """Пишем данные по событиям в текстовый файл"""
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Файл с результатами",
            filter="Текстовые файлы (*.txt)"
        )[0]

        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                for event in self.events:
                    file.write(event.data)

    def _deactivate(self) -> None:
        """Деактивируем все элементы управления и обновление карты"""
        self.refresh_timer.timeout.disconnect()

    def _connect_map_update(self) -> None:
        """Подключаем обновление карты по таймеру"""
        self.refresh_timer = QtCore.QTimer()
        self.refresh_timer.timeout.connect(
            lambda: self.map.update(
                self.instruments.get_stations(),
                self.current_figure.get_figure(),
                self.events,
                self.event_names_visible
            )
        )
        self.refresh_timer.start(self.MAP_UPDATE_FREQ)

    def _create_layout(
        self,
        layout_class: QtWidgets.QLayout
    ) -> None:
        """Настройка разметки окна"""
        self._main_widget = QtWidgets.QWidget(self)
        self.l = layout_class(self._main_widget)
        self._main_widget.setFocus()
        self.setCentralWidget(self._main_widget)

    def add_widget(
        self,
        widget: QtWidgets.QWidget,
        pos_x: int,
        pos_y: int
    ) -> None:
        """Добавляем виджеты в окно"""
        # Показываем подпись
        self.l.addWidget(
            widget.label,
            pos_y,
            pos_x
        )

        # Показываем саму форму справа от подписи
        self.l.addWidget(
            widget,
            pos_y,
            pos_x + 1
        )

    def add_map(
        self,
        globe_map: GlobeMap
    ) -> None:
        """Добавляем карту в окно"""
        self.l.addWidget(globe_map.canvas, 2, 0, 1, 9)
        self.l.addWidget(globe_map.toolbar, 3, 0, 1, 9)

    def remove_widget(
        self,
        widget: QtWidgets
    ) -> None:
        """Удаляем виджеты из окна"""
        widget.label.setParent(None)
        widget.setParent(None)

    def _create_menu(self) -> None:
        """Создаем меню в верхней части окна"""
        # Раздел `Файл`
        self.file_menu = QtWidgets.QMenu(
            "&Файл",
            self
        )

        # Действие `Выход`
        self.file_menu.addAction(
            "&Выход",
            self.file_quit,
            QtCore.Qt.CTRL + QtCore.Qt.Key_Q
        )

        self.menuBar().addMenu(self.file_menu)

        # Раздел `Фигуры`
        self.figure_menu = QtWidgets.QMenu(
            "&Фигуры",
            self
        )

        # Действие `Эллипс`
        self.figure_menu.addAction(
            "&Эллипс",
            self.ellipse
        )

        # Действие `Прямоугольник`
        self.figure_menu.addAction(
            "&Прямоугольник",
            self.rectangle
        )

        self.menuBar().addMenu(self.figure_menu)

        # Раздел `О программе`
        self.about_menu = QtWidgets.QMenu(
            "&О Программе",
            self
        )

        # Действие `О программе`
        self.about_menu.addAction(
            "&О программе",
            self.about
        )

        # Действие `Инструкция`
        self.about_menu.addAction(
            "&Инструкция",
            self.instruction
        )

        self.menuBar().addMenu(self.about_menu)

        self.title_menu = QtWidgets.QMenu(
            "&Подписи",
            self
        )

        self.title_menu.addAction(
            "&Отобразить/скрыть подписи событий",
            self.toggle_events_titles
        )

        self.menuBar().addMenu(self.title_menu)

    def file_quit(self) -> None:
        """Закрытие окна"""
        self.close()

    def closeEvent(
        self,
        ce: QtGui.QCloseEvent
    ) -> None:
        """Еще одно закрытие окна"""
        self.file_quit()

    def _apply_figure(
        self,
        figure: Figure
    ) -> None:
        """Заменить текущую фигуру для окна"""
        if self.current_figure:
            self.current_figure.clear_window()

        self.current_figure = figure(self)

        self.current_figure.populate_window()

    def ellipse(self) -> None:
        # На карте эллипс
        self._apply_figure(EllipseButton)

    def rectangle(self) -> None:
        # На карте прямоугольник
        self._apply_figure(RectangleButton)

    def about(self) -> None:
        QtWidgets.QMessageBox.about(
            self,
            "О программе",
            """{}\n
            Программа для обработки REB файлов\n
            Разработана под не знаю какой лицензией :3\n\n
            By Zhurik\n
            2019-2020""".format(
                self.window_title
            )
        )

    def instruction(self) -> None:
        """Открываем PDF с документацией"""
        if os.path.exists(self.resources_path + "README.pdf"):
            subprocess.run(
                [
                    "start",
                    self.resources_path + "README.pdf"
                ],
                check=True,
                shell=True
            )

        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Инструкция не найдена",
                "Не могу показать инструкцию"
            )

    def toggle_events_titles(self) -> None:
        """Включаем и выключаем подписи событий"""
        self.event_names_visible = not self.event_names_visible

        self.map.update(
            self.instruments.get_stations(),
            self.current_figure.get_figure(),
            self.events,
            self.event_names_visible
        )
