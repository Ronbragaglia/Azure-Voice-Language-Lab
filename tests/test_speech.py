"""
Azure Voice Language Lab - Testes de Speech
===========================================

Testes unitários para os módulos de fala (Speech).
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.speech import SpeechRecognition, TextToSpeech


@pytest.mark.speech
class TestSpeechRecognition:
    """Testes para a classe SpeechRecognition."""

    def test_initialization(self):
        """Testa inicialização do reconhecimento de fala."""
        recognizer = SpeechRecognition("test_key", "test_region", "pt-BR")
        assert recognizer.speech_key == "test_key"
        assert recognizer.service_region == "test_region"
        assert recognizer.language == "pt-BR"

    def test_set_language(self):
        """Testa mudança de idioma."""
        recognizer = SpeechRecognition("test_key", "test_region", "pt-BR")
        recognizer.set_language("en-US")
        assert recognizer.language == "en-US"

    @patch('src.speech.recognition.speechsdk')
    def test_recognize_from_file_success(self, mock_speechsdk):
        """Testa reconhecimento de fala de arquivo com sucesso."""
        # Mock do resultado
        mock_result = Mock()
        mock_result.reason = 1  # RecognizedSpeech
        mock_result.text = "Olá, mundo!"
        mock_speechsdk.ResultReason.RecognizedSpeech = 1

        # Mock do recognizer
        mock_recognizer = Mock()
        mock_recognizer.recognize_once.return_value = mock_result
        mock_speechsdk.SpeechRecognizer.return_value = mock_recognizer
        mock_speechsdk.AudioConfig = Mock()

        recognizer = SpeechRecognition("test_key", "test_region", "pt-BR")
        result = recognizer.recognize_from_file("test.wav")

        assert result['status'] == 'success'
        assert result['text'] == "Olá, mundo!"
        assert result['language'] == "pt-BR"

    @patch('src.speech.recognition.speechsdk')
    def test_recognize_from_file_no_match(self, mock_speechsdk):
        """Testa reconhecimento de fala sem match."""
        # Mock do resultado
        mock_result = Mock()
        mock_result.reason = 0  # NoMatch
        mock_speechsdk.ResultReason.NoMatch = 0
        mock_speechsdk.ResultReason.RecognizedSpeech = 1

        # Mock do recognizer
        mock_recognizer = Mock()
        mock_recognizer.recognize_once.return_value = mock_result
        mock_speechsdk.SpeechRecognizer.return_value = mock_recognizer
        mock_speechsdk.AudioConfig = Mock()

        recognizer = SpeechRecognition("test_key", "test_region", "pt-BR")
        result = recognizer.recognize_from_file("test.wav")

        assert result['status'] == 'no_match'
        assert result['text'] == ""


@pytest.mark.speech
class TestTextToSpeech:
    """Testes para a classe TextToSpeech."""

    def test_initialization(self):
        """Testa inicialização da síntese de voz."""
        synthesizer = TextToSpeech("test_key", "test_region", "pt-BR-FranciscaNeural")
        assert synthesizer.speech_key == "test_key"
        assert synthesizer.service_region == "test_region"
        assert synthesizer.voice_name == "pt-BR-FranciscaNeural"

    def test_set_voice(self):
        """Testa mudança de voz."""
        synthesizer = TextToSpeech("test_key", "test_region", "pt-BR-FranciscaNeural")
        synthesizer.set_voice("en-US-JennyNeural")
        assert synthesizer.voice_name == "en-US-JennyNeural"

    def test_get_available_voices(self):
        """Testa obtenção de vozes disponíveis."""
        synthesizer = TextToSpeech("test_key", "test_region")
        voices = synthesizer.get_available_voices()

        assert "pt-BR" in voices
        assert "en-US" in voices
        assert len(voices["pt-BR"]) > 0
        assert "pt-BR-FranciscaNeural" in voices["pt-BR"]

    def test_list_voices_by_language(self):
        """Testa listagem de vozes por idioma."""
        synthesizer = TextToSpeech("test_key", "test_region")
        voices = synthesizer.list_voices_by_language("pt-BR")

        assert isinstance(voices, list)
        assert len(voices) > 0
        assert "pt-BR-FranciscaNeural" in voices

    @patch('src.speech.synthesis.speechsdk')
    def test_synthesize_to_file_success(self, mock_speechsdk):
        """Testa síntese de voz para arquivo com sucesso."""
        # Mock do resultado
        mock_result = Mock()
        mock_result.reason = 2  # SynthesizingAudioCompleted
        mock_speechsdk.ResultReason.SynthesizingAudioCompleted = 2

        # Mock do synthesizer
        mock_synthesizer = Mock()
        mock_synthesizer.speak_ssml_async.return_value.get.return_value = mock_result
        mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
        mock_speechsdk.AudioOutputConfig = Mock()

        synthesizer = TextToSpeech("test_key", "test_region", "pt-BR-FranciscaNeural")
        result = synthesizer.synthesize_to_file("Olá, mundo!", "output.wav")

        assert result['status'] == 'success'
        assert result['output_file'] == "output.wav"
        assert result['text'] == "Olá, mundo!"

    @patch('src.speech.synthesis.speechsdk')
    def test_synthesize_to_file_canceled(self, mock_speechsdk):
        """Testa síntese de voz cancelada."""
        # Mock do resultado
        mock_result = Mock()
        mock_result.reason = 3  # Canceled
        mock_cancellation = Mock()
        mock_cancellation.reason = "Test cancellation"
        mock_result.cancellation_details = mock_cancellation
        mock_speechsdk.ResultReason.Canceled = 3

        # Mock do synthesizer
        mock_synthesizer = Mock()
        mock_synthesizer.speak_ssml_async.return_value.get.return_value = mock_result
        mock_speechsdk.SpeechSynthesizer.return_value = mock_synthesizer
        mock_speechsdk.AudioOutputConfig = Mock()

        synthesizer = TextToSpeech("test_key", "test_region", "pt-BR-FranciscaNeural")
        result = synthesizer.synthesize_to_file("Olá, mundo!", "output.wav")

        assert result['status'] == 'canceled'

    def test_create_ssml(self):
        """Testa criação de SSML."""
        synthesizer = TextToSpeech("test_key", "test_region", "pt-BR-FranciscaNeural")
        ssml = synthesizer._create_ssml("Olá, mundo!", "+10%", "-5%")

        assert "<speak" in ssml
        assert "pt-BR-FranciscaNeural" in ssml
        assert "Olá, mundo!" in ssml
        assert "rate='+10%'" in ssml
        assert "pitch='-5%'" in ssml
