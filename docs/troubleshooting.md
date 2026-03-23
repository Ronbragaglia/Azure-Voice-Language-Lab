# Troubleshooting

Este guia ajuda a resolver problemas comuns ao usar o Azure Voice Language Lab.

## 📋 Índice

- [Problemas de Instalação](#problemas-de-instalação)
- [Problemas de Configuração](#problemas-de-configuração)
- [Problemas de Execução](#problemas-de-execução)
- [Problemas de Performance](#problemas-de-performance)
- [Problemas de Azure](#problemas-de-azure)

## 🔧 Problemas de Instalação

### Erro: "ModuleNotFoundError: No module named 'azure'"

**Descrição:** O módulo do Azure não foi encontrado.

**Causa:** As dependências do Azure não foram instaladas.

**Solução:**

```bash
# Reinstalar o pacote com todas as dependências
pip install -e ".[all]"

# Ou instalar manualmente
pip install azure-cognitiveservices-speech azure-ai-textanalytics azure-ai-translation-text azure-ai-language
```

### Erro: "Permission denied: '.env'"

**Descrição:** Permissão negada ao acessar o arquivo `.env`.

**Causa:** O arquivo `.env` não tem permissões de leitura.

**Solução:**

**Linux/macOS:**
```bash
chmod 644 .env
```

**Windows:**
```bash
# Clique com o botão direito no arquivo .env
# Propriedades > Segurança > Editar permissões
# Marque "Leitura" para seu usuário
```

### Erro: "pip: command not found"

**Descrição:** O comando `pip` não foi encontrado.

**Causa:** O Python não está instalado ou não está no PATH.

**Solução:**

```bash
# Verificar se Python está instalado
python --version

# Ou python3
python3 --version

# Se não estiver instalado, instale do site oficial
# https://www.python.org/downloads/
```

## ⚙️ Problemas de Configuração

### Erro: "Configuração inválida"

**Descrição:** A configuração do Azure não é válida.

**Causa:** Variáveis de ambiente não configuradas ou incorretas.

**Solução:**

1. Verifique se o arquivo `.env` existe na raiz do projeto
2. Verifique se todas as variáveis estão presentes:
   ```env
   AZURE_SPEECH_KEY=...
   AZURE_SPEECH_REGION=...
   AZURE_LANGUAGE_KEY=...
   AZURE_LANGUAGE_ENDPOINT=...
   AZURE_TRANSLATOR_KEY=...
   AZURE_TRANSLATOR_REGION=...
   ```
3. Valide a configuração:
   ```python
   from src.utils import Config
   config = Config()
   print(config.validate_config())
   ```

### Erro: "Chave inválida"

**Descrição:** A chave do Azure não é válida ou expirou.

**Causa:** Chave incorreta ou expirada.

**Solução:**

1. Acesse o [Azure Portal](https://portal.azure.com/)
2. Navegue até o recurso correspondente
3. Gere uma nova chave em "Chaves e ponto de extremidade"
4. Atualize o arquivo `.env` com a nova chave

### Erro: "Região inválida"

**Descrição:** A região do Azure não é válida.

**Causa:** Código de região incorreto.

**Solução:**

Use o código de região correto:

| Nome da Região | Código |
|----------------|--------|
| Brazil South | `brazilsouth` |
| East US | `eastus` |
| West Europe | `westeurope` |
| Southeast Asia | `southeastasia` |

**Não use:** `Brazil South` (com espaço), `Brazil-South`, etc.

### Erro: "Endpoint inválido"

**Descrição:** O endpoint do Azure não é válido.

**Causa:** URL do endpoint incorreta ou incompleta.

**Solução:**

O endpoint deve seguir este formato:
```
https://seu-recurso.cognitiveservices.azure.com/
```

**Verifique:**
- Começa com `https://`
- Termina com `/`
- Não contém espaços

## 🚀 Problemas de Execução

### Erro: "FileNotFoundError: audio.wav"

**Descrição:** Arquivo de áudio não encontrado.

**Causa:** Caminho do arquivo incorreto ou arquivo não existe.

**Solução:**

1. Verifique se o arquivo existe:
   ```bash
   ls -la audio.wav
   ```
2. Use o caminho absoluto:
   ```python
   from pathlib import Path
   audio_file = Path("/caminho/completo/audio.wav")
   ```
3. Verifique a extensão do arquivo (`.wav`, `.mp3`, etc.)

### Erro: "ConnectionError: Failed to establish connection"

**Descrição:** Falha ao conectar ao Azure.

**Causa:** Problema de rede ou firewall bloqueando a conexão.

**Solução:**

1. Verifique sua conexão com a internet
2. Verifique se o firewall não está bloqueando:
   - Porta 443 (HTTPS)
   - Domínios do Azure (`*.cognitiveservices.azure.com`, `*.api.cognitive.microsoft.com`)
3. Tente usar um proxy:
   ```python
   import os
   os.environ['HTTP_PROXY'] = 'http://proxy:porta'
   os.environ['HTTPS_PROXY'] = 'http://proxy:porta'
   ```

### Erro: "TimeoutError: Request timed out"

**Descrição:** A requisição ao Azure expirou.

**Causa:** Lentidão da rede ou do serviço Azure.

**Solução:**

1. Aumente o timeout:
   ```python
   # Para reconhecimento de fala
   recognizer = SpeechRecognition(key, region, language, timeout=30)
   ```
2. Tente novamente após alguns instantes
3. Verifique o status do Azure: [https://status.azure.com/]

## 📊 Problemas de Performance

### Problema: Reconhecimento de fala muito lento

**Descrição:** O reconhecimento de fala está demorando muito.

**Causas Possíveis:**

1. **Arquivo de áudio muito grande**
2. **Conexão de internet lenta**
3. **Região do Azure distante**

**Soluções:**

1. Divida arquivos grandes em partes menores
2. Use uma região mais próxima
3. Use processamento em lote para múltiplos arquivos

### Problema: Síntese de voz demorando

**Descrição:** A síntese de voz está demorando muito.

**Causas Possíveis:**

1. **Texto muito longo**
2. **Conexão de internet lenta**
3. **Região do Azure distante**

**Soluções:**

1. Divida textos longos em partes menores
2. Use uma região mais próxima
3. Cache os resultados de síntese frequentes

### Problema: Alto uso de memória

**Descrição:** O aplicativo está consumindo muita memória.

**Causas Possíveis:**

1. **Múltiplas instâncias de clientes**
2. **Arquivos de áudio grandes**
3. **Textos muito longos**

**Soluções:**

1. Reutilize instâncias de clientes
2. Processe arquivos/textos em lotes menores
3. Use garbage collection:
   ```python
   import gc
   gc.collect()
   ```

## ☁️ Problemas de Azure

### Erro: "QuotaExceeded: The quota has been exceeded"

**Descrição:** A cota do Azure foi excedida.

**Causa:** Limite de uso do plano gratuito atingido.

**Solução:**

1. Verifique seu uso no [Azure Portal](https://portal.azure.com/)
2. Aguarde até o próximo ciclo de faturamento
3. Faça upgrade para um plano pago

### Erro: "Unauthorized: Invalid API key"

**Descrição:** Chave de API inválida ou expirou.

**Causa:** Chave incorreta ou expirou.

**Solução:**

1. Gere uma nova chave no Azure Portal
2. Atualize o arquivo `.env`
3. Reinicie o aplicativo

### Erro: "ResourceNotFound: The specified resource does not exist"

**Descrição:** O recurso do Azure não existe.

**Causa:** Endpoint incorreto ou recurso foi deletado.

**Solução:**

1. Verifique o endpoint no Azure Portal
2. Atualize o arquivo `.env`
3. Verifique se o recurso ainda existe

## 🐛 Outros Problemas

### Problema: Resultados inconsistentes

**Descrição:** Os resultados variam entre execuções.

**Causa:** Aleatoriedade natural dos serviços de IA.

**Solução:**

1. Execute múltiplas vezes e use a média
2. Aumente a confiança mínima aceita
3. Use pontuação de confiança para filtrar resultados

### Problema: Caracteres especiais não reconhecidos

**Descrição:** Caracteres especiais não são reconhecidos corretamente.

**Causa:** Limitações do modelo de IA.

**Solução:**

1. Use SSML para melhorar a pronúncia:
   ```python
   ssml = f"""
   <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'>
       <voice name='pt-BR-FranciscaNeural'>
           <phoneme alphabet='ipa'>seu texto</phoneme>
       </voice>
   </speak>
   """
   ```
2. Use dicionário de pronúncia personalizado

## 📞 Obtendo Ajuda

### Relatar Bugs

Se encontrar um bug que não está listado aqui:

1. Abra uma issue no [GitHub](https://github.com/Ronbragaglia/Azure-Voice-Language-Lab/issues)
2. Forneça informações detalhadas:
   - Descrição do problema
   - Passos para reproduzir
   - Comportamento esperado
   - Comportamento atual
   - Ambiente (SO, versão do Python, etc.)
   - Logs ou mensagens de erro

### Pedir Ajuda

Se precisar de ajuda:

1. Consulte a [Documentação](index.md)
2. Verifique os [Exemplos](../examples/)
3. Abra uma issue no GitHub com a tag "question"
4. Entre em contato: [ronbragaglia@gmail.com](mailto:ronbragaglia@gmail.com)

### Links Úteis

- [Documentação do Azure Speech](https://docs.microsoft.com/azure/cognitive-services/speech-service/)
- [Documentação do Azure Language](https://docs.microsoft.com/azure/cognitive-services/language-service/)
- [Documentação do Azure Translator](https://docs.microsoft.com/azure/cognitive-services/translator/)
- [Status do Azure](https://status.azure.com/)
- [Preços do Azure](https://azure.microsoft.com/pricing/)

---

<p align="center">
  <a href="index.md">← Voltar para Documentação</a>
</p>
