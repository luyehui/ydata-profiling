"""Translation utilities for YData Profiling reports."""

import os
import yaml
from pathlib import Path
from typing import Dict, Optional


class Translations:
    """Translation class for report text."""
    
    def __init__(self, language: str = "en"):
        self.language = language
        self._translations = self._load_translations()
    
    def _load_translations(self) -> Dict[str, str]:
        """Load translations from YAML file."""
        # Get the path to the translations directory
        translations_dir = Path(__file__).parent
        
        # Try to load the specific language file
        language_file = translations_dir / f"{self.language}.yaml"
        
        if language_file.exists():
            try:
                with open(language_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Failed to load translations for {self.language}: {e}")
                return {}
        else:
            # Fallback to English if the language file doesn't exist
            if self.language != "en":
                print(f"Warning: Translation file for {self.language} not found, falling back to English")
                en_file = translations_dir / "en.yaml"
                if en_file.exists():
                    try:
                        with open(en_file, 'r', encoding='utf-8') as f:
                            return yaml.safe_load(f) or {}
                    except Exception as e:
                        print(f"Warning: Failed to load English translations: {e}")
                        return {}
            return {}
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """Get translation for a key."""
        return self._translations.get(key, default or key)
    
    def __getitem__(self, key: str) -> str:
        """Get translation for a key using bracket notation."""
        return self.get(key)

    def dict(self) -> dict[str, str]:
        return self._translations


def get_translations(language: str = "en") -> Translations:
    """Get translations instance for the specified language."""
    return Translations(language)


def translate_text(text: str, language: str = "en") -> str:
    """Translate a text string to the specified language.
    
    This function provides a simple way to translate common text patterns
    that might appear in variable names or other dynamic content.
    
    Args:
        text: The text to translate
        language: The target language ("en" or "zh-CN")
        
    Returns:
        The translated text
    """
    translations = get_translations(language)
    
    # Try to get translation from the main translations first
    translated = translations.get(text)
    if translated != text:
        return translated
    
    # If not found, return the original text
    return text
