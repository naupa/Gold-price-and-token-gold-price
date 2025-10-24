import reflex as rx
from app.state import TimeSeriesState
import json
import logging

DEFAULT_CONFIG = {
    "chart_config": {
        "series": {
            "price_a": {
                "name": "XAU/USDT",
                "stroke": "#3b82f6",
                "fill": "rgba(59, 130, 246, 0.2)",
            },
            "price_b": {
                "name": "Gold/USD",
                "stroke": "#f97316",
                "fill": "rgba(249, 115, 22, 0.2)",
            },
        },
        "tooltip_props": {
            "cursor": False,
            "content_style": {
                "backgroundColor": "#FFFFFF",
                "border": "1px solid #E5E7EB",
                "borderRadius": "0.75rem",
                "boxShadow": "0px 1px 3px rgba(0,0,0,0.12)",
            },
            "label_style": {"fontWeight": "600", "color": "#1F2937"},
        },
        "grid_stroke": "#e5e7eb",
        "height": 300,
        "margin": {"top": 5, "right": 20, "left": -10, "bottom": 5},
    }
}
config = DEFAULT_CONFIG
CHART_CONFIG = config["chart_config"]
SERIES_CONFIG = CHART_CONFIG["series"]
TOOLTIP_PROPS = CHART_CONFIG["tooltip_props"]


def legend_item(color: str, name: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name=f"w-3 h-3 rounded-sm {color}"),
        rx.el.span(name, class_name="text-sm text-gray-600 font-medium"),
        class_name="flex items-center gap-2",
    )


def chart_card(title: str, data: rx.Var[list[dict]]) -> rx.Component:
    """A card component to display a time series chart."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(title, class_name="text-lg font-medium text-gray-800"),
            rx.el.div(
                legend_item("bg-blue-500", "XAU/USDT"),
                legend_item("bg-orange-500", SERIES_CONFIG["price_b"]["name"]),
                class_name="flex items-center gap-4",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                horizontal=True,
                vertical=False,
                stroke=CHART_CONFIG["grid_stroke"],
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="time",
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                custom_attrs={"fontSize": "12px"},
            ),
            rx.recharts.y_axis(
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                domain=["auto", "auto"],
                allow_decimals=False,
                custom_attrs={"fontSize": "12px"},
            ),
            rx.recharts.area(
                data_key="price_a",
                name=SERIES_CONFIG["price_a"]["name"],
                type_="monotone",
                stroke=SERIES_CONFIG["price_a"]["stroke"],
                fill=SERIES_CONFIG["price_a"]["fill"],
                stroke_width=2,
                dot=True,
                active_dot={
                    "r": 6,
                    "stroke_width": 2,
                    "stroke": "#FFFFFF",
                    "fill": SERIES_CONFIG["price_a"]["stroke"],
                },
            ),
            rx.recharts.area(
                data_key="price_b",
                name=SERIES_CONFIG["price_b"]["name"],
                type_="monotone",
                stroke=SERIES_CONFIG["price_b"]["stroke"],
                fill=SERIES_CONFIG["price_b"]["fill"],
                stroke_width=2,
                dot=True,
                active_dot={
                    "r": 6,
                    "stroke_width": 2,
                    "stroke": "#FFFFFF",
                    "fill": SERIES_CONFIG["price_b"]["stroke"],
                },
            ),
            data=data,
            height=CHART_CONFIG["height"],
            margin=CHART_CONFIG["margin"],
            class_name="[&_.recharts-tooltip-cursor]:stroke-gray-300",
        ),
        class_name="bg-white rounded-2xl p-6 shadow-[0px_1px_3px_rgba(0,0,0,0.12)] hover:shadow-[0px_4px_8px_rgba(0,0,0,0.15)] transition-shadow duration-300",
    )


def difference_chart_card(title: str, data: rx.Var[list[dict]]) -> rx.Component:
    """A card component to display the difference chart."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(title, class_name="text-lg font-medium text-gray-800"),
            rx.el.div(
                legend_item("bg-teal-500", "Relative Difference (%)"),
                class_name="flex items-center gap-4",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                horizontal=True,
                vertical=False,
                stroke=CHART_CONFIG["grid_stroke"],
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="time",
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                custom_attrs={"fontSize": "12px"},
            ),
            rx.recharts.y_axis(
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                domain=[-0.75, 0.75],
                allow_decimals=True,
                custom_attrs={"fontSize": "12px"},
            ),
            rx.recharts.area(
                data_key="relative",
                name="Relative Difference",
                type_="monotone",
                stroke="#14b8a6",
                fill="rgba(20, 184, 166, 0.2)",
                stroke_width=2,
                dot=True,
                active_dot={
                    "r": 6,
                    "stroke_width": 2,
                    "stroke": "#FFFFFF",
                    "fill": "#14b8a6",
                },
            ),
            data=data,
            height=CHART_CONFIG["height"],
            margin=CHART_CONFIG["margin"],
            class_name="[&_.recharts-tooltip-cursor]:stroke-gray-300",
        ),
        class_name="bg-white rounded-2xl p-6 shadow-[0px_1px_3px_rgba(0,0,0,0.12)] hover:shadow-[0px_4px_8px_rgba(0,0,0,0.15)] transition-shadow duration-300",
    )


def header() -> rx.Component:
    """The header component for the dashboard."""
    return rx.el.header(
        rx.el.div(
            rx.el.h1(
                "Real-Time Time Series Dashboard",
                class_name="text-2xl font-medium text-gray-900",
            ),
            rx.el.div(
                rx.icon("upload", class_name="mr-2 h-5 w-5 text-gray-500"),
                rx.el.span(
                    "Last updated: ", class_name="text-sm text-gray-600 font-medium"
                ),
                rx.el.span(
                    TimeSeriesState.last_updated,
                    class_name="text-sm text-gray-800 font-semibold",
                ),
                class_name="flex items-center",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center w-full",
        ),
        class_name="w-full p-6 bg-white border-b border-gray-200",
    )