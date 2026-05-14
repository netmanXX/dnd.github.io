import json
import os
from fastapi import *
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
USERS_FILE = "users.json"

@app.get("/")
def open_log_page():
    return FileResponse('templates/loging.html')

@app.get("/register")
def open_reg_page():
    return FileResponse('templates/register.html')

@app.get("/dnd")
def open_dnd():
    return FileResponse('templates/character.html')

@app.post("/dnd")
def open_dnd_post():
    return FileResponse('templates/character.html')

@app.post("/register")
async def register(request: Request):
    form = await request.form()
    username = form.get("username")
    email = form.get("email")
    password = form.get("password")
    confirm_password = form.get("confirm_password")
    gender = form.get("gender")
    terms = form.get("terms")
    if password != confirm_password:
        return RedirectResponse("/register?error=password_mismatch", status_code=303)
    if terms != "on":
        return RedirectResponse("/register?error=terms_oshibka", status_code=303)
    users = load_users()
    if any(i["username"]==username for i in users):
        return RedirectResponse("/register?error=username_exists", status_code=303)
    new_user = {
        "username": username,
        "email": email,
        "password": password,
        "gender": gender
    }
    users.append(new_user)
    save_users(users)
    return RedirectResponse("/?registered=true", status_code=303)

@app.post('/')
async def loging(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    users = load_users()
    for i in users:
        if i['username'] == username:
            if password == i["password"]:
                return RedirectResponse("/dnd", status_code=303)

    return RedirectResponse("/?error=password_or_username_mistake", status_code=303)

@app.post("/dnd")
async def save_dnd(request: Request):
    form = await request.form()
    save_button = form.get("exportBtn")



def load_users() -> list:
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users: list) -> None :
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)