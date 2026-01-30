"""Charts and dashboard."""

from .charts import (
    plot_comparison,
    plot_price_with_indicators,
    plot_rsi,
    plot_volume,
)


def run_dashboard() -> None:
    """Run the Streamlit dashboard. Lazy import so streamlit is only required when used."""
    from .dashboard import run
    run()


__all__ = [
    "plot_comparison",
    "plot_price_with_indicators",
    "plot_rsi",
    "plot_volume",
    "run_dashboard",
]
