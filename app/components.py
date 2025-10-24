import reflex as rx
from app.state import TimeSeriesState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "#FFFFFF",
        "border": "1px solid #E0E0E0",
        "border_radius": "8px",
        "box_shadow": "0px 1px 3px rgba(0,0,0,0.12)",
        "font_family": "Roboto",
        "font_size": "14px",
    },
    "label_style": {"color": "#212121", "font_weight": "500"},
    "item_style": {"color": "#00796B"},
    "separator": ": ",
}


def legend_item(color: str, name: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name=f"w-3 h-3 rounded-sm bg-[{color}]"),
        rx.el.span(name, class_name="text-sm text-gray-600 font-medium"),
        class_name="flex items-center gap-2",
    )


def chart_card(title: str, data: rx.Var[list[dict]]) -> rx.Component:
    """A card component to display a time series chart."""
    return rx.el.div(
        rx.el.div(
            rx.el.h2(title, class_name="text-lg font-medium text-gray-800"),
            rx.el.div(
                legend_item("#009688", "XAUT"),
                legend_item("#607D8B", "Gold USD"),
                class_name="flex items-center gap-4",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                horizontal=True,
                vertical=False,
                stroke="#E0E0E0",
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="time",
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                font_size="12px",
                font_family="Roboto",
                color="#757575",
            ),
            rx.recharts.y_axis(
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                font_size="12px",
                font_family="Roboto",
                color="#757575",
                domain=["auto", "auto"],
                allow_decimals=False,
            ),
            rx.recharts.area(
                data_key="price_a",
                name="XAUT",
                type_="monotone",
                stroke="#009688",
                fill="rgba(0, 150, 136, 0.2)",
                stroke_width=2,
                dot=True,
                active_dot={
                    "r": 6,
                    "stroke_width": 2,
                    "stroke": "#FFFFFF",
                    "fill": "#009688",
                },
            ),
            rx.recharts.area(
                data_key="price_b",
                name="Gold USD",
                type_="monotone",
                stroke="#607D8B",
                fill="rgba(96, 125, 139, 0.2)",
                stroke_width=2,
                dot=True,
                active_dot={
                    "r": 6,
                    "stroke_width": 2,
                    "stroke": "#FFFFFF",
                    "fill": "#607D8B",
                },
            ),
            data=data,
            height=300,
            margin={"top": 5, "right": 20, "left": -10, "bottom": 5},
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
        class_name="w-full p-6 bg-white shadow-[0px_8px_16px_rgba(0,0,0,0.2)]",
    )