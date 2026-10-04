# Manoa — Mock do Módulo de Recomendação


Mock do módulo de recomendação da plataforma Manoa, marketplace de artesanato autêntico de Pernambuco.


Este projeto foi desenvolvido para a AV2 da disciplina de Inteligência Artificial e simula o funcionamento do módulo de recomendação definido na AV1.


O serviço utiliza BentoML e FastAPI, com um catálogo de produtos sintético e sem utilização de dados reais.


## Integrantes

<table width="100%">
  <tr>
    <td align="center" width="33%">
      <a href="https://github.com/emanoelhenrick">
        <img src="https://github.com/emanoelhenrick.png" width="90px" style="border-radius:50%;" alt="Emanoel Henrick"/><br />
        <b>Emanoel Henrick</b>
      </a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/jenniferzeferino">
        <img src="https://github.com/jenniferzeferino.png" width="90px" style="border-radius:50%;" alt="Jennifer Zeferino"/><br />
        <b>Jennifer Zeferino</b>
      </a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/RaieleLeite">
        <img src="https://github.com/RaieleLeite.png" width="90px" style="border-radius:50%;" alt="Raiele Leite"/><br />
        <b>Raiele Leite</b>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center" width="33%">
      <a href="https://github.com/RayssaRR">
        <img src="https://github.com/RayssaRR.png" width="90px" style="border-radius:50%;" alt="Rayssa Santana"/><br />
        <b>Rayssa Santana</b>
      </a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/FelipeLV12">
        <img src="https://github.com/FelipeLV12.png" width="90px" style="border-radius:50%;" alt="Felipe Lopes"/><br />
        <b>Felipe Lopes</b>
      </a>
    </td>
    <td align="center" width="33%">
      <a href="https://github.com/injuje">
        <img src="https://github.com/injuje.png" width="90px" style="border-radius:50%;" alt="José Leandro"/><br />
        <b>José Leandro</b>
      </a>
    </td>
  </tr>
</table>


---


## Tecnologias


- Python

- BentoML 1.4.39

- FastAPI 0.142.2


---


## Estrutura do projeto


```text

manoa-recomendador/

├── src/

│   ├── catalogo.py

│   └── service.py

├── requirements.txt

├── README.md

└── .gitignore

```


---


## Catálogo sintético


O mock utiliza um catálogo local com **10 produtos fictícios** de artesanato pernambucano.


Cada produto possui informações como:


- `productId`

- `title`

- `category`

- `municipality`

- `technique`

- `price`

- `imageUrl`

- `seloAutoriaCultural`

- `stock`


Os dados são exclusivamente sintéticos e não representam produtos ou usuários reais.


---


# Instalação


## 1. Clonar o repositório


```powershell

git clone <URL_DO_REPOSITORIO>

cd manoa-recomendador

```


## 2. Criar o ambiente virtual


No Windows PowerShell:


```powershell

python -m venv .venv

```


## 3. Ativar o ambiente virtual


```powershell

.\.venv\Scripts\Activate.ps1

```


Após a ativação, o terminal deverá apresentar algo semelhante a:


```text

(.venv) PS C:\...\manoa-recomendador>

```


## 4. Instalar as dependências


```powershell

pip install -r requirements.txt

```


---


# Execução


Com o ambiente virtual ativado, execute:


```powershell

bentoml serve src/service.py

```


O serviço será disponibilizado localmente em:


```text

http\://localhost:3000

```


O terminal deverá indicar que o serviço está escutando na porta `3000`.


---


# Requisitos Funcionais Implementados


O mock implementa os quatro requisitos funcionais definidos para o módulo de recomendação na AV1.


| Requisito | Método | Endpoint | Estratégia/Comportamento |

|---|---|---|---|

| RF-01 | GET | `/api/v1/recommendations/product/{productId}` | Recomenda produtos similares ao produto informado |

| RF-02 | GET | `/api/v1/recommendations/home` | Retorna recomendações para cenário de Cold Start |

| RF-03 | PUT | `/api/v1/recommendations/config` | Valida e simula a atualização da estratégia de recomendação |

| RF-04 | GET | `/api/v1/recommendations/product/{productId}?simulateTimeout=true` | Simula timeout e utiliza uma lista pré-computada de fallback |


---


# Detalhamento dos endpoints


## RF-01 — Recomendação por produto


### Endpoint


```http

GET /api/v1/recommendations/product/{productId}

```


O serviço recebe o identificador de um produto e calcula a similaridade dos demais produtos do catálogo.


A pontuação considera:


| Critério | Peso |

|---|---:|

| Categoria | 0.5 |

| Município | 0.3 |

