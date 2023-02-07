from fastapi import FastAPI, WebSocket
import random
from fastapi.responses import PlainTextResponse

from fastapi import FastAPI, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import uvicorn

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

    try:
        # send "Connection established" message to client
        await websocket.send_text("Connection established!")

        # await for messages and send messages
        while True:
            msg = await websocket.receive_text()
            if msg.lower() == "close":
                await websocket.close()
                break
            else:
                print(f'CLIENT says - {msg}')
                await websocket.send_text(f"Your message was: {msg}")

    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == 'main':
    uvicorn.run(
               app,
               host="0.0.0.0",
               port=443,
               ssl_keyfile=".ssl/key.pem",
               ssl_certfile=".ssl/cert.pem"
               )