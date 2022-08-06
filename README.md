# Delivery-api

Este projeto consiste em uma API para um CRUD de pedidos, para serem salvos em um arquivo JSON. Foi utilizado FastAPI, Python e Docker.

## Como utilizar a api
### Primeiros passos

1 – Instalação do Docker na máquina
2 – Clonar ou baixar o repositório do github (https://github.com/Gabrielunb/teste-prog-api)
3 – Basta rodar o seguinte código “docker run --publish 8000:8000 gabriel:unb”, pois a imagem já está no Hub do Docker.
4 – Para facilitar a visualização e envio dos parâmetros é recomendável utilizar localhost:8000/docs
Informações
1. Faça o donwload e instalação do **Docker** na máquina.
2. Clonar ou baixar o repositório do github [RepoGIT](https://github.com/Gabrielunb/teste-prog-api).
3. Basta rodar o seguinte código 'docker run --publish 8000:8000 gabriel:unb', pois a imagem já está no Hub do **Docker**.
4. Para facilitar a visualização e envio dos parâmetros é recomendável utilizar 'localhost:8000/docs' Informações.

### Informações
#### Foram criadas 7 ENDPOINTS, toda a iteração com os pedidos são salvas no arquivo JSON na pasta do projeto.
1. localhost:8000  \
Endpoitn principal, mas não tem nada como retorna, apenas boas vindas
2. localhost: 8000/novo-pedido/ \
ele recebe um request body com os seguintes parâmetros:\
{ "cliente": "string", "produto": "string", "valor": 0, "entregue": true }
Trazendo como retorno um json do novo pedido com todas as informações.
3. localhost: 8000/apagar-pedido/ \
ele recebe um id para pesquisar o pedido e deleta ele, tendo como retorno sucesso ou falha caso o pedido não exista.\
{“id”: “int”}
4. localhost:8000/procurar-pedido/ \
Caso mande o parâmetro de retorna um pedido, caso mande sem parâmetro ele retorna todos os pedidos.\
{“id”: “int”}
5. localhost:8000/alterar-pedido/ \
Recebe como paramentros: \
{“id”: “int”, "cliente": "string", "produto": "string", "valor": 0, "entregue": true}
O id é para encontrar o pedido, o retorno desse pedido vai ser o pedido alterado
6. localhost:8000/alterar-pedido/ \
Recebe como paramentros: \
{“id”: “int”, "estado": "string}\
Ele verifica se o estado pode ser alterado para o desejado, sendo possível ele retorna o pedido com a alteração de estado, caso não seja possível ele retorna uma mensagem de erro.


### Observação importante
1. O arquivo "pedidos.json" na pasta pedidos contém todos os dados iniciais utilizados nesta api e todo CRUD ele irá utilizar este arquivo, importante está na pasta.
