from PyQt5 import QtWidgets

from figures import Figure, Ellipse, Rectangle

from fields import NumberField


class FigureButton:
    """Базовый класс для кнопки фигуры"""
    def __init__(
        self,
        parent: QtWidgets.QMainWindow
    ) -> None:
        raise NotImplementedError

    def populate_window(self) -> None:
        """Собирает на экране необходимые элементы управления"""
        raise NotImplementedError

    def clear_window(self) -> None:
        """Убирает с экрана элементы управления"""
        raise NotImplementedError

    def get_figure(self) -> Figure:
        """Собирает данные с элементов управления и возвращает нужную фигуру"""
        raise NotImplementedError


class RectangleButton(FigureButton):
    """Кнопка для простого прямоугольника"""
    def __init__(
        self,
        parent: QtWidgets.QMainWindow
    ) -> None:
        self.parent = parent

        self.field_lat_1 = NumberField(
            "Верхняя граница",
            10,
            -90,
            90
        )

        self.field_lat_2 = NumberField(
            "Нижняя граница",
            -10,
            -90,
            90
        )

        self.field_long_1 = NumberField(
            "Левая граница",
            -10,
            -180,
            180
        )

        self.field_long_2 = NumberField(
            "Правая граница",
            10,
            -180,
            180
        )

    def populate_window(self) -> None:
        """Собирает на экране необходимые элементы управления"""
        self.parent.add_widget(
            self.field_lat_1,
            0,
            0
        )

        self.parent.add_widget(
            self.field_lat_2,
            0,
            1
        )

        self.parent.add_widget(
            self.field_long_1,
            2,
            0
        )

        self.parent.add_widget(
            self.field_long_2,
            2,
            1
        )

    def clear_window(self) -> None:
        """Убирает с экрана элементы управления"""
        self.parent.remove_widget(self.field_lat_1)
        self.parent.remove_widget(self.field_lat_2)
        self.parent.remove_widget(self.field_long_1)
        self.parent.remove_widget(self.field_long_2)

    def get_figure(self) -> Rectangle:
        """Собирает данные и возвращает готовый Rectangle"""
        return Rectangle(
            max(
                self.field_lat_1.get_data(),
                self.field_lat_2.get_data(),
            ),
            min(
                self.field_lat_1.get_data(),
                self.field_lat_2.get_data(),
            ),
            min(
                self.field_long_1.get_data(),
                self.field_long_2.get_data(),
            ),
            max(
                self.field_long_1.get_data(),
                self.field_long_2.get_data(),
            )
        )


class EllipseButton(FigureButton):
    """Кнопка эллипса"""
    def __init__(
        self,
        parent: QtWidgets.QMainWindow
    ) -> None:
        self.parent = parent

        self.field_par_a = NumberField(
            "Параметр a",
            10,
            1,
            100
        )

        self.field_par_b = NumberField(
            "Параметр b",
            5,
            1,
            100
        )

        self.field_par_phi = NumberField(
            "Угол наклона",
            45,
            -90,
            90
        )

        self.field_lat = NumberField(
            "Широта центра",
            0,
            -90,
            90
        )

        self.field_long = NumberField(
            "Долгота центра",
            0,
            -180,
            180
        )

    def populate_window(self) -> None:
        """Собирает на экране необходимые элементы управления"""
        self.parent.add_widget(
            self.field_par_a,
            0,
            0
        )

        self.parent.add_widget(
            self.field_par_b,
            0,
            1
        )

        self.parent.add_widget(
            self.field_par_phi,
            2,
            0
        )

        self.parent.add_widget(
            self.field_lat,
            4,
            0
        )

        self.parent.add_widget(
            self.field_long,
            4,
            1
        )

    def clear_window(self) -> None:
        """Убирает с экрана элементы управления"""
        self.parent.remove_widget(self.field_par_a)
        self.parent.remove_widget(self.field_par_b)
        self.parent.remove_widget(self.field_par_phi)
        self.parent.remove_widget(self.field_lat)
        self.parent.remove_widget(self.field_long)

    def get_figure(self) -> Ellipse:
        """Собирает данные и возвращает готовый Ellipse"""
        return Ellipse(
            max(
                self.field_par_a.get_data(),
                self.field_par_b.get_data(),
            ),
            min(
                self.field_par_a.get_data(),
                self.field_par_b.get_data(),
            ),
            self.field_par_phi.get_data(),
            self.field_lat.get_data(),
            self.field_long.get_data()
        )
