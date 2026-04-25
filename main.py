from fastapi import FastAPI
from routers import clientes
from routers import pedidos
from routers import prendas
from routers import detalle_pedido

app = FastAPI()
app.include_router(clientes.router)
app.include_router(pedidos.router)
app.include_router(prendas.router)
app.include_router(detalle_pedido.router)