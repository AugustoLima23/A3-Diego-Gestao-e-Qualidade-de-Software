import sqlite3
from datetime import datetime

DB_NAME = "dados.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS locais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        endereco TEXT NOT NULL,
        descricao TEXT NOT NULL,
        gravidade TEXT NOT NULL,
        criado_em TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ajudas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,          -- 'oferta' ou 'solicitacao'
        descricao TEXT NOT NULL,
        contato TEXT NOT NULL,
        local_id INTEGER,
        status TEXT NOT NULL,        -- 'aberta', 'em_andamento', 'concluida'
        criado_em TEXT NOT NULL,
        FOREIGN KEY(local_id) REFERENCES locais(id)
    )
    """)
    conn.commit()
    conn.close()

def create_local(nome, endereco, descricao, gravidade):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO locais (nome, endereco, descricao, gravidade, criado_em)
    VALUES (?, ?, ?, ?, ?)
    """, (nome, endereco, descricao, gravidade, datetime.utcnow().isoformat()))
    conn.commit()
    local_id = cur.lastrowid
    conn.close()
    return local_id

def list_locais():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, endereco, descricao, gravidade, criado_em FROM locais ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "nome": r[1],
            "endereco": r[2],
            "descricao": r[3],
            "gravidade": r[4],
            "criado_em": r[5],
        } for r in rows
    ]

def create_ajuda(tipo, descricao, contato, local_id=None, status="aberta"):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO ajudas (tipo, descricao, contato, local_id, status, criado_em)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (tipo, descricao, contato, local_id, status, datetime.utcnow().isoformat()))
    conn.commit()
    ajuda_id = cur.lastrowid
    conn.close()
    return ajuda_id

def list_ajudas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, tipo, descricao, contato, local_id, status, criado_em
    FROM ajudas ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "tipo": r[1],
            "descricao": r[2],
            "contato": r[3],
            "local_id": r[4],
            "status": r[5],
            "criado_em": r[6],
        } for r in rows
    ]
