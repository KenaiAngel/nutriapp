from fastapi import FastAPI, status, Depends, HTTPException
from security import auth
from security.encrypt import user_dependency
from security.roleCheck import role_access_check
from pydantic import BaseModel
from domain.nutriologist import get_all_food_by_id_nutriologist, get_patients, get_all_menu_parts_from_a_food_event, add_menu_part, add_patient, add_food_event
from domain.patient import get_food_by_id_patient, add_new_register, get_all_registers_date_food_id
from domain.equivalent import get_all_food_groups,get_all_aliments_by_food_group_id
from domain.users import add_user
from datetime import date

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(auth.router)
#app.include_router(common.router)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5500"
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


class FoodEventRequest(BaseModel):
    food_name: str
    description:str | None
    patient_id: int

@app.post("/food/nutriologist",status_code=status.HTTP_201_CREATED)
async def post_food_to_patient (new_food_event:FoodEventRequest,user: user_dependency):
    message_handler(user,'/food/nutriologist')       
    response = add_food_event(new_food_event, user["id"])
    return response


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
class CreatenPacienteRequest(BaseModel):
    name: str
    first_name: str
    last_name: str
    mail: str
    password: str

@app.post("/patients/nutriologist",status_code=status.HTTP_201_CREATED)
async def add_new_patient(patient:CreatenPacienteRequest, user: user_dependency):
    message_handler(user,'/patients/nutriologist')
    response = add_user(patient,user["id"])

    if not response['valid']:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )
    
    return response


class MenuPartRequest(BaseModel):
    food_event_id:int
    group_name: str
    description: str
    aliment: str
    amount: float
    unit: str

# Endpoint que usara el NUTRIOLOGO para anadir partes que integran al menu 
# descritos en la Clase 'MenuPartRequest'
@app.post("/food/menu/nutriologist", status_code=status.HTTP_201_CREATED)
async def post_a_menu_part(new_menu_part:MenuPartRequest, user:user_dependency):
    print("Food group ingresado: ", new_menu_part)
    message_handler(user,"/food/menu/nutriologist")
    return {"data": add_menu_part(new_menu_part)}

# Endpoint que usaran tanto PACIENTE como NUTRIOLOGO para obtener las partes que integran al menu 
# descritos en la Clase 'MenuPartRequest'
@app.get("/food/menu", status_code=status.HTTP_200_OK)
async def get_all_parts_from_menu(food_id:int, user: user_dependency):
    message_handler(user,'/food/menu')
    return {"data": get_all_menu_parts_from_a_food_event(food_id)}


@app.get("/equivalent/group", status_code= status.HTTP_200_OK)
async def get_all_groups(user: user_dependency):
    message_handler(user,'/equivalent/group')
    return {"data": get_all_food_groups()}


@app.get("/equivalent/aliment", status_code= status.HTTP_200_OK)
async def get_all_aliment_from_a_group(group_id:int, user: user_dependency):
    message_handler(user,'/equivalent/aliment')
    return {"data": get_all_aliments_by_food_group_id(group_id)}

class MenuRegisterRequest(BaseModel): 
    date: date
    food_event_id: int

    group_name: str
    description: str
    aliment: str
    amount: float
    unit: str

@app.post('/food/menu/register',status_code=status.HTTP_201_CREATED)
async def post_new_resgister_patient(new_menu_register:MenuRegisterRequest, user:user_dependency):
    message_handler(user,'/food/menu/register')
    return {"data": add_new_register(new_menu_register)}


@app.get('/food/menu/register',status_code=status.HTTP_200_OK)
async def get_all_resgisters_with_date_event_id(date:date, food_event_id:int,user: user_dependency):
    message_handler(user,'/food/menu/register')
    return {"data": get_all_registers_date_food_id(date, food_event_id)}
