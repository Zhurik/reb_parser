from matplotlib import axes
from cartopy.crs import Projection
from matplotlib.transforms import offset_copy
import json
from typing import List

from area_shapes import AreaDot, AreaRectangle

from testing_area import TestingArea


class Station:
    """Данные станции"""

    TEXT_OFFSET = -25
    MARKER_SIZE = 7
    MARKER_TRANSPARENCY = 0.7
    TEXT_BOX_TRANSPARENCY = 0.5

    def __init__(
        self,
        name: str,
        latitude: float,
        longtitude: float,
        testing_areas: List[TestingArea],
        symbol="g^"
    ) -> None:
        self.name = name
        self.latitude = latitude
        self.longtitude = longtitude
        self.testing_areas = testing_areas
        self.symbol = symbol

    def __str__(self) -> str:
        return "Station: " + self.name

    @staticmethod
    def load_from_json(json_path: str) -> List["Station"]:
        """Формируем список станций из json"""
        with open(json_path, "r", encoding="utf-8") as file:
            stations = json.load(file)

        stations_list = []
        for station in stations:
            testing_areas = []
            for area in station["testing_areas"]:
                if area["type"] == "square":
                    testing_areas.append(
                        TestingArea(
                            area["name"],
                            area["country"],
                            AreaRectangle(
                                area["lat1"],
                                area["lat2"],
                                area["long1"],
                                area["long2"]
                            )
                        )
                    )

                elif area["type"] == "dot":
                    testing_areas.append(
                        TestingArea(
                            area["name"],
                            area["country"],
                            AreaDot(
                                area["lat"],
                                area["long"]
                            )
                        )
                    )

                else:
                    # Если непонятный тип полигона, то не добавляем его
                    pass

            stations_list.append(
                Station(
                    station["name"],
                    station["lat"],
                    station["long"],
                    testing_areas
                )
            )

        return stations_list

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection
    ) -> None:
        """Отрисовываем станцию и ее полигоны на карте"""
        # Отрисовываем сам полигон
        ax.plot(
            self.longtitude,
            self.latitude,
            self.symbol,
            markersize=self.MARKER_SIZE,
            alpha=self.MARKER_TRANSPARENCY,
            transform=projection
        )

        # Рисуем подпись слева от полигона
        ax.text(
            self.longtitude,
            self.latitude,
            self.name,
            verticalalignment="center",
            horizontalalignment="right",
            transform=offset_copy(
                projection._as_mpl_transform(ax),
                units="dots",
                x=self.TEXT_OFFSET
            ),
            bbox=dict(
                alpha=self.TEXT_BOX_TRANSPARENCY,
                boxstyle="round"
            )
        )
