import reflex as rx
import numpy as np
import asyncio
from datetime import datetime
import urllib3
import json
import logging
from typing import TypedDict, Literal

DEFAULT_CONFIG = {
    "api_endpoints": {
        "mexc": "https://api.mexc.com/api/v3/ticker/price?symbol=XAUTUSDT",
        "edelmetalle": "https://api.edelmetalle.de/public.json",
    },
    "data_settings": {"data_point_count_limit": 50, "update_interval_seconds": 5},
}
config = DEFAULT_CONFIG
API_ENDPOINTS = config["api_endpoints"]
DATA_SETTINGS = config["data_settings"]


class PricePoint(TypedDict):
    time: str
    price_a: float | None
    price_b: float | None


def get_data() -> PricePoint:
    """Fetch price data from MEXC and Edelmetalle APIs."""
    http = urllib3.PoolManager()
    price_mexc = None
    price_gold_de = None
    try:
        r = http.request("GET", API_ENDPOINTS["mexc"])
        if r.status == 200:
            data_mexc = json.loads(r.data.decode("utf-8"))
            price_mexc = float(data_mexc["price"])
    except Exception as e:
        logging.exception(f"Error fetching MEXC data: {e}")
    try:
        r = http.request("GET", API_ENDPOINTS["edelmetalle"])
        if r.status == 200:
            data_gold_de = json.loads(r.data.decode("utf-8"))
            price_gold_de = float(data_gold_de["gold_usd"])
    except Exception as e:
        logging.exception(f"Error fetching Edelmetalle data: {e}")
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "price_a": price_mexc,
        "price_b": price_gold_de,
    }


class TimeSeriesState(rx.State):
    data: list[PricePoint] = []
    last_updated: str = ""
    _data_point_count: int = DATA_SETTINGS["data_point_count_limit"]
    _update_interval: int = DATA_SETTINGS["update_interval_seconds"]

    def _generate_initial_data(self):
        """Helper to generate initial time series data."""
        initial_data = []
        for _ in range(3):
            point = get_data()
            initial_data.append(point)
        self.data = initial_data
        self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event
    def on_load(self):
        """Event handler for page load."""
        self._generate_initial_data()
        return TimeSeriesState.update_data

    @rx.event(background=True)
    async def update_data(self):
        """Background task to update time series data."""
        while True:
            await asyncio.sleep(self._update_interval)
            async with self:
                new_point = get_data()
                if new_point["price_a"] is None:
                    if self.data and self.data[-1]["price_a"] is not None:
                        new_point["price_a"] = self.data[-1]["price_a"]
                if new_point["price_b"] is None:
                    if self.data and self.data[-1]["price_b"] is not None:
                        new_point["price_b"] = self.data[-1]["price_b"]
                current_data = self.data
                if len(current_data) >= self._data_point_count:
                    current_data = current_data[1:]
                if new_point["price_a"] is not None or new_point["price_b"] is not None:
                    self.data = current_data + [new_point]
                self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")