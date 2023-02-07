from subprocess import Popen
import uvicorn

from fastapi import FastAPI, WebSocket
import random
from fastapi.responses import PlainTextResponse

from fastapi import FastAPI, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Create application
app = FastAPI(title='FastAPI Templates')

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
app.add_middleware(HTTPSRedirectMiddleware)

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


if __name__ == '__main__':
    # start redirect process for port 80
    Popen(['python3', '-m', 'https_redirect'])
    # run Ssl server
    uvicorn.run(
        'main:app', port=443, host='0.0.0.0',
        reload=True,
        ssl_keyfile='./key.pem',
        ssl_certfile='./cert.pem',
    )