from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import LeadAuto
from database import get_db_connection
import uvicorn
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="API Leads Seguro Auto")

# Configuração de CORS para permitir o React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, coloque a URL do seu frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"Erro de validação: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.post("/leads")
async def create_lead(lead: LeadAuto):
    """
    Cria um novo lead de seguro auto
    
    Validações aplicadas:
    - CPF/CNPJ: valida algoritmo de dígitos verificadores
    - Telefone: valida formato e estrutura brasileira
    - Campos obrigatórios: nome, cidade, UF, etc
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco")
    
    try:
        cur = conn.cursor()
        query = """
            INSERT INTO leads_auto (
                nome, cpf_cnpj, whatsapp, data_nascimento, estado_civil,
                banco_relacionamento, endereco, cidade, estado, uf,
                marca_carro, modelo_carro, versao_carro, ano_fabricacao, ano_modelo,
                tipo_residencia, tipo_portao, km_diario, possui_condutor_jovem,
                tipo_seguro, classe_bonus, tem_plano_saude
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        
        values = (
            lead.nome, lead.cpf_cnpj, lead.whatsapp, lead.data_nascimento, lead.estado_civil,
            lead.banco_relacionamento, lead.endereco, lead.cidade, lead.estado, lead.uf,
            lead.marca_carro, lead.modelo_carro, lead.versao_carro, lead.ano_fabricacao, lead.ano_modelo,
            lead.tipo_residencia, lead.tipo_portao, lead.km_diario, lead.possui_condutor_jovem,
            lead.tipo_seguro, lead.classe_bonus, lead.tem_plano_saude
        )
        
        cur.execute(query, values)
        lead_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return {"id": lead_id, "message": "Lead criado com sucesso!"}
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/leads")
async def list_leads():
    """Lista todos os leads criados"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erro de conexão com o banco de dados")
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM leads_auto ORDER BY data_criacao DESC LIMIT 100")
        leads = cur.fetchall()
        cur.close()
        conn.close()
        return leads
    except Exception as e:
        conn.close()
        print(f"Erro ao listar leads: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
