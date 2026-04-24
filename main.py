from fastapi import FastAPI
from routers import clientes
from routers import pedidos
from routers import prendas

app = FastAPI()
app.include_router(clientes.router)
app.include_router(pedidos.router)
app.include_router(prendas.router)