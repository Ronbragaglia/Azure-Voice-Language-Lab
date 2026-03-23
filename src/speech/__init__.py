"""
Speech Module
=============

Módulo para funcionalidades de fala do Azure Speech Service.

Inclui:
- SpeechRecognition: Reconhecimento de fala (Speech-to-Text)
- TextToSpeech: Síntese de voz (Text-to-Speech)
"""

from .recognition import SpeechRecognition
from .synthesis import TextToSpeech

__all__ = ["SpeechRecognition", "TextToSpeech"]
