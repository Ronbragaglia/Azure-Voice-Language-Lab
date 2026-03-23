"""
Speech Recognition Module
==========================

Módulo para reconhecimento de fala usando Azure Speech Service.
"""

import azure.cognitiveservices.speech as speechsdk
from typing import Optional, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechRecognition:
    """
    Classe para reconhecimento de fala usando Azure Speech Service.
    
    Attributes:
        speech_key (str): Chave de autenticação do Azure Speech Service.
        service_region (str): Região do serviço Azure.
        language (str): Idioma do reconhecimento (padrão: pt-BR).
    """
    
    def __init__(
        self,
        speech_key: str,
        service_region: str,
        language: str = "pt-BR"
    ):
        """
        Inicializa o reconhecimento de fala.
        
        Args:
            speech_key: Chave de autenticação do Azure Speech Service.
            service_region: Região do serviço Azure.
            language: Idioma do reconhecimento (padrão: pt-BR).
        """
        self.speech_key = speech_key
        self.service_region = service_region
        self.language = language
        self.speech_config = None
        self._initialize_config()
    
    def _initialize_config(self) -> None:
        """Inicializa a configuração do Azure Speech Service."""
        try:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.service_region
            )
            self.speech_config.speech_recognition_language = self.language
            logger.info(f"Configuração inicializada para idioma: {self.language}")
        except Exception as e:
            logger.error(f"Erro ao inicializar configuração: {e}")
            raise
    
    def recognize_from_file(self, audio_file: str) -> Dict[str, str]:
        """
        Reconhece fala de um arquivo de áudio.
        
        Args:
            audio_file: Caminho do arquivo de áudio.
            
        Returns:
            Dicionário com o texto reconhecido e status.
            
        Raises:
            FileNotFoundError: Se o arquivo de áudio não existir.
            Exception: Se ocorrer erro no reconhecimento.
        """
        try:
            audio_input = speechsdk.AudioConfig(filename=audio_file)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_input
            )
            
            result = speech_recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return {
                    "status": "success",
                    "text": result.text,
                    "language": self.language
                }
            elif result.reason == speechsdk.ResultReason.NoMatch:
                return {
                    "status": "no_match",
                    "text": "",
                    "error": "Nenhuma fala reconhecida"
                }
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                return {
                    "status": "canceled",
                    "text": "",
                    "error": f"Reconhecimento cancelado: {cancellation_details.reason}"
                }
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {audio_file}")
            raise
        except Exception as e:
            logger.error(f"Erro no reconhecimento de fala: {e}")
            raise
    
    def recognize_from_microphone(self) -> Dict[str, str]:
        """
        Reconhece fala do microfone em tempo real.
        
        Returns:
            Dicionário com o texto reconhecido e status.
            
        Raises:
            Exception: Se ocorrer erro no reconhecimento.
        """
        try:
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config
            )
            
            logger.info("Fale agora...")
            result = speech_recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return {
                    "status": "success",
                    "text": result.text,
                    "language": self.language
                }
            elif result.reason == speechsdk.ResultReason.NoMatch:
                return {
                    "status": "no_match",
                    "text": "",
                    "error": "Nenhuma fala reconhecida"
                }
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                return {
                    "status": "canceled",
                    "text": "",
                    "error": f"Reconhecimento cancelado: {cancellation_details.reason}"
                }
        except Exception as e:
            logger.error(f"Erro no reconhecimento de fala: {e}")
            raise
    
    def recognize_continuous(self, audio_file: str) -> List[Dict[str, str]]:
        """
        Reconhece fala contínua de um arquivo de áudio.
        
        Args:
            audio_file: Caminho do arquivo de áudio.
            
        Returns:
            Lista de dicionários com os textos reconhecidos.
            
        Raises:
            FileNotFoundError: Se o arquivo de áudio não existir.
            Exception: Se ocorrer erro no reconhecimento.
        """
        try:
            audio_input = speechsdk.AudioConfig(filename=audio_file)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_input
            )
            
            results = []
            
            def handle_result(evt):
                if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    results.append({
                        "status": "success",
                        "text": evt.result.text,
                        "language": self.language
                    })
            
            speech_recognizer.recognizing.connect(lambda evt: None)
            speech_recognizer.recognized.connect(handle_result)
            
            speech_recognizer.start_continuous_recognition()
            speech_recognizer.stop_continuous_recognition()
            
            return results
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {audio_file}")
            raise
        except Exception as e:
            logger.error(f"Erro no reconhecimento contínuo: {e}")
            raise
    
    def set_language(self, language: str) -> None:
        """
        Define o idioma do reconhecimento.
        
        Args:
            language: Código do idioma (ex: pt-BR, en-US, es-ES).
        """
        self.language = language
        if self.speech_config:
            self.speech_config.speech_recognition_language = language
        logger.info(f"Idioma alterado para: {language}")
