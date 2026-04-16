"""
Módulo de validadores para CPF, CNPJ e Telefone
Implementa algoritmos de validação brasileiros
"""

import re
from typing import Tuple


def remove_formatting(value: str) -> str:
    """Remove caracteres especiais de um documento"""
    return re.sub(r'\D', '', value)


def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF usando algoritmo de dígitos verificadores
    
    Args:
        cpf: CPF com ou sem formatação
        
    Returns:
        bool: True se CPF válido, False caso contrário
    """
    cpf = remove_formatting(cpf)
    
    if len(cpf) != 11:
        return False
    
    # Rejeita sequências repetidas
    if re.match(r'^(\d)\1{10}$', cpf):
        return False
    
    # Calcula primeiro dígito verificador
    sum_value = sum(int(cpf[i]) * (10 - i) for i in range(9))
    first_digit = 11 - (sum_value % 11)
    first_digit = 0 if first_digit > 9 else first_digit
    
    if int(cpf[9]) != first_digit:
        return False
    
    # Calcula segundo dígito verificador
    sum_value = sum(int(cpf[i]) * (11 - i) for i in range(10))
    second_digit = 11 - (sum_value % 11)
    second_digit = 0 if second_digit > 9 else second_digit
    
    if int(cpf[10]) != second_digit:
        return False
    
    return True


def validate_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ usando algoritmo de dígitos verificadores
    
    Args:
        cnpj: CNPJ com ou sem formatação
        
    Returns:
        bool: True se CNPJ válido, False caso contrário
    """
    cnpj = remove_formatting(cnpj)
    
    if len(cnpj) != 14:
        return False
    
    # Rejeita sequências repetidas
    if re.match(r'^(\d)\1{13}$', cnpj):
        return False
    
    # Calcula primeiro dígito verificador
    multiplier = 5
    sum_value = 0
    for i in range(8):
        sum_value += int(cnpj[i]) * multiplier
        multiplier = 9 if multiplier == 2 else multiplier - 1
    
    first_digit = 11 - (sum_value % 11)
    first_digit = 0 if first_digit > 9 else first_digit
    
    if int(cnpj[8]) != first_digit:
        return False
    
    # Calcula segundo dígito verificador
    multiplier = 6
    sum_value = 0
    for i in range(9):
        sum_value += int(cnpj[i]) * multiplier
        multiplier = 9 if multiplier == 2 else multiplier - 1
    
    second_digit = 11 - (sum_value % 11)
    second_digit = 0 if second_digit > 9 else second_digit
    
    if int(cnpj[9]) != second_digit:
        return False
    
    return True


def validate_cpf_or_cnpj(document: str) -> Tuple[bool, str]:
    """
    Valida CPF ou CNPJ
    
    Args:
        document: CPF ou CNPJ
        
    Returns:
        Tuple: (is_valid, type) onde type é 'cpf', 'cnpj' ou 'unknown'
    """
    formatted = remove_formatting(document)
    
    if len(formatted) == 11:
        return (validate_cpf(formatted), 'cpf')
    
    if len(formatted) == 14:
        return (validate_cnpj(formatted), 'cnpj')
    
    return (False, 'unknown')


def validate_phone(phone: str) -> bool:
    """
    Valida telefone brasileiro (com DDD)
    Aceita: (XX) 9XXXX-XXXX (11 dígitos) ou (XX) XXXX-XXXX (10 dígitos)
    """
    phone = remove_formatting(phone)
    
    # Telefone brasileiro deve ter 10 ou 11 dígitos (incluindo DDD)
    if len(phone) < 10 or len(phone) > 11:
        return False
    
    # DDD: Primeiro dígito nunca é 0
    if phone[0] == '0':
        return False

    # Se tem 11 dígitos, o terceiro dígito (index 2) deve ser 9 (celular: DD 9XXXX-XXXX)
    if len(phone) == 11 and phone[2] != '9':
        return False
    
    # Se tem 10 dígitos (fixo), o terceiro dígito (index 2) deve ser entre 2 e 5 (DD XXXX-XXXX)
    if len(phone) == 10 and not re.match(r'^[2-5]', phone[2]):
        return False
    
    # Rejeita sequências repetidas
    if re.match(r'^(\d)\1{9,10}$', phone):
        return False
    
    return True


def format_cpf(cpf: str) -> str:
    """Formata CPF: 123.456.789-00"""
    cpf = remove_formatting(cpf)
    if len(cpf) != 11:
        return cpf
    return re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})', r'\1.\2.\3-\4', cpf)


def format_cnpj(cnpj: str) -> str:
    """Formata CNPJ: 12.345.678/0001-90"""
    cnpj = remove_formatting(cnpj)
    if len(cnpj) != 14:
        return cnpj
    return re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})', r'\1.\2.\3/\4-\5', cnpj)


def format_phone(phone: str) -> str:
    """Formata telefone: (XX) 9XXXX-XXXX ou (XX) XXXX-XXXX"""
    phone = remove_formatting(phone)
    if len(phone) == 11:
        return re.sub(r'(\d{2})(\d{5})(\d{4})', r'(\1) \2-\3', phone)
    if len(phone) == 10:
        return re.sub(r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3', phone)
    return phone
