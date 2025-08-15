from ydata_profiling.report.presentation.core.alerts import Alerts
from ydata_profiling.report.presentation.flavours.html import templates
from ydata_profiling.utils.styles import get_alert_styles
from ydata_profiling.utils.translations import get_translations
from ydata_profiling.model.alerts import get_alert_language


class HTMLAlerts(Alerts):
    def render(self, **kwargs) -> str:
        styles = get_alert_styles()
        
        # Get language from kwargs, global setting, or default to English
        language = get_alert_language()
        translations = get_translations(language).dict()

        return templates.template("alerts.html").render(
            **self.content, 
            styles=styles,
            t=translations,
            language=language
        )
