from pydantic import BaseModel

nutriologist_routes = [
    '/patients/nutriologist',
    '/food/nutriologist/{patient_id}',
    '/food/nutriologist',
    '/food/menu/nutriologist',
    '/food/menu',
    '/equivalent/group',
    '/equivalent/aliment',
    '/food/menu/register',
    '/patient/nutriologist',
    '/me'
]

patient_routes = [
    '/food/patient',
    '/food/menu',
    '/equivalent/group',
    '/equivalent/aliment',
    '/food/menu/register',
    '/me'
]

valid_roles = [
    'PACIENTE',
    'NUTRIOLOGO'
]

class RoleResponse(BaseModel):
    access: bool 
    message: str
    user: dict | None

def role_access_check (user:dict, route:str ):
    print(user)
    print(route)
    if user is  None:
        return RoleResponse (
            access= False,
            message='User Not Found',
            user= None
        )

    if user['role'] not in valid_roles: 
        return RoleResponse (
            access= False,
            message='Role Not Found',
            user= None
        )

    if user['role'] == valid_roles[0] and route not in patient_routes:
        return RoleResponse (
            access= False,
            message='Forbidden access',
            user= None
        )

    if user['role'] == valid_roles[1] and route not in nutriologist_routes:
        return RoleResponse (
            access= False,
            message='Forbidden access',
            user= None
        )

    return RoleResponse(
        access= True,
        message= 'Ok', 
        user= user
    )
