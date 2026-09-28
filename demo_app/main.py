from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Casewake checkout demo")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return "<main><h1>Checkout demo</h1></main>"
