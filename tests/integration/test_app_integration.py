import pytest
import tkinter as tk
from carbon_app import CarbonApp
from pollution_map import PollutionMapPage

@pytest.fixture
def tk_root():
    root = tk.Tk()
    yield root
    root.destroy()

def test_carbon_app_initialization(tk_root):
    app = CarbonApp(tk_root, tk_root)
    assert hasattr(app, "create_widgets")
    assert hasattr(app, "fetch_data")
    assert hasattr(app, "fetch_forecast_data")

def test_pollution_map_page_initialization(tk_root):
    page = PollutionMapPage(tk_root, None)
    assert hasattr(page, "on_map_click")
    assert hasattr(page, "get_pollution_level")
