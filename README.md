# 🎤 Azure Voice Language Lab

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Azure](https://img.shields.io/badge/Azure-Cognitive%20Services-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/services/cognitive-services/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![GitHub stars](https://img.shields.io/github/stars/Ronbragaglia/Azure-Voice-Language-Lab?style=social)](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Ronbragaglia/Azure-Voice-Language-Lab?style=social)](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab/network/members)

> 🚀 **Laboratório completo para exploração de Azure Speech e Language Studio com Python**

Um toolkit abrangente para trabalhar com serviços cognitivos do Azure, incluindo reconhecimento de fala, síntese de voz, análise de texto, tradução e detecção de idioma. Perfeito para desenvolvedores, pesquisadores e entusiastas de IA.

## ✨ Funcionalidades

### 🎤 Speech (Fala)
- **Speech-to-Text**: Converta áudio em texto com alta precisão
- **Text-to-Speech**: Sintetize voz natural a partir de texto
- **Suporte a múltiplos idiomas**: Português, Inglês, Espanhol, Francês, Alemão, Italiano, Japonês, Chinês e mais
- **Vozes neurais**: Mais de 50 vozes neurais de alta qualidade
- **Ajustes de prosódia**: Controle taxa de fala e tom

### 📝 Language (Linguagem)
- **Análise de Sentimento**: Detecte emoções em textos (positivo, neutro, negativo)
- **Extração de Entidades**: Identifique pessoas, lugares, organizações e mais
- **Frases-Chave**: Extraia os principais tópicos de um texto
- **Detecção de Idioma**: Identifique automaticamente o idioma do texto
- **Entidades de Saúde**: Análise especializada para textos médicos

### 🌐 Translation (Tradução)
- **Tradução em tempo real**: Traduza textos entre mais de 100 idiomas
- **Detecção automática**: Sistema detecta idioma de origem automaticamente
- **Pontuação de confiança**: Avalie a qualidade da tradução

### 🖥️ Interfaces
- **CLI completa**: Interface de linha de comando para todas as funcionalidades
- **Web App Streamlit**: Interface gráfica interativa e amigável
- **API Python**: Biblioteca programática para integração

## 📦 Instalação

### Via pip (recomendado)

```bash
pip install azure-voice-language-lab
```

### Via pip com extras

```bash
# Instalação completa com todas as dependências
pip install azure-voice-language-lab[all]

# Apenas funcionalidades web
pip install azure-voice-language-lab[web]

# Apenas processamento de áudio
pip install azure-voice-language-lab[audio]

# Ferramentas de desenvolvimento
pip install azure-voice-language-lab[dev]
```

### Via Docker

```bash
docker pull ronbragaglia/azure-voice-language-lab:latest
```

### Desenvolvimento

```bash
git clone https://github.com/Ronbragaglia/Azure-Voice-Language-Lab.git
cd Azure-Voice-Language-Lab
pip install -e ".[dev]"
```

## ⚙️ Configuração

### 1. Criar recursos no Azure

1. Acesse o [Azure Portal](https://portal.azure.com/)
2. Crie os recursos necessários:
   - **Speech Service**: Para reconhecimento e síntese de voz
   - **Language Service**: Para análise de texto
   - **Translator Service**: Para tradução (opcional)

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Azure Speech Service
AZURE_SPEECH_KEY=sua_chave_speech
AZURE_SPEECH_REGION=brazilsouth

# Azure Language Service
AZURE_LANGUAGE_KEY=sua_chave_language
AZURE_LANGUAGE_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/

# Azure Translator (opcional)
AZURE_TRANSLATOR_KEY=sua_chave_translator
AZURE_TRANSLATOR_REGION=brazilsouth
```

### 3. Validar configuração

```bash
azure-speech-lab --help
```

## 🚀 Uso Rápido

### CLI (Linha de Comando)

```bash
# Reconhecimento de fala
azure-speech-lab recognize --audio audio.wav --language pt-BR

# Síntese de voz
azure-speech-lab synthesize --text "Olá, mundo!" --output voz.wav --voice pt-BR-FranciscaNeural

# Análise de sentimento
azure-speech-lab sentiment --text "Estou muito feliz hoje!" --language pt-BR

# Tradução
azure-speech-lab translate --text "Hello world" --to pt --from en

# Detecção de idioma
azure-speech-lab detect --text "Bonjour le monde"

# Extração de entidades
azure-speech-lab entities --text "A Microsoft foi fundada em 1975" --language pt-BR

# Frases-chave
azure-speech-lab phrases --text "Machine learning é uma área em crescimento" --language pt-BR
```

### Python API

```python
from src.speech import SpeechRecognition, TextToSpeech
from src.language import TextAnalysis, LanguageDetection
from src.utils import Config

# Carregar configuração
config = Config()

# === RECONHECIMENTO DE FALA ===
speech_key, speech_region = config.get_speech_config()
recognizer = SpeechRecognition(speech_key, speech_region, "pt-BR")

# De arquivo
result = recognizer.recognize_from_file("audio.wav")
print(result["text"])

# === SÍNTESE DE VOZ ===
synthesizer = TextToSpeech(speech_key, speech_region, "pt-BR-FranciscaNeural")
result = synthesizer.synthesize_to_file(
    "Olá! Este é um teste de síntese de voz.",
    "output.wav",
    rate="+10%",
    pitch="-5%"
)

# === ANÁLISE DE SENTIMENTO ===
language_key, language_endpoint = config.get_language_config()
analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

result = analyzer.analyze_sentiment("Estou muito feliz com este projeto!")
print(f"Sentimento: {result['sentiment']}")
print(f"Confiança: {result['confidence_scores']}")

# === DETECÇÃO DE IDIOMA ===
detector = LanguageDetection(language_key, language_endpoint)
result = detector.detect_language("Bonjour, comment allez-vous?")
print(f"Idioma: {result['language_name']} ({result['language']})")
```

### Web App (Streamlit)

```bash
# Iniciar aplicação web
streamlit run web/app.py

# Ou via CLI
azure-speech-lab web
```

Acesse `http://localhost:8501` para usar a interface gráfica.

## 📖 Documentação

### Estrutura do Projeto

```
Azure-Voice-Language-Lab/
├── 📁 src/                    # Código fonte principal
│   ├── 📁 speech/            # Módulos de fala (STT/TTS)
│   │   ├── recognition.py    # Reconhecimento de fala
│   │   └── synthesis.py      # Síntese de voz
│   ├── 📁 language/          # Módulos de linguagem
│   │   ├── analysis.py       # Análise de texto
│   │   ├── detection.py      # Detecção de idioma
│   │   └── translation.py    # Tradução
│   └── 📁 utils/             # Utilitários
│       ├── config.py         # Gerenciamento de configuração
│       ├── logger.py         # Sistema de logging
│       └── validators.py     # Validadores
├── 📁 web/                   # Aplicação web Streamlit
│   └── app.py               # Interface gráfica
├── 📁 examples/              # Exemplos de uso
├── 📁 tests/                 # Testes unitários
├── 📁 docs/                  # Documentação
├── 📁 audio_samples/         # Amostras de áudio para teste
└── 📁 output/                # Arquivos de saída
```

### Vozes Disponíveis

<details>
<summary>🇧🇷 Português (Brasil)</summary>

| Voz | Gênero | Descrição |
|-----|--------|-----------|
| `pt-BR-FranciscaNeural` | Feminino | Voz natural e expressiva |
| `pt-BR-AntonioNeural` | Masculino | Voz calma e profissional |
| `pt-BR-BrendaNeural` | Feminino | Voz jovem e dinâmica |
| `pt-BR-DonatoNeural` | Masculino | Voz grave e séria |
| `pt-BR-ElzaNeural` | Feminino | Voz suave |
| `pt-BR-FabioNeural` | Masculino | Voz energética |
| `pt-BR-GiovannaNeural` | Feminino | Voz amigável |
| `pt-BR-HenriqueNeural` | Masculino | Voz jovial |
| `pt-BR-IsabelaNeural` | Feminino | Voz doce |
| `pt-BR-LeandroNeural` | Masculino | Voz confiável |
| `pt-BR-LeticiaNeural` | Feminino | Voz clara |
| `pt-BR-ManuelaNeural` | Feminino | Voz alegre |
| `pt-BR-NicolauNeural` | Masculino | Voz experiente |
| `pt-BR-ValerioNeural` | Masculino | Voz marcante |
| `pt-BR-YaraNeural` | Feminino | Voz versátil |

</details>

<details>
<summary>🇺🇸 Inglês (EUA)</summary>

| Voz | Gênero | Descrição |
|-----|--------|-----------|
| `en-US-JennyNeural` | Feminino | Voz natural multistyle |
| `en-US-GuyNeural` | Masculino | Voz profissional |
| `en-US-AriaNeural` | Feminino | Voz expressiva |
| `en-US-DavisNeural` | Masculino | Voz calma |
| `en-US-JaneNeural` | Feminino | Voz amigável |
| `en-US-JasonNeural` | Masculino | Voz confiável |
| `en-US-SaraNeural` | Feminino | Voz suave |
| `en-US-TonyNeural` | Masculino | Voz energética |
| `en-US-NancyNeural` | Feminino | Voz alegre |

</details>

<details>
<summary>🇪🇸 Espanhol (Espanha)</summary>

| Voz | Gênero | Descrição |
|-----|--------|-----------|
| `es-ES-ElviraNeural` | Feminino | Voz natural |
| `es-ES-AlvaroNeural` | Masculino | Voz profissional |
| `es-ES-JavierNeural` | Masculino | Voz clara |

</details>

<details>
<summary>🇫🇷 Francês (França)</summary>

| Voz | Gênero | Descrição |
|-----|--------|-----------|
| `fr-FR-DeniseNeural` | Feminino | Voz natural |
| `fr-FR-HenriNeural` | Masculino | Voz profissional |
| `fr-FR-AlainNeural` | Masculino | Voz calma |
| `fr-FR-JulieNeural` | Feminino | Voz suave |

</details>

### Idiomas Suportados

| Código | Idioma |
|--------|--------|
| `pt-BR` | Português (Brasil) |
| `pt-PT` | Português (Portugal) |
| `en-US` | Inglês (EUA) |
| `en-GB` | Inglês (Reino Unido) |
| `es-ES` | Espanhol (Espanha) |
| `es-MX` | Espanhol (México) |
| `fr-FR` | Francês |
| `de-DE` | Alemão |
| `it-IT` | Italiano |
| `ja-JP` | Japonês |
| `zh-CN` | Chinês (Mandarim) |
| `ko-KR` | Coreano |
| `ru-RU` | Russo |
| `ar-SA` | Árabe |

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/test_speech.py -v
pytest tests/test_language.py -v
```

## 🐳 Docker

### Build

```bash
docker build -t azure-voice-language-lab .
```

### Executar

```bash
docker run -p 8501:8501 --env-file .env azure-voice-language-lab
```

### Docker Compose

```bash
docker-compose up -d
```

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para diretrizes completas.

### Formas de contribuir

- 🐛 Reportar bugs
- 💡 Sugerir novas funcionalidades
- 📝 Melhorar documentação
- 🔧 Enviar pull requests
- ⭐ Dar uma estrela no projeto

## 📊 Roadmap

- [ ] Suporte a reconhecimento de fala em tempo real via WebSocket
- [ ] API REST com FastAPI
- [ ] Dashboard de métricas e analytics
- [ ] Suporte a Custom Voice (vozes personalizadas)
- [ ] Integração com WhatsApp/Telegram bots
- [ ] Plugin para VS Code
- [ ] SDK para JavaScript/TypeScript

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Microsoft Azure](https://azure.microsoft.com/) pelos serviços cognitivos
- [Digital Innovation One (DIO)](https://www.dio.me/) pela inspiração do projeto
- Comunidade open source pelas contribuições

## 📞 Contato

**Rone Bragaglia** - [@ronbragaglia](https://github.com/Ronbragaglia)

📧 Email: ronbragaglia@gmail.com

🔗 LinkedIn: [rone-bragaglia](https://linkedin.com/in/rone-bragaglia)

---

<p align="center">
  Feito com ❤️ por <a href="https://github.com/Ronbragaglia">Rone Bragaglia</a>
</p>

<p align="center">
  <a href="#-azure-voice-language-lab">Voltar ao topo</a>
</p>
