"""
Azure Voice Language Lab
========================

Um laboratório completo para exploração de Azure Speech e Language Studio.

Este pacote fornece funcionalidades para:
- Reconhecimento de fala (Speech-to-Text)
- Síntese de voz (Text-to-Speech)
- Análise de texto (NLP)
- Tradução de texto
- Detecção de idioma
- Análise de sentimento
- Extração de entidades

Author: Rone Bragaglia
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Rone Bragaglia"
__license__ = "MIT"

from .speech import SpeechRecognition, TextToSpeech
from .language import TextAnalysis, Translation, LanguageDetection

__all__ = [
    "SpeechRecognition",
    "TextToSpeech",
    "TextAnalysis",
    "Translation",
    "LanguageDetection",
]
