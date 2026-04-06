import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine, inspect, MetaData, Table, delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine

DATABASE_USER = os.getenv("DB_USER", "root")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD", "")
DATABASE_HOST = os.getenv("DB_HOST", "127.0.0.1")
DATABASE_PORT = os.getenv("DB_PORT", "3306")
DATABASE_NAME = os.getenv("DB_NAME", "proyecto_fin_grado")

DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
)


def get_engine() -> Engine:
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def get_users_table(engine: Engine) -> Table:
    metadata = MetaData()
    inspector = inspect(engine)
    if "usuarios" not in inspector.get_table_names():
        users_table = Table(
            "usuarios",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("nombre", String(255)),
            Column("email", String(255)),
        )
        metadata.create_all(engine, tables=[users_table])
        return users_table
    return Table("usuarios", metadata, autoload_with=engine)


def row_to_dict(row: Any) -> Dict[str, Any]:
    return {key: row[key] for key in row.keys()}


class UserSchema(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
    email: Optional[str] = None

    class Config:
        extra = "allow"


app = FastAPI(title="Usuarios API - proyecto_fin_grado")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "FastAPI MySQL usuarios API"}


@app.get("/users")
async def read_users():
    engine = get_engine()
    users_table = get_users_table(engine)
    with engine.connect() as conn:
        result = conn.execute(select(users_table))
        return [row_to_dict(row) for row in result]


@app.get("/users/{user_id}")
async def read_user(user_id: int):
    engine = get_engine()
    users_table = get_users_table(engine)
    pk_columns = list(users_table.primary_key.columns)
    if not pk_columns:
        raise HTTPException(status_code=500, detail="La tabla usuarios no tiene clave primaria definida")
    pk = pk_columns[0]

    with engine.connect() as conn:
        row = conn.execute(select(users_table).where(pk == user_id)).first()
        if row is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return row_to_dict(row)


@app.post("/users")
async def create_user(user: UserSchema):
    engine = get_engine()
    users_table = get_users_table(engine)
    data = user.dict(exclude_none=True, exclude={"id"})
    if not data:
        raise HTTPException(status_code=400, detail="Los datos del usuario no pueden estar vacíos")

    with engine.connect() as conn:
        try:
            result = conn.execute(insert(users_table).values(**data))
            conn.commit()
            new_id = result.inserted_primary_key[0] if result.inserted_primary_key else None
            return {"id": new_id, **data}
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=500, detail=str(exc))


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserSchema):
    engine = get_engine()
    users_table = get_users_table(engine)
    data = user.dict(exclude_none=True, exclude={"id"})
    if not data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    pk_columns = list(users_table.primary_key.columns)
    if not pk_columns:
        raise HTTPException(status_code=500, detail="La tabla usuarios no tiene clave primaria definida")
    pk = pk_columns[0]

    with engine.connect() as conn:
        result = conn.execute(update(users_table).where(pk == user_id).values(**data))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"id": user_id, **data}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    engine = get_engine()
    users_table = get_users_table(engine)
    pk_columns = list(users_table.primary_key.columns)
    if not pk_columns:
        raise HTTPException(status_code=500, detail="La tabla usuarios no tiene clave primaria definida")
    pk = pk_columns[0]

    with engine.connect() as conn:
        result = conn.execute(delete(users_table).where(pk == user_id))
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"detail": "Usuario eliminado"}
