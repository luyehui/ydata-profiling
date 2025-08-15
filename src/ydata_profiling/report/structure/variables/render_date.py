from typing import Any, Dict

from ydata_profiling.config import Settings
from ydata_profiling.report.formatters import fmt, fmt_bytesize, fmt_percent
from ydata_profiling.report.presentation.core import (
    Container,
    Image,
    Table,
    VariableInfo,
)
from ydata_profiling.visualisation.plot import histogram, mini_histogram
from ydata_profiling.utils.translations import get_translations


def render_date(config: Settings, summary: Dict[str, Any]) -> Dict[str, Any]:
    # Get translations
    language = config.html.language
    t = get_translations(language)
    
    varid = summary["varid"]
    template_variables = {}

    image_format = config.plot.image_format

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Date",
        summary["alerts"],
        summary["description"],
        style=config.html.style,
    )

    table1 = Table(
        [
            {
                "name": t.get("distinct", "Distinct"),
                "value": fmt(summary["n_distinct"]),
                "alert": False,
            },
            {
                "name": t.get("distinct_percent", "Distinct (%)"),
                "value": fmt_percent(summary["p_distinct"]),
                "alert": False,
            },
            {
                "name": t.get("missing", "Missing"),
                "value": fmt(summary["n_missing"]),
                "alert": False,
            },
            {
                "name": t.get("missing_percent", "Missing (%)"),
                "value": fmt_percent(summary["p_missing"]),
                "alert": False,
            },
            {
                "name": t.get("memory_size", "Memory size"),
                "value": fmt_bytesize(summary["memory_size"]),
                "alert": False,
            },
        ],
        style=config.html.style,
    )

    table2 = Table(
        [
            {"name": t.get("minimum", "Minimum"), "value": fmt(summary["min"]), "alert": False},
            {"name": t.get("maximum", "Maximum"), "value": fmt(summary["max"]), "alert": False},
            {
                "name": t.get("invalid_dates", "Invalid dates"),
                "value": fmt(summary["n_invalid_dates"]),
                "alert": False,
            },
            {
                "name": t.get("invalid_dates_percent", "Invalid dates (%)"),
                "value": fmt_percent(summary["p_invalid_dates"]),
                "alert": False,
            },
        ],
        style=config.html.style,
    )

    if isinstance(summary["histogram"], list):
        mini_histo = Image(
            mini_histogram(
                config,
                [x[0] for x in summary["histogram"]],
                [x[1] for x in summary["histogram"]],
                date=True,
            ),
            image_format=image_format,
            alt="Mini histogram",
        )
    else:
        mini_histo = Image(
            mini_histogram(
                config, summary["histogram"][0], summary["histogram"][1], date=True
            ),
            image_format=image_format,
            alt="Mini histogram",
        )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    if isinstance(summary["histogram"], list):
        hist_data = histogram(
            config,
            [x[0] for x in summary["histogram"]],
            [x[1] for x in summary["histogram"]],
            date=True,
        )
    else:
        hist_data = histogram(
            config, summary["histogram"][0], summary["histogram"][1], date=True
        )

    # Bottom
    n_bins = len(summary["histogram"][1]) - 1 if summary["histogram"] else 0
    bottom = Container(
        [
            Image(
                hist_data,
                image_format=image_format,
                alt="Histogram",
                caption=f"<strong>{t.get('histogram_fixed_bins_caption', 'Histogram with fixed size bins')}</strong> (bins={n_bins})",
                name=t.get("histogram", "Histogram"),
                anchor_id=f"{varid}histogram",
            )
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    template_variables["bottom"] = bottom

    return template_variables
