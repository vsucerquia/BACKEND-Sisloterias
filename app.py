from fastapi import FastAPI
from endpoints import (
    jugadores_router,
    juegos_router,
    sorteos_router,
    boletos_router,
    premios_router,
    pagos_router,
)

app = FastAPI(
    title="API Sistema de Lotería",
    version="1.0.0"
)

app.include_router(jugadores_router.router)
app.include_router(juegos_router.router)
app.include_router(sorteos_router.router)
app.include_router(boletos_router.router)
app.include_router(premios_router.router)
app.include_router(pagos_router.router)


@app.get("/")
def root():
    return {"message": "API Lotería funcionando"}