# Contribuindo com o Azure Voice Language Lab

Obrigado pelo seu interesse em contribuir com o Azure Voice Language Lab! Este documento fornece diretrizes e instruções para contribuir com o projeto.

## Como Contribuir

### Reportando Bugs

Antes de criar um bug report, por favor:
1. Verifique se o bug já foi reportado
2. Certifique-se de que o bug é reprodutível
3. Forneça informações detalhadas sobre o bug

Ao reportar um bug, inclua:
- Título descritivo
- Descrição detalhada do problema
- Passos para reproduzir
- Comportamento esperado
- Comportamento atual
- Ambiente (sistema operacional, versão do Python, etc.)
- Logs ou capturas de tela relevantes

### Sugerindo Melhorias

Sugestões de melhorias são sempre bem-vindas! Ao sugerir uma melhoria:
1. Verifique se a sugestão já foi feita
2. Descreva claramente a melhoria proposta
3. Explique por que essa melhoria seria útil
4. Forneça exemplos de uso, se aplicável

### Pull Requests

1. **Fork o repositório**
2. **Crie uma branch** para sua feature ou bugfix:
   ```bash
   git checkout -b feature/minha-nova-feature
   ```
3. **Faça suas alterações**
4. **Teste suas alterações**:
   ```bash
   pytest
   ```
5. **Commit suas alterações**:
   ```bash
   git commit -m "Add: descrição concisa das mudanças"
   ```
6. **Push para a branch**:
   ```bash
   git push origin feature/minha-nova-feature
   ```
7. **Crie um Pull Request**

## Padrões de Commit

Usamos o seguinte padrão para mensagens de commit:
- `Add:` Adiciona nova funcionalidade
- `Fix:` Corrige um bug
- `Update:` Atualiza funcionalidade existente
- `Refactor:` Refatora código sem mudar funcionalidade
- `Docs:` Atualiza documentação
- `Test:` Adiciona ou atualiza testes
- `Style:` Formatação e estilo (sem mudança de código)

Exemplos:
- `Add: implement speech recognition with real-time streaming`
- `Fix: resolve audio file format compatibility issue`
- `Update: upgrade Azure SDK to version 1.46.0`
- `Docs: add API documentation for text analysis`

## Estilo de Código

### Python
- Seguir o guia de estilo PEP 8
- Usar type hints quando apropriado
- Adicionar docstrings para funções e classes
- Limitar linhas a 100 caracteres

### Formatação
```bash
# Formatar código com Black
black .

# Verificar estilo com Flake8
flake8 .

# Verificar tipos com MyPy
mypy .
```

## Testes

### Executando Testes
```bash
# Executar todos os testes
pytest

# Executar com coverage
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/test_speech.py
```

### Escrevendo Testes
- Escreva testes unitários para novas funcionalidades
- Mantenha testes independentes
- Use fixtures do pytest quando apropriado
- Mantenha testes rápidos e focados

## Estrutura do Projeto

```
Azure-Voice-Language-Lab/
├── src/                    # Código fonte
│   ├── speech/            # Funcionalidades de fala
│   ├── language/          # Funcionalidades de linguagem
│   └── utils/             # Utilitários
├── tests/                 # Testes
├── docs/                  # Documentação
├── notebooks/             # Jupyter Notebooks
├── examples/              # Exemplos de uso
└── web/                   # Aplicação web
```

## Processo de Desenvolvimento

1. Escolha uma issue ou crie uma nova
2. Comente na issue que vai trabalhar nela
3. Crie uma branch a partir de `main`
4. Desenvolva e teste suas alterações
5. Atualize a documentação se necessário
6. Abra um Pull Request
7. Aguarde revisão e feedback
8. Faça ajustes conforme necessário
9. Aguarde merge

## Diretrizes Gerais

- Seja respeitoso e construtivo
- Forneça feedback útil aos outros
- Mantenha discussões focadas e produtivas
- Documente suas alterações
- Teste antes de enviar PR
- Siga os padrões de código estabelecidos

## Perguntas?

Se você tiver dúvidas sobre como contribuir, sinta-se à vontade para:
- Abrir uma issue com a tag "question"
- Entrar em contato através das discussões do GitHub
- Consultar a documentação do projeto

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a licença MIT do projeto.
