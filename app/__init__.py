from fastapi import FastAPI


app = FastAPI(
    title="Aeon API",
    description="REST API for Aeon Bot",
)


@app.get("/")
async def root() -> dict:
    return { "msg": "OK!" }