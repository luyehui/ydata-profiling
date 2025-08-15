from ydata_profiling.config import Settings
from ydata_profiling.report.formatters import fmt, fmt_bytesize, fmt_percent
from ydata_profiling.report.presentation.core import (
    HTML,
    Container,
    Table,
    VariableInfo,
)
from ydata_profiling.utils.translations import get_translations
from ydata_profiling.model.alerts import get_alert_language


def render_generic(config: Settings, summary: dict) -> dict:
    # Get translations
    language = config.html.language
    t = get_translations(language)
    
    info = VariableInfo(
        anchor_id=summary["varid"],
        alerts=summary["alerts"],
        var_type=summary["cast_type"] or "Unsupported",
        var_name=summary["varname"],
        description=summary["description"],
        style=config.html.style,
    )

    table = Table(
        [
            {
                "name": t.get("missing", "Missing"),
                "value": fmt(summary["n_missing"]),
                "alert": "n_missing" in summary["alert_fields"],
            },
            {
                "name": t.get("missing_percent", "Missing (%)"),
                "value": fmt_percent(summary["p_missing"]),
                "alert": "p_missing" in summary["alert_fields"],
            },
            {
                "name": t.get("memory_size", "Memory size"),
                "value": fmt_bytesize(summary["memory_size"]),
                "alert": False,
            },
        ],
        style=config.html.style,
    )

    return {
        "top": Container([info, table, HTML("")], sequence_type="grid"),
        "bottom": None,
    }
