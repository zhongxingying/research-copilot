from fastapi import FastAPI

app = FastAPI(title="Research Copilot")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
