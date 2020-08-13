from matplotlib import axes
from cartopy.crs import Projection

from area_shapes import AreaShape


class TestingArea:
    """Данные испытательного полигона"""
    def __init__(
        self,
        name: str,
        country: str,
        shape: AreaShape
    ) -> None:
        self.name = name
        self.country = country
        self.shape = shape

    def __hash__(self) -> int:
        return hash(
            (
                hash(self.name),
                hash(self.country),
                hash(self.shape)
            )
        )

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection
    ) -> None:
        """Отрисовка полигона на карте"""
        self.shape.draw_on_map(
            ax,
            projection,
            self.name
        )

    def __eq__(
        self,
        other: "TestingArea"
    ) -> bool:
        if self.name != other.name:
            return False

        if self.country != other.country:
            return False

        if self.shape != other.shape:
            return False

        return True

    def __ne__ (
        self,
        other: "TestingArea"
    ) -> bool:
        return not self == other
