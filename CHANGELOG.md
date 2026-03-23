# Changelog

Todos os notáveis mudanças deste projeto serão documentados neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2024-01-15

### Adicionado
- **pyproject.toml**: Configuração moderna do projeto com suporte a setuptools
- **GitHub Actions CI/CD**: Pipeline completo com testes, linting e build
  - Testes automatizados em múltiplas versões de Python (3.8-3.12)
  - Verificação de código com Black, Flake8, isort e MyPy
  - Análise de segurança com Bandit e Safety
  - Build automático de pacotes e imagens Docker
- **Testes Unitários**: Suíte completa de testes
  - Testes para módulos de utilitários (Config, Logger)
  - Testes para módulos de Speech (SpeechRecognition, TextToSpeech)
  - Testes para módulos de Language (TextAnalysis, Translation, LanguageDetection)
  - Fixtures reutilizáveis no conftest.py
- **Exemplos de Código**: Coleção de exemplos práticos
  - `examples/basic_usage.py`: Exemplos básicos de todas as funcionalidades
  - `examples/advanced_usage.py`: Exemplos avançados e casos de uso complexos
- **Makefile**: Automação de tarefas comuns
  - Comandos para instalação, testes, linting e formatação
  - Comandos para Docker, documentação e exemplos
  - Comandos para verificação de segurança e tipos
- **Documentação Aprimorada**: README.md profissional com
  - Badges de status, versão e licença
  - Tabelas de vozes disponíveis por idioma
  - Exemplos de código interativos
  - Seções de arquitetura e roadmap
  - Links para documentação e contribuição

### Alterado
- **README.md**: Reformulado completamente com nova estrutura visual
  - Adicionadas badges de qualidade e status
  - Melhorada a organização das seções
  - Adicionados exemplos de uso em CLI, Python API e Web App
  - Incluídas tabelas de vozes disponíveis
  - Adicionada seção de roadmap do projeto

### Melhorado
- **Estrutura do Projeto**: Organização mais clara de diretórios
- **Configuração**: Suporte a extras no pyproject.toml (web, audio, visualization, dev, docs)
- **Documentação**: Adicionados docstrings detalhados em todos os módulos
- **Testes**: Cobertura de testes para todas as funcionalidades principais

### Corrigido
- Correções de formatação e estilo de código
- Melhoria na validação de configuração

## [1.0.0] - 2024-01-01

### Adicionado
- **Reconhecimento de Fala (Speech-to-Text)**: Suporte a múltiplos formatos de áudio
- **Síntese de Voz (Text-to-Speech)**: Suporte a mais de 50 vozes neurais
- **Análise de Sentimento**: Detecção de emoções em textos
- **Extração de Entidades**: Identificação de pessoas, lugares, organizações
- **Tradução**: Suporte a mais de 100 idiomas
- **Detecção de Idioma**: Identificação automática de idioma
- **Extração de Frases-Chave**: Identificação de tópicos principais
- **CLI Completa**: Interface de linha de comando para todas as funcionalidades
- **Aplicação Web Streamlit**: Interface gráfica interativa
- **Sistema de Configuração**: Gerenciamento de credenciais do Azure
- **Sistema de Logging**: Logs estruturados e configuráveis
- **Validadores**: Validação de entrada e configuração

### Funcionalidades
- Suporte a múltiplos idiomas (Português, Inglês, Espanhol, Francês, Alemão, Italiano, Japonês, Chinês)
- Ajustes de prosódia (taxa de fala e tom)
- Processamento em lote de áudios e textos
- Análise de entidades de saúde
- Detecção de entidades vinculadas
- Pontuação de confiança em todas as operações

## [0.1.0] - 2023-12-15

### Adicionado
- Estrutura inicial do projeto
- Integração básica com Azure Speech Service
- Integração básica com Azure Language Service
- Documentação básica (README.md)
- Setup.py para instalação do pacote

---

## Roadmap

### Próximas Versões

#### [1.2.0] - Planejado
- [ ] Suporte a reconhecimento de fala em tempo real via WebSocket
- [ ] API REST com FastAPI
- [ ] Dashboard de métricas e analytics
- [ ] Suporte a Custom Voice (vozes personalizadas)

#### [1.3.0] - Planejado
- [ ] Integração com WhatsApp/Telegram bots
- [ ] Plugin para VS Code
- [ ] SDK para JavaScript/TypeScript
- [ ] Melhorias na UI da aplicação web

#### [2.0.0] - Planejado
- [ ] Arquitetura baseada em plugins
- [ ] Suporte a múltiplos provedores (AWS, Google Cloud)
- [ ] Sistema de cache para melhorar performance
- [ ] Suporte a processamento distribuído

---

## Tipos de Mudanças

- `Adicionado` para novas funcionalidades
- `Alterado` para mudanças em funcionalidades existentes
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Melhorado` para melhorias em funcionalidades existentes
- `Segurança` para correções de segurança

---

## Links

- [Repositório](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab)
- [Issues](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab/issues)
- [Pull Requests](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab/pulls)
- [Documentação](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab#readme)
