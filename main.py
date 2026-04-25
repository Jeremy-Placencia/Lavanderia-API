from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clientes, pedidos, prendas, detalle_pedido
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://127.0.0.1:5500", "http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(pedidos.router)
app.include_router(prendas.router)
app.include_router(detalle_pedido.router)


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def frontend():
    return FileResponse("static/index.html")