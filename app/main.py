from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import json
import datetime


# Iniciando o FastAPI
app = FastAPI()

# Criando os status dos pedidospip
class StatusPedido(str, Enum):
    RECEIVED = "RECEIVED"
    CONFIRMED = "CONFIRMED"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"

# Criando uma basemodel de pedidos
class Pedidos(BaseModel):
        cliente: str
        produto: str
        valor: float
        entregue: bool


# Abrindo o arquivo e deixando ele na memória
with open('pedidos.json', encoding='utf8') as json_file:
    pedidos = json.load(json_file)


# Abrindo o arquivo novamente e escrevendo nele
def AbrirSalvarArquivo(pedido, filename='pedidos.json'):
    with open(filename, 'w', encoding='utf8') as json_file:
        json.dump(pedido, json_file, ensure_ascii=False, indent=2)
        json_file.close()


# Função para gerar o próximo id
def GeraId():
    novoId = pedidos['nextId']
    pedidos['nextId'] = pedidos['nextId'] + 1
    return novoId


# Função para buscar o pedido
def BuscaPedido(id: int):
    for pedido in pedidos['pedidos']:
        if pedido != None:
            if pedido.get('id') == id:
                return pedido


# Rotas
@app.post("/novo-pedido/")
async def novoPedido(pedidoObjs:Pedidos):
    temp = pedidos['pedidos']
    pedidoNovo = {
        "id": GeraId(),
        "cliente": pedidoObjs.cliente,
        "produto": pedidoObjs.produto,
        "valor": pedidoObjs.valor,
        "entregue": pedidoObjs.entregue,
        "estado": StatusPedido.RECEIVED.value,
        "timestamp": f'{datetime.datetime.now().isoformat()[:-3]}Z'
    }
    temp.append(pedidoNovo)
    AbrirSalvarArquivo(pedidos)

    return {"Pedido Criado": pedidoNovo}


@app.delete("/apagar-pedido/{id}")
async def deletarPedido(id:int):
    pedidoDelete = BuscaPedido(id)
    index = pedidos['pedidos'].index(pedidoDelete)
    del pedidos['pedidos'][index]
    AbrirSalvarArquivo(pedidos)
    return "Error"


@app.get("/procurar-pedido/{id}")
async def procuraPedido(id: int):
    return BuscaPedido(id)


@app.get("/procurar-pedido/")
async def procuraTodosPedidos():
    return pedidos['pedidos']


@app.put("/alterar-pedido/{id}")
async def alterarPedido(id: int,pedidoObjs:Pedidos):
    pedidoAlterar = BuscaPedido(id)
    index = pedidos['pedidos'].index(pedidoAlterar)
    pedidoAlterado = {
        "id": pedidoAlterar['id'],
        "cliente": pedidoObjs.cliente,
        "produto": pedidoObjs.produto,
        "valor": pedidoObjs.valor,
        "entregue": pedidoObjs.entregue,
        "estado": pedidoAlterar['estado'],
        "timestamp": pedidoAlterar['timestamp']
    }
    pedidos['pedidos'][index] = pedidoAlterado
    AbrirSalvarArquivo(pedidos)

    return {"Pedidos Alterado": pedidoAlterado}


@app.put("/estado-pedido/{id}/{estado}")
async def estadoPedido(id: int, estado: str):
    pedidoAlterar = BuscaPedido(id)

    estadoAtual = pedidoAlterar['estado']
    novoEstado = False

    # "Pode ir CONFIRMED ou CANCELED"
    if estado in StatusPedido.__members__.values():

        # "Pode ir CONFIRMED ou CANCELED"
        if estadoAtual == StatusPedido.RECEIVED:
            if estado == StatusPedido.CONFIRMED:
                novoEstado = StatusPedido.CONFIRMED.value
            elif estado == StatusPedido.CANCELED:
                novoEstado = StatusPedido.CANCELED.value

        # "Pode ir DESPACHED ou CANCELED")
        elif estadoAtual == StatusPedido.CONFIRMED:
            if estado == StatusPedido.DISPATCHED:
                novoEstado = StatusPedido.DISPATCHED.value
            elif estado == StatusPedido.CANCELED:
                novoEstado = StatusPedido.CANCELED.value

        # "Pode ir DELIVERED ou CANCELED"
        elif estadoAtual == StatusPedido.DISPATCHED:
            if estado == StatusPedido.DELIVERED:
                novoEstado = StatusPedido.DELIVERED.value
            elif estado == StatusPedido.CANCELED:
                novoEstado = StatusPedido.CANCELED.value

    if novoEstado == False:
        return {"Error": "O pedido não pode ser alterado de " + estadoAtual + " para " + estado}

    indexPedido = index = pedidos['pedidos'].index(pedidoAlterar)

    pedidoAlterado = {
        "id": pedidoAlterar['id'],
        "cliente": pedidoAlterar['cliente'],
        "produto": pedidoAlterar['produto'],
        "valor": pedidoAlterar['valor'],
        "entregue": pedidoAlterar['entregue'],
        "estado": novoEstado,
        "timestamp": pedidoAlterar['timestamp']
    }
    pedidos['pedidos'][index] = pedidoAlterado
    AbrirSalvarArquivo(pedidos)

    return {"Estado Alterado": pedidoAlterado}

