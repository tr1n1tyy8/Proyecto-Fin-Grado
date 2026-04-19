from fastapi import APIRouter
from pydantic import BaseModel # Asegúrate de importar esto

# 1. Configuramos el router con el prefijo
router = APIRouter(
    prefix="/transacciones",    # con el prefijo ya no haría falta indicar cuál es en cada operación de router (get, post...)
    tags=["transacciones"],
    responses={404: {"message": "Not found"}}    # para definir respuestas personalizadas (ej 404)
)

# 2. Definimos la ruta (fíjate que ahora solo pongo /{cliente_id})
@router.get("/{cliente_id}")    # como hemos definido un prefijo para el router, ya no es necesario indicarlo en cada operación (solo id)
async def historial(cliente_id: int):
    return {"historial": [], "cliente_id": cliente_id}