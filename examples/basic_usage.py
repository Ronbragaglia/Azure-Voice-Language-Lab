"""
Azure Voice Language Lab - Exemplos Básicos de Uso
=================================================

Este arquivo demonstra o uso básico das principais funcionalidades do Azure Voice Language Lab.
"""

import os
from pathlib import Path

# Adicionar diretório src ao path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.speech import SpeechRecognition, TextToSpeech
from src.language import TextAnalysis, Translation, LanguageDetection
from src.utils import Config


def example_1_speech_to_text():
    """
    Exemplo 1: Reconhecimento de Fala (Speech-to-Text)
    --------------------------------------------------
    Converte um arquivo de áudio em texto.
    """
    print("\n" + "="*60)
    print("Exemplo 1: Reconhecimento de Fala")
    print("="*60)

    try:
        # Carregar configuração
        config = Config()
        speech_key, speech_region = config.get_speech_config()

        # Inicializar reconhecimento de fala
        recognizer = SpeechRecognition(speech_key, speech_region, "pt-BR")

        # Reconhecer fala de um arquivo
        audio_file = "audio_samples/sample.wav"
        if os.path.exists(audio_file):
            result = recognizer.recognize_from_file(audio_file)

            if result['status'] == 'success':
                print(f"✅ Texto reconhecido: {result['text']}")
                print(f"🌐 Idioma: {result['language']}")
            else:
                print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
        else:
            print(f"⚠️ Arquivo de áudio não encontrado: {audio_file}")
            print("💡 Dica: Coloque um arquivo .wav em audio_samples/")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def example_2_text_to_speech():
    """
    Exemplo 2: Síntese de Voz (Text-to-Speech)
    --------------------------------------------
    Converte texto em áudio.
    """
    print("\n" + "="*60)
    print("Exemplo 2: Síntese de Voz")
    print("="*60)

    try:
        # Carregar configuração
        config = Config()
        speech_key, speech_region = config.get_speech_config()

        # Inicializar síntese de voz
        synthesizer = TextToSpeech(
            speech_key,
            speech_region,
            voice_name="pt-BR-FranciscaNeural"
        )

        # Texto para sintetizar
        text = "Olá! Este é um exemplo de síntese de voz usando Azure Speech Service."

        # Sintetizar texto
        result = synthesizer.synthesize_to_file(
            text,
            "output/example_speech.wav",
            rate="+10%",
            pitch="-5%"
        )

        if result['status'] == 'success':
            print(f"✅ Áudio gerado: {result['output_file']}")
            print(f"🎤 Voz: {result['voice']}")
            print(f"📝 Texto: {result['text']}")
        else:
            print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def example_3_sentiment_analysis():
    """
    Exemplo 3: Análise de Sentimento
    ---------------------------------
    Analisa o sentimento de um texto.
    """
    print("\n" + "="*60)
    print("Exemplo 3: Análise de Sentimento")
    print("="*60)

    try:
        # Carregar configuração
        config = Config()
        language_key, language_endpoint = config.get_language_config()

        # Inicializar análise de texto
        analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

        # Textos para analisar
        texts = [
            "Estou muito feliz com os resultados deste projeto!",
            "O serviço não funcionou como esperado.",
            "O produto é bom, mas o preço é alto."
        ]

        for text in texts:
            result = analyzer.analyze_sentiment(text, "pt-BR")

            if result['status'] == 'success':
                sentiment = result['sentiment']
                confidence = result['confidence_scores']

                print(f"\n📝 Texto: {text}")
                print(f"😊 Sentimento: {sentiment.upper()}")
                print(f"📊 Confiança:")
                print(f"   Positivo: {confidence['positive']:.2%}")
                print(f"   Neutro: {confidence['neutral']:.2%}")
                print(f"   Negativo: {confidence['negative']:.2%}")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def example_4_entity_extraction():
    """
    Exemplo 4: Extração de Entidades
    --------------------------------
    Extrai entidades nomeadas de um texto.
    """
    print("\n" + "="*60)
    print("Exemplo 4: Extração de Entidades")
    print("="*60)

    try:
        # Carregar configuração
        config = Config()
        language_key, language_endpoint = config.get_language_config()

        # Inicializar análise de texto
        analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

        # Texto para análise
        text = """
        A Microsoft foi fundada por Bill Gates e Paul Allen em 1975 em Albuquerque,
        Novo México. A empresa está sediada em Redmond, Washington, e é liderada
        pelo CEO Satya Nadella.
        """

        result = analyzer.extract_entities(text, "pt-BR")

        if result['status'] == 'success':
            print(f"✅ {len(result['entities'])} entidades encontradas:\n")

            for entity in result['entities']:
                print(f"📌 {entity['text']}")
                print(f"   Categoria: {entity['category']}")
                print(f"   Subcategoria: {entity.get('subcategory', 'N/A')}")
                print(f"   Confiança: {entity['confidence_score']:.2%}")
                print()

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def example_5_translation():
    """
    Exemplo 5: Tradução
    --------------------
    Traduz texto entre idiomas.
    """
    print("\n" + "="*60)
    print("Exemplo 5: Tradução")
    print("="*60)

    try:
        # Carregar configuração
        config = Config()
        translator_key, translator_region = config.get_translator_config()

        # Inicializar tradutor
        translator = Translation(translator_key, translator_region)

        # Textos para traduzir
        translations = [
            ("Hello, how are you?", "pt", "en"),
            ("Olá, tudo bem?", "en", "pt"),
            ("Bonjour, comment allez-vous?", "pt", "fr"),
        ]

        for text, to_lang, from_lang in translations:
            result = translator.translate(text, to_lang, from_lang)

            if result['status'] == 'success':
                print(f"\n📝 Original ({result['from_language']}): {result['text']}")
                print(f"🌐 Tradução ({result['to_language']}): {result['translation']}")
                if 'confidence' in result:
                    print(f"📊 Confiança: {result['confidence']:.2%}")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def example_6_language_detection():
    """
    Exemplo 6: Detecção de Idioma
    ------------------------------
    Detecta o idioma de um texto.
    """
    print("\n" + "="*60)
    print("Exemplo 6: Detecção de Idioma")
    print("="*60)

    try:
        # Carregar configuração
        config = Config()
        language_key, language_endpoint = config.get_language_config()

        # Inicializar detector de idioma
        detector = LanguageDetection(language_key, language_endpoint)

        # Textos em diferentes idiomas
        texts = [
            "Olá, como você está?",
            "Hello, how are you?",
            "Bonjour, comment allez-vous?",
            "Hola, ¿cómo estás?",
            "Ciao, come stai?",
        ]

        for text in texts:
            result = detector.detect_language(text)

            if result['status'] == 'success':
                print(f"\n📝 Texto: {text}")
                print(f"🌍 Idioma: {result['language_name']} ({result['language']})")
                print(f"📊 Confiança: {result['confidence_score']:.2%}")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def example_7_key_phrases():
    """
    Exemplo 7: Extração de Frases-Chave
    -----------------------------------
    Extrai as frases-chave de um texto.
    """
    print("\n" + "="*60)
    print("Exemplo 7: Extração de Frases-Chave")
    print("="*60)

    try:
        # Carregar configuração
        config = Config()
        language_key, language_endpoint = config.get_language_config()

        # Inicializar análise de texto
        analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

        # Texto para análise
        text = """
        A inteligência artificial está transformando a maneira como trabalhamos e vivemos.
        Machine learning e deep learning são áreas em crescimento constante.
        O processamento de linguagem natural permite que computadores entendam textos humanos.
        """

        result = analyzer.extract_key_phrases(text, "pt-BR")

        if result['status'] == 'success':
            print(f"✅ {len(result['key_phrases'])} frases-chave encontradas:\n")

            for i, phrase in enumerate(result['key_phrases'], 1):
                print(f"{i}. {phrase}")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def example_8_multiple_voices():
    """
    Exemplo 8: Usando Múltiplas Vozes
    ----------------------------------
    Demonstra como usar diferentes vozes para síntese.
    """
    print("\n" + "="*60)
    print("Exemplo 8: Usando Múltiplas Vozes")
    print("="*60)

    try:
        # Carregar configuração
        config = Config()
        speech_key, speech_region = config.get_speech_config()

        # Inicializar síntese de voz
        synthesizer = TextToSpeech(speech_key, speech_region)

        # Obter vozes disponíveis
        voices = synthesizer.get_available_voices("pt-BR")

        print(f"✅ {len(voices['pt-BR'])} vozes disponíveis em Português (BR):\n")

        for i, voice in enumerate(voices['pt-BR'][:5], 1):
            print(f"{i}. {voice}")

        # Sintetizar com diferentes vozes
        text = "Olá! Esta é uma demonstração de diferentes vozes."
        selected_voices = ["pt-BR-FranciscaNeural", "pt-BR-AntonioNeural"]

        for voice in selected_voices:
            synthesizer.set_voice(voice)
            result = synthesizer.synthesize_to_file(
                text,
                f"output/voice_{voice.split('-')[-1]}.wav"
            )

            if result['status'] == 'success':
                print(f"\n✅ Áudio gerado com voz: {voice}")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def main():
    """
    Função principal que executa todos os exemplos.
    """
    print("\n" + "="*60)
    print("Azure Voice Language Lab - Exemplos de Uso")
    print("="*60)
    print("\nEste script demonstra as principais funcionalidades do projeto.")
    print("Certifique-se de configurar suas credenciais do Azure no arquivo .env\n")

    # Criar diretório de saída se não existir
    Path("output").mkdir(exist_ok=True)

    # Executar exemplos
    examples = [
        ("Reconhecimento de Fala", example_1_speech_to_text),
        ("Síntese de Voz", example_2_text_to_speech),
        ("Análise de Sentimento", example_3_sentiment_analysis),
        ("Extração de Entidades", example_4_entity_extraction),
        ("Tradução", example_5_translation),
        ("Detecção de Idioma", example_6_language_detection),
        ("Extração de Frases-Chave", example_7_key_phrases),
        ("Múltiplas Vozes", example_8_multiple_voices),
    ]

    print("\nSelecione um exemplo para executar:")
    print("0. Executar todos os exemplos")

    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")

    try:
        choice = input("\nEscolha (0-8): ").strip()

        if choice == "0":
            for name, func in examples:
                func()
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            examples[int(choice) - 1][1]()
        else:
            print("❌ Escolha inválida")

    except KeyboardInterrupt:
        print("\n\n⚠️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

    print("\n" + "="*60)
    print("Fim dos exemplos")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
