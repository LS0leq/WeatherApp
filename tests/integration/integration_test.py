import pytest
import tkinter as tk
from pollution_map import PollutionMapPage


@pytest.fixture
def tk_root():
    root = tk.Tk()
    yield root
    root.destroy()


def test_pollution_map_click_fetches_data(tk_root):
    # tworzy strone mapy
    page = PollutionMapPage(tk_root, controller=None)

    # wybiera na mapie koordynaty warszawy
    page.on_map_click(52.2297, 21.0122)

    # Sprawdza czy jest info na etykiecie info_text
    info_text = page.info_text.cget("text")

    # Testuje dane ktore wyswietlamy
    assert "Temperatura" in info_text
    assert "CO" in info_text
    assert "PM2.5" in info_text
    assert "Zagrożenie" in info_text
