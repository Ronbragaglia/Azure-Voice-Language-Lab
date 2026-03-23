"""
Azure Voice Language Lab - Testes de Utilitários
=================================================

Testes unitários para os módulos de utilitários.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import Config, Logger, setup_logger


class TestConfig:
    """Testes para a classe Config."""

    def test_config_initialization(self):
        """Testa inicialização da configuração."""
        config = Config()
        assert config is not None

    def test_get_speech_config(self):
        """Testa obtenção da configuração de Speech."""
        with patch.dict(os.environ, {
            'AZURE_SPEECH_KEY': 'test_key',
            'AZURE_SPEECH_REGION': 'test_region'
        }):
            config = Config()
            key, region = config.get_speech_config()
            assert key == 'test_key'
            assert region == 'test_region'

    def test_get_language_config(self):
        """Testa obtenção da configuração de Language."""
        with patch.dict(os.environ, {
            'AZURE_LANGUAGE_KEY': 'test_key',
            'AZURE_LANGUAGE_ENDPOINT': 'https://test.endpoint.com'
        }):
            config = Config()
            key, endpoint = config.get_language_config()
            assert key == 'test_key'
            assert endpoint == 'https://test.endpoint.com'

    def test_get_translator_config(self):
        """Testa obtenção da configuração de Translator."""
        with patch.dict(os.environ, {
            'AZURE_TRANSLATOR_KEY': 'test_key',
            'AZURE_TRANSLATOR_REGION': 'test_region'
        }):
            config = Config()
            key, region = config.get_translator_config()
            assert key == 'test_key'
            assert region == 'test_region'

    def test_validate_config_valid(self):
        """Testa validação de configuração válida."""
        with patch.dict(os.environ, {
            'AZURE_SPEECH_KEY': 'test_key',
            'AZURE_SPEECH_REGION': 'test_region',
            'AZURE_LANGUAGE_KEY': 'test_key',
            'AZURE_LANGUAGE_ENDPOINT': 'https://test.endpoint.com'
        }):
            config = Config()
            validation = config.validate_config()
            assert validation['valid'] is True
            assert len(validation['errors']) == 0

    def test_validate_config_invalid(self):
        """Testa validação de configuração inválida."""
        with patch.dict(os.environ, {}, clear=True):
            config = Config()
            validation = config.validate_config()
            assert validation['valid'] is False
            assert len(validation['errors']) > 0


class TestLogger:
    """Testes para a classe Logger."""

    def test_logger_initialization(self):
        """Testa inicialização do logger."""
        logger = Logger('test_logger')
        assert logger is not None
        assert logger.name == 'test_logger'

    def test_setup_logger(self):
        """Testa configuração do logger."""
        logger = setup_logger('test_logger', level=20)  # INFO
        assert logger is not None
        assert logger.name == 'test_logger'
        assert logger.level == 20

    def test_logger_levels(self):
        """Testa diferentes níveis de log."""
        logger = setup_logger('test_logger', level=10)  # DEBUG
        assert logger.level == 10

        logger = setup_logger('test_logger', level=20)  # INFO
        assert logger.level == 20

        logger = setup_logger('test_logger', level=30)  # WARNING
        assert logger.level == 30
