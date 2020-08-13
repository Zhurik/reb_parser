from matplotlib import axes
from cartopy.crs import Projection
from matplotlib.transforms import offset_copy
from matplotlib.patches import Rectangle as Rect


class AreaShape:
    """Базовый класс для формы полигонов"""

    TEXT_BOX_TRANSPARENCY = 0.5

    def __init__(self):
        raise NotImplementedError

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection,
        name: str
    ) -> None:
        """Отрисовываем полигон на графике"""
        raise NotImplementedError


class AreaDot(AreaShape):
    """Полигон в форме точки"""

    TEXT_OFFSET = -25
    MARKER_SIZE = 7
    MARKER_TRANSPARENCY = 0.7

    def __init__(
        self,
        latitude: float,
        longtitude: float,
        symbol: str="bs"
    ) -> None:
        self.latitude = latitude
        self.longtitude = longtitude
        self.symbol = symbol

    def __eq__(
        self,
        other: AreaShape
    ) -> bool:
        if type(self) != type(other):
            return False

        if self.latitude != other.latitude:
            return False

        if self.longtitude != other.longtitude:
            return False

        return True

    def __ne__(
        self,
        other: AreaShape
    ) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(
            (
                self.latitude,
                self.longtitude
            )
        )

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection,
        name: str
    ) -> None:
        """Отрисовываем точку на карте"""
        # Рисуем саму точку
        ax.plot(
            self.longtitude,
            self.latitude,
            self.symbol,
            # transform=projection,
            markersize=self.MARKER_SIZE,
            alpha=self.MARKER_TRANSPARENCY
        )

        # Рисуем подпись слева от полигона
        ax.text(
            self.longtitude,
            self.latitude,
            name,
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


class AreaRectangle(AreaShape):
    """Полигон в форме прямоугольника"""

    RGBA_BLUE = (0, 0, 1, 1)
    LINE_WIDTH = 2
    INNER_TRANSPARENCY = 0.4

    def __init__(
        self,
        latitude1: float,
        latitude2: float,
        longtitude1: float,
        longtitude2: float,
        color: str="green"
    ) -> None:
        self.latitude1 = latitude1
        self.latitude2 = latitude2
        self.longtitude1 = longtitude1
        self.longtitude2 = longtitude2
        self.color = color

    def __eq__(
        self,
        other: AreaShape
    ) -> bool:
        if type(self) != type(other):
            return False

        if self.latitude1 != other.latitude1:
            return False

        if self.latitude2 != other.latitude2:
            return False

        if self.longtitude1 != other.longtitude1:
            return False

        if self.longtitude2 != other.longtitude2:
            return False

        return True

    def __ne__(
        self,
        other: AreaShape
    ) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(
            (
                self.latitude1,
                self.latitude2,
                self.longtitude1,
                self.longtitude2,
            )
        )

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection,
        name: str
    ) -> None:
        """Отрисовываем прямоугольник на карте"""
        # Рисуем сам прямоугольник
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
                edgecolor=self.RGBA_BLUE,
                lw=self.LINE_WIDTH
            )
        )

        # Рисуем подпись в центре прямоугольника
        ax.text(
            (self.longtitude1 + self.longtitude2) / 2,
            (self.latitude1 + self.latitude2) / 2,
            name,
            verticalalignment="center",
            horizontalalignment="right",
            transform=projection,
            bbox=dict(
                alpha=self.TEXT_BOX_TRANSPARENCY,
                boxstyle="round"
            )
        )
