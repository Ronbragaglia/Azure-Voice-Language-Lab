"""
Configuration Module
====================

Módulo para gerenciar configurações do Azure Voice Language Lab.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class Config:
    """
    Classe para gerenciar configurações do projeto.
    
    Attributes:
        speech_key (str): Chave de autenticação do Azure Speech Service.
        speech_region (str): Região do serviço Azure Speech.
        language_key (str): Chave de autenticação do Azure Language Service.
        language_endpoint (str): Endpoint do serviço Azure Language.
        translator_key (str): Chave de autenticação do Azure Translator Service.
        translator_region (str): Região do serviço Azure Translator.
    """
    
    def __init__(self):
        """Inicializa a configuração carregando variáveis de ambiente."""
        # Azure Speech Service
        self.speech_key = os.getenv("AZURE_SPEECH_KEY", "")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION", "")
        
        # Azure Language Service
        self.language_key = os.getenv("AZURE_LANGUAGE_KEY", "")
        self.language_endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT", "")
        
        # Azure Translator Service
        self.translator_key = os.getenv("AZURE_TRANSLATOR_KEY", "")
        self.translator_region = os.getenv("AZURE_TRANSLATOR_REGION", "")
        
        # Application Configuration
        self.app_name = os.getenv("APP_NAME", "Azure Voice Language Lab")
        self.app_version = os.getenv("APP_VERSION", "1.0.0")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        
        # Audio Configuration
        self.default_audio_format = os.getenv("DEFAULT_AUDIO_FORMAT", "wav")
        self.default_sample_rate = int(os.getenv("DEFAULT_SAMPLE_RATE", "16000"))
        self.default_channels = int(os.getenv("DEFAULT_CHANNELS", "1"))
        
        # Language Configuration
        self.default_language = os.getenv("DEFAULT_LANGUAGE", "pt-BR")
        self.supported_languages = os.getenv(
            "SUPPORTED_LANGUAGES",
            "pt-BR,en-US,es-ES,fr-FR,de-DE,it-IT,ja-JP,zh-CN"
        ).split(",")
        
        # Voice Configuration
        self.default_voice = os.getenv("DEFAULT_VOICE", "pt-BR-FranciscaNeural")
        self.voice_gender = os.getenv("VOICE_GENDER", "Female")
        self.voice_style = os.getenv("VOICE_STYLE", "Neutral")
        
        # Directory Configuration
        self.base_dir = Path(__file__).parent.parent.parent
        self.audio_samples_dir = self.base_dir / "audio_samples"
        self.output_dir = self.base_dir / "output"
        self.logs_dir = self.base_dir / "logs"
        
        # Criar diretórios se não existirem
        self._create_directories()
    
    def _create_directories(self) -> None:
        """Cria os diretórios necessários se não existirem."""
        directories = [
            self.audio_samples_dir,
            self.output_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate_config(self) -> dict:
        """
        Valida se as configurações mínimas estão definidas.
        
        Returns:
            Dicionário com status da validação e erros encontrados.
        """
        errors = []
        
        if not self.speech_key:
            errors.append("AZURE_SPEECH_KEY não está definida")
        
        if not self.speech_region:
            errors.append("AZURE_SPEECH_REGION não está definida")
        
        if not self.language_key:
            errors.append("AZURE_LANGUAGE_KEY não está definida")
        
        if not self.language_endpoint:
            errors.append("AZURE_LANGUAGE_ENDPOINT não está definida")
        
        if not self.translator_key:
            errors.append("AZURE_TRANSLATOR_KEY não está definida")
        
        if not self.translator_region:
            errors.append("AZURE_TRANSLATOR_REGION não está definida")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def get_speech_config(self) -> tuple:
        """
        Retorna a configuração do Azure Speech Service.
        
        Returns:
            Tupla com (speech_key, speech_region).
        """
        return (self.speech_key, self.speech_region)
    
    def get_language_config(self) -> tuple:
        """
        Retorna a configuração do Azure Language Service.
        
        Returns:
            Tupla com (language_key, language_endpoint).
        """
        return (self.language_key, self.language_endpoint)
    
    def get_translator_config(self) -> tuple:
        """
        Retorna a configuração do Azure Translator Service.
        
        Returns:
            Tupla com (translator_key, translator_region).
        """
        return (self.translator_key, self.translator_region)
    
    def __repr__(self) -> str:
        """Representação string da configuração."""
        return (
            f"Config(\n"
            f"  app_name={self.app_name},\n"
            f"  app_version={self.app_version},\n"
            f"  debug={self.debug},\n"
            f"  default_language={self.default_language},\n"
            f"  default_voice={self.default_voice}\n"
            f")"
        )


# Instância global de configuração
config = Config()
