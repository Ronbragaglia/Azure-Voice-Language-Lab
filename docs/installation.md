# Guia de Instalação

Este guia detalha como instalar e configurar o Azure Voice Language Lab.

## 📋 Pré-requisitos

### Requisitos de Sistema

- **Sistema Operacional**: Windows, macOS ou Linux
- **Python**: 3.8 ou superior
- **Memória RAM**: Mínimo 2GB (recomendado 4GB)
- **Espaço em Disco**: Mínimo 500MB

### Requisitos do Azure

Para usar o Azure Voice Language Lab, você precisa de uma conta do Azure com os seguintes recursos:

1. **Azure Speech Service**
   - Para reconhecimento de fala e síntese de voz

2. **Azure Language Service**
   - Para análise de texto, extração de entidades e detecção de idioma

3. **Azure Translator Service** (opcional)
   - Para tradução de texto

## 🔧 Instalação

### Método 1: Via pip (Recomendado)

#### Instalação Básica

```bash
pip install azure-voice-language-lab
```

#### Instalação com Extras

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

### Método 2: Via Git

#### Clonar o Repositório

```bash
git clone https://github.com/Ronbragaglia/Azure-Voice-Language-Lab.git
cd Azure-Voice-Language-Lab
```

#### Criar Ambiente Virtual (Recomendado)

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### Instalar Dependências

```bash
# Instalação básica
pip install -e .

# Instalação com extras de desenvolvimento
pip install -e ".[dev]"

# Instalação completa
pip install -e ".[all]"
```

### Método 3: Via Docker

#### Build da Imagem

```bash
docker build -t azure-voice-language-lab .
```

#### Executar com Docker Compose

```bash
docker-compose up -d
```

#### Executar Manualmente

```bash
docker run -p 8501:8501 --env-file .env azure-voice-language-lab
```

## ⚙️ Configuração

### 1. Criar Recursos no Azure

#### Azure Speech Service

1. Acesse o [Azure Portal](https://portal.azure.com/)
2. Clique em "Criar um recurso"
3. Pesquise por "Speech"
4. Selecione "Speech Services"
5. Clique em "Criar"
6. Preencha os campos:
   - **Assinatura**: Sua assinatura do Azure
   - **Grupo de recursos**: Criar ou selecionar existente
   - **Região**: Escolha a região mais próxima (ex: Brazil South)
   - **Nome**: Um nome único para o recurso
   - **Camada de preços**: Gratuito (F0) ou Standard (S0)
7. Clique em "Revisar + criar"
8. Aguarde a implantação ser concluída
9. Anote a **Chave** e a **Região**

#### Azure Language Service

1. No Azure Portal, clique em "Criar um recurso"
2. Pesquise por "Language Service"
3. Selecione "Language Service"
4. Clique em "Criar"
5. Preencha os campos:
   - **Assinatura**: Sua assinatura do Azure
   - **Grupo de recursos**: Criar ou selecionar existente
   - **Região**: Escolha a região mais próxima
   - **Nome**: Um nome único para o recurso
   - **Camada de preços**: Gratuito (F0) ou Standard (S0)
6. Clique em "Revisar + criar"
7. Aguarde a implantação ser concluída
8. Anote a **Chave** e o **Endpoint**

#### Azure Translator Service (Opcional)

1. No Azure Portal, clique em "Criar um recurso"
2. Pesquise por "Translator"
3. Selecione "Translator"
4. Clique em "Criar"
5. Preencha os campos:
   - **Assinatura**: Sua assinatura do Azure
   - **Grupo de recursos**: Criar ou selecionar existente
   - **Região**: Escolha a região mais próxima
   - **Nome**: Um nome único para o recurso
   - **Camada de preços**: Gratuito (F0) ou Standard (S0)
6. Clique em "Revisar + criar"
7. Aguarde a implantação ser concluída
8. Anote a **Chave** e a **Região**

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Azure Speech Service
AZURE_SPEECH_KEY=sua_chave_speech_aqui
AZURE_SPEECH_REGION=brazilsouth

# Azure Language Service
AZURE_LANGUAGE_KEY=sua_chave_language_aqui
AZURE_LANGUAGE_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/

# Azure Translator (opcional)
AZURE_TRANSLATOR_KEY=sua_chave_translator_aqui
AZURE_TRANSLATOR_REGION=brazilsouth
```

### 3. Validar Configuração

Você pode validar se a configuração está correta usando:

```bash
# Via CLI
azure-speech-lab --help

# Via Python
python -c "from src.utils import Config; config = Config(); print(config.validate_config())"
```

## ✅ Verificação da Instalação

### Testar Instalação

```bash
# Verificar se o pacote foi instalado
pip show azure-voice-language-lab

# Verificar a versão
azure-speech-lab --version
```

### Executar Testes

```bash
# Executar todos os testes
pytest

# Executar com coverage
pytest --cov=src --cov-report=html
```

### Testar CLI

```bash
# Listar comandos disponíveis
azure-speech-lab --help

# Testar reconhecimento de fala
azure-speech-lab recognize --help

# Testar síntese de voz
azure-speech-lab synthesize --help
```

### Testar Web App

```bash
# Iniciar aplicação web
streamlit run web/app.py

# Acesse http://localhost:8501
```

## 🐛 Solução de Problemas

### Erro: "Configuração inválida"

**Solução:** Verifique se todas as variáveis de ambiente estão configuradas corretamente no arquivo `.env`.

### Erro: "Chave inválida"

**Solução:** Verifique se as chaves do Azure estão corretas e não expiraram.

### Erro: "Região inválida"

**Solução:** Verifique se a região está correta. Use o código de região (ex: `brazilsouth`, não `Brazil South`).

### Erro: "Endpoint inválido"

**Solução:** Verifique se o endpoint está correto. Deve incluir `https://` e terminar com `/`.

### Erro: "Módulo não encontrado"

**Solução:** Certifique-se de instalar todas as dependências necessárias:

```bash
pip install -e ".[all]"
```

### Erro: "Permissão negada"

**Solução:** Verifique se o arquivo `.env` tem permissões de leitura:

**Linux/macOS:**
```bash
chmod 644 .env
```

**Windows:**
```bash
# Verifique as propriedades do arquivo
```

## 📚️ Próximos Passos

Após a instalação bem-sucedida:

1. **Explore os Exemplos**: Execute os exemplos em `examples/`
2. **Leia a Documentação**: Consulte `docs/` para mais informações
3. **Use a Web App**: Inicie a aplicação web para explorar as funcionalidades
4. **Contribua**: Se encontrar bugs ou tiver sugestões, abra uma issue no GitHub

## 🆘 Suporte

Se encontrar problemas durante a instalação:

1. Consulte o [Troubleshooting](troubleshooting.md)
2. Abra uma [issue no GitHub](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab/issues)
3. Entre em contato: [ronbragaglia@gmail.com](mailto:ronbragaglia@gmail.com)

---

<p align="center">
  <a href="index.md">← Voltar para Documentação</a>
</p>
