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
        else:
            return {"Busca": "Pedido não encontrado"}

@app.get("/")
def hello_root():
    return

# Rotas
# Novo pedido
@app.post("/novo-pedido/")
async def novoPedido(pedidoObjs:Pedidos):
    temp = pedidos['pedidos']
    if pedidoObjs.valor < 0:
        return {"Error": "Valor do pedido NEGATIVO"}
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


# Deletar pedido
@app.delete("/apagar-pedido/{id}")
async def deletarPedido(id:int):
    pedidoDelete = BuscaPedido(id)
    print('Retorno', pedidoDelete)
    if pedidoDelete != None:
        index = pedidos['pedidos'].index(pedidoDelete)
        del pedidos['pedidos'][index]
        AbrirSalvarArquivo(pedidos)
        return {"Pedido Deletado":"success"}
    else:
        return {"Pedido Deletado": "Pedido não existe"}

# Procuro pedido pelo id
@app.get("/procurar-pedido/{id}")
async def procuraPedido(id: int):
    if BuscaPedido(id) == None:
        return {"Busca": "Pedido não encontrado"}
    return BuscaPedido(id)


# Retorno todos os pediso
@app.get("/procurar-pedido/")
async def procuraTodosPedidos():
    return pedidos['pedidos']

# Altero o pedido
@app.put("/alterar-pedido/{id}")
async def alterarPedido(id: int,pedidoObjs:Pedidos):
    pedidoAlterar = BuscaPedido(id)
    if pedidoAlterar == None:
        return {"Busca": "Pedido não encontrado"}

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


# Altero o estado do pedido
@app.put("/estado-pedido/{id}/{estado}")
async def estadoPedido(id: int, estado: str):
    pedidoAlterar = BuscaPedido(id)

    if pedidoAlterar == None:
        return {"Busca": "Pedido não encontrado"}

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
    # Verifico se pode ter mudança no estado do pedido
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