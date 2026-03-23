"""
Validators Module
=================

Módulo para validação de entradas do Azure Voice Language Lab.
"""

import os
from pathlib import Path
from typing import Optional


def validate_audio_file(audio_file: str) -> dict:
    """
    Valida se um arquivo de áudio é válido.
    
    Args:
        audio_file: Caminho do arquivo de áudio.
        
    Returns:
        Dicionário com status da validação e erros encontrados.
    """
    errors = []
    
    # Verificar se o arquivo existe
    if not os.path.exists(audio_file):
        errors.append(f"Arquivo não encontrado: {audio_file}")
        return {"valid": False, "errors": errors}
    
    # Verificar se é um arquivo
    if not os.path.isfile(audio_file):
        errors.append(f"Caminho não é um arquivo: {audio_file}")
        return {"valid": False, "errors": errors}
    
    # Verificar extensão do arquivo
    valid_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.wma']
    file_extension = Path(audio_file).suffix.lower()
    
    if file_extension not in valid_extensions:
        errors.append(
            f"Formato de arquivo não suportado: {file_extension}. "
            f"Formatos suportados: {', '.join(valid_extensions)}"
        )
    
    # Verificar tamanho do arquivo (máximo 100MB)
    file_size = os.path.getsize(audio_file)
    max_size = 100 * 1024 * 1024  # 100MB
    
    if file_size > max_size:
        errors.append(
            f"Arquivo muito grande: {file_size / (1024 * 1024):.2f}MB. "
            f"Tamanho máximo: 100MB"
        )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "file_size": file_size,
        "file_extension": file_extension
    }


def validate_text(text: str, min_length: int = 1, max_length: int = 10000) -> dict:
    """
    Valida se um texto é válido.
    
    Args:
        text: Texto a ser validado.
        min_length: Comprimento mínimo do texto (padrão: 1).
        max_length: Comprimento máximo do texto (padrão: 10000).
        
    Returns:
        Dicionário com status da validação e erros encontrados.
    """
    errors = []
    
    # Verificar se o texto não está vazio
    if not text or not text.strip():
        errors.append("Texto não pode estar vazio")
        return {"valid": False, "errors": errors}
    
    # Verificar comprimento mínimo
    if len(text) < min_length:
        errors.append(
            f"Texto muito curto: {len(text)} caracteres. "
            f"Mínimo: {min_length} caracteres"
        )
    
    # Verificar comprimento máximo
    if len(text) > max_length:
        errors.append(
            f"Texto muito longo: {len(text)} caracteres. "
            f"Máximo: {max_length} caracteres"
        )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "length": len(text)
    }


def validate_language(language: str, supported_languages: list) -> dict:
    """
    Valida se um idioma é suportado.
    
    Args:
        language: Código do idioma (ex: pt-BR, en-US).
        supported_languages: Lista de idiomas suportados.
        
    Returns:
        Dicionário com status da validação e erros encontrados.
    """
    errors = []
    
    if not language:
        errors.append("Idioma não pode estar vazio")
        return {"valid": False, "errors": errors}
    
    if language not in supported_languages:
        errors.append(
            f"Idioma não suportado: {language}. "
            f"Idiomas suportados: {', '.join(supported_languages)}"
        )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_voice(voice: str, available_voices: list) -> dict:
    """
    Valida se uma voz está disponível.
    
    Args:
        voice: Nome da voz (ex: pt-BR-FranciscaNeural).
        available_voices: Lista de vozes disponíveis.
        
    Returns:
        Dicionário com status da validação e erros encontrados.
    """
    errors = []
    
    if not voice:
        errors.append("Voz não pode estar vazia")
        return {"valid": False, "errors": errors}
    
    if voice not in available_voices:
        errors.append(
            f"Voz não disponível: {voice}. "
            f"Vozez disponíveis: {', '.join(available_voices[:10])}..."
        )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_api_key(api_key: str) -> dict:
    """
    Valida se uma chave de API é válida.
    
    Args:
        api_key: Chave de API a ser validada.
        
    Returns:
        Dicionário com status da validação e erros encontrados.
    """
    errors = []
    
    if not api_key:
        errors.append("Chave de API não pode estar vazia")
        return {"valid": False, "errors": errors}
    
    # Verificar comprimento mínimo (chaves do Azure geralmente têm 32 caracteres)
    if len(api_key) < 32:
        errors.append(
            f"Chave de API muito curta: {len(api_key)} caracteres. "
            f"Mínimo: 32 caracteres"
        )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def validate_region(region: str) -> dict:
    """
    Valida se uma região do Azure é válida.
    
    Args:
        region: Região do Azure (ex: eastus, westeurope).
        
    Returns:
        Dicionário com status da validação e erros encontrados.
    """
    errors = []
    
    if not region:
        errors.append("Região não pode estar vazia")
        return {"valid": False, "errors": errors}
    
    # Regiões válidas do Azure (lista não exaustiva)
    valid_regions = [
        "eastus", "westus", "eastus2", "westus2",
        "eastasia", "southeastasia",
        "westeurope", "northeurope",
        "brazilsouth", "australiaeast",
        "japaneast", "koreacentral",
        "southcentralus", "centralus"
    ]
    
    if region.lower() not in [r.lower() for r in valid_regions]:
        errors.append(
            f"Região não reconhecida: {region}. "
            f"Regiões comuns: {', '.join(valid_regions[:10])}..."
        )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