| Técnica | 0.2 |


O próprio produto consultado não é incluído nas recomendações.


A resposta retorna as quatro melhores recomendações ordenadas pelo score.


### Exemplo


```powershell

curl.exe "http\://localhost:3000/api/v1/recommendations/product/1"

```


### Resposta esperada


```json

{

  "productId": 1,

  "strategy": "SAME_CATEGORY_AND_ORIGIN",

  "fallbackUsed": false,

  "recommendations": [

    {

      "productId": 3,

      "title": "Bolsa Artesanal de Palha",

      "category": "bolsas",

      "municipality": "Tracunhaém",

      "price": 109.9,

      "imageUrl": "https://example.com/bolsa-artesanal.jpg",

      "score": 1.0

    },

    {

      "productId": 9,

      "title": "Carteira de Palha",

      "category": "bolsas",

      "municipality": "Recife",

      "price": 69.9,

      "imageUrl": "https://example.com/carteira-palha.jpg",

      "score": 0.7

    }

  ]

}

```


A resposta completa contém quatro recomendações.


---


## RF-02 — Cold Start


### Endpoint


```http

GET /api/v1/recommendations/home

```


Este endpoint simula o cenário em que não existe histórico de interação do usuário.


É necessário informar um `anonymousSessionId`.


O serviço seleciona produtos que:


- possuem `seloAutoriaCultural = true`;

- possuem `stock > 0`.


São retornados exatamente quatro produtos.


### Exemplo


```powershell

curl.exe "http\://localhost:3000/api/v1/recommendations/home?anonymousSessionId=teste-123"

```


### Resposta esperada


```json

{

  "anonymousSessionId": "teste-123",

  "strategy": "COLD_START",

  "recommendations": [

    {

      "productId": 7,

      "title": "Colar de Miçangas Artesanal",

      "stock": 20

    },

    {

      "productId": 6,

      "title": "Boneca de Barro",

      "stock": 15

    },

    {

      "productId": 2,

      "title": "Cesto Decorativo de Palha",

      "stock": 12

    },

    {

      "productId": 4,

      "title": "Chapéu de Palha Artesanal",

      "stock": 10

    }

  ]

}

```


Os demais atributos dos produtos também são retornados pelo serviço.


---


## RF-03 — Configuração da estratégia


### Endpoint


```http

PUT /api/v1/recommendations/config

```


O endpoint recebe um `strategyId` e utiliza uma chave de API administrativa simulada.


Estratégias aceitas pelo mock:


- `SAME_CATEGORY_AND_ORIGIN`

- `COLD_START`


### Exemplo


```powershell

curl.exe -X PUT "http\://localhost:3000/api/v1/recommendations/config?strategyId=COLD_START" -H "X-Api-Key: manoa-admin-123"

```


### Resposta esperada


```json

{

  "strategyId": "COLD_START",

  "status": "ACTIVE",

  "message": "Estratégia atualizada com sucesso"

}

```


A configuração é simulada no mock e não utiliza um banco de dados ou serviço externo de configuração.


---


## RF-04 — Timeout e fallback


### Endpoint


```http

GET /api/v1/recommendations/product/{productId}?simulateTimeout=true

```


O parâmetro `simulateTimeout=true` permite simular um cenário de timeout para fins de teste.


Quando esse parâmetro é utilizado, o serviço simula a demora da consulta e retorna uma lista pré-computada de recomendações de fallback.


A resposta identifica que o fallback foi utilizado através de:


```json

"fallbackUsed": true

```


e utiliza a estratégia:


```text

TIMEOUT_FALLBACK_CACHE

```


### Exemplo


```powershell

curl.exe "http\://localhost:3000/api/v1/recommendations/product/1?simulateTimeout=true"

```


### Resposta esperada


```json

{

  "productId": 1,

  "strategy": "TIMEOUT_FALLBACK_CACHE",

  "fallbackUsed": true,

  "recommendations": [

    {

      "productId": 3,

      "title": "Bolsa Artesanal de Palha",

      "score": 1.0

    },

    {

      "productId": 9,

      "title": "Carteira de Palha",

      "score": 0.7

    },

    {

      "productId": 2,

      "title": "Cesto Decorativo de Palha",

      "score": 0.5

    },

    {

      "productId": 4,

      "title": "Chapéu de Palha Artesanal",

      "score": 0.5

    }

  ]

}

```


---


# Casos de teste


Os testes abaixo foram executados com o serviço rodando localmente na porta `3000`.


## Caso de teste 1 — RF-01


### Objetivo


Verificar se o serviço retorna recomendações de produtos similares ao produto informado.


### Comando


