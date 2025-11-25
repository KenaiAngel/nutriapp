from fastapi import FastAPI, status, Depends, HTTPException
from security import auth
from security.encrypt import user_dependency
from pydantic import BaseModel
from domain.nutriologist import get_all_food_by_id_nutriologist, get_patients, get_all_food_groups_associate_food, add_food_group, add_patient
from domain.patient import get_food_by_id_patient


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(auth.router)
#app.include_router(common.router)


# Endpoint que usara el PACIENTE para obtener sus comidas 
# (Desayuno, Merienda, Cena, Colacion, etc)
@app.get("/food/patient",status_code=status.HTTP_200_OK)
async def get_food_patient(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    if user["role"] != "PACIENTE":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"data": get_food_by_id_patient(user["id"])}

# Endpoint que usara el NUTRIOLOGO para obtener a las comidas (Desayuno, Merienda, Cena, Colacion, etc) 
# segun el id propio (nutriologo) y el id del paciente
@app.get("/food/nutriologist/{patient_id}",status_code=status.HTTP_200_OK)
async def get_food_nutriologist (patient_id: int, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    if user["role"] != "NUTRIOLOGO":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"data": get_all_food_by_id_nutriologist(user["id"], patient_id)}


# Endpoint que usara el NUTRIOLOGO para obtener la info de todos sus pacientes asociados
@app.get("/patients/nutriologist",status_code=status.HTTP_200_OK)
async def get_all_patients(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    if user["role"] != "NUTRIOLOGO":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"data": get_patients(user["id"])}

# Endpoint que usara el NUTRIOLOGO para asignarse un paciente usando el id del paciente
@app.post("/patients/nutriologist",status_code=status.HTTP_201_CREATED)
async def add_new_patient(patient_id:int, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    if user["role"] != "NUTRIOLOGO":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"data": add_patient(patient_id,user["id"])}


class CreateFoodGroupRequest(BaseModel):
    food_id:int
    group_name: str
    description: str
    kcal: float
    protein: float
    carbohydrates: float
    fats: float

# Endpoint que usara el NUTRIOLOGO para anadir grupos de comida 
# descritos en la Clase 'CreateFoodGroupRequest'
@app.post("/group/food/nutriologist ", status_code=status.HTTP_201_CREATED)
async def post_a_food_group(new_food_group:CreateFoodGroupRequest, user:user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    if user["role"] != "NUTRIOLOGO":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"data": add_food_group(new_food_group)}

# Endpoint que usaran tanto PACIENTE como NUTRIOLOGO para obtener los grupos de comida 
# descritos en la Clase 'CreateFoodGroupRequest'
@app.get("/group/food/", status_code=status.HTTP_200_OK)
async def get_all_food_groups(food_id:int, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    return {"data": get_all_food_groups_associate_food(food_id)}




