from fastapi import FastAPI, Path, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, AnyHttpUrl
from db_ops import insert_value, get_long_url

### Models

class HttpURL(BaseModel):
    url: AnyHttpUrl

### App related configs

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

### Path definitions and functions

@app.get('/', response_class=HTMLResponse)
def getRoot(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/api/v1/create/')
def createUrl(long_url: HttpURL):
    short_url = insert_value(long_url.url)
    return {'short_url': short_url}


@app.get('/{short_url}')
def urlFetch(short_url: str = Path(
        description='Short URL path',
        pattern='^[a-zA-Z0-9]{5}$'
        ), info: bool = False
    ):
    long_url, c_date = get_long_url(short_url)
    if info:
        return {"short_url":short_url, "long_url": long_url, "c_date": c_date.strftime("%Y-%m-%d %H:%M:%S")}
    return RedirectResponse(long_url)
