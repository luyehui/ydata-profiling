from ydata_profiling.model.alerts import get_alert_language
from ydata_profiling.report.presentation.core import Dropdown
from ydata_profiling.report.presentation.flavours.html import templates
from ydata_profiling.utils.translations import get_translations


class HTMLDropdown(Dropdown):
    def render(self) -> str:
        language = get_alert_language()
        translations = get_translations(language).dict()
        return templates.template("dropdown.html").render(**self.content, t=translations, language=language)
