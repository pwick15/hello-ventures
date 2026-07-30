import json
import asyncpg
from config.settings import DATABASE_URL

pool = None

async def get_pool():
    global pool
    if not pool:
        # Supabase requires SSL, but local postgres doesn't
        if "localhost" not in DATABASE_URL and "127.0.0.1" not in DATABASE_URL:
            pool = await asyncpg.create_pool(DATABASE_URL, ssl="require")
        else:
            pool = await asyncpg.create_pool(DATABASE_URL)
    return pool

async def init_db():
    p = await get_pool()
    async with p.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS ventures (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                website TEXT,
                description TEXT,
                location TEXT,
                founding_year INTEGER,
                team_size TEXT,
                funding_stage TEXT,
                sector TEXT,
                enrichment_data TEXT,
                scores TEXT,
                overall_score REAL,
                rationale TEXT,
                strengths TEXT,
                weaknesses TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def _parse_json_fields(record):
    if not record:
        return None
    res = dict(record)
    for field in ["enrichment_data", "scores", "strengths", "weaknesses"]:
        if res.get(field):
            try:
                res[field] = json.loads(res[field])
            except json.JSONDecodeError:
                pass
    return res

async def get_all_ventures():
    p = await get_pool()
    async with p.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM ventures ORDER BY overall_score DESC NULLS LAST')
        return [_parse_json_fields(row) for row in rows]

async def get_venture(venture_id: int):
    p = await get_pool()
    async with p.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM ventures WHERE id = $1', venture_id)
        return _parse_json_fields(row)

async def create_venture(name: str, website: str, description: str = None):
    p = await get_pool()
    async with p.acquire() as conn:
        row = await conn.fetchrow(
            'INSERT INTO ventures (name, website, description) VALUES ($1, $2, $3) RETURNING *',
            name, website, description
        )
        return _parse_json_fields(row)

async def update_venture(venture_id: int, **kwargs):
    if not kwargs:
        return
    
    set_clauses = []
    values = []
    for i, (k, v) in enumerate(kwargs.items(), start=1):
        set_clauses.append(f"{k} = ${i}")
        # asyncpg expects dict/list to be passed as JSON strings if the column is TEXT,
        # so if the user passes a dict, we dump it. The previous code didn't dump,
        # wait, let's just make sure it dumps.
        if isinstance(v, (dict, list)):
            values.append(json.dumps(v))
        else:
            values.append(v)
            
    set_clause = ", ".join(set_clauses)
    set_clause += ", updated_at = CURRENT_TIMESTAMP"
    values.append(venture_id)
    venture_id_idx = len(values)
    
    p = await get_pool()
    async with p.acquire() as conn:
        await conn.execute(f'UPDATE ventures SET {set_clause} WHERE id = ${venture_id_idx}', *values)

async def delete_venture(venture_id: int):
    p = await get_pool()
    async with p.acquire() as conn:
        await conn.execute('DELETE FROM ventures WHERE id = $1', venture_id)
