"""
Text to Speech Module
=====================

Módulo para síntese de voz usando Azure Speech Service.
"""

import azure.cognitiveservices.speech as speechsdk
from typing import Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextToSpeech:
    """
    Classe para síntese de voz usando Azure Speech Service.
    
    Attributes:
        speech_key (str): Chave de autenticação do Azure Speech Service.
        service_region (str): Região do serviço Azure.
        voice_name (str): Nome da voz a ser usada.
        language (str): Idioma da voz (padrão: pt-BR).
    """
    
    # Vozes disponíveis por idioma
    AVAILABLE_VOICES = {
        "pt-BR": [
            "pt-BR-FranciscaNeural",
            "pt-BR-AntonioNeural",
            "pt-BR-BrendaNeural",
            "pt-BR-DonatoNeural",
            "pt-BR-ElzaNeural",
            "pt-BR-FabioNeural",
            "pt-BR-GiovannaNeural",
            "pt-BR-HenriqueNeural",
            "pt-BR-IsabelaNeural",
            "pt-BR-LeandroNeural",
            "pt-BR-LeticiaNeural",
            "pt-BR-ManuelaNeural",
            "pt-BR-NicolauNeural",
            "pt-BR-ValerioNeural",
            "pt-BR-YaraNeural"
        ],
        "en-US": [
            "en-US-JennyNeural",
            "en-US-GuyNeural",
            "en-US-AriaNeural",
            "en-US-DavisNeural",
            "en-US-GuyNeural",
            "en-US-JaneNeural",
            "en-US-JasonNeural",
            "en-US-SaraNeural",
            "en-US-TonyNeural",
            "en-US-NancyNeural"
        ],
        "es-ES": [
            "es-ES-ElviraNeural",
            "es-ES-AlvaroNeural",
            "es-ES-ElviraNeural",
            "es-ES-JavierNeural"
        ],
        "fr-FR": [
            "fr-FR-DeniseNeural",
            "fr-FR-HenriNeural",
            "fr-FR-AlainNeural",
            "fr-FR-JulieNeural"
        ],
        "de-DE": [
            "de-DE-KatjaNeural",
            "de-DE-ConradNeural",
            "de-DE-AmalaNeural",
            "de-DE-BerndNeural"
        ],
        "it-IT": [
            "it-IT-ElsaNeural",
            "it-IT-DiegoNeural",
            "it-IT-BenignoNeural",
            "it-IT-FabiolaNeural"
        ],
        "ja-JP": [
            "ja-JP-NanamiNeural",
            "ja-JP-KeitaNeural",
            "ja-JP-AoiNeural",
            "ja-JP-DaichiNeural"
        ],
        "zh-CN": [
            "zh-CN-XiaoxiaoNeural",
            "zh-CN-YunxiNeural",
            "zh-CN-XiaoyiNeural",
            "zh-CN-YunyangNeural"
        ]
    }
    
    def __init__(
        self,
        speech_key: str,
        service_region: str,
        voice_name: str = "pt-BR-FranciscaNeural",
        language: str = "pt-BR"
    ):
        """
        Inicializa a síntese de voz.
        
        Args:
            speech_key: Chave de autenticação do Azure Speech Service.
            service_region: Região do serviço Azure.
            voice_name: Nome da voz a ser usada.
            language: Idioma da voz (padrão: pt-BR).
        """
        self.speech_key = speech_key
        self.service_region = service_region
        self.voice_name = voice_name
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
            self.speech_config.speech_synthesis_voice_name = self.voice_name
            logger.info(f"Configuração inicializada com voz: {self.voice_name}")
        except Exception as e:
            logger.error(f"Erro ao inicializar configuração: {e}")
            raise
    
    def synthesize_to_file(
        self,
        text: str,
        output_file: str = "output.wav",
        rate: str = "0%",
        pitch: str = "0%"
    ) -> Dict[str, str]:
        """
        Sintetiza texto em áudio e salva em arquivo.
        
        Args:
            text: Texto a ser sintetizado.
            output_file: Nome do arquivo de saída (padrão: output.wav).
            rate: Taxa de fala (ex: "+10%", "-10%", "0%").
            pitch: Tom da voz (ex: "+10%", "-10%", "0%").
            
        Returns:
            Dicionário com status e informações do arquivo gerado.
            
        Raises:
            Exception: Se ocorrer erro na síntese.
        """
        try:
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Configurar SSML para ajustar taxa e tom
            ssml = self._create_ssml(text, rate, pitch)
            
            result = synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Áudio gerado com sucesso: {output_file}")
                return {
                    "status": "success",
                    "output_file": output_file,
                    "text": text,
                    "voice": self.voice_name
                }
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logger.error(f"Síntese cancelada: {cancellation_details.reason}")
                return {
                    "status": "canceled",
                    "error": f"Síntese cancelada: {cancellation_details.reason}"
                }
        except Exception as e:
            logger.error(f"Erro na síntese de voz: {e}")
            raise
    
    def synthesize_to_stream(self, text: str) -> Dict[str, any]:
        """
        Sintetiza texto em áudio e retorna como stream.
        
        Args:
            text: Texto a ser sintetizado.
            
        Returns:
            Dicionário com status e stream de áudio.
            
        Raises:
            Exception: Se ocorrer erro na síntese.
        """
        try:
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=None
            )
            
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return {
                    "status": "success",
                    "audio_data": result.audio_data,
                    "text": text,
                    "voice": self.voice_name
                }
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logger.error(f"Síntese cancelada: {cancellation_details.reason}")
                return {
                    "status": "canceled",
                    "error": f"Síntese cancelada: {cancellation_details.reason}"
                }
        except Exception as e:
            logger.error(f"Erro na síntese de voz: {e}")
            raise
    
    def _create_ssml(
        self,
        text: str,
        rate: str = "0%",
        pitch: str = "0%"
    ) -> str:
        """
        Cria SSML para síntese de voz.
        
        Args:
            text: Texto a ser sintetizado.
            rate: Taxa de fala.
            pitch: Tom da voz.
            
        Returns:
            String SSML formatada.
        """
        return f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{self.language}'>
            <voice name='{self.voice_name}'>
                <prosody rate='{rate}' pitch='{pitch}'>
                    {text}
                </prosody>
            </voice>
        </speak>
        """
    
    def set_voice(self, voice_name: str) -> None:
        """
        Define a voz a ser usada.
        
        Args:
            voice_name: Nome da voz (ex: pt-BR-FranciscaNeural).
        """
        self.voice_name = voice_name
        if self.speech_config:
            self.speech_config.speech_synthesis_voice_name = voice_name
        logger.info(f"Voz alterada para: {voice_name}")
    
    def get_available_voices(self, language: Optional[str] = None) -> Dict[str, list]:
        """
        Retorna as vozes disponíveis.
        
        Args:
            language: Idioma para filtrar vozes (opcional).
            
        Returns:
            Dicionário com vozes disponíveis por idioma.
        """
        if language:
            return {language: self.AVAILABLE_VOICES.get(language, [])}
        return self.AVAILABLE_VOICES
    
    def list_voices_by_language(self, language: str) -> list:
        """
        Lista vozes disponíveis para um idioma específico.
        
        Args:
            language: Idioma para filtrar vozes.
            
        Returns:
            Lista de vozes disponíveis para o idioma.
        """
        return self.AVAILABLE_VOICES.get(language, [])
