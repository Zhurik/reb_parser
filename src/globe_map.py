import matplotlib.pyplot as plt
from cartopy.crs import Projection, PlateCarree
from matplotlib.image import imread

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from typing import List

from station import Station

from figures import Figure

from reb_event import Event


class GlobeMap:
    """Карта мира"""
    def __init__(
        self,
        window: QtWidgets,
        projection: Projection,
        light: bool,
        resources_path: str,
        *args,
        **kwargs
    ) -> None:
        self.window = window
        self.projection = projection
        self.light = light
        self.resources_path = resources_path
        self.globe = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.globe)
        self.toolbar = NavigationToolbar2QT(
            self.canvas,
            self.window
        )
        self._first_draw()

    def _draw_stock_img(self) -> None:
        """
        Пишем свою версию stock_img, чтобы cartopy не тянула из интернета
        изображения
        """
        self.ax.imshow(
            imread(
                self.resources_path + "50-natural-earth-1-downsampled.png"
            ),
            origin="upper",
            transform=PlateCarree(),
            extent=[
                -180,
                180,
                -90,
                90
            ]
        )

    def _draw_chunks(self) -> None:
        """
        Отрисовываем части карты в высоком разрешении, чтобы
        не так сильно тормозило
        """
        self.ax.imshow(
            imread(
                self.resources_path + "chunks/nevada.jpg"
            ),
            origin="upper",
            transform=PlateCarree(),
            extent=[
                -125,
                -110,
                30,
                45
            ]
        )

        self.ax.imshow(
            imread(
                self.resources_path + "chunks/pungeri.jpg"
            ),
            origin="upper",
            transform=PlateCarree(),
            extent=[
                120,
                135,
                30,
                50
            ]
        )

        self.ax.imshow(
            imread(
                self.resources_path + "chunks/lobnor.jpg"
            ),
            origin="upper",
            transform=PlateCarree(),
            extent=[
                50,
                110,
                20,
                55
            ]
        )

        self.ax.set_global()

    def _first_draw(self) -> None:
        """Инициализация карты"""
        self.window.add_map(self)

        self.globe.clear()

        self.ax = self.globe.add_subplot(
            1,
            1,
            1,
            projection=self.projection
        )

        self._draw_stock_img()
        self.ax.gridlines()

        if not self.light:
            self._draw_chunks()

        self.globe.tight_layout()
        self.canvas.draw()

    def _clear(self) -> None:
        """Очищаем все нарисованное на карте"""
        # Оставляем 2 первых элемента из-за cartopy
        self.ax.patches = self.ax.patches[:2]
        self.ax.texts = list()
        self.ax.lines = list()

    def _draw_stations(
        self,
        stations: List[Station]
    ) -> None:
        """Отображаем полученные станции на карте"""
        testing_areas = set()

        for station in stations:
            station.draw_on_map(self.ax, self.projection)

            # Собираем уникальные полигоны, чтобы не дублировать их на карте
            for area in station.testing_areas:
                testing_areas.add(area)

        for testing_area in testing_areas:
            testing_area.draw_on_map(self.ax, self.projection)

    def _draw_figure(
        self,
        figure: Figure
    ) -> None:
        figure.draw_on_map(self.ax, self.projection)

    def _draw_events(
        self,
        events: List[Event],
        event_names_visible: bool
    ) -> None:
        """Отрисовываем события на карте"""
        for event in events:
            event.draw_on_map(
                self.ax,
                self.projection,
                event_names_visible
            )

    def update(
        self,
        stations: List[Station],
        figure: Figure,
        events: List[Event],
        event_names_visible: bool
    ) -> None:
        """Обновление карты"""
        self._clear()

        self._draw_stations(stations)

        self._draw_figure(figure)

        self._draw_events(events, event_names_visible)

        self.canvas.draw_idle()
