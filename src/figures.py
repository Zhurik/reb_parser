import math
from matplotlib import axes
from cartopy.crs import Projection

import numpy as np

from matplotlib.patches import Rectangle as Rect
from matplotlib.patches import Ellipse as Ell


class Figure:
    """
    Базовый класс для фигур, которые могут быть использованы,
    для выборки событий в REB данных
    """

    RGBA_RED = (1, 0, 0, 1)
    LINE_WIDTH = 2
    INNER_TRANSPARENCY = 0.2

    def __init__(
        self,
        color: str="red"
    ) -> None:
        self.color = color

    def check_inside(
        self,
        latitude: float,
        longtitude: float
    ) -> float:
        """Проверка попадания координат в заданную фигуру"""
        raise NotImplementedError

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection
    ) -> None:
        """Отрисовка фигуры на графике"""
        raise NotImplementedError


class Rectangle(Figure):
    """
    Простой прямоугольник
    
    latitude1 - верхняя граница  
    latitude2 - нижняя граница  
    longtitude1 - левая граница  
    longtitude2 - правая граница
    """
    def __init__(
        self,
        latitude1: float,
        latitude2: float,
        longtitude1: float,
        longtitude2: float,
        *args,
        **kwargs
    ) -> None:
        super().__init__(self, *args, **kwargs)
        self.latitude1 = latitude1
        self.latitude2 = latitude2
        self.longtitude1 = longtitude1
        self.longtitude2 = longtitude2

    def check_inside(
        self,
        latitude: float,
        longtitude: float
    ) -> bool:
        """Проверка попадания координат в прямоугольник"""
        if self.latitude1 >= latitude >= self.latitude2 and \
            self.longtitude1 <= longtitude <= self.longtitude2:
            return True
        else:
            return False

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection
    ) -> None:
        """Отрисовка прямоугольника на графике"""
        ax.add_patch(
            Rect(
                (
                    self.longtitude1,
                    self.latitude2
                ),
                self.longtitude2 - self.longtitude1,
                self.latitude1 - self.latitude2,
                # transform=projection,
                alpha=self.INNER_TRANSPARENCY,
                edgecolor=self.RGBA_RED,
                lw=self.LINE_WIDTH
            )
        )


class Ellipse(Figure):
    """
    Эллипс
    
    a, b - параметры эллипса, где a > b  
    phi - угол поворота эллипса  
    latitude - широта центра эллипса  
    longtitude - долгота центра эллипса
    """
    def __init__(
        self,
        a: float,
        b: float,
        phi: float,
        latitude: float,
        longtitude: float,
        *args,
        **kwargs
    ) -> None:
        super().__init__(self, *args, **kwargs)
        self.a = a
        self.b = b
        self.phi = phi
        self.latitude = latitude
        self.longtitude = longtitude

    def check_inside(
        self,
        latitude: float,
        longtitude: float
    ) -> bool:
        """Проверка попадания координат в эллипс"""
        x = (
            math.cos(math.radians(self.phi)) * (longtitude - self.longtitude) \
                + math.sin(math.radians(self.phi)) * (latitude - self.latitude)
        ) ** 2 / (self.a ** 2)

        y = (
            math.sin(math.radians(self.phi)) * (longtitude - self.longtitude) \
                - math.cos(math.radians(self.phi)) * (latitude - self.latitude)
        ) ** 2 / (self.b ** 2)

        return x + y <= 1

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection
    ) -> None:
        """Отрисовка эллипса на графике"""
        ax.add_patch(
            Ell(
                (
                    self.longtitude,
                    self.latitude
                ),
                self.a * 2,
                self.b * 2,
                angle=self.phi,
                # transform=projection,
                alpha=self.INNER_TRANSPARENCY,
                edgecolor=self.RGBA_RED,
                lw=self.LINE_WIDTH
            )
        )
