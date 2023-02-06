from fastapi import FastAPI, WebSocket
import random
from fastapi.responses import PlainTextResponse

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# Create application
app = FastAPI(title='FastAPI Templates')

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.get("/socket", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("socket.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
   await websocket.accept()
   while True:
      data = await websocket.receive_text()
      print(f"Message rx: {data}")
      await websocket.send_text(f"Message text was: {data}")