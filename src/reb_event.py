from matplotlib import axes
from cartopy.crs import Projection
from matplotlib.transforms import offset_copy


class Event:
    """Событие REB"""

    MARKER_SIZE = 2
    MARKER_TRANSPARENCY = 0.7

    TEXT_OFFSET = -15
    TEXT_BOX_TRANSPARENCY = 0.5
    FONTSIZE = 6

    def __init__(
        self,
        data: str,
        latitude: float,
        longtitude: float
    ) -> None:
        self.data = data
        self.latitude = latitude
        self.longtitude = longtitude
        self.event = data.split("\n")[0].split()[1]

        if len(data.split("\n")[0].split()) == 2:
            self.date = data.split("\n")[4].split()[0]
        else:
            self.date = data.split("\n")[2].split()[0]

    def draw_on_map(
        self,
        ax: axes,
        projection: Projection,
        show_names: bool
    ) -> None:
        """Отрисовка события на карте"""
        ax.plot(
            self.longtitude,
            self.latitude,
            marker="o",
            color="red",
            markersize=self.MARKER_SIZE,
            alpha=self.MARKER_TRANSPARENCY,
            transform=projection
        )

        if show_names:
            ax.text(
                self.longtitude,
                self.latitude,
                self.event + "\n" + self.date,
                fontsize=self.FONTSIZE,
                verticalalignment="center",
                horizontalalignment="right",
                transform=offset_copy(
                    projection._as_mpl_transform(ax),
                    units="dots",
                    y=self.TEXT_OFFSET
                ),
                bbox=dict(
                    alpha=self.TEXT_BOX_TRANSPARENCY,
                    boxstyle="round"
                )
            )
