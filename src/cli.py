"""
CLI Module
==========

Módulo para interface de linha de comando do Azure Voice Language Lab.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .speech import SpeechRecognition, TextToSpeech
from .language import TextAnalysis, Translation, LanguageDetection
from .utils import Config, Logger, setup_logger


def main():
    """Função principal da CLI."""
    parser = argparse.ArgumentParser(
        description="Azure Voice Language Lab - CLI Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Reconhecimento de fala
  azure-speech-lab recognize --audio audio.wav
  
  # Síntese de voz
  azure-speech-lab synthesize --text "Olá mundo" --output output.wav
  
  # Análise de sentimento
  azure-speech-lab sentiment --text "Estou muito feliz hoje"
  
  # Tradução
  azure-speech-lab translate --text "Hello world" --to es
  
  # Detecção de idioma
  azure-speech-lab detect --text "Bonjour le monde"
        """
    )
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Reconhecimento de fala
    recognize_parser = subparsers.add_parser('recognize', help='Reconhecimento de fala')
    recognize_parser.add_argument('--audio', required=True, help='Arquivo de áudio')
    recognize_parser.add_argument('--language', default='pt-BR', help='Idioma (padrão: pt-BR)')
    
    # Síntese de voz
    synthesize_parser = subparsers.add_parser('synthesize', help='Síntese de voz')
    synthesize_parser.add_argument('--text', required=True, help='Texto a ser sintetizado')
    synthesize_parser.add_argument('--output', default='output.wav', help='Arquivo de saída')
    synthesize_parser.add_argument('--voice', default='pt-BR-FranciscaNeural', help='Voz')
    synthesize_parser.add_argument('--rate', default='0%', help='Taxa de fala')
    synthesize_parser.add_argument('--pitch', default='0%', help='Tom da voz')
    
    # Análise de sentimento
    sentiment_parser = subparsers.add_parser('sentiment', help='Análise de sentimento')
    sentiment_parser.add_argument('--text', required=True, help='Texto a ser analisado')
    sentiment_parser.add_argument('--language', default='pt-BR', help='Idioma')
    
    # Extração de entidades
    entities_parser = subparsers.add_parser('entities', help='Extração de entidades')
    entities_parser.add_argument('--text', required=True, help='Texto a ser analisado')
    entities_parser.add_argument('--language', default='pt-BR', help='Idioma')
    
    # Tradução
    translate_parser = subparsers.add_parser('translate', help='Tradução de texto')
    translate_parser.add_argument('--text', required=True, help='Texto a ser traduzido')
    translate_parser.add_argument('--to', required=True, help='Idioma de destino')
    translate_parser.add_argument('--from', dest='from_lang', help='Idioma de origem')
    
    # Detecção de idioma
    detect_parser = subparsers.add_parser('detect', help='Detecção de idioma')
    detect_parser.add_argument('--text', required=True, help='Texto a ser analisado')
    
    # Frases-chave
    phrases_parser = subparsers.add_parser('phrases', help='Extração de frases-chave')
    phrases_parser.add_argument('--text', required=True, help='Texto a ser analisado')
    phrases_parser.add_argument('--language', default='pt-BR', help='Idioma')
    
    # Argumentos gerais
    parser.add_argument('--verbose', '-v', action='store_true', help='Modo verboso')
    parser.add_argument('--config', help='Arquivo de configuração')
    
    args = parser.parse_args()
    
    # Configurar logger
    log_level = 20 if args.verbose else 30  # INFO ou WARNING
    logger = setup_logger('azure_voice_lab', log_level)
    
    # Carregar configuração
    config = Config()
    validation = config.validate_config()
    
    if not validation['valid']:
        logger.error("Configuração inválida:")
        for error in validation['errors']:
            logger.error(f"  - {error}")
        sys.exit(1)
    
    # Executar comando
    try:
        if args.command == 'recognize':
            cmd_recognize(args, config, logger)
        elif args.command == 'synthesize':
            cmd_synthesize(args, config, logger)
        elif args.command == 'sentiment':
            cmd_sentiment(args, config, logger)
        elif args.command == 'entities':
            cmd_entities(args, config, logger)
        elif args.command == 'translate':
            cmd_translate(args, config, logger)
        elif args.command == 'detect':
            cmd_detect(args, config, logger)
        elif args.command == 'phrases':
            cmd_phrases(args, config, logger)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        logger.error(f"Erro ao executar comando: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def cmd_recognize(args, config, logger):
    """Executa reconhecimento de fala."""
    logger.info(f"Reconhecendo fala do arquivo: {args.audio}")
    
    speech_key, speech_region = config.get_speech_config()
    recognizer = SpeechRecognition(speech_key, speech_region, args.language)
    
    result = recognizer.recognize_from_file(args.audio)
    
    if result['status'] == 'success':
        print(f"Texto reconhecido: {result['text']}")
        print(f"Idioma: {result['language']}")
    else:
        print(f"Erro: {result.get('error', 'Erro desconhecido')}")
        sys.exit(1)


def cmd_synthesize(args, config, logger):
    """Executa síntese de voz."""
    logger.info(f"Sintetizando texto: {args.text}")
    
    speech_key, speech_region = config.get_speech_config()
    synthesizer = TextToSpeech(speech_key, speech_region, args.voice)
    
    result = synthesizer.synthesize_to_file(
        args.text,
        args.output,
        args.rate,
        args.pitch
    )
    
    if result['status'] == 'success':
        print(f"Áudio gerado: {result['output_file']}")
        print(f"Voz: {result['voice']}")
    else:
        print(f"Erro: {result.get('error', 'Erro desconhecido')}")
        sys.exit(1)


def cmd_sentiment(args, config, logger):
    """Executa análise de sentimento."""
    logger.info(f"Analisando sentimento do texto: {args.text}")
    
    language_key, language_endpoint = config.get_language_config()
    analyzer = TextAnalysis(language_key, language_endpoint, args.language)
    
    result = analyzer.analyze_sentiment(args.text, args.language)
    
    if result['status'] == 'success':
        print(f"Sentimento: {result['sentiment']}")
        print(f"Confiança - Positivo: {result['confidence_scores']['positive']:.2f}")
        print(f"Confiança - Neutro: {result['confidence_scores']['neutral']:.2f}")
        print(f"Confiança - Negativo: {result['confidence_scores']['negative']:.2f}")
    else:
        print(f"Erro: {result.get('error', 'Erro desconhecido')}")
        sys.exit(1)


def cmd_entities(args, config, logger):
    """Executa extração de entidades."""
    logger.info(f"Extraindo entidades do texto: {args.text}")
    
    language_key, language_endpoint = config.get_language_config()
    analyzer = TextAnalysis(language_key, language_endpoint, args.language)
    
    result = analyzer.extract_entities(args.text, args.language)
    
    if result['status'] == 'success':
        print(f"Entidades encontradas: {len(result['entities'])}")
        for entity in result['entities']:
            print(f"  - {entity['text']}: {entity['category']} "
                  f"({entity.get('subcategory', 'N/A')}) - "
                  f"Confiança: {entity['confidence_score']:.2f}")
    else:
        print(f"Erro: {result.get('error', 'Erro desconhecido')}")
        sys.exit(1)


def cmd_translate(args, config, logger):
    """Executa tradução."""
    logger.info(f"Traduzindo texto: {args.text}")
    
    translator_key, translator_region = config.get_translator_config()
    translator = Translation(translator_key, translator_region)
    
    result = translator.translate(args.text, args.to, args.from_lang)
    
    if result['status'] == 'success':
        print(f"Texto original: {result['text']}")
        print(f"Tradução: {result['translation']}")
        print(f"De: {result['from_language']} -> Para: {result['to_language']}")
        if 'confidence' in result:
            print(f"Confiança: {result['confidence']:.2f}")
    else:
        print(f"Erro: {result.get('error', 'Erro desconhecido')}")
        sys.exit(1)


def cmd_detect(args, config, logger):
    """Executa detecção de idioma."""
    logger.info(f"Detectando idioma do texto: {args.text}")
    
    language_key, language_endpoint = config.get_language_config()
    detector = LanguageDetection(language_key, language_endpoint)
    
    result = detector.detect_language(args.text)
    
    if result['status'] == 'success':
        print(f"Idioma detectado: {result['language']} ({result['language_name']})")
        print(f"Confiança: {result['confidence_score']:.2f}")
    else:
        print(f"Erro: {result.get('error', 'Erro desconhecido')}")
        sys.exit(1)


def cmd_phrases(args, config, logger):
    """Executa extração de frases-chave."""
    logger.info(f"Extraindo frases-chave do texto: {args.text}")
    
    language_key, language_endpoint = config.get_language_config()
    analyzer = TextAnalysis(language_key, language_endpoint, args.language)
    
    result = analyzer.extract_key_phrases(args.text, args.language)
    
    if result['status'] == 'success':
        print(f"Frases-chave encontradas: {len(result['key_phrases'])}")
        for phrase in result['key_phrases']:
            print(f"  - {phrase}")
    else:
        print(f"Erro: {result.get('error', 'Erro desconhecido')}")
        sys.exit(1)


if __name__ == '__main__':
    main()
