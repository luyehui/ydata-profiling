from ydata_profiling.report.presentation.core.root import Root
from ydata_profiling.report.presentation.flavours.html import templates
from ydata_profiling.utils.translations import get_translations


class HTMLRoot(Root):
    def render(self, **kwargs) -> str:
        nav_items = [
            (section.name, section.anchor_id)
            for section in self.content["body"].content["items"]
        ]

        # Get language from config or default to English
        language = kwargs.get("language", "en")
        translations = get_translations(language).dict()

        # Remove language from kwargs to avoid duplicate parameter
        render_kwargs = {k: v for k, v in kwargs.items() if k != "language"}

        return templates.template("report.html").render(
            **self.content, 
            nav_items=nav_items, 
            language=language,
            t=translations,
            **render_kwargs
        )
