"""
Azure Voice Language Lab - Testes de Language
=============================================

Testes unitários para os módulos de linguagem (Language).
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.language import TextAnalysis, Translation, LanguageDetection


@pytest.mark.language
class TestTextAnalysis:
    """Testes para a classe TextAnalysis."""

    def test_initialization(self):
        """Testa inicialização da análise de texto."""
        analyzer = TextAnalysis("test_key", "https://test.endpoint.com", "pt-BR")
        assert analyzer.api_key == "test_key"
        assert analyzer.endpoint == "https://test.endpoint.com"
        assert analyzer.language == "pt-BR"

    def test_set_language(self):
        """Testa mudança de idioma."""
        analyzer = TextAnalysis("test_key", "https://test.endpoint.com", "pt-BR")
        analyzer.set_language("en-US")
        assert analyzer.language == "en-US"

    @patch('src.language.analysis.TextAnalyticsClient')
    def test_analyze_sentiment_success(self, mock_client):
        """Testa análise de sentimento com sucesso."""
        # Mock do resultado
        mock_result = Mock()
        mock_result.is_error = False
        mock_result.sentiment.name = "positive"
        mock_result.confidence_scores.positive = 0.9
        mock_result.confidence_scores.neutral = 0.05
        mock_result.confidence_scores.negative = 0.05

        # Mock da resposta
        mock_response = [mock_result]
        mock_client.return_value.analyze_sentiment.return_value = mock_response

        analyzer = TextAnalysis("test_key", "https://test.endpoint.com", "pt-BR")
        result = analyzer.analyze_sentiment("Estou muito feliz!", "pt-BR")

        assert result['status'] == 'success'
        assert result['sentiment'] == 'positive'
        assert result['confidence_scores']['positive'] == 0.9

    @patch('src.language.analysis.TextAnalyticsClient')
    def test_extract_entities_success(self, mock_client):
        """Testa extração de entidades com sucesso."""
        # Mock da entidade
        mock_entity = Mock()
        mock_entity.text = "Microsoft"
        mock_entity.category = "Organization"
        mock_entity.subcategory = "Technology"
        mock_entity.confidence_score = 0.95
        mock_entity.length = 9
        mock_entity.offset = 0

        # Mock do resultado
        mock_result = Mock()
        mock_result.is_error = False
        mock_result.entities = [mock_entity]

        # Mock da resposta
        mock_response = [mock_result]
        mock_client.return_value.recognize_entities.return_value = mock_response

        analyzer = TextAnalysis("test_key", "https://test.endpoint.com", "pt-BR")
        result = analyzer.extract_entities("A Microsoft é uma empresa de tecnologia.", "pt-BR")

        assert result['status'] == 'success'
        assert len(result['entities']) == 1
        assert result['entities'][0]['text'] == "Microsoft"
        assert result['entities'][0]['category'] == "Organization"

    @patch('src.language.analysis.TextAnalyticsClient')
    def test_extract_key_phrases_success(self, mock_client):
        """Testa extração de frases-chave com sucesso."""
        # Mock do resultado
        mock_result = Mock()
        mock_result.is_error = False
        mock_result.key_phrases = ["inteligência artificial", "machine learning", "tecnologia"]

        # Mock da resposta
        mock_response = [mock_result]
        mock_client.return_value.extract_key_phrases.return_value = mock_response

        analyzer = TextAnalysis("test_key", "https://test.endpoint.com", "pt-BR")
        result = analyzer.extract_key_phrases(
            "A inteligência artificial e o machine learning estão transformando a tecnologia.",
            "pt-BR"
        )

        assert result['status'] == 'success'
        assert len(result['key_phrases']) == 3
        assert "inteligência artificial" in result['key_phrases']


@pytest.mark.language
class TestTranslation:
    """Testes para a classe Translation."""

    def test_initialization(self):
        """Testa inicialização do tradutor."""
        translator = Translation("test_key", "test_region")
        assert translator.api_key == "test_key"
        assert translator.region == "test_region"

    @patch('src.language.translation.requests')
    def test_translate_success(self, mock_requests):
        """Testa tradução com sucesso."""
        # Mock da resposta
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "translations": [{"text": "Olá, mundo!", "to": "pt"}],
                "detectedLanguage": {"language": "en", "confidence": 0.95}
            }
        ]
        mock_requests.post.return_value = mock_response

        translator = Translation("test_key", "test_region")
        result = translator.translate("Hello, world!", "pt", "en")

        assert result['status'] == 'success'
        assert result['translation'] == "Olá, mundo!"
        assert result['to_language'] == "pt"
        assert result['confidence'] == 0.95

    @patch('src.language.translation.requests')
    def test_translate_error(self, mock_requests):
        """Testa tradução com erro."""
        # Mock da resposta
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_requests.post.return_value = mock_response

        translator = Translation("test_key", "test_region")
        result = translator.translate("Hello, world!", "pt", "en")

        assert result['status'] == 'error'
        assert 'error' in result


@pytest.mark.language
class TestLanguageDetection:
    """Testes para a classe LanguageDetection."""

    def test_initialization(self):
        """Testa inicialização do detector de idioma."""
        detector = LanguageDetection("test_key", "https://test.endpoint.com")
        assert detector.api_key == "test_key"
        assert detector.endpoint == "https://test.endpoint.com"

    @patch('src.language.detection.TextAnalyticsClient')
    def test_detect_language_success(self, mock_client):
        """Testa detecção de idioma com sucesso."""
        # Mock do resultado
        mock_result = Mock()
        mock_result.is_error = False
        mock_result.primary_language.name = "Portuguese"
        mock_result.primary_language.iso6391_name = "pt"
        mock_result.primary_language.confidence_score = 0.98

        # Mock da resposta
        mock_response = [mock_result]
        mock_client.return_value.detect_language.return_value = mock_response

        detector = LanguageDetection("test_key", "https://test.endpoint.com")
        result = detector.detect_language("Olá, como você está?")

        assert result['status'] == 'success'
        assert result['language'] == "pt"
        assert result['language_name'] == "Portuguese"
        assert result['confidence_score'] == 0.98

    @patch('src.language.detection.TextAnalyticsClient')
    def test_detect_language_error(self, mock_client):
        """Testa detecção de idioma com erro."""
        # Mock do resultado
        mock_result = Mock()
        mock_result.is_error = True
        mock_result.error = "Invalid request"

        # Mock da resposta
        mock_response = [mock_result]
        mock_client.return_value.detect_language.return_value = mock_response

        detector = LanguageDetection("test_key", "https://test.endpoint.com")
        result = detector.detect_language("")

        assert result['status'] == 'error'
        assert 'error' in result
