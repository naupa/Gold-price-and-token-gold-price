import reflex as rx
import pandas as pd
import numpy as np
import asyncio
from datetime import datetime
import urllib3
import json
import logging


def get_data():
    """Fetch price data from MEXC and Edelmetalle APIs."""
    http = urllib3.PoolManager()
    try:
        r = http.request(
            "GET", "https://api.mexc.com/api/v3/ticker/price?symbol=XAUTUSDT"
        )
        if r.status == 200:
            data_mexc = json.loads(r.data.decode("utf-8"))
            price_mexc = float(data_mexc["price"])
        else:
            price_mexc = np.nan
    except Exception as e:
        logging.exception(f"Error fetching MEXC data: {e}")
        price_mexc = np.nan
    try:
        r = http.request("GET", "https://api.edelmetalle.de/public.json")
        if r.status == 200:
            data_gold_de = json.loads(r.data.decode("utf-8"))
            price_gold_de = float(data_gold_de["gold_usd"])
        else:
            price_gold_de = np.nan
    except Exception as e:
        logging.exception(f"Error fetching Edelmetalle data: {e}")
        price_gold_de = np.nan
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "price_a": price_mexc,
        "price_b": price_gold_de,
    }


class TimeSeriesState(rx.State):
    data: list[dict[str, str | float]] = []
    last_updated: str = ""
    _data_point_count: int = 240

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
        """Background task to update time series data every 5 seconds."""
        while True:
            await asyncio.sleep(5)
            async with self:
                new_point = get_data()
                if np.isnan(new_point["price_a"]):
                    if self.data:
                        new_point["price_a"] = self.data[-1]["price_a"]
                if np.isnan(new_point["price_b"]):
                    if self.data:
                        new_point["price_b"] = self.data[-1]["price_b"]
                current_data = self.data
                if len(current_data) >= self._data_point_count:
                    current_data = current_data[1:]
                self.data = current_data + [new_point]
                self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")