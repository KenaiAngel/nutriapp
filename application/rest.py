from fastapi import FastAPI, status, Depends, HTTPException
from security import auth
from security.encrypt import user_dependency
from security.roleCheck import role_access_check
from pydantic import BaseModel
from domain.nutriologist import get_all_food_by_id_nutriologist, get_patients, get_all_food_groups_associate_food, add_food_group, add_patient
from domain.patient import get_food_by_id_patient


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(auth.router)
#app.include_router(common.router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

not_found_exception = HTTPException(status_code=401, detail="Authentication Failed")
forbidden_access = HTTPException(status_code=403, detail="Forbidden")

def message_handler (user, route):
    check = role_access_check(user,route)

    if not check.access:

        if check.message == 'User Not Found':
            raise not_found_exception
        
        if check.message== 'Role Not Found':
            raise not_found_exception
        
        if check.message == 'Forbidden access':
            raise forbidden_access

# Endpoint que usara el PACIENTE para obtener sus comidas 
# (Desayuno, Merienda, Cena, Colacion, etc)
@app.get("/food/patient",status_code=status.HTTP_200_OK)
async def get_food_patient(user: user_dependency):
    message_handler(user,"/food/patient")
    return {"data": get_food_by_id_patient(user["id"])}

# Endpoint que usara el NUTRIOLOGO para obtener a las comidas (Desayuno, Merienda, Cena, Colacion, etc) 
# segun el id propio (nutriologo) y el id del paciente
@app.get("/food/nutriologist/{patient_id}",status_code=status.HTTP_200_OK)
async def get_food_nutriologist (patient_id: int, user: user_dependency):
    message_handler(user,'/food/nutriologist/{patient_id}')           
    return {"data": get_all_food_by_id_nutriologist(user["id"], patient_id)}


# Endpoint que usara el NUTRIOLOGO para obtener la info de todos sus pacientes asociados
@app.get("/patients/nutriologist",status_code=status.HTTP_200_OK)
async def get_all_patients(user: user_dependency):
    message_handler(user,'/patients/nutriologist')
    return {"data": get_patients(user["id"])}

# Endpoint que usara el NUTRIOLOGO para asignarse un paciente usando el id del paciente
@app.post("/patients/nutriologist",status_code=status.HTTP_201_CREATED)
async def add_new_patient(patient_id:int, user: user_dependency):
    message_handler(user,'/patients/nutriologist')
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
@app.post("/group/food/nutriologist", status_code=status.HTTP_201_CREATED)
async def post_a_food_group(new_food_group:CreateFoodGroupRequest, user:user_dependency):
    print("Food group ingresado: ", new_food_group)
    message_handler(user,'/group/food/nutriologist')
    return {"data": add_food_group(new_food_group)}

# Endpoint que usaran tanto PACIENTE como NUTRIOLOGO para obtener los grupos de comida 
# descritos en la Clase 'CreateFoodGroupRequest'
@app.get("/group/food", status_code=status.HTTP_200_OK)
async def get_all_food_groups(food_id:int, user: user_dependency):
    message_handler(user,'/group/food')
    return {"data": get_all_food_groups_associate_food(food_id)}