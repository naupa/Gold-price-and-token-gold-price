import reflex as rx
from app.state import TimeSeriesState
from app.components import chart_card, header, difference_chart_card


def index() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.div(
                chart_card("Real-Time Price Feed", TimeSeriesState.data),
                difference_chart_card(
                    "Price Difference (Absolute & Relative)",
                    TimeSeriesState.difference_data,
                ),
                class_name="w-full space-y-6",
            ),
            class_name="p-8 w-full max-w-7xl mx-auto",
        ),
        on_mount=TimeSeriesState.on_load,
        class_name="min-h-screen bg-gray-50 font-['Roboto']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)