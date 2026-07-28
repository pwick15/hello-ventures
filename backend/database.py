import sqlite3
import json
import aiosqlite
from config.settings import DATABASE_PATH

async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS ventures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        await db.commit()

def _parse_json_fields(row):
    if not row:
        return None
    res = dict(row)
    for field in ["enrichment_data", "scores", "strengths", "weaknesses"]:
        if res.get(field):
            try:
                res[field] = json.loads(res[field])
            except json.JSONDecodeError:
                pass
    return res

async def get_all_ventures():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM ventures ORDER BY overall_score DESC NULLS LAST') as cursor:
            rows = await cursor.fetchall()
            return [_parse_json_fields(row) for row in rows]

async def get_venture(venture_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM ventures WHERE id = ?', (venture_id,)) as cursor:
            row = await cursor.fetchone()
            return _parse_json_fields(row)

async def create_venture(name: str, website: str, description: str = None):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            'INSERT INTO ventures (name, website, description) VALUES (?, ?, ?) RETURNING *',
            (name, website, description)
        )
        row = await cursor.fetchone()
        await db.commit()
        return _parse_json_fields(row)

async def update_venture(venture_id: int, **kwargs):
    if not kwargs:
        return
    
    set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
    set_clause += ", updated_at = CURRENT_TIMESTAMP"
    values = list(kwargs.values())
    values.append(venture_id)
    
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f'UPDATE ventures SET {set_clause} WHERE id = ?', tuple(values))
        await db.commit()

async def delete_venture(venture_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('DELETE FROM ventures WHERE id = ?', (venture_id,))
        await db.commit()
