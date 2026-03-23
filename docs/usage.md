# Guia de Uso

Este guia detalha como usar as funcionalidades principais do Azure Voice Language Lab.

## 📚️ Conteúdo

- [Reconhecimento de Fala](#reconhecimento-de-fala)
- [Síntese de Voz](#síntese-de-voz)
- [Análise de Sentimento](#análise-de-sentimento)
- [Extração de Entidades](#extração-de-entidades)
- [Tradução](#tradução)
- [Detecção de Idioma](#detecção-de-idioma)
- [Extração de Frases-Chave](#extração-de-frases-chave)

## 🎤 Reconhecimento de Fala

### Visão Geral

O reconhecimento de fala converte áudio em texto usando o Azure Speech Service.

### Uso via CLI

```bash
# Reconhecer fala de um arquivo
azure-speech-lab recognize --audio audio.wav --language pt-BR

# Reconhecer fala com idioma diferente
azure-speech-lab recognize --audio audio.wav --language en-US
```

### Uso via Python API

```python
from src.speech import SpeechRecognition
from src.utils import Config

# Carregar configuração
config = Config()
speech_key, speech_region = config.get_speech_config()

# Inicializar reconhecimento
recognizer = SpeechRecognition(speech_key, speech_region, "pt-BR")

# Reconhecer fala de arquivo
result = recognizer.recognize_from_file("audio.wav")

if result['status'] == 'success':
    print(f"Texto: {result['text']}")
    print(f"Idioma: {result['language']}")
else:
    print(f"Erro: {result.get('error')}")
```

### Formatos de Áudio Suportados

- WAV (PCM, 16kHz, 16-bit, mono)
- MP3
- OGG
- FLAC

### Idiomas Suportados

- `pt-BR` - Português (Brasil)
- `pt-PT` - Português (Portugal)
- `en-US` - Inglês (EUA)
- `en-GB` - Inglês (Reino Unido)
- `es-ES` - Espanhol
- `fr-FR` - Francês
- `de-DE` - Alemão
- `it-IT` - Italiano
- `ja-JP` - Japonês
- `zh-CN` - Chinês (Mandarim)

## 🔊 Síntese de Voz

### Visão Geral

A síntese de voz converte texto em áudio usando o Azure Speech Service.

### Uso via CLI

```bash
# Sintetizar voz com configurações padrão
azure-speech-lab synthesize --text "Olá, mundo!" --output output.wav

# Sintetizar com voz específica
azure-speech-lab synthesize --text "Olá, mundo!" --output output.wav --voice pt-BR-FranciscaNeural

# Ajustar taxa e tom
azure-speech-lab synthesize --text "Olá, mundo!" --output output.wav --rate "+10%" --pitch "-5%"
```

### Uso via Python API

```python
from src.speech import TextToSpeech
from src.utils import Config

# Carregar configuração
config = Config()
speech_key, speech_region = config.get_speech_config()

# Inicializar síntese
synthesizer = TextToSpeech(speech_key, speech_region, "pt-BR-FranciscaNeural")

# Sintetizar texto
result = synthesizer.synthesize_to_file(
    "Olá, este é um teste de síntese de voz.",
    "output.wav",
    rate="+10%",
    pitch="-5%"
)

if result['status'] == 'success':
    print(f"Áudio gerado: {result['output_file']}")
    print(f"Voz: {result['voice']}")
else:
    print(f"Erro: {result.get('error')}")
```

### Vozes Disponíveis

#### Português (Brasil)

- `pt-BR-FranciscaNeural` (Feminino)
- `pt-BR-AntonioNeural` (Masculino)
- `pt-BR-BrendaNeural` (Feminino)
- `pt-BR-DonatoNeural` (Masculino)
- `pt-BR-ElzaNeural` (Feminino)
- `pt-BR-FabioNeural` (Masculino)

#### Inglês (EUA)

- `en-US-JennyNeural` (Feminino)
- `en-US-GuyNeural` (Masculino)
- `en-US-AriaNeural` (Feminino)
- `en-US-DavisNeural` (Masculino)

### Ajustes de Prosódia

- **Rate (Taxa de Fala)**: Controla a velocidade da fala
  - Valores: `-50%` a `+50%`
  - Padrão: `0%`

- **Pitch (Tom)**: Controla a altura da voz
  - Valores: `-50%` a `+50%`
  - Padrão: `0%`

## 😊 Análise de Sentimento

### Visão Geral

A análise de sentimento detecta emoções em textos (positivo, neutro, negativo).

### Uso via CLI

```bash
# Analisar sentimento
azure-speech-lab sentiment --text "Estou muito feliz hoje!" --language pt-BR

# Analisar sentimento em inglês
azure-speech-lab sentiment --text "I'm very happy today!" --language en-US
```

### Uso via Python API

```python
from src.language import TextAnalysis
from src.utils import Config

# Carregar configuração
config = Config()
language_key, language_endpoint = config.get_language_config()

# Inicializar análise
analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

# Analisar sentimento
result = analyzer.analyze_sentiment("Estou muito feliz com este projeto!", "pt-BR")

if result['status'] == 'success':
    print(f"Sentimento: {result['sentiment']}")
    print(f"Confiança:")
    print(f"  Positivo: {result['confidence_scores']['positive']:.2%}")
    print(f"  Neutro: {result['confidence_scores']['neutral']:.2%}")
    print(f"  Negativo: {result['confidence_scores']['negative']:.2%}")
else:
    print(f"Erro: {result.get('error')}")
```

### Interpretação dos Resultados

- **Positive**: Texto expressa emoções positivas (alegria, satisfação, etc.)
- **Neutral**: Texto é neutro ou equilibrado
- **Negative**: Texto expressa emoções negativas (tristeza, raiva, etc.)

### Pontuação de Confiança

Cada sentimento tem uma pontuação de confiança (0 a 1):

- **Alta confiança (> 0.8)**: Resultado muito confiável
- **Média confiança (0.5 - 0.8)**: Resulto razoavelmente confiável
- **Baixa confiança (< 0.5)**: Resulto pode não ser confiável

## 🔍 Extração de Entidades

### Visão Geral

A extração de entidades identifica pessoas, lugares, organizações e outras entidades nomeadas.

### Uso via CLI

```bash
# Extrair entidades
azure-speech-lab entities --text "A Microsoft foi fundada por Bill Gates em 1975" --language pt-BR
```

### Uso via Python API

```python
from src.language import TextAnalysis
from src.utils import Config

# Carregar configuração
config = Config()
language_key, language_endpoint = config.get_language_config()

# Inicializar análise
analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

# Extrair entidades
result = analyzer.extract_entities(
    "A Microsoft foi fundada por Bill Gates e Paul Allen em 1975 em Albuquerque.",
    "pt-BR"
)

if result['status'] == 'success':
    for entity in result['entities']:
        print(f"Texto: {entity['text']}")
        print(f"Categoria: {entity['category']}")
        print(f"Subcategoria: {entity.get('subcategory', 'N/A')}")
        print(f"Confiança: {entity['confidence_score']:.2%}")
        print()
else:
    print(f"Erro: {result.get('error')}")
```

### Categorias de Entidades

- **Person**: Pessoas (reais ou fictícias)
- **Location**: Lugares, cidades, países
- **Organization**: Empresas, organizações
- **Event**: Eventos históricos ou atuais
- **DateTime**: Datas e horas
- **Quantity**: Números e quantidades
- **Product**: Produtos e serviços

## 🌐 Tradução

### Visão Geral

A tradução converte texto entre mais de 100 idiomas usando o Azure Translator Service.

### Uso via CLI

```bash
# Traduzir texto
azure-speech-lab translate --text "Hello, world!" --to pt --from en

# Traduzir com detecção automática de idioma
azure-speech-lab translate --text "Hello, world!" --to pt
```

### Uso via Python API

```python
from src.language import Translation
from src.utils import Config

# Carregar configuração
config = Config()
translator_key, translator_region = config.get_translator_config()

# Inicializar tradutor
translator = Translation(translator_key, translator_region)

# Traduzir texto
result = translator.translate("Hello, world!", "pt", "en")

if result['status'] == 'success':
    print(f"Original: {result['text']}")
    print(f"Tradução: {result['translation']}")
    print(f"De: {result['from_language']} -> Para: {result['to_language']}")
    print(f"Confiança: {result['confidence']:.2%}")
else:
    print(f"Erro: {result.get('error')}")
```

### Idiomas Suportados

Mais de 100 idiomas são suportados, incluindo:

- `pt` - Português
- `en` - Inglês
- `es` - Espanhol
- `fr` - Francês
- `de` - Alemão
- `it` - Italiano
- `ja` - Japonês
- `zh` - Chinês
- `ko` - Coreano
- `ru` - Russo
- `ar` - Árabe

## 🔎 Detecção de Idioma

### Visão Geral

A detecção de idioma identifica automaticamente o idioma de um texto.

### Uso via CLI

```bash
# Detectar idioma
azure-speech-lab detect --text "Bonjour, comment allez-vous?"
```

### Uso via Python API

```python
from src.language import LanguageDetection
from src.utils import Config

# Carregar configuração
config = Config()
language_key, language_endpoint = config.get_language_config()

# Inicializar detector
detector = LanguageDetection(language_key, language_endpoint)

# Detectar idioma
result = detector.detect_language("Bonjour, comment allez-vous?")

if result['status'] == 'success':
    print(f"Idioma: {result['language']}")
    print(f"Nome: {result['language_name']}")
    print(f"Confiança: {result['confidence_score']:.2%}")
else:
    print(f"Erro: {result.get('error')}")
```

### Interpretação dos Resultados

- **Confiança alta (> 0.9)**: Idioma detectado com alta certeza
- **Confiança média (0.7 - 0.9)**: Idioma provavelmente correto
- **Confiança baixa (< 0.7)**: Idioma pode não ser correto

## 📝 Extração de Frases-Chave

### Visão Geral

A extração de frases-chave identifica os principais tópicos de um texto.

### Uso via CLI

```bash
# Extrair frases-chave
azure-speech-lab phrases --text "A inteligência artificial está transformando a tecnologia" --language pt-BR
```

### Uso via Python API

```python
from src.language import TextAnalysis
from src.utils import Config

# Carregar configuração
config = Config()
language_key, language_endpoint = config.get_language_config()

# Inicializar análise
analyzer = TextAnalysis(language_key, language_endpoint, "pt-BR")

# Extrair frases-chave
result = analyzer.extract_key_phrases(
    "A inteligência artificial está transformando a maneira como trabalhamos e vivemos.",
    "pt-BR"
)

if result['status'] == 'success':
    print(f"Frases-chave encontradas: {len(result['key_phrases'])}")
    for i, phrase in enumerate(result['key_phrases'], 1):
        print(f"{i}. {phrase}")
else:
    print(f"Erro: {result.get('error')}")
```

## 💡 Dicas de Uso

### Para Melhores Resultados

1. **Use áudio de alta qualidade** para reconhecimento de fala
2. **Forneça contexto suficiente** ao analisar sentimento
3. **Use textos claros e bem estruturados** para extração de entidades
4. **Especifique o idioma correto** quando conhecido
5. **Teste diferentes vozes** para encontrar a mais adequada

### Performance

1. **Reutilize instâncias** de clientes quando possível
2. **Use cache** para operações repetidas
3. **Processamento em lote** para múltiplos arquivos/textos
4. **Evite criar novas instâncias** desnecessariamente

## 🆘 Suporte

Se encontrar problemas ao usar o Azure Voice Language Lab:

1. Consulte o [Troubleshooting](troubleshooting.md)
2. Abra uma [issue no GitHub](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab/issues)
3. Entre em contato: [ronbragaglia@gmail.com](mailto:ronbragaglia@gmail.com)

---

<p align="center">
  <a href="index.md">← Voltar para Documentação</a>
</p>
