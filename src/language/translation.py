"""
Translation Module
==================

Módulo para tradução de texto usando Azure Translator Service.
"""

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Translation:
    """
    Classe para tradução de texto usando Azure Translator Service.
    
    Attributes:
        api_key (str): Chave de autenticação do Azure Translator Service.
        region (str): Região do serviço Azure.
        endpoint (str): Endpoint do serviço Azure.
    """
    
    # Idiomas suportados
    SUPPORTED_LANGUAGES = {
        "pt": "Português",
        "en": "Inglês",
        "es": "Espanhol",
        "fr": "Francês",
        "de": "Alemão",
        "it": "Italiano",
        "ja": "Japonês",
        "zh": "Chinês",
        "ko": "Coreano",
        "ru": "Russo",
        "ar": "Árabe",
        "hi": "Hindi"
    }
    
    def __init__(
        self,
        api_key: str,
        region: str,
        endpoint: Optional[str] = None
    ):
        """
        Inicializa o serviço de tradução.
        
        Args:
            api_key: Chave de autenticação do Azure Translator Service.
            region: Região do serviço Azure.
            endpoint: Endpoint do serviço Azure (opcional).
        """
        self.api_key = api_key
        self.region = region
        self.endpoint = endpoint or f"https://api.cognitive.microsofttranslator.com/"
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Inicializa o cliente do Azure Translator Service."""
        try:
            credential = AzureKeyCredential(self.api_key)
            self.client = TextTranslationClient(
                credential=credential,
                region=self.region,
                endpoint=self.endpoint
            )
            logger.info("Cliente de tradução inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente: {e}")
            raise
    
    def translate(
        self,
        text: str,
        to_language: str,
        from_language: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Traduz um texto para o idioma especificado.
        
        Args:
            text: Texto a ser traduzido.
            to_language: Idioma de destino (ex: en, es, fr).
            from_language: Idioma de origem (opcional, detecta automaticamente se não informado).
            
        Returns:
            Dicionário com o resultado da tradução.
            
        Raises:
            Exception: Se ocorrer erro na tradução.
        """
        try:
            if from_language:
                response = self.client.translate(
                    body=[text],
                    to_language=[to_language],
                    from_language=from_language
                )
            else:
                response = self.client.translate(
                    body=[text],
                    to_language=[to_language]
                )
            
            result = response[0]
            
            if result.translations:
                translation = result.translations[0]
                return {
                    "status": "success",
                    "text": text,
                    "translation": translation.text,
                    "from_language": result.detected_language.language if not from_language else from_language,
                    "to_language": to_language,
                    "confidence": result.detected_language.score if not from_language else 1.0
                }
            else:
                return {
                    "status": "error",
                    "error": "Nenhuma tradução encontrada"
                }
        except Exception as e:
            logger.error(f"Erro na tradução: {e}")
            raise
    
    def translate_multiple(
        self,
        texts: List[str],
        to_language: str,
        from_language: Optional[str] = None
    ) -> List[Dict[str, any]]:
        """
        Traduz múltiplos textos para o idioma especificado.
        
        Args:
            texts: Lista de textos a serem traduzidos.
            to_language: Idioma de destino (ex: en, es, fr).
            from_language: Idioma de origem (opcional, detecta automaticamente se não informado).
            
        Returns:
            Lista de dicionários com os resultados das traduções.
            
        Raises:
            Exception: Se ocorrer erro na tradução.
        """
        try:
            if from_language:
                response = self.client.translate(
                    body=texts,
                    to_language=[to_language],
                    from_language=from_language
                )
            else:
                response = self.client.translate(
                    body=texts,
                    to_language=[to_language]
                )
            
            results = []
            for result in response:
                if result.translations:
                    translation = result.translations[0]
                    results.append({
                        "status": "success",
                        "text": result.text,
                        "translation": translation.text,
                        "from_language": result.detected_language.language if not from_language else from_language,
                        "to_language": to_language,
                        "confidence": result.detected_language.score if not from_language else 1.0
                    })
                else:
                    results.append({
                        "status": "error",
                        "error": "Nenhuma tradução encontrada"
                    })
            
            return results
        except Exception as e:
            logger.error(f"Erro na tradução múltipla: {e}")
            raise
    
    def translate_to_multiple(
        self,
        text: str,
        to_languages: List[str],
        from_language: Optional[str] = None
    ) -> List[Dict[str, any]]:
        """
        Traduz um texto para múltiplos idiomas.
        
        Args:
            text: Texto a ser traduzido.
            to_languages: Lista de idiomas de destino (ex: [en, es, fr]).
            from_language: Idioma de origem (opcional, detecta automaticamente se não informado).
            
        Returns:
            Lista de dicionários com os resultados das traduções.
            
        Raises:
            Exception: Se ocorrer erro na tradução.
        """
        try:
            if from_language:
                response = self.client.translate(
                    body=[text],
                    to_language=to_languages,
                    from_language=from_language
                )
            else:
                response = self.client.translate(
                    body=[text],
                    to_language=to_languages
                )
            
            result = response[0]
            results = []
            
            for translation in result.translations:
                results.append({
                    "status": "success",
                    "text": text,
                    "translation": translation.text,
                    "from_language": result.detected_language.language if not from_language else from_language,
                    "to_language": translation.to,
                    "confidence": result.detected_language.score if not from_language else 1.0
                })
            
            return results
        except Exception as e:
            logger.error(f"Erro na tradução para múltiplos idiomas: {e}")
            raise
    
    def transliterate(
        self,
        text: str,
        from_language: str,
        from_script: str,
        to_script: str
    ) -> Dict[str, any]:
        """
        Translitera texto de um script para outro.
        
        Args:
            text: Texto a ser transliterado.
            from_language: Idioma do texto (ex: ja, zh, hi).
            from_script: Script de origem (ex: Jpan, Hant, Deva).
            to_script: Script de destino (ex: Latn).
            
        Returns:
            Dicionário com o resultado da transliteração.
            
        Raises:
            Exception: Se ocorrer erro na transliteração.
        """
        try:
            response = self.client.transliterate(
                body=[text],
                language=from_language,
                from_script=from_script,
                to_script=to_script
            )
            
            result = response[0]
            
            if result.text:
                return {
                    "status": "success",
                    "text": text,
                    "transliteration": result.text,
                    "from_language": from_language,
                    "from_script": from_script,
                    "to_script": to_script
                }
            else:
                return {
                    "status": "error",
                    "error": "Nenhuma transliteração encontrada"
                }
        except Exception as e:
            logger.error(f"Erro na transliteração: {e}")
            raise
    
    def get_supported_languages(self) -> Dict[str, Dict[str, str]]:
        """
        Retorna os idiomas suportados pelo serviço de tradução.
        
        Returns:
            Dicionário com idiomas suportados.
            
        Raises:
            Exception: Se ocorrer erro ao obter idiomas.
        """
        try:
            response = self.client.get_supported_languages()
            return response.translation
        except Exception as e:
            logger.error(f"Erro ao obter idiomas suportados: {e}")
            raise
    
    def get_language_name(self, language_code: str) -> str:
        """
        Retorna o nome do idioma a partir do código.
        
        Args:
            language_code: Código do idioma (ex: pt, en, es).
            
        Returns:
            Nome do idioma em português.
        """
        return self.SUPPORTED_LANGUAGES.get(language_code, language_code)
