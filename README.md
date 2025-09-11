# Laboratório Azure Speech & Language Studio - DIO

## Introdução
Este projeto tem como objetivo explorar e aplicar conceitos do Azure Speech Studio e Language Studio. Durante o laboratório, foram testadas funcionalidades de reconhecimento de fala, síntese de voz e análise de texto, com foco em Processamento de Linguagem Natural (NLP) e inteligência artificial aplicada à voz.

## Objetivos de Aprendizagem
- Aplicar os conceitos aprendidos em um ambiente prático.
- Documentar processos técnicos de forma clara e estruturada.
- Utilizar o GitHub como ferramenta para compartilhamento de documentação técnica.

## Ferramentas Utilizadas
- [Azure Speech Studio](https://learn.microsoft.com/azure/cognitive-services/speech-service/)
- [Azure Language Studio](https://learn.microsoft.com/azure/cognitive-services/language-service/)
- Python 3
- Google Colab
- Bibliotecas Python:
  - `azure-cognitiveservices-speech`
  - `requests`
  - `json`

## Passo a Passo da Execução

### 1. Configuração do Azure
1. Criar conta no [Azure Portal](https://portal.azure.com/).
2. Criar recurso **Speech** e **Language**.
3. Anotar `KEY` e `REGION` para uso no Python.

### 2. Reconhecimento de Fala (Speech-to-Text)
- Testes realizados convertendo áudio em texto.
- Exemplos de comandos e outputs foram salvos.

### 3. Síntese de Voz (Text-to-Speech)
- Testes convertendo texto em fala.
- Resultados em arquivos de áudio `.wav`.

### 4. Análise de Texto (Language Studio)
- Testes de detecção de sentimento, entidades e resumo.
- Exemplos com textos em português e inglês.

## Código Python de Exemplo
- Executável no Google Colab.
- Mostra integração com Azure Speech e Language Studio.
- Exemplo de reconhecimento de fala e análise de texto.

## Resultados Obtidos
- Reconhecimento de fala com precisão de até 95%.
- Análise de sentimento e entidades funcionando conforme esperado.
- Geração de áudio a partir de texto com vozes realistas.

## Aprendizados e Desafios
- Configuração inicial do Azure é essencial para evitar erros de autenticação.
- Ajustes finos em reconhecimento de fala melhoram resultados.
- Documentação e organização no GitHub ajudam a manter o projeto escalável.

## Referências
- [Documentação Speech Studio](https://learn.microsoft.com/azure/cognitive-services/speech-service/)
- [Documentação Language Studio](https://learn.microsoft.com/azure/cognitive-services/language-service/)
- [GitHub Markdown Guide](https://guides.github.com/features/mastering-markdown/)
