import uvicorn
import requests
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hamsa@123",
  database="bhumi"
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class = HTMLResponse)
async def home(request : Request):
    return templates.TemplateResponse("home.html", {"request" : request})

@app.get("/home.html", response_class = HTMLResponse)
async def home(request : Request):
    return templates.TemplateResponse("home.html", {"request" : request})

@app.get("/volunteer.html", response_class = HTMLResponse)
async def volunteer(request : Request):
    return templates.TemplateResponse("volunteer.html", {"request" : request})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, f_name: str = Form(...), number: str = Form(...), email: str = Form(...)):
    cur = db.cursor(dictionary=True)
    x = "SELECT count(*) as count FROM volunteers WHERE name=%s"
    y = (f_name,)
    cur.execute(x,y)
    r = cur.fetchone()
    if r["count"] == 0:
      x = "INSERT INTO volunteers(name, mobile, email) VALUES(%s, %s, %s)"
      y = (f_name, number, email)
      cur.execute(x,y)
      db.commit()
      return templates.TemplateResponse("registered.html", {"request": request})
    else:
      return templates.TemplateResponse("already_registered.html", {"request": request})

@app.get("/donate.html", response_class = HTMLResponse)
async def volunteer(request : Request):
    return templates.TemplateResponse("donate.html", {"request" : request})

@app.post("/donate", response_class=HTMLResponse)
async def register(request: Request, f_name: str = Form(...), number: str = Form(...), email: str = Form(...), v_name: str = Form(...), amount: str = Form(), date: str = Form(...)):
    cur = db.cursor(dictionary=True)
    x = "INSERT INTO donations(name, mobile, email, vname, amount, dt) VALUES(%s, %s, %s, %s, %s, %s)"
    y = (f_name, number, email, v_name, amount, date)
    cur.execute(x,y)
    db.commit()
    return templates.TemplateResponse("donated.html", {"request": request})

@app.get("/contact.html", response_class = HTMLResponse)
async def home(request : Request):
    return templates.TemplateResponse("contact.html", {"request" : request})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5500, reload=True)