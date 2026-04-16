import psycopg2
from psycopg2.extras import RealDictCursor
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Encontrar o caminho absoluto para o .env no diretório do backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Construir DATABASE_URL com encoding de caracteres especiais
_db_user = os.getenv("DB_USER", "postgres")
_db_password = os.getenv("DB_PASSWORD", "")
_db_host = os.getenv("DB_HOST", "localhost")
_db_port = os.getenv("DB_PORT", "5432")
_db_name = os.getenv("DB_NAME", "postgres")

# URL encoding da senha para caracteres especiais
_db_password_encoded = quote_plus(_db_password)

# Prioridade 1: DATABASE_URL direto do ambiente (com sslmode se necessário)
DATABASE_URL = os.getenv("DATABASE_URL")

# Prioridade 2: Construir se não houver DATABASE_URL
if not DATABASE_URL:
    DATABASE_URL = f"postgresql://{_db_user}:{_db_password_encoded}@{_db_host}:{_db_port}/{_db_name}"

# Garantir sslmode=require para Supabase se for um host da supabase
if "supabase.com" in DATABASE_URL or "supabase.co" in DATABASE_URL:
    if "sslmode" not in DATABASE_URL:
        # Se já tiver parâmetros (?par=val), adiciona com &, se não, com ?
        separator = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL += f"{separator}sslmode=require"

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None
