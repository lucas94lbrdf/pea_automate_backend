from pydantic import BaseModel, field_validator
from datetime import date
from typing import Optional
from validators import validate_cpf_or_cnpj, validate_phone, format_cpf, format_cnpj, format_phone


class LeadAuto(BaseModel):
    # Pessoais
    nome: str
    cpf_cnpj: str
    whatsapp: str
    data_nascimento: date
    estado_civil: str
    banco_relacionamento: Optional[str] = None
    
    # Endereço
    endereco: Optional[str] = None
    cidade: str
    estado: Optional[str] = None
    uf: str
    
    # Veículo
    marca_carro: str
    modelo_carro: str
    versao_carro: Optional[str] = None
    ano_fabricacao: Optional[int] = None
    ano_modelo: int
    
    # Perfil
    tipo_residencia: str
    tipo_portao: Optional[str] = None
    km_diario: int
    possui_condutor_jovem: bool = False
    
    # Seguro
    tipo_seguro: str = "Novo"
    classe_bonus: int = 0
    
    # Outros
    tem_plano_saude: bool = False
    status: str = "Novo"
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v):
        if not v or not v.strip():
            raise ValueError('Nome é obrigatório')
        if len(v.strip()) < 3:
            raise ValueError('Nome deve ter no mínimo 3 caracteres')
        return v.strip()
    
    @field_validator('cpf_cnpj')
    @classmethod
    def validate_cpf_cnpj(cls, v):
        if not v or not v.strip():
            raise ValueError('CPF/CNPJ é obrigatório')
        is_valid, doc_type = validate_cpf_or_cnpj(v)
        if not is_valid:
            if doc_type == 'cpf':
                raise ValueError('CPF inválido')
            elif doc_type == 'cnpj':
                raise ValueError('CNPJ inválido')
            else:
                raise ValueError('CPF ou CNPJ com formato inválido')
        # Retorna formatado
        if doc_type == 'cpf':
            return format_cpf(v)
        else:
            return format_cnpj(v)
    
    @field_validator('whatsapp')
    @classmethod
    def validate_whatsapp(cls, v):
        if not v or not v.strip():
            raise ValueError('WhatsApp é obrigatório')
        if not validate_phone(v):
            raise ValueError('Telefone inválido')
        # Retorna formatado
        return format_phone(v)
    
    @field_validator('cidade')
    @classmethod
    def validate_cidade(cls, v):
        if not v or not v.strip():
            raise ValueError('Cidade é obrigatória')
        return v.strip()
    
    @field_validator('uf')
    @classmethod
    def validate_uf(cls, v):
        valid_ufs = [
            'AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT',
            'PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO'
        ]
        if not v or v not in valid_ufs:
            raise ValueError(f'UF inválido. Aceitos: {", ".join(valid_ufs)}')
        return v
