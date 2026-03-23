"""
Azure Voice Language Lab - Web Application
=========================================

Aplicação web usando Streamlit para demonstrar as funcionalidades do Azure Speech e Language Studio.
"""

import streamlit as st
import os
from pathlib import Path
import io
import json
from datetime import datetime
import pandas as pd

# Adicionar diretório src ao path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.speech import SpeechRecognition, TextToSpeech
from src.language import TextAnalysis, Translation, LanguageDetection
from src.utils import Config, Logger


# Configuração da página
st.set_page_config(
    page_title="Azure Voice Language Lab",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar histórico de operações
if 'history' not in st.session_state:
    st.session_state.history = []

# Título e descrição
st.title("🎤 Azure Voice Language Lab")
st.markdown("""
Laboratório completo para exploração de Azure Speech e Language Studio.
Explore funcionalidades de reconhecimento de fala, síntese de voz, análise de texto e tradução.
""")

# Carregar configuração
@st.cache_resource
def load_config():
    """Carrega a configuração do projeto."""
    config = Config()
    validation = config.validate_config()
    if not validation['valid']:
        st.error("⚠️ Configuração inválida. Verifique as variáveis de ambiente.")
        for error in validation['errors']:
            st.error(f"- {error}")
        return None
    return config

config = load_config()

if config is None:
    st.stop()

# Barra lateral
st.sidebar.header("⚙️ Configurações")

# Seletor de funcionalidade
page = st.sidebar.selectbox(
    "Selecione uma funcionalidade:",
    [
        "🏠 Dashboard",
        "📜 Histórico de Operações",
        "🎤 Reconhecimento de Fala",
        "🔊 Síntese de Voz",
        "😊 Análise de Sentimento",
        "🔍 Extração de Entidades",
        "🌐 Tradução",
        "🔎 Detecção de Idioma",
        "📝 Frases-Chave"
    ]
)

# Informações sobre as credenciais
with st.sidebar.expander("🔑 Credenciais Azure"):
    st.info("""
    Configure suas credenciais do Azure no arquivo `.env`:
    - AZURE_SPEECH_KEY
    - AZURE_SPEECH_REGION
    - AZURE_LANGUAGE_KEY
    - AZURE_LANGUAGE_ENDPOINT
    - AZURE_TRANSLATOR_KEY
    - AZURE_TRANSLATOR_REGION
    """)

# Adicionar ao histórico
def add_to_history(operation, details, status):
    """Adiciona operação ao histórico."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append({
        'timestamp': timestamp,
        'operation': operation,
        'details': details,
        'status': status
    })

# Página de Dashboard
if page == "🏠 Dashboard":
    st.header("🏠 Dashboard")
    st.markdown("Visão geral do uso e funcionalidades do Azure Voice Language Lab.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Operações Realizadas",
            len(st.session_state.history),
            delta="Total"
        )

    with col2:
        st.metric(
            "Funcionalidades",
            7,
            delta="Disponíveis"
        )

    with col3:
        st.metric(
            "Idiomas Suportados",
            8,
            delta="Múltiplos"
        )

    # Estatísticas por tipo de operação
    if st.session_state.history:
        st.subheader("📊 Estatísticas por Tipo de Operação")

        operations = [op['operation'] for op in st.session_state.history]
        operation_counts = pd.Series(operations).value_counts()

        st.bar_chart(operation_counts)

        # Últimas operações
        st.subheader("📜 Últimas Operações")
        recent_history = st.session_state.history[-5:]
        for op in reversed(recent_history):
            status_emoji = "✅" if op['status'] == 'success' else "❌"
            st.markdown(f"""
            **{status_emoji} {op['operation']}**
            - *{op['timestamp']}*
            - {op['details']}
            """)

# Página de Histórico
elif page == "📜 Histórico de Operações":
    st.header("📜 Histórico de Operações")
    st.markdown("Todas as operações realizadas na sessão atual.")

    if st.session_state.history:
        # Converter para DataFrame
        df = pd.DataFrame(st.session_state.history)

        # Mostrar tabela
        st.dataframe(
            df,
            column_config={
                "timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
                "operation": st.column_config.TextColumn("Operação", width="medium"),
                "details": st.column_config.TextColumn("Detalhes", width="large"),
                "status": st.column_config.TextColumn("Status", width="small"),
            },
            use_container_width=True
        )

        # Botão para limpar histórico
        if st.button("🗑️ Limpar Histórico"):
            st.session_state.history = []
            st.rerun()

        # Botão para exportar histórico
        if st.button("📥 Exportar Histórico"):
            st.download_button(
                "Exportar",
                df.to_csv(index=False).encode('utf-8'),
                "historico.csv",
                "text/csv"
            )
    else:
        st.info("Nenhuma operação realizada ainda.")

# Página de Reconhecimento de Fala
elif page == "🎤 Reconhecimento de Fala":
    st.header("🎤 Reconhecimento de Fala (Speech-to-Text)")
    st.markdown("Converta áudio em texto usando Azure Speech Service.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Upload de Arquivo")
        audio_file = st.file_uploader(
            "Selecione um arquivo de áudio",
            type=['wav', 'mp3', 'ogg', 'flac']
        )

        language = st.selectbox(
            "Idioma",
            ['pt-BR', 'en-US', 'es-ES', 'fr-FR', 'de-DE', 'it-IT', 'ja-JP', 'zh-CN'],
            index=0
        )

    with col2:
        st.subheader("Opções")
        use_microphone = st.checkbox("Usar Microfone (Experimental)")

    if audio_file:
        st.audio(audio_file, format='audio/wav')

        if st.button("🚀 Reconhecer Fala"):
            with st.spinner("Reconhecendo fala..."):
                try:
                    # Salvar arquivo temporariamente
                    temp_path = Path("temp_audio.wav")
                    with open(temp_path, "wb") as f:
                        f.write(audio_file.getbuffer())

                    # Reconhecer fala
                    speech_key, speech_region = config.get_speech_config()
                    recognizer = SpeechRecognition(speech_key, speech_region, language)
                    result = recognizer.recognize_from_file(str(temp_path))

                    # Remover arquivo temporário
                    temp_path.unlink()

                    if result['status'] == 'success':
                        st.success("✅ Reconhecimento realizado com sucesso!")
                        st.subheader("Texto Reconhecido:")
                        st.write(result['text'])
                        st.caption(f"Idioma: {result['language']}")

                        add_to_history(
                            "Reconhecimento de Fala",
                            f"Arquivo: {audio_file.name}",
                            "success"
                        )
                    else:
                        st.error(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                        add_to_history(
                            "Reconhecimento de Fala",
                            f"Arquivo: {audio_file.name} - Erro",
                            "error"
                        )

                except Exception as e:
                    st.error(f"❌ Erro ao reconhecer fala: {str(e)}")

# Página de Síntese de Voz
elif page == "🔊 Síntese de Voz":
    st.header("🔊 Síntese de Voz (Text-to-Speech)")
    st.markdown("Converta texto em áudio usando Azure Speech Service.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Texto")
        text = st.text_area(
            "Digite o texto para ser sintetizado",
            "Olá, este é um teste de síntese de voz no Azure.",
            height=150
        )

    with col2:
        st.subheader("Opções")
        language = st.selectbox(
            "Idioma",
            ['pt-BR', 'en-US', 'es-ES', 'fr-FR', 'de-DE', 'it-IT', 'ja-JP', 'zh-CN'],
            index=0
        )

        # Obter vozes disponíveis
        speech_key, speech_region = config.get_speech_config()
        synthesizer = TextToSpeech(speech_key, speech_region)
        available_voices = synthesizer.list_voices_by_language(language)

        voice = st.selectbox("Voz", available_voices, index=0)

        rate = st.slider("Taxa de Fala", -50, 50, 0, 5)
        pitch = st.slider("Tom", -50, 50, 0, 5)

    if st.button("🚀 Sintetizar Voz"):
        with st.spinner("Sintetizando voz..."):
            try:
                synthesizer.set_voice(voice)
                result = synthesizer.synthesize_to_file(
                    text,
                    "output.wav",
                    f"{rate}%",
                    f"{pitch}%"
                )

                if result['status'] == 'success':
                    st.success("✅ Síntese realizada com sucesso!")

                    # Reproduzir áudio
                    audio_file = open(result['output_file'], 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/wav')

                    st.download_button(
                        "⬇️ Baixar Áudio",
                        audio_bytes,
                        "output.wav",
                        "audio/wav"
                    )

                    add_to_history(
                        "Síntese de Voz",
                        f"Voz: {voice}, Texto: {text[:50]}...",
                        "success"
                    )
                else:
                    st.error(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                    add_to_history(
                        "Síntese de Voz",
                        f"Voz: {voice} - Erro",
                        "error"
                    )

            except Exception as e:
                st.error(f"❌ Erro ao sintetizar voz: {str(e)}")

# Página de Análise de Sentimento
elif page == "😊 Análise de Sentimento":
    st.header("😊 Análise de Sentimento")
    st.markdown("Analise o sentimento de um texto usando Azure Language Service.")

    text = st.text_area(
        "Digite o texto para análise",
        "Estou muito feliz com os resultados deste projeto!",
        height=150
    )

    language = st.selectbox(
        "Idioma",
        ['pt-BR', 'en-US', 'es-ES', 'fr-FR', 'de-DE', 'it-IT'],
        index=0
    )

    if st.button("🚀 Analisar Sentimento"):
        with st.spinner("Analisando sentimento..."):
            try:
                language_key, language_endpoint = config.get_language_config()
                analyzer = TextAnalysis(language_key, language_endpoint, language)
                result = analyzer.analyze_sentiment(text, language)

                if result['status'] == 'success':
                    st.success("✅ Análise realizada com sucesso!")

                    # Mostrar resultado principal
                    sentiment = result['sentiment']
                    if sentiment == 'positive':
                        st.success(f"🎉 Sentimento: Positivo")
                    elif sentiment == 'negative':
                        st.error(f"😔 Sentimento: Negativo")
                    else:
                        st.info(f"😐 Sentimento: Neutro")

                    # Mostrar confiança
                    st.subheader("Confiança:")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Positivo", f"{result['confidence_scores']['positive']:.2%}")
                    with col2:
                        st.metric("Neutro", f"{result['confidence_scores']['neutral']:.2%}")
                    with col3:
                        st.metric("Negativo", f"{result['confidence_scores']['negative']:.2%}")

                    # Gráfico de barras
                    import matplotlib.pyplot as plt
                    fig, ax = plt.subplots()
                    sentiments = ['Positivo', 'Neutro', 'Negativo']
                    scores = [
                        result['confidence_scores']['positive'],
                        result['confidence_scores']['neutral'],
                        result['confidence_scores']['negative']
                    ]
                    colors = ['green', 'gray', 'red']
                    ax.bar(sentiments, scores, color=colors)
                    ax.set_ylim(0, 1)
                    ax.set_ylabel('Confiança')
                    ax.set_title('Análise de Sentimento')
                    st.pyplot(fig)

                    add_to_history(
                        "Análise de Sentimento",
                        f"Sentimento: {sentiment}",
                        "success"
                    )
                else:
                    st.error(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                    add_to_history(
                        "Análise de Sentimento",
                        "Erro",
                        "error"
                    )

            except Exception as e:
                st.error(f"❌ Erro ao analisar sentimento: {str(e)}")

# Página de Extração de Entidades
elif page == "🔍 Extração de Entidades":
    st.header("🔍 Extração de Entidades")
    st.markdown("Extraia entidades nomeadas de um texto usando Azure Language Service.")

    text = st.text_area(
        "Digite o texto para extração",
        "A Microsoft foi fundada por Bill Gates e Paul Allen em 1975 em Albuquerque, Novo México.",
        height=150
    )

    language = st.selectbox(
        "Idioma",
        ['pt-BR', 'en-US', 'es-ES', 'fr-FR', 'de-DE', 'it-IT'],
        index=0
    )

    if st.button("🚀 Extrair Entidades"):
        with st.spinner("Extraindo entidades..."):
            try:
                language_key, language_endpoint = config.get_language_config()
                analyzer = TextAnalysis(language_key, language_endpoint, language)
                result = analyzer.extract_entities(text, language)

                if result['status'] == 'success':
                    st.success(f"✅ {len(result['entities'])} entidades encontradas!")

                    # Mostrar entidades em tabela
                    entities_data = []
                    for entity in result['entities']:
                        entities_data.append({
                            "Texto": entity['text'],
                            "Categoria": entity['category'],
                            "Subcategoria": entity.get('subcategory', 'N/A'),
                            "Confiança": f"{entity['confidence_score']:.2%}"
                        })

                    st.dataframe(entities_data, use_container_width=True)

                    add_to_history(
                        "Extração de Entidades",
                        f"{len(result['entities'])} entidades encontradas",
                        "success"
                    )
                else:
                    st.error(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                    add_to_history(
                        "Extração de Entidades",
                        "Erro",
                        "error"
                    )

            except Exception as e:
                st.error(f"❌ Erro ao extrair entidades: {str(e)}")

# Página de Tradução
elif page == "🌐 Tradução":
    st.header("🌐 Tradução")
    st.markdown("Traduza texto usando Azure Translator Service.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Texto Original")
        text = st.text_area(
            "Digite o texto para traduzir",
            "Hello, how are you?",
            height=150
        )

        from_lang = st.selectbox(
            "Idioma de Origem",
            ['Detectar automaticamente', 'pt', 'en', 'es', 'fr', 'de', 'it', 'ja', 'zh'],
            index=0
        )

    with col2:
        st.subheader("Texto Traduzido")
        to_lang = st.selectbox(
            "Idioma de Destino",
            ['pt', 'en', 'es', 'fr', 'de', 'it', 'ja', 'zh'],
            index=0
        )

        if st.button("🚀 Traduzir"):
            with st.spinner("Traduzindo..."):
                try:
                    translator_key, translator_region = config.get_translator_config()
                    translator = Translation(translator_key, translator_region)

                    from_lang_code = None if from_lang == 'Detectar automaticamente' else from_lang
                    result = translator.translate(text, to_lang, from_lang_code)

                    if result['status'] == 'success':
                        st.success("✅ Tradução realizada com sucesso!")
                        st.write(result['translation'])
                        st.caption(f"De: {result['from_language']} -> Para: {result['to_language']}")
                        if 'confidence' in result:
                            st.caption(f"Confiança: {result['confidence']:.2%}")

                        add_to_history(
                            "Tradução",
                            f"{result['from_language']} -> {result['to_language']}",
                            "success"
                        )
                    else:
                        st.error(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                        add_to_history(
                            "Tradução",
                            "Erro",
                            "error"
                        )

                except Exception as e:
                    st.error(f"❌ Erro ao traduzir: {str(e)}")

# Página de Detecção de Idioma
elif page == "🔎 Detecção de Idioma":
    st.header("🔎 Detecção de Idioma")
    st.markdown("Detecte o idioma de um texto usando Azure Language Service.")

    text = st.text_area(
        "Digite o texto para detecção",
        "Bonjour, comment allez-vous?",
        height=150
    )

    if st.button("🚀 Detectar Idioma"):
        with st.spinner("Detectando idioma..."):
            try:
                language_key, language_endpoint = config.get_language_config()
                detector = LanguageDetection(language_key, language_endpoint)
                result = detector.detect_language(text)

                if result['status'] == 'success':
                    st.success("✅ Idioma detectado com sucesso!")
                    st.subheader(f"🌍 {result['language_name']}")
                    st.write(f"Código: {result['language']}")
                    st.write(f"Confiança: {result['confidence_score']:.2%}")

                    add_to_history(
                        "Detecção de Idioma",
                        f"Idioma: {result['language_name']}",
                        "success"
                    )
                else:
                    st.error(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                    add_to_history(
                        "Detecção de Idioma",
                        "Erro",
                        "error"
                    )

            except Exception as e:
                st.error(f"❌ Erro ao detectar idioma: {str(e)}")

# Página de Frases-Chave
elif page == "📝 Frases-Chave":
    st.header("📝 Extração de Frases-Chave")
    st.markdown("Extraia frases-chave de um texto usando Azure Language Service.")

    text = st.text_area(
        "Digite o texto para extração",
        "A inteligência artificial está transformando a maneira como trabalhamos e vivemos. Machine learning e deep learning são áreas em crescimento.",
        height=150
    )

    language = st.selectbox(
        "Idioma",
        ['pt-BR', 'en-US', 'es-ES', 'fr-FR', 'de-DE', 'it-IT'],
        index=0
    )

    if st.button("🚀 Extrair Frases-Chave"):
        with st.spinner("Extraindo frases-chave..."):
            try:
                language_key, language_endpoint = config.get_language_config()
                analyzer = TextAnalysis(language_key, language_endpoint, language)
                result = analyzer.extract_key_phrases(text, language)

                if result['status'] == 'success':
                    st.success(f"✅ {len(result['key_phrases'])} frases-chave encontradas!")

                    for i, phrase in enumerate(result['key_phrases'], 1):
                        st.write(f"{i}. {phrase}")

                    add_to_history(
                        "Extração de Frases-Chave",
                        f"{len(result['key_phrases'])} frases-chave",
                        "success"
                    )
                else:
                    st.error(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                    add_to_history(
                        "Extração de Frases-Chave",
                        "Erro",
                        "error"
                    )

            except Exception as e:
                st.error(f"❌ Erro ao extrair frases-chave: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
**Azure Voice Language Lab** - Desenvolvido por Rone Bragaglia

Este projeto demonstra as capacidades do Azure Speech Service e Azure Language Studio.
""")