```powershell

curl.exe "http\://localhost:3000/api/v1/recommendations/product/1"

```


### Resultado esperado


- Retorno HTTP com as recomendações.

- Estratégia `SAME_CATEGORY_AND_ORIGIN`.

- `fallbackUsed` igual a `false`.

- Quatro produtos recomendados.

- Produtos ordenados pelo score de similaridade.

- O produto consultado não aparece na lista de recomendações.


### Resultado obtido


```text

productId: 1

strategy: SAME_CATEGORY_AND_ORIGIN

fallbackUsed: false

```


As pontuações observadas foram:


```text

Produto 3 → 1.0

Produto 9 → 0.7

Produto 2 → 0.5

Produto 4 → 0.5

```


---


## Caso de teste 2 — RF-02


### Objetivo


Verificar o comportamento de Cold Start.


### Comando


```powershell

curl.exe "http\://localhost:3000/api/v1/recommendations/home?anonymousSessionId=teste-123"

```


### Resultado esperado


- Estratégia `COLD_START`.

- Exatamente quatro produtos.

- Todos os produtos com `seloAutoriaCultural = true`.

- Todos os produtos com estoque disponível.

- Recomendações ordenadas pelo estoque.


### Resultado obtido


```text

strategy: COLD_START

quantidade: 4 produtos

```


Produtos retornados:


```text

Produto 7 → estoque 20

Produto 6 → estoque 15

Produto 2 → estoque 12

Produto 4 → estoque 10

```


---


## Caso de teste 3 — RF-03


### Objetivo


Verificar a validação da chave administrativa e do identificador de estratégia.


### Comando


```powershell

curl.exe -X PUT "http\://localhost:3000/api/v1/recommendations/config?strategyId=COLD_START" -H "X-Api-Key: manoa-admin-123"

```


### Resultado esperado


```json

{

  "strategyId": "COLD_START",

  "status": "ACTIVE",

  "message": "Estratégia atualizada com sucesso"

}

```


### Resultado obtido


A resposta retornada pelo serviço foi:


```json

{

  "strategyId": "COLD_START",

  "status": "ACTIVE",

  "message": "Estratégia atualizada com sucesso"

}

```


---


## Caso de teste 4 — RF-04


### Objetivo


Verificar o comportamento de fallback em uma situação de timeout simulada.


### Comando


```powershell

curl.exe "http\://localhost:3000/api/v1/recommendations/product/1?simulateTimeout=true"

```


### Resultado esperado


- Estratégia `TIMEOUT_FALLBACK_CACHE`.

- `fallbackUsed` igual a `true`.

- Retorno da lista pré-computada de fallback.


### Resultado obtido


```text

productId: 1

strategy: TIMEOUT_FALLBACK_CACHE

fallbackUsed: true

```


A lista de fallback foi retornada corretamente.


---


# Resumo dos testes


| Caso | RF | Resultado |

|---|---|---|

| 1 | RF-01 | ✅ Aprovado |

| 2 | RF-02 | ✅ Aprovado |

| 3 | RF-03 | ✅ Aprovado |

| 4 | RF-04 | ✅ Aprovado |


---


# Observações sobre o Mock


Este projeto tem como objetivo representar o **contrato de entrada e saída do módulo de recomendação** definido na AV1.


Por se tratar de um mock:


- o catálogo utilizado é sintético;

- não existe banco de dados real;

- não são utilizados dados reais de usuários;

- as funções internas podem ser simplificadas ou simuladas;

- o fallback utiliza uma lista pré-computada local;

- a atualização de configuração é simulada;

- o parâmetro `simulateTimeout` existe exclusivamente para possibilitar a demonstração e o teste do comportamento de fallback.


O foco do projeto é demonstrar que o módulo pode ser executado localmente e que suas interfaces respondem conforme os requisitos funcionais especificados.


---


# Execução rápida


Depois de clonar o projeto:


```powershell

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

bentoml serve src/service.py

```


Em outro terminal, com o serviço em execução:


```powershell

curl.exe "http\://localhost:3000/api/v1/recommendations/product/1"

```


Se uma resposta JSON for retornada, o mock está funcionando corretamente.


---


# Status do projeto


**Mock do módulo de recomendação concluído e testado localmente.**


Requisitos funcionais implementados:


- [x] RF-01 — Recomendação por produto

- [x] RF-02 — Cold Start

- [x] RF-03 — Configuração de estratégia

- [x] RF-04 — Timeout/Fallback

- [x] Catálogo sintético

- [x] Instalação documentada

- [x] Execução local documentada

- [x] Mapeamento dos RFs para endpoints

- [x] Casos de teste documentados
