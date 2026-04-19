from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ENTIDAD USER (OBJETO)
class User(BaseModel):  #basemodel da la capacidad de crear una entidad sin hacer def init self
    id: int    #para el path
    nombre: str
    apellidos: str
    email: str
    edad: int

users_list = [User(id=1, nombre="Sandra", apellidos="García", email="sandra.garcia@example.com", edad=30),
        User(id=2, nombre="Juan", apellidos="Pérez", email="juan.perez@example.com", edad=25),
        User(id=3, nombre="María", apellidos="López", email="maria.lopez@example.com", edad=28)]

@router.get("/usersjson")
async def usersjson():
    return [{"nombre": "Sandra", "apellidos": "García", "email": "sandra.garcia@example.com", "edad": 30}]


# OPERACIONES GET (obtener usuarios)
@router.get("/users")
async def get_users():
    return users_list

@router.get("/user/{id}")    # pasar parametros al path (ej id del usuario)
async def get_user_path(id: int):
    try:
        users = filter(lambda user: user.id == id, users_list)
        return list(users)[0]
    except:
        return {"error": "Usuario no encontrado"}


@router.get("/user/")    # para la query (peticiones de manera concreta)
async def user(id: int):

    def search_user(id: int):
        users = filter(lambda user: user.id == id, users_list)
        try:
            return list(users)[0]
        except:
            return {"error": "Usuario no encontrado"}
    return search_user(id)


# OPERACIONES POST (añadir usuarios)
@router.post("/user/", status_code=201)    #podemos definir el codigo de estado que devuelve (201 es que se ha creado en la bbdd el usuario)
async def create_user(user: User):

    def search_user(id: int):
        users = filter(lambda user: user.id == id, users_list)
        try:
            return list(users)[0]
        except:
            return {"error": "Usuario no encontrado"}
        
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=409, detail="El usuario ya existe")  #409 cuando se intenta crear un recurso que ya existe
        return {"error": "El usuario ya existe"}
    else:
        users_list.append(user)
        return user


# OPERACIONES PUT (actualizar usuarios completos)
@router.put("/user/")
async def update_user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            return {"message": "Usuario actualizado"}
    if not found:
        return {"error": "Usuario no actualizado"}
    else:
        return user
    

# OPERACIONES DELETE (eliminar usuarios)
@router.delete("/user/{id}")
async def delete_user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            deleted_user = saved_user.nombre
            del users_list[index]
            found = True
            return {"message": f"Usuario {deleted_user} eliminado"}
    if not found:
        return {"error": "Usuario no eliminado"}