import warnings

import geopandas as gpd  # type: ignore
from textual.app import App, ComposeResult

from textual_map import Map

# Ignore that the geopandas.dataset module is deprecated!
warnings.filterwarnings("ignore", category=FutureWarning)


class WorldPopulationApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        world = gpd.read_file(
            gpd.datasets.get_path("naturalearth_lowres"),  # type: ignore
        )
        # Remove Antarctica
        world = world[world["continent"] != "Antarctica"]

        yield Map(world, column="pop_est")


if __name__ == "__main__":
    app = WorldPopulationApp()
    app.run()
