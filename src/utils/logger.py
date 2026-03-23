"""
Logger Module
=============

Módulo para configurar logging do Azure Voice Language Lab.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logger(
    name: str = "azure_voice_lab",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """
    Configura e retorna um logger.
    
    Args:
        name: Nome do logger.
        level: Nível de logging (padrão: logging.INFO).
        log_file: Caminho do arquivo de log (opcional).
        console: Se True, exibe logs no console (padrão: True).
        
    Returns:
        Logger configurado.
    """
    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remover handlers existentes para evitar duplicação
    logger.handlers.clear()
    
    # Formato do log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_log_file_path(base_dir: Path, name: str = "azure_voice_lab") -> str:
    """
    Gera um caminho para arquivo de log com data atual.
    
    Args:
        base_dir: Diretório base para logs.
        name: Nome do arquivo de log.
        
    Returns:
        Caminho completo do arquivo de log.
    """
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = logs_dir / f"{name}_{date_str}.log"
    
    return str(log_file)


class Logger:
    """
    Classe wrapper para logging com métodos convenientes.
    
    Attributes:
        logger (logging.Logger): Logger interno.
    """
    
    def __init__(
        self,
        name: str = "azure_voice_lab",
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        console: bool = True
    ):
        """
        Inicializa o Logger.
        
        Args:
            name: Nome do logger.
            level: Nível de logging (padrão: logging.INFO).
            log_file: Caminho do arquivo de log (opcional).
            console: Se True, exibe logs no console (padrão: True).
        """
        self.logger = setup_logger(name, level, log_file, console)
    
    def debug(self, message: str) -> None:
        """Registra mensagem de nível DEBUG."""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Registra mensagem de nível INFO."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Registra mensagem de nível WARNING."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Registra mensagem de nível ERROR."""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Registra mensagem de nível CRITICAL."""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """Registra mensagem de exceção com traceback."""
        self.logger.exception(message)
    
    def set_level(self, level: int) -> None:
        """
        Define o nível de logging.
        
        Args:
            level: Nível de logging.
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
