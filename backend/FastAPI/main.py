from fastapi import FastAPI
from .routers import transacciones, prueba, jwt_auth

app = FastAPI()

# ROUTERS
app.include_router(transacciones.router)    #incluimos el router de transacciones
app.include_router(prueba.router)    #incluimos el router de prueba
app.include_router(jwt_auth.router)     #incluimos el router de autenticación

@app.get("/")
async def root():
    return "Hola FastAPI"
