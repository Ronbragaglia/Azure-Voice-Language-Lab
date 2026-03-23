"""
Azure Voice Language Lab - Exemplos Avançados de Uso
====================================================

Este arquivo demonstra funcionalidades avançadas e casos de uso complexos.
"""

import os
import asyncio
from pathlib import Path
from typing import List, Dict

# Adicionar diretório src ao path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.speech import SpeechRecognition, TextToSpeech
from src.language import TextAnalysis, Translation, LanguageDetection
from src.utils import Config


def advanced_example_1_batch_processing():
    """
    Exemplo Avançado 1: Processamento em Lote
    ------------------------------------------
    Processa múltiplos arquivos de áudio ou textos de uma vez.
    """
    print("\n" + "="*60)
    print("Exemplo Avançado 1: Processamento em Lote")
    print("="*60)

    try:
        config = Config()
        speech_key, speech_region = config.get_speech_config()
        language_key, language_endpoint = config.get_language_config()

        # Inicializar serviços
        recognizer = SpeechRecognition(speech_key, speech_region, "pt-BR")
        analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

        # Lista de arquivos para processar
        audio_files = [
            "audio_samples/sample1.wav",
            "audio_samples/sample2.wav",
            "audio_samples/sample3.wav",
        ]

        results = []

        for audio_file in audio_files:
            if os.path.exists(audio_file):
                # Reconhecer fala
                speech_result = recognizer.recognize_from_file(audio_file)

                if speech_result['status'] == 'success':
                    text = speech_result['text']

                    # Analisar sentimento
                    sentiment_result = analyzer.analyze_sentiment(text, "pt-BR")

                    results.append({
                        'file': audio_file,
                        'text': text,
                        'sentiment': sentiment_result['sentiment'],
                        'confidence': sentiment_result['confidence_scores']
                    })

        # Exibir resultados
        print(f"\n✅ Processados {len(results)} arquivos:\n")

        for i, result in enumerate(results, 1):
            print(f"{i}. Arquivo: {result['file']}")
            print(f"   Texto: {result['text']}")
            print(f"   Sentimento: {result['sentiment'].upper()}")
            print(f"   Confiança (Positivo): {result['confidence']['positive']:.2%}")
            print()

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def advanced_example_2_real_time_translation():
    """
    Exemplo Avançado 2: Tradução em Tempo Real
    -------------------------------------------
    Simula um sistema de tradução em tempo real.
    """
    print("\n" + "="*60)
    print("Exemplo Avançado 2: Tradução em Tempo Real")
    print("="*60)

    try:
        config = Config()
        translator_key, translator_region = config.get_translator_config()
        language_key, language_endpoint = config.get_language_config()

        # Inicializar serviços
        translator = Translation(translator_key, translator_region)
        detector = LanguageDetection(language_key, language_endpoint)

        # Simular mensagens de chat
        messages = [
            {"user": "Alice", "text": "Hello, how are you?"},
            {"user": "Bob", "text": "Olá, tudo bem?"},
            {"user": "Alice", "text": "I'm doing great, thanks!"},
            {"user": "Bob", "text": "Estou bem também, obrigado!"},
        ]

        print("\n💬 Chat com Tradução em Tempo Real:\n")

        for message in messages:
            user = message['user']
            text = message['text']

            # Detectar idioma
            lang_result = detector.detect_language(text)
            detected_lang = lang_result['language']

            # Traduzir para o outro idioma
            if detected_lang == 'en':
                target_lang = 'pt'
                target_name = 'Português'
            else:
                target_lang = 'en'
                target_name = 'Inglês'

            translate_result = translator.translate(text, target_lang, detected_lang)

            print(f"👤 {user}:")
            print(f"   Original ({lang_result['language_name']}): {text}")
            print(f"   Tradução ({target_name}): {translate_result['translation']}")
            print()

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def advanced_example_3_sentiment_dashboard():
    """
    Exemplo Avançado 3: Dashboard de Sentimentos
    --------------------------------------------
    Cria um resumo de sentimentos de múltiplos textos.
    """
    print("\n" + "="*60)
    print("Exemplo Avançado 3: Dashboard de Sentimentos")
    print("="*60)

    try:
        config = Config()
        language_key, language_endpoint = config.get_language_config()

        # Inicializar análise
        analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

        # Reviews de produtos
        reviews = [
            "O produto é excelente! Superou todas as minhas expectativas.",
            "Não gostei do produto. A qualidade é ruim.",
            "O produto é bom, mas o preço poderia ser melhor.",
            "Excelente custo-benefício. Recomendo!",
            "A entrega foi rápida e o produto chegou em perfeitas condições.",
            "O produto tem alguns problemas, mas no geral é aceitável.",
        ]

        results = []

        for review in reviews:
            result = analyzer.analyze_sentiment(review, "pt-BR")
            results.append({
                'text': review,
                'sentiment': result['sentiment'],
                'confidence': result['confidence_scores']
            })

        # Calcular estatísticas
        total = len(results)
        positive = sum(1 for r in results if r['sentiment'] == 'positive')
        negative = sum(1 for r in results if r['sentiment'] == 'negative')
        neutral = sum(1 for r in results if r['sentiment'] == 'neutral')

        # Exibir dashboard
        print("\n📊 Dashboard de Sentimentos\n")
        print(f"Total de Reviews: {total}")
        print(f"Positivos: {positive} ({positive/total:.1%})")
        print(f"Negativos: {negative} ({negative/total:.1%})")
        print(f"Neutros: {neutral} ({neutral/total:.1%})")

        print("\n📝 Reviews por Sentimento:\n")

        # Positivos
        print("✅ Positivos:")
        for r in results:
            if r['sentiment'] == 'positive':
                print(f"   - {r['text']}")

        # Negativos
        print("\n❌ Negativos:")
        for r in results:
            if r['sentiment'] == 'negative':
                print(f"   - {r['text']}")

        # Neutros
        print("\n😐 Neutros:")
        for r in results:
            if r['sentiment'] == 'neutral':
                print(f"   - {r['text']}")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def advanced_example_4_multi_language_podcast():
    """
    Exemplo Avançado 4: Podcast Multilíngue
    ----------------------------------------
    Cria um podcast com vozes em diferentes idiomas.
    """
    print("\n" + "="*60)
    print("Exemplo Avançado 4: Podcast Multilíngue")
    print("="*60)

    try:
        config = Config()
        speech_key, speech_region = config.get_speech_config()

        # Inicializar síntese
        synthesizer = TextToSpeech(speech_key, speech_region)

        # Segmentos do podcast em diferentes idiomas
        segments = [
            {
                "voice": "pt-BR-FranciscaNeural",
                "language": "pt-BR",
                "text": "Olá e bem-vindos ao nosso podcast multilíngue!"
            },
            {
                "voice": "en-US-JennyNeural",
                "language": "en-US",
                "text": "Hello and welcome to our multilingual podcast!"
            },
            {
                "voice": "es-ES-ElviraNeural",
                "language": "es-ES",
                "text": "¡Hola y bienvenidos a nuestro podcast multilingüe!"
            },
            {
                "voice": "fr-FR-DeniseNeural",
                "language": "fr-FR",
                "text": "Bonjour et bienvenue dans notre podcast multilingue!"
            },
        ]

        print("\n🎙️ Criando Podcast Multilíngue:\n")

        for i, segment in enumerate(segments, 1):
            voice = segment['voice']
            text = segment['text']
            language = segment['language']

            synthesizer.set_voice(voice)
            result = synthesizer.synthesize_to_file(
                text,
                f"output/podcast_segment_{i}.wav"
            )

            if result['status'] == 'success':
                print(f"✅ Segmento {i} ({language}): {text[:50]}...")

        print("\n🎧 Podcast criado com sucesso!")
        print("💡 Dica: Use um editor de áudio para combinar os segmentos.")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def advanced_example_5_entity_analysis_pipeline():
    """
    Exemplo Avançado 5: Pipeline de Análise de Entidades
    ----------------------------------------------------
    Cria um pipeline completo para análise de entidades em textos.
    """
    print("\n" + "="*60)
    print("Exemplo Avançado 5: Pipeline de Análise de Entidades")
    print("="*60)

    try:
        config = Config()
        language_key, language_endpoint = config.get_language_config()

        # Inicializar análise
        analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

        # Texto de notícia
        news_text = """
        A Microsoft anunciou hoje uma parceria estratégica com a OpenAI.
        A empresa, liderada pelo CEO Satya Nadella, investiu bilhões
        de dólares na empresa de inteligência artificial. A parceria
        visa acelerar o desenvolvimento de tecnologias de IA e expandir
        o acesso a ferramentas avançadas de machine learning.
        """

        print("\n📰 Análise de Notícia:\n")
        print(f"Texto: {news_text}\n")

        # Extrair entidades
        result = analyzer.extract_entities(news_text, "pt-BR")

        if result['status'] == 'success':
            entities = result['entities']

            # Agrupar por categoria
            categories: Dict[str, List[Dict]] = {}
            for entity in entities:
                category = entity['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(entity)

            # Exibir por categoria
            print("📊 Entidades por Categoria:\n")

            for category, ents in categories.items():
                print(f"🔹 {category}:")
                for entity in ents:
                    print(f"   - {entity['text']} (Confiança: {entity['confidence_score']:.2%})")
                print()

            # Resumo
            print(f"\n📈 Resumo:")
            print(f"   Total de entidades: {len(entities)}")
            print(f"   Categorias encontradas: {len(categories)}")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def advanced_example_6_custom_voice_settings():
    """
    Exemplo Avançado 6: Configurações Personalizadas de Voz
    --------------------------------------------------------
    Demonstra como ajustar parâmetros avançados de síntese de voz.
    """
    print("\n" + "="*60)
    print("Exemplo Avançado 6: Configurações Personalizadas de Voz")
    print("="*60)

    try:
        config = Config()
        speech_key, speech_region = config.get_speech_config()

        # Inicializar síntese
        synthesizer = TextToSpeech(speech_key, speech_region, "pt-BR-FranciscaNeural")

        # Texto para testar
        text = "Este é um teste de diferentes configurações de voz."

        # Configurações diferentes
        settings = [
            {"name": "Normal", "rate": "0%", "pitch": "0%"},
            {"name": "Rápido", "rate": "+30%", "pitch": "0%"},
            {"name": "Lento", "rate": "-20%", "pitch": "0%"},
            {"name": "Agudo", "rate": "0%", "pitch": "+20%"},
            {"name": "Grave", "rate": "0%", "pitch": "-20%"},
            {"name": "Rápido e Agudo", "rate": "+30%", "pitch": "+20%"},
        ]

        print("\n🎤 Testando Configurações de Voz:\n")

        for setting in settings:
            name = setting['name']
            rate = setting['rate']
            pitch = setting['pitch']

            result = synthesizer.synthesize_to_file(
                text,
                f"output/voice_{name.lower().replace(' ', '_')}.wav",
                rate=rate,
                pitch=pitch
            )

            if result['status'] == 'success':
                print(f"✅ {name}: Taxa={rate}, Tom={pitch}")

        print("\n💡 Dica: Ouça os arquivos para comparar as diferenças.")

    except Exception as e:
        print(f"❌ Erro ao executar exemplo: {e}")


def main():
    """
    Função principal que executa todos os exemplos avançados.
    """
    print("\n" + "="*60)
    print("Azure Voice Language Lab - Exemplos Avançados")
    print("="*60)
    print("\nEste script demonstra funcionalidades avançadas do projeto.")
    print("Certifique-se de configurar suas credenciais do Azure no arquivo .env\n")

    # Criar diretório de saída se não existir
    Path("output").mkdir(exist_ok=True)

    # Executar exemplos
    examples = [
        ("Processamento em Lote", advanced_example_1_batch_processing),
        ("Tradução em Tempo Real", advanced_example_2_real_time_translation),
        ("Dashboard de Sentimentos", advanced_example_3_sentiment_dashboard),
        ("Podcast Multilíngue", advanced_example_4_multi_language_podcast),
        ("Pipeline de Análise de Entidades", advanced_example_5_entity_analysis_pipeline),
        ("Configurações Personalizadas de Voz", advanced_example_6_custom_voice_settings),
    ]

    print("\nSelecione um exemplo para executar:")
    print("0. Executar todos os exemplos")

    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")

    try:
        choice = input("\nEscolha (0-6): ").strip()

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
    print("Fim dos exemplos avançados")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
