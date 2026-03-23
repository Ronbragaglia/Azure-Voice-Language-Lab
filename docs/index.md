# Azure Voice Language Lab - Documentação

Bem-vindo à documentação oficial do Azure Voice Language Lab!

## 📚️ Índice

- [Guia de Instalação](installation.md) - Como instalar e configurar o projeto
- [Guia de Uso](usage.md) - Como usar as funcionalidades principais
- [API Reference](api.md) - Referência completa da API
- [Exemplos](examples.md) - Exemplos de código e casos de uso
- [Troubleshooting](troubleshooting.md) - Solução de problemas comuns
- [Contribuindo](contributing.md) - Como contribuir com o projeto

## 🚀 Começando Rápido

### Instalação

```bash
pip install azure-voice-language-lab
```

### Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
AZURE_SPEECH_KEY=sua_chave_speech
AZURE_SPEECH_REGION=brazilsouth
AZURE_LANGUAGE_KEY=sua_chave_language
AZURE_LANGUAGE_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/
AZURE_TRANSLATOR_KEY=sua_chave_translator
AZURE_TRANSLATOR_REGION=brazilsouth
```

### Uso Básico

```python
from src.speech import SpeechRecognition, TextToSpeech
from src.language import TextAnalysis, Translation, LanguageDetection
from src.utils import Config

# Carregar configuração
config = Config()

# Reconhecimento de fala
speech_key, speech_region = config.get_speech_config()
recognizer = SpeechRecognition(speech_key, speech_region, "pt-BR")
result = recognizer.recognize_from_file("audio.wav")
print(result['text'])

# Síntese de voz
synthesizer = TextToSpeech(speech_key, speech_region, "pt-BR-FranciscaNeural")
result = synthesizer.synthesize_to_file("Olá, mundo!", "output.wav")

# Análise de sentimento
language_key, language_endpoint = config.get_language_config()
analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")
result = analyzer.analyze_sentiment("Estou muito feliz!", "pt-BR")
print(result['sentiment'])
```

## 🎯 Funcionalidades

### Speech (Fala)

- **Speech-to-Text**: Converta áudio em texto com alta precisão
- **Text-to-Speech**: Sintetize voz natural a partir de texto
- **Suporte a múltiplos idiomas**: Português, Inglês, Espanhol, Francês, Alemão, Italiano, Japonês, Chinês
- **Vozes neurais**: Mais de 50 vozes neurais de alta qualidade
- **Ajustes de prosódia**: Controle taxa de fala e tom

### Language (Linguagem)

- **Análise de Sentimento**: Detecte emoções em textos (positivo, neutro, negativo)
- **Extração de Entidades**: Identifique pessoas, lugares, organizações e mais
- **Frases-Chave**: Extraia os principais tópicos de um texto
- **Detecção de Idioma**: Identifique automaticamente o idioma do texto
- **Entidades de Saúde**: Análise especializada para textos médicos

### Translation (Tradução)

- **Tradução em tempo real**: Traduza textos entre mais de 100 idiomas
- **Detecção automática**: Sistema detecta idioma de origem automaticamente
- **Pontuação de confiança**: Avalie a qualidade da tradução

## 🖥️ Interfaces

### CLI (Linha de Comando)

Interface completa de linha de comando para todas as funcionalidades:

```bash
# Reconhecimento de fala
azure-speech-lab recognize --audio audio.wav --language pt-BR

# Síntese de voz
azure-speech-lab synthesize --text "Olá, mundo!" --output voz.wav

# Análise de sentimento
azure-speech-lab sentiment --text "Estou muito feliz hoje!" --language pt-BR

# Tradução
azure-speech-lab translate --text "Hello world" --to pt --from en

# Detecção de idioma
azure-speech-lab detect --text "Bonjour le monde"
```

### Web App (Streamlit)

Interface gráfica interativa e amigável:

```bash
streamlit run web/app.py
```

Acesse `http://localhost:8501` para usar a interface gráfica.

## 📊 Arquitetura

```
Azure-Voice-Language-Lab/
├── src/                    # Código fonte principal
│   ├── speech/            # Módulos de fala (STT/TTS)
│   │   ├── recognition.py    # Reconhecimento de fala
│   │   └── synthesis.py      # Síntese de voz
│   ├── language/          # Módulos de linguagem
│   │   ├── analysis.py       # Análise de texto
│   │   ├── detection.py      # Detecção de idioma
│   │   └── translation.py    # Tradução
│   └── utils/             # Utilitários
│       ├── config.py         # Gerenciamento de configuração
│       ├── logger.py         # Sistema de logging
│       └── validators.py     # Validadores
├── web/                   # Aplicação web Streamlit
│   └── app.py           # Interface gráfica
├── examples/              # Exemplos de uso
├── tests/                 # Testes unitários
└── docs/                  # Documentação
```

## 🔧 Desenvolvimento

### Configuração do Ambiente

```bash
# Clonar repositório
git clone https://github.com/Ronbragaglia/Azure-Voice-Language-Lab.git
cd Azure-Voice-Language-Lab

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Instalar hooks do pre-commit
pre-commit install
```

### Executar Testes

```bash
# Executar todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/test_speech.py -v
```

### Formatação de Código

```bash
# Formatar com Black
black src/ tests/ examples/

# Ordenar imports com isort
isort src/ tests/ examples/
```

### Linting

```bash
# Verificar código com Flake8
flake8 src/ tests/

# Verificar tipos com MyPy
mypy src/ --ignore-missing-imports

# Verificar segurança com Bandit
bandit -r src/
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

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](../LICENSE) para detalhes.

## 🙏�️ Agradecimentos

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
