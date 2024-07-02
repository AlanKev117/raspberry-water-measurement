from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .handlers.handlers import SensorHandlers

from .tools.misc import initialize_sensor

sensor = initialize_sensor()
handlers = SensorHandlers(sensor)
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/cli")
async def cli():
    return handlers.get_minimal_data()

@app.get("/", response_class=HTMLResponse)
async def web(request: Request):
    data = handlers.get_minimal_data()
    level = data["level"]
    return templates.TemplateResponse(
        request=request, name="level.html", context={"level": level}
    )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")