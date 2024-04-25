import tempfile

import geopandas as gpd  # type: ignore
import matplotlib.pyplot as plt
from PIL import Image
from rich_pixels import Pixels
from textual import work
from textual.widgets import Static
from textual.worker import get_current_worker


class Map(Static):
    def __init__(
        self,
        geodataframe: gpd.GeoDataFrame,
        column: str | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        self.geodataframe = geodataframe
        self.column = column
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def on_mount(self) -> None:
        self.draw_map()

    @work(thread=True)
    def draw_map(self) -> None:
        worker = get_current_worker()
        temp_image_file = tempfile.TemporaryFile()
        # Create Choropleth map if required
        ax = self.geodataframe.plot()  # type: ignore
        # Remove axis labels
        ax.set_axis_off()
        # Save as temporory image
        plt.savefig(temp_image_file, bbox_inches="tight", transparent="True")

        with Image.open(temp_image_file) as image:
            size_ratio = image.width / self.size.width
            new_width = int(image.width / size_ratio)
            new_height = int(image.height / size_ratio)
            resized_image = image.resize(
                (new_width, new_height),
                Image.Resampling.NEAREST,
            )
            pixels = Pixels.from_image(resized_image)

        if not worker.is_cancelled:
            self.app.call_from_thread(self.update, pixels)
