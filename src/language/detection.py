"""
Language Detection Module
=========================

Módulo para detecção de idioma usando Azure Language Service.
"""

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LanguageDetection:
    """
    Classe para detecção de idioma usando Azure Language Service.
    
    Attributes:
        api_key (str): Chave de autenticação do Azure Language Service.
        endpoint (str): Endpoint do serviço Azure.
    """
    
    # Nomes de idiomas suportados
    LANGUAGE_NAMES = {
        "pt": "Português",
        "pt-BR": "Português (Brasil)",
        "pt-PT": "Português (Portugal)",
        "en": "Inglês",
        "en-US": "Inglês (Estados Unidos)",
        "en-GB": "Inglês (Reino Unido)",
        "es": "Espanhol",
        "es-ES": "Espanhol (Espanha)",
        "es-MX": "Espanhol (México)",
        "fr": "Francês",
        "fr-FR": "Francês (França)",
        "de": "Alemão",
        "de-DE": "Alemão (Alemanha)",
        "it": "Italiano",
        "it-IT": "Italiano (Itália)",
        "ja": "Japonês",
        "ja-JP": "Japonês (Japão)",
        "zh": "Chinês",
        "zh-CN": "Chinês (Simplificado)",
        "zh-TW": "Chinês (Tradicional)",
        "ko": "Coreano",
        "ko-KR": "Coreano (Coreia do Sul)",
        "ru": "Russo",
        "ar": "Árabe",
        "hi": "Hindi"
    }
    
    def __init__(
        self,
        api_key: str,
        endpoint: str
    ):
        """
        Inicializa a detecção de idioma.
        
        Args:
            api_key: Chave de autenticação do Azure Language Service.
            endpoint: Endpoint do serviço Azure.
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Inicializa o cliente do Azure Language Service."""
        try:
            credential = AzureKeyCredential(self.api_key)
            self.client = TextAnalyticsClient(
                endpoint=self.endpoint,
                credential=credential
            )
            logger.info("Cliente de detecção de idioma inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente: {e}")
            raise
    
    def detect_language(
        self,
        text: str,
        country_hint: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Detecta o idioma de um texto.
        
        Args:
            text: Texto a ser analisado.
            country_hint: Dica de país para melhorar a detecção (opcional, ex: BR, US).
            
        Returns:
            Dicionário com o resultado da detecção de idioma.
            
        Raises:
            Exception: Se ocorrer erro na detecção.
        """
        try:
            if country_hint:
                documents = [{"id": "1", "country_hint": country_hint, "text": text}]
            else:
                documents = [{"id": "1", "text": text}]
            
            response = self.client.detect_language(documents=documents)
            result = response[0]
            
            if not result.is_error:
                primary_language = result.primary_language
                return {
                    "status": "success",
                    "language": primary_language.name,
                    "language_name": self.get_language_name(primary_language.name),
                    "confidence_score": primary_language.confidence_score,
                    "iso6391_name": primary_language.iso6391_name
                }
            else:
                logger.error(f"Erro na detecção de idioma: {result.error}")
                return {
                    "status": "error",
                    "error": str(result.error)
                }
        except Exception as e:
            logger.error(f"Erro na detecção de idioma: {e}")
            raise
    
    def detect_language_multiple(
        self,
        texts: List[str],
        country_hint: Optional[str] = None
    ) -> List[Dict[str, any]]:
        """
        Detecta o idioma de múltiplos textos.
        
        Args:
            texts: Lista de textos a serem analisados.
            country_hint: Dica de país para melhorar a detecção (opcional, ex: BR, US).
            
        Returns:
            Lista de dicionários com os resultados da detecção de idioma.
            
        Raises:
            Exception: Se ocorrer erro na detecção.
        """
        try:
            if country_hint:
                documents = [
                    {"id": str(i), "country_hint": country_hint, "text": text}
                    for i, text in enumerate(texts)
                ]
            else:
                documents = [
                    {"id": str(i), "text": text}
                    for i, text in enumerate(texts)
                ]
            
            response = self.client.detect_language(documents=documents)
            results = []
            
            for result in response:
                if not result.is_error:
                    primary_language = result.primary_language
                    results.append({
                        "status": "success",
                        "text": documents[int(result.id)]["text"],
                        "language": primary_language.name,
                        "language_name": self.get_language_name(primary_language.name),
                        "confidence_score": primary_language.confidence_score,
                        "iso6391_name": primary_language.iso6391_name
                    })
                else:
                    results.append({
                        "status": "error",
                        "error": str(result.error)
                    })
            
            return results
        except Exception as e:
            logger.error(f"Erro na detecção de idioma múltipla: {e}")
            raise
    
    def get_language_name(self, language_code: str) -> str:
        """
        Retorna o nome do idioma a partir do código.
        
        Args:
            language_code: Código do idioma (ex: pt-BR, en-US, es-ES).
            
        Returns:
            Nome do idioma em português.
        """
        return self.LANGUAGE_NAMES.get(language_code, language_code)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Retorna os idiomas suportados.
        
        Returns:
            Dicionário com códigos e nomes dos idiomas suportados.
        """
        return self.LANGUAGE_NAMES
