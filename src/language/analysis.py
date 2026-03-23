"""
Text Analysis Module
====================

Módulo para análise de texto usando Azure Language Service.
"""

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextAnalysis:
    """
    Classe para análise de texto usando Azure Language Service.
    
    Attributes:
        api_key (str): Chave de autenticação do Azure Language Service.
        endpoint (str): Endpoint do serviço Azure.
        language (str): Idioma padrão para análise (padrão: pt-BR).
    """
    
    def __init__(
        self,
        api_key: str,
        endpoint: str,
        language: str = "pt-BR"
    ):
        """
        Inicializa a análise de texto.
        
        Args:
            api_key: Chave de autenticação do Azure Language Service.
            endpoint: Endpoint do serviço Azure.
            language: Idioma padrão para análise (padrão: pt-BR).
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.language = language
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
            logger.info("Cliente de análise de texto inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente: {e}")
            raise
    
    def analyze_sentiment(
        self,
        text: str,
        language: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Analisa o sentimento de um texto.
        
        Args:
            text: Texto a ser analisado.
            language: Idioma do texto (opcional, usa padrão se não informado).
            
        Returns:
            Dicionário com o resultado da análise de sentimento.
            
        Raises:
            Exception: Se ocorrer erro na análise.
        """
        try:
            lang = language or self.language
            documents = [{"id": "1", "language": lang, "text": text}]
            response = self.client.analyze_sentiment(documents=documents)
            
            result = response[0]
            
            if not result.is_error:
                return {
                    "status": "success",
                    "sentiment": result.sentiment.name,
                    "confidence_scores": {
                        "positive": result.confidence_scores.positive,
                        "neutral": result.confidence_scores.neutral,
                        "negative": result.confidence_scores.negative
                    },
                    "language": lang
                }
            else:
                logger.error(f"Erro na análise de sentimento: {result.error}")
                return {
                    "status": "error",
                    "error": str(result.error)
                }
        except Exception as e:
            logger.error(f"Erro na análise de sentimento: {e}")
            raise
    
    def extract_entities(
        self,
        text: str,
        language: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Extrai entidades nomeadas de um texto.
        
        Args:
            text: Texto a ser analisado.
            language: Idioma do texto (opcional, usa padrão se não informado).
            
        Returns:
            Dicionário com as entidades extraídas.
            
        Raises:
            Exception: Se ocorrer erro na análise.
        """
        try:
            lang = language or self.language
            documents = [{"id": "1", "language": lang, "text": text}]
            response = self.client.recognize_entities(documents=documents)
            
            result = response[0]
            
            if not result.is_error:
                entities = []
                for entity in result.entities:
                    entities.append({
                        "text": entity.text,
                        "category": entity.category,
                        "subcategory": entity.subcategory,
                        "confidence_score": entity.confidence_score,
                        "length": entity.length,
                        "offset": entity.offset
                    })
                
                return {
                    "status": "success",
                    "entities": entities,
                    "language": lang
                }
            else:
                logger.error(f"Erro na extração de entidades: {result.error}")
                return {
                    "status": "error",
                    "error": str(result.error)
                }
        except Exception as e:
            logger.error(f"Erro na extração de entidades: {e}")
            raise
    
    def extract_key_phrases(
        self,
        text: str,
        language: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Extrai frases-chave de um texto.
        
        Args:
            text: Texto a ser analisado.
            language: Idioma do texto (opcional, usa padrão se não informado).
            
        Returns:
            Dicionário com as frases-chave extraídas.
            
        Raises:
            Exception: Se ocorrer erro na análise.
        """
        try:
            lang = language or self.language
            documents = [{"id": "1", "language": lang, "text": text}]
            response = self.client.extract_key_phrases(documents=documents)
            
            result = response[0]
            
            if not result.is_error:
                return {
                    "status": "success",
                    "key_phrases": result.key_phrases,
                    "language": lang
                }
            else:
                logger.error(f"Erro na extração de frases-chave: {result.error}")
                return {
                    "status": "error",
                    "error": str(result.error)
                }
        except Exception as e:
            logger.error(f"Erro na extração de frases-chave: {e}")
            raise
    
    def detect_linked_entities(
        self,
        text: str,
        language: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Detecta entidades vinculadas (Linked Entities) de um texto.
        
        Args:
            text: Texto a ser analisado.
            language: Idioma do texto (opcional, usa padrão se não informado).
            
        Returns:
            Dicionário com as entidades vinculadas detectadas.
            
        Raises:
            Exception: Se ocorrer erro na análise.
        """
        try:
            lang = language or self.language
            documents = [{"id": "1", "language": lang, "text": text}]
            response = self.client.recognize_linked_entities(documents=documents)
            
            result = response[0]
            
            if not result.is_error:
                entities = []
                for entity in result.entities:
                    matches = []
                    for match in entity.matches:
                        matches.append({
                            "text": match.text,
                            "confidence_score": match.confidence_score,
                            "length": match.length,
                            "offset": match.offset
                        })
                    
                    entities.append({
                        "name": entity.name,
                        "url": entity.url,
                        "data_source": entity.data_source,
                        "matches": matches
                    })
                
                return {
                    "status": "success",
                    "linked_entities": entities,
                    "language": lang
                }
            else:
                logger.error(f"Erro na detecção de entidades vinculadas: {result.error}")
                return {
                    "status": "error",
                    "error": str(result.error)
                }
        except Exception as e:
            logger.error(f"Erro na detecção de entidades vinculadas: {e}")
            raise
    
    def analyze_health_entities(
        self,
        text: str,
        language: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Analisa entidades de saúde em um texto.
        
        Args:
            text: Texto a ser analisado.
            language: Idioma do texto (opcional, usa padrão se não informado).
            
        Returns:
            Dicionário com as entidades de saúde detectadas.
            
        Raises:
            Exception: Se ocorrer erro na análise.
        """
        try:
            lang = language or self.language
            documents = [{"id": "1", "language": lang, "text": text}]
            response = self.client.analyze_healthcare_entities(documents=documents)
            
            result = response[0]
            
            if not result.is_error:
                entities = []
                for entity in result.entities:
                    entities.append({
                        "text": entity.text,
                        "category": entity.category,
                        "subcategory": entity.subcategory,
                        "confidence_score": entity.confidence_score,
                        "length": entity.length,
                        "offset": entity.offset
                    })
                
                return {
                    "status": "success",
                    "health_entities": entities,
                    "language": lang
                }
            else:
                logger.error(f"Erro na análise de entidades de saúde: {result.error}")
                return {
                    "status": "error",
                    "error": str(result.error)
                }
        except Exception as e:
            logger.error(f"Erro na análise de entidades de saúde: {e}")
            raise
    
    def set_language(self, language: str) -> None:
        """
        Define o idioma padrão para análise.
        
        Args:
            language: Código do idioma (ex: pt-BR, en-US, es-ES).
        """
        self.language = language
        logger.info(f"Idioma padrão alterado para: {language}")
