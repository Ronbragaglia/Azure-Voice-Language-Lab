"""
Language Module
===============

Módulo para funcionalidades de linguagem do Azure Language Service.

Inclui:
- TextAnalysis: Análise de texto (sentimento, entidades, frases-chave)
- Translation: Tradução de texto
- LanguageDetection: Detecção de idioma
"""

from .analysis import TextAnalysis
from .translation import Translation
from .detection import LanguageDetection

__all__ = ["TextAnalysis", "Translation", "LanguageDetection"]
