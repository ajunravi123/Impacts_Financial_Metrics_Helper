from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from services.workflow import Workflow

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
workflow = Workflow()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.get("/analyze/{input_str}")
async def analyze_company(input_str: str):
    result = workflow.analyze(input_str)
    return result