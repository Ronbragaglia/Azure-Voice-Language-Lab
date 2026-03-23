"""
Azure Voice Language Lab - Configuração de Testes
==================================================

Configurações e fixtures para os testes do projeto.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch


@pytest.fixture
def sample_text():
    """Fixture que retorna um texto de exemplo."""
    return "Este é um texto de exemplo para testes."


@pytest.fixture
def sample_audio_file():
    """Fixture que retorna o caminho de um arquivo de áudio de exemplo."""
    return "audio_samples/sample.wav"


@pytest.fixture
def mock_azure_credentials():
    """Fixture que mocka as credenciais do Azure."""
    with patch.dict(os.environ, {
        'AZURE_SPEECH_KEY': 'test_speech_key',
        'AZURE_SPEECH_REGION': 'test_region',
        'AZURE_LANGUAGE_KEY': 'test_language_key',
        'AZURE_LANGUAGE_ENDPOINT': 'https://test.endpoint.com',
        'AZURE_TRANSLATOR_KEY': 'test_translator_key',
        'AZURE_TRANSLATOR_REGION': 'test_region'
    }):
        yield


@pytest.fixture
def temp_output_dir(tmp_path):
    """Fixture que cria um diretório temporário para saídas."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_texts():
    """Fixture que retorna uma lista de textos de exemplo."""
    return [
        "Estou muito feliz com os resultados!",
        "O produto não funcionou como esperado.",
        "O serviço é bom, mas pode melhorar.",
    ]


@pytest.fixture
def sample_translations():
    """Fixture que retorna pares de texto para tradução."""
    return [
        {"text": "Hello, world!", "from": "en", "to": "pt"},
        {"text": "Olá, mundo!", "from": "pt", "to": "en"},
        {"text": "Bonjour le monde!", "from": "fr", "to": "pt"},
    ]
