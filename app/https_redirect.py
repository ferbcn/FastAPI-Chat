import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse

app = FastAPI()


@app.route('/{_:path}')
async def https_redirect(request: Request):
    return RedirectResponse(request.url.replace(scheme='https'))

# uvicorn app.https_redirect:app --host 0.0.0.0 --port 80
if __name__ == '__main__':
    uvicorn.run('https_redirect:app', port=80, host='0.0.0.0')

