from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json, os

CONFIG_PATH = "/app/data/mock-config.json"
app = FastAPI(title="Mocker UI")

templates = Jinja2Templates(directory = "templates")

#Load config
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        config = json.load(f)
else:
    config = {"endpoints":[]}

def register_endpoint(ep):
    async def handler():
        return ep["response"]["body"]
    app.add_api_route(ep["path"], handler, methods=[ep["method"]])

# Register existing endpoints
for ep in config["endpoints"]:
    register_endpoint(ep)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html",{"request":request, "endpoints": config["endpoints"]})

@app.post("/add")
async def add_mock(method: str = Form(...), path: str = Form(...), body: str = Form(...)):
    ep = {"method": method, "path": path, "response": {"status": 200, "body": {"message": body}}}
    config["endpoints"].append(ep)
    register_endpoint(ep)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    return RedirectResponse("/", status_code=303)

# Admin API for programmatic updates
@app.post("/__admin/mappings")
async def add_mapping(ep: dict):
    config["endpoints"].append(ep)
    register_endpoint(ep)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    return {"status": "added", "endpoint": ep}