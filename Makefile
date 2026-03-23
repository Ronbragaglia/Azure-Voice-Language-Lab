# Azure Voice Language Lab - Makefile
# =====================================
#
# Makefile para automação de tarefas comuns do projeto.

.PHONY: help install install-dev install-all clean test lint format type-check security build docker docker-run docker-stop docs serve-web run-examples

# Variáveis
PYTHON := python3
PIP := pip3
VENV := venv
ACTIVATE := $(VENV)/bin/activate
PYTHON_VERSION := 3.11

# Cores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Mostra esta mensagem de ajuda
	@echo "$(BLUE)Azure Voice Language Lab - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Exemplos de uso:$(NC)"
	@echo "  make install          # Instala o projeto"
	@echo "  make test            # Executa os testes"
	@echo "  make lint            # Verifica o código"
	@echo "  make format          # Formata o código"
	@echo "  make serve-web       # Inicia a aplicação web"
	@echo "  make docker-run      # Executa com Docker"

install: ## Instala o projeto e suas dependências
	@echo "$(BLUE)Instalando Azure Voice Language Lab...$(NC)"
	$(PIP) install -e .
	@echo "$(GREEN)✅ Instalação concluída!$(NC)"

install-dev: ## Instala o projeto com dependências de desenvolvimento
	@echo "$(BLUE)Instalando Azure Voice Language Lab (dev)...$(NC)"
	$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✅ Instalação de desenvolvimento concluída!$(NC)"

install-all: ## Instala o projeto com todas as dependências
	@echo "$(BLUE)Instalando Azure Voice Language Lab (all)...$(NC)"
	$(PIP) install -e ".[all]"
	@echo "$(GREEN)✅ Instalação completa concluída!$(NC)"

clean: ## Remove arquivos temporários e de build
	@echo "$(BLUE)Limpando arquivos temporários...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf .eggs 2>/dev/null || true
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

test: ## Executa os testes
	@echo "$(BLUE)Executando testes...$(NC)"
	pytest tests/ -v
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"

test-cov: ## Executa os testes com coverage
	@echo "$(BLUE)Executando testes com coverage...$(NC)"
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)✅ Testes concluídos!$(NC)"
	@echo "$(YELLOW)Relatório de coverage: htmlcov/index.html$(NC)"

test-unit: ## Executa apenas testes unitários
	@echo "$(BLUE)Executando testes unitários...$(NC)"
	pytest tests/ -v -m unit
	@echo "$(GREEN)✅ Testes unitários concluídos!$(NC)"

test-integration: ## Executa apenas testes de integração
	@echo "$(BLUE)Executando testes de integração...$(NC)"
	pytest tests/ -v -m integration
	@echo "$(GREEN)✅ Testes de integração concluídos!$(NC)"

lint: ## Executa verificação de código (flake8)
	@echo "$(BLUE)Verificando código com flake8...$(NC)"
	flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "$(GREEN)✅ Verificação concluída!$(NC)"

format: ## Formata o código com black e isort
	@echo "$(BLUE)Formatando código...$(NC)"
	black src/ tests/ examples/
	isort src/ tests/ examples/
	@echo "$(GREEN)✅ Código formatado!$(NC)"

format-check: ## Verifica se o código está formatado
	@echo "$(BLUE)Verificando formatação...$(NC)"
	black --check src/ tests/ examples/
	isort --check-only src/ tests/ examples/
	@echo "$(GREEN)✅ Código formatado corretamente!$(NC)"

type-check: ## Executa verificação de tipos com mypy
	@echo "$(BLUE)Verificando tipos com mypy...$(NC)"
	mypy src/ --ignore-missing-imports
	@echo "$(GREEN)✅ Verificação de tipos concluída!$(NC)"

security: ## Executa verificação de segurança
	@echo "$(BLUE)Verificando segurança...$(NC)"
	bandit -r src/ -f json -o bandit-report.json || true
	safety check || true
	@echo "$(GREEN)✅ Verificação de segurança concluída!$(NC)"

check-all: format-check lint type-check security ## Executa todas as verificações
	@echo "$(GREEN)✅ Todas as verificações concluídas!$(NC)"

build: ## Constrói o pacote do projeto
	@echo "$(BLUE)Construindo pacote...$(NC)"
	python -m build
	@echo "$(GREEN)✅ Build concluído!$(NC)"

publish: ## Publica o pacote no PyPI
	@echo "$(BLUE)Publicando no PyPI...$(NC)"
	python -m twine upload dist/*
	@echo "$(GREEN)✅ Publicação concluída!$(NC)"

docker-build: ## Constrói a imagem Docker
	@echo "$(BLUE)Construindo imagem Docker...$(NC)"
	docker build -t azure-voice-language-lab:latest .
	@echo "$(GREEN)✅ Imagem Docker construída!$(NC)"

docker-run: ## Executa o container Docker
	@echo "$(BLUE)Executando container Docker...$(NC)"
	docker run -p 8501:8501 --env-file .env azure-voice-language-lab:latest

docker-stop: ## Para todos os containers Docker
	@echo "$(BLUE)Parando containers Docker...$(NC)"
	docker stop $$(docker ps -q --filter ancestor=azure-voice-language-lab:latest) 2>/dev/null || true
	@echo "$(GREEN)✅ Containers parados!$(NC)"

docker-clean: ## Remove imagens e containers Docker
	@echo "$(BLUE)Limpando Docker...$(NC)"
	docker system prune -f
	@echo "$(GREEN)✅ Limpeza Docker concluída!$(NC)"

docs: ## Gera a documentação
	@echo "$(BLUE)Gerando documentação...$(NC)"
	cd docs && make html
	@echo "$(GREEN)✅ Documentação gerada!$(NC)"
	@echo "$(YELLOW)Abra docs/_build/html/index.html no navegador$(NC)"

docs-serve: ## Serve a documentação localmente
	@echo "$(BLUE)Servindo documentação...$(NC)"
	cd docs && python -m http.server 8000 -d _build/html

serve-web: ## Inicia a aplicação web Streamlit
	@echo "$(BLUE)Iniciando aplicação web...$(NC)"
	streamlit run web/app.py

run-examples: ## Executa os exemplos básicos
	@echo "$(BLUE)Executando exemplos...$(NC)"
	python examples/basic_usage.py

run-advanced: ## Executa os exemplos avançados
	@echo "$(BLUE)Executando exemplos avançados...$(NC)"
	python examples/advanced_usage.py

setup-env: ## Cria o arquivo .env de exemplo
	@echo "$(BLUE)Criando arquivo .env...$(NC)"
	cp .env.example .env
	@echo "$(GREEN)✅ Arquivo .env criado!$(NC)"
	@echo "$(YELLOW)Edite o arquivo .env com suas credenciais do Azure$(NC)"

init: install-dev setup-env ## Inicializa o projeto (instala e configura)
	@echo "$(GREEN)✅ Projeto inicializado!$(NC)"
	@echo "$(YELLOW)Próximos passos:$(NC)"
	@echo "  1. Edite o arquivo .env com suas credenciais do Azure"
	@echo "  2. Execute 'make test' para verificar a instalação"
	@echo "  3. Execute 'make serve-web' para iniciar a aplicação"

pre-commit-install: ## Instala os hooks do pre-commit
	@echo "$(BLUE)Instalando hooks do pre-commit...$(NC)"
	pre-commit install
	@echo "$(GREEN)✅ Hooks instalados!$(NC)"

pre-commit-run: ## Executa todos os hooks do pre-commit
	@echo "$(BLUE)Executando hooks do pre-commit...$(NC)"
	pre-commit run --all-files
	@echo "$(GREEN)✅ Hooks executados!$(NC)"

update-deps: ## Atualiza as dependências
	@echo "$(BLUE)Atualizando dependências...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -e ".[all]"
	@echo "$(GREEN)✅ Dependências atualizadas!$(NC)"

freeze: ## Gera requirements.txt das dependências instaladas
	@echo "$(BLUE)Gerando requirements.txt...$(NC)"
	$(PIP) freeze > requirements-freeze.txt
	@echo "$(GREEN)✅ requirements-freeze.txt gerado!$(NC)"

version: ## Mostra a versão do projeto
	@echo "Azure Voice Language Lab v1.1.0"

info: ## Mostra informações do projeto
	@echo "$(BLUE)Azure Voice Language Lab$(NC)"
	@echo "Versão: 1.1.0"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Pip: $(shell $(PIP) --version)"
	@echo ""
	@echo "$(YELLOW)Comandos úteis:$(NC)"
	@echo "  make help           # Mostra todos os comandos"
	@echo "  make init           # Inicializa o projeto"
	@echo "  make test           # Executa os testes"
	@echo "  make serve-web      # Inicia a aplicação web"
	@echo "  make docker-run     # Executa com Docker"
