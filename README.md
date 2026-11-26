# Manoa — Mock do Módulo de Recomendação

Mock do módulo de recomendação da plataforma **Manoa**, um marketplace de artesanato autêntico de Pernambuco.

O projeto foi desenvolvido inicialmente para a AV1 da disciplina de Inteligência Artificial e ampliado para a AV2. Na AV1, o serviço simulava as estratégias de recomendação. Na AV2, o módulo passou a consultar os dados por meio de funções de acesso centralizadas, registrar cada acesso em um arquivo JSONL e gerar um resumo de utilização.

O serviço utiliza Python, BentoML e FastAPI. O catálogo contém 10 produtos fictícios de artesanato pernambucano. Não são utilizados dados pessoais reais.


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
- BentoML
- FastAPI
- JSONL para registro dos acessos
- `collections.Counter` para consolidação das estatísticas

---

# AV2 — Dados, funções de acesso e rastreabilidade

## 1. Instalação e execução

### 1.1. Clonar o repositório

No Windows PowerShell:

```powershell
git clone https://github.com/RayssaRR/manoa-recomendador.git
cd manoa-recomendador
```

### 1.2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

### 1.3. Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação nesta sessão, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 1.4. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 1.5. Iniciar o serviço

Na raiz do projeto, com o ambiente virtual ativado:

```powershell
bentoml serve src/service.py
```

O serviço ficará disponível localmente em:

```text
http://localhost:3000
```

Mantenha esse terminal aberto enquanto realiza os testes. Abra um segundo terminal PowerShell, ative o ambiente virtual e entre na pasta do projeto para executar as chamadas HTTP e os comandos de análise.

## 2. Estrutura do projeto

A estrutura atual do repositório é:

```text
manoa-recomendador/
├── logs/
│   └── acessos.jsonl
├── src/
│   ├── __init__.py
│   ├── catalogo.py
│   ├── data_access.py
│   ├── resumo.py
│   └── service.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Arquivos do projeto

- `src/catalogo.py`: mantém o catálogo fictício de produtos utilizado nas recomendações.
- `src/service.py`: implementa o serviço BentoML/FastAPI e os endpoints do módulo de recomendação.
- `src/data_access.py`: centraliza as funções de acesso ao catálogo e registra cada chamada no log.
- `src/resumo.py`: lê o arquivo JSONL e apresenta as estatísticas de utilização.
- `logs/acessos.jsonl`: armazena, em formato JSON Lines, o histórico de chamadas às funções.
- `requirements.txt`: contém as dependências necessárias para executar o projeto.

O arquivo `logs/acessos.jsonl` é criado automaticamente quando uma função de acesso registra sua primeira chamada. O arquivo `src/__init__.py` identifica o diretório `src` como pacote Python.

## 3. Dicionário de dados

### 3.1. Fonte e versão dos dados

Os dados utilizados são mantidos localmente em `src/catalogo.py`.

O catálogo atual contém **11 registros fictícios de produtos artesanais**. Essa versão permite executar e repetir os testes sem depender de banco de dados ou serviço externo.

Não há dados pessoais de compradores, vendedores ou usuários reais.

### 3.2. Campos utilizados

| Campo | Tipo | Significado no negócio |
|---|---|---|
| `productId` | Inteiro | Identificador único do produto no catálogo |
| `title` | Texto | Nome comercial do produto |
| `category` | Texto | Categoria usada para agrupar produtos semelhantes |
| `municipality` | Texto | Município associado à produção ou origem artesanal |
| `technique` | Texto | Técnica artesanal utilizada na produção |
| `price` | Número | Preço fictício do produto |
| `imageUrl` | Texto (URL) | Endereço ilustrativo da imagem do produto |
| `seloAutoriaCultural` | Booleano | Indica se o produto possui o selo de autoria cultural |
| `stock` | Inteiro | Quantidade fictícia disponível em estoque |

### 3.3. Regra de seleção do Cold Start

A estratégia `COLD_START` não depende de histórico de navegação ou compra. Ela seleciona produtos que atendam simultaneamente aos seguintes critérios:

- `seloAutoriaCultural == true`;
- `stock > 0`.

Depois da filtragem, o serviço ordena os produtos elegíveis pelo estoque em ordem decrescente e retorna até quatro recomendações.

Na versão atual, existem nove produtos elegíveis.

### 3.4. Casos difíceis previstos nos dados

O projeto possui casos que permitem verificar o comportamento das funções de acesso e das regras de negócio:

- **Produto ID 999:** identificador inexistente no catálogo. A busca deve retornar ausência de resultado, sem interromper o serviço, e registrar o status `not_found`.
- **Produto ID 10:** não possui selo de autoria cultural (`seloAutoriaCultural == false`), portanto não deve ser selecionado no Cold Start.
- **Produto ID 11:** possui estoque igual a zero (`stock == 0`), portanto também não deve ser selecionado no Cold Start.

Esses casos permitem verificar tanto o tratamento de identificadores inexistentes quanto a aplicação dos critérios de elegibilidade.

### 3.5. Validação das regras de seleção

Foi realizada uma verificação direta do catálogo e dos critérios utilizados pelo Cold Start.

Resultado obtido:

```text
Total no catálogo: 11
Total elegível: 9
IDs elegíveis: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

O resultado confirma que os produtos de IDs 1 a 9 atendem aos critérios de selo e estoque disponível.

Os produtos 10 e 11 são excluídos por motivos diferentes: ausência do selo de autoria cultural e ausência de estoque, respectivamente.

## 4. Funções de acesso aos dados

O módulo de recomendação acessa o catálogo por meio das funções centralizadas em `src/data_access.py`.

As rotas do serviço utilizam essas funções para consultar os dados, evitando que cada endpoint implemente diretamente sua própria lógica de acesso ao catálogo.

### 4.1. Funções implementadas

| Função | Parâmetros | Responsabilidade |
|---|---|---|
| `get_product_by_id(product_id, caller)` | ID do produto e rota chamadora | Busca um produto específico pelo identificador |
| `get_recommendation_candidates(product_id, caller)` | ID do produto e rota chamadora | Recupera produtos candidatos, excluindo o próprio produto consultado |
| `get_cold_start_products(caller)` | Rota chamadora | Recupera produtos com selo de autoria cultural e estoque disponível |
| `get_fallback_products(product_ids, caller)` | Lista de IDs e rota chamadora | Recupera os produtos utilizados na estratégia de fallback |

### 4.2. Tratamento de resultados e erros

As funções tratam os resultados de acordo com o tipo de consulta:

- Uma busca por produto inexistente é registrada como `not_found`, com zero registros retornados.
- Uma chamada executada normalmente é registrada como `success`.
- Uma exceção durante a execução é registrada como `error` e propagada novamente.
- A função de candidatos exclui o produto de origem para evitar recomendá-lo a si mesmo.
- A função de Cold Start retorna somente produtos que atendem aos critérios de selo e estoque.
- A função de fallback recupera os produtos definidos para a estratégia alternativa.

Todas as funções registram seus acessos por meio de `registrar_acesso()`, também definida em `src/data_access.py`.

## 5. Registro dos acessos

Cada chamada a uma função de acesso acrescenta uma linha ao arquivo:

```text
logs/acessos.jsonl
```

O arquivo utiliza o formato JSON Lines: cada linha é um objeto JSON independente.

O registro é feito em modo de acréscimo (`a`), portanto as novas chamadas são adicionadas ao final do arquivo, sem sobrescrever o histórico.

### 5.1. Campos registrados

| Campo | Conteúdo |
|---|---|
| `timestamp` | Data e hora do acesso, com fuso horário |
| `function` | Nome da função de acesso chamada |
| `caller` | Rota que originou a chamada |
| `parameters` | Parâmetros resumidos, como o ID do produto |
| `recordsReturned` | Quantidade de registros retornados |
| `recordIds` | Identificadores dos produtos retornados |
| `status` | Resultado: `success`, `not_found` ou `error` |

### 5.2. Exemplo de chamada bem-sucedida

```json
{
  "timestamp": "2026-11-26T12:56:07.986396-03:00",
  "function": "get_product_by_id",
  "caller": "/api/v1/recommendations/product",
  "parameters": {
    "productId": 1
  },
  "recordsReturned": 1,
  "recordIds": [1],
  "status": "success"
}
```

### 5.3. Exemplo de consulta sem resultado

```json
{
  "timestamp": "2026-11-26T12:56:11.541606-03:00",
  "function": "get_product_by_id",
  "caller": "/api/v1/recommendations/product",
  "parameters": {
    "productId": 999
  },
  "recordsReturned": 0,
  "recordIds": [],
  "status": "not_found"
}
```

O campo `recordIds` permite identificar quais produtos foram retornados pelas funções de acesso. Ele não representa, por si só, visualizações, cliques ou compras de usuários.

## 6. Gerar o log — chamadas reproduzíveis

Com o serviço em execução na porta `3000`, abra um segundo terminal PowerShell na raiz do projeto.

Execute as quatro chamadas abaixo, nesta ordem, para exercitar as funções de acesso e o caso difícil.

### Chamada 1 — Buscar recomendações para o produto 1

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/1"
```

Essa requisição aciona duas funções:

- `get_product_by_id`: busca o produto de origem;
- `get_recommendation_candidates`: recupera os demais produtos do catálogo.

Por isso, uma única requisição HTTP gera duas linhas no log.

### Chamada 2 — Consultar um produto inexistente

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/999"
```

Essa chamada exercita o caso difícil. A busca não encontra o produto e deve registrar `not_found`, com `recordsReturned` igual a `0` e `recordIds` vazio.

### Chamada 3 — Executar Cold Start

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/home?anonymousSessionId=teste-final"
```

Essa requisição aciona `get_cold_start_products` e retorna até quatro produtos elegíveis, ordenados pelo estoque.

### Chamada 4 — Executar fallback simulado

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/1?simulateTimeout=true"
```

Essa chamada simula o cenário de timeout e aciona `get_fallback_products`, que recupera os produtos previamente definidos para a estratégia alternativa.

A resposta deve apresentar:

```json
{
  "strategy": "TIMEOUT_FALLBACK_CACHE",
  "fallbackUsed": true
}
```

**Observação:** o parâmetro `simulateTimeout=true` simula o comportamento de timeout para fins de demonstração. Ele não representa uma detecção automática de timeout em uma chamada externa real.

### 6.1. Conferir os registros gerados

Para visualizar o conteúdo do arquivo:

```powershell
Get-Content .\logs\acessos.jsonl
```

Para contar as linhas registradas:

```powershell
(Get-Content .\logs\acessos.jsonl).Count
```

As chamadas são reproduzíveis. Ao executá-las novamente, novas linhas serão acrescentadas ao arquivo. Para reproduzir os números da execução controlada documentada na seção 8, utilize um arquivo de log limpo antes de realizar os testes.

## 7. Gerar e visualizar o resumo

O projeto possui o script `src/resumo.py`, que lê o arquivo JSONL e consolida as informações de acesso.

Na raiz do projeto, execute:

```powershell
python -m src.resumo
```

O resumo apresenta:

- total de chamadas registradas;
- total de erros técnicos (`status == "error"`);
- total de consultas sem resultado (`status == "not_found"`);
- chamadas agrupadas por função;
- produtos mais consultados individualmente;
- produtos do catálogo que nunca foram consultados individualmente.

### 7.1. Como interpretar a contagem de produtos

A identificação dos produtos mais consultados individualmente considera exclusivamente os registros da função `get_product_by_id`, utilizando o identificador presente em `parameters.productId`.

As demais funções podem retornar vários produtos em `recordIds`, como ocorre na recuperação de candidatos, no Cold Start e no fallback. Entretanto, esses retornos não são contabilizados como consultas individuais aos produtos.

Assim, um produto pode participar de recomendações sem ter sido consultado diretamente pela função `get_product_by_id`.

Essa distinção evita interpretar a participação de um produto em uma lista de resultados como uma solicitação individual feita por um usuário.

## 8. Análise dos resultados — itens A, B e C

A execução controlada dos testes, realizada em 26/11/2026, gerou **cinco registros** no arquivo `logs/acessos.jsonl`, a partir de quatro requisições HTTP.

Os resultados consolidados foram:

- **Total de registros de acesso:** 5.
- **Erros técnicos:** 0.
- **Consultas sem resultado:** 1.
- **Chamadas de `get_product_by_id`:** 2.
- **Chamadas de `get_recommendation_candidates`:** 1.
- **Chamadas de `get_cold_start_products`:** 1.
- **Chamadas de `get_fallback_products`:** 1.
- **Produto mais consultado individualmente:** produto de ID 1, com uma consulta bem-sucedida.
- **Produtos nunca consultados individualmente:** IDs 2 a 11.

### A) Quais dados foram mais utilizados?

O produto de ID 1 foi o único produto do catálogo consultado individualmente com sucesso durante a execução controlada.

A função `get_product_by_id` foi acionada duas vezes: uma para o produto existente de ID 1 e outra para o identificador inexistente 999.

As demais funções foram acionadas uma vez cada. A função de candidatos retornou dez produtos, a função de Cold Start retornou nove produtos elegíveis e a função de fallback recuperou quatro produtos.

Esses números representam chamadas às funções e consultas individuais, não visualizações ou cliques de usuários.

### B) Existem dados que nunca foram consultados? O que isso pode indicar?

Sim. Os produtos de IDs 2 a 11 não foram consultados individualmente pela função `get_product_by_id` durante a execução controlada.

Isso indica que o conjunto de testes utilizou apenas o produto de ID 1 como produto de origem para a recomendação. Os outros produtos participaram dos resultados de candidatos, Cold Start ou fallback, mas isso não significa que tenham sido pesquisados individualmente.

A distinção é importante porque a presença de um produto em uma lista de recomendações não comprova que ele foi solicitado diretamente por um usuário.

### C) Ocorreram erros? O que eles indicam?

Não foram registrados erros técnicos, pois nenhuma função apresentou o status `error`.

Entretanto, ocorreu uma consulta sem resultado: a busca pelo identificador 999, que não existe no catálogo, foi registrada com o status `not_found`.

Esse comportamento demonstra que a função `get_product_by_id` trata a ausência de um produto de maneira controlada, retornando `None` e registrando zero resultados. Assim, uma consulta por identificador inexistente não precisa ser tratada como uma falha técnica do serviço.

## 9. Declaração de uso de IA generativa

A IA generativa foi utilizada como apoio durante o desenvolvimento e a documentação do trabalho, especialmente para discutir a organização das funções de acesso, o registro dos eventos, a geração do resumo e a revisão do README.

As sugestões foram analisadas e adaptadas ao código e aos requisitos do projeto. As alterações e os testes foram executados pela equipe, que conferiu as respostas dos endpoints e os registros produzidos.

A IA foi utilizada como ferramenta de apoio, não como substituta da implementação, validação ou compreensão do funcionamento do sistema.

---

---

# AV1 — Documentação do módulo de recomendação

Esta seção mantém a documentação funcional da primeira entrega. A AV1 definiu o comportamento esperado do mock de recomendação, incluindo as estratégias de recomendação por produto, Cold Start, configuração da estratégia e tratamento de timeout com fallback. A AV2 acrescenta a camada de acesso rastreável aos dados, sem substituir os comportamentos documentados nesta seção.

## Estrutura do projeto na AV1

Na primeira entrega, a estrutura do projeto era:

```text
manoa-recomendador/
├── src/
│   ├── catalogo.py
│   └── service.py
├── requirements.txt
├── README.md
└── .gitignore
```

A pasta `.venv/` é utilizada apenas localmente e está configurada no `.gitignore` para não ser enviada ao GitHub.

Na AV1:

- `src/catalogo.py` armazenava o catálogo sintético utilizado pelo mock.
- `src/service.py` implementava o serviço BentoML/FastAPI e os endpoints de recomendação.

Os arquivos `data_access.py`, `resumo.py`, `__init__.py` e a pasta `logs/` foram incorporados posteriormente, na evolução da AV2. A estrutura atual completa está documentada na seção AV2.

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

Os dados são exclusivamente sintéticos e não representam produtos ou usuários reais. O catálogo permite demonstrar as regras de recomendação sem depender de um banco de dados ou de serviços externos.

## Tecnologias utilizadas

- Python
- BentoML
- FastAPI

## Requisitos funcionais implementados

O mock implementa os quatro requisitos funcionais definidos para o módulo de recomendação na AV1.

| Requisito | Método | Endpoint | Estratégia/comportamento |
|---|---|---|---|
| RF-01 | GET | `/api/v1/recommendations/product/{productId}` | Recomenda produtos similares ao produto informado |
| RF-02 | GET | `/api/v1/recommendations/home` | Retorna recomendações para cenário de Cold Start |
| RF-03 | PUT | `/api/v1/recommendations/config` | Valida e simula a atualização da estratégia de recomendação |
| RF-04 | GET | `/api/v1/recommendations/product/{productId}?simulateTimeout=true` | Simula timeout e utiliza uma lista pré-computada de fallback |

## Detalhamento dos endpoints

### RF-01 — Recomendação por produto

**Endpoint:**

```http
GET /api/v1/recommendations/product/{productId}
```

O serviço recebe o identificador de um produto e calcula a similaridade dos demais produtos do catálogo. O próprio produto consultado não é incluído nas recomendações.

A pontuação considera três critérios:

| Critério | Peso |
|---|---:|
| Categoria | 0.5 |
| Município | 0.3 |
| Técnica | 0.2 |

A pontuação final é calculada a partir da combinação desses critérios. Produtos que compartilham mais características com o produto de origem tendem a receber um score maior.

A resposta retorna as quatro melhores recomendações ordenadas pelo score.

**Exemplo de chamada:**

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/1"
```

**Exemplo de resposta documentada na AV1:**

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

A resposta completa contém quatro recomendações. O exemplo acima apresenta parte da lista, conforme documentado na primeira versão do README.

### RF-02 — Cold Start

**Endpoint:**

```http
GET /api/v1/recommendations/home
```

Este endpoint simula o cenário em que não existe histórico de interação do usuário. Para identificar a sessão anônima, é necessário informar um `anonymousSessionId`.

O serviço seleciona produtos que atendam aos seguintes critérios:

- `seloAutoriaCultural = true`;
- `stock > 0`.

Na implementação atual, os produtos elegíveis são ordenados pelo estoque em ordem decrescente e o serviço retorna até quatro recomendações.

**Exemplo de chamada:**

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/home?anonymousSessionId=teste-123"
```

**Exemplo de resposta documentada:**

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

### RF-03 — Configuração da estratégia

**Endpoint:**

```http
PUT /api/v1/recommendations/config
```

O endpoint recebe um `strategyId` e utiliza uma chave de API administrativa simulada para validar a operação.

Estratégias aceitas pelo mock:

- `SAME_CATEGORY_AND_ORIGIN`
- `COLD_START`

**Exemplo de chamada:**

```powershell
curl.exe -X PUT "http://localhost:3000/api/v1/recommendations/config?strategyId=COLD_START" -H "X-Api-Key: manoa-admin-123"
```

**Resposta esperada:**

```json
{
  "strategyId": "COLD_START",
  "status": "ACTIVE",
  "message": "Estratégia atualizada com sucesso"
}
```

A configuração é simulada no mock e não utiliza um banco de dados ou serviço externo de configuração.

### RF-04 — Timeout e fallback

**Endpoint:**

```http
GET /api/v1/recommendations/product/{productId}?simulateTimeout=true
```

O parâmetro `simulateTimeout=true` permite simular um cenário de timeout para fins de teste.

Quando esse parâmetro é utilizado, o serviço simula a demora da consulta e retorna uma lista pré-computada de recomendações de fallback. Dessa forma, o mock demonstra uma alternativa de resposta quando a consulta principal não pode ser concluída dentro do fluxo simulado.

A resposta identifica que o fallback foi utilizado por meio do campo:

```json
"fallbackUsed": true
```

E utiliza a estratégia:

```text
TIMEOUT_FALLBACK_CACHE
```

**Exemplo de chamada:**

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/1?simulateTimeout=true"
```

**Exemplo de resposta documentada:**

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

## Casos de teste da AV1

Os testes abaixo foram documentados para execução com o serviço rodando localmente na porta `3000`.

### Caso de teste 1 — RF-01: recomendação por produto

**Objetivo:** verificar se o serviço retorna recomendações de produtos similares ao produto informado.

**Comando:**

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/1"
```

**Resultado esperado:**

- Retorno HTTP com as recomendações.
- Estratégia `SAME_CATEGORY_AND_ORIGIN`.
- `fallbackUsed` igual a `false`.
- Quatro produtos recomendados.
- Produtos ordenados pelo score de similaridade.
- O produto consultado não aparece na lista de recomendações.

**Resultado obtido documentado:**

```text
productId: 1
strategy: SAME_CATEGORY_AND_ORIGIN
fallbackUsed: false
```

Pontuações observadas:

```text
Produto 3 → 1.0
Produto 9 → 0.7
Produto 2 → 0.5
Produto 4 → 0.5
```

### Caso de teste 2 — RF-02: Cold Start

**Objetivo:** verificar o comportamento de Cold Start.

**Comando:**

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/home?anonymousSessionId=teste-123"
```

**Resultado esperado:**

- Estratégia `COLD_START`.
- Quatro produtos recomendados.
- Todos os produtos com `seloAutoriaCultural = true`.
- Todos os produtos com estoque disponível.
- Recomendações ordenadas pelo estoque.

**Resultado obtido documentado:**

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

### Caso de teste 3 — RF-03: configuração da estratégia

**Objetivo:** verificar a validação da chave administrativa e do identificador de estratégia.

**Comando:**

```powershell
curl.exe -X PUT "http://localhost:3000/api/v1/recommendations/config?strategyId=COLD_START" -H "X-Api-Key: manoa-admin-123"
```

**Resultado esperado:**

```json
{
  "strategyId": "COLD_START",
  "status": "ACTIVE",
  "message": "Estratégia atualizada com sucesso"
}
```

**Resultado obtido documentado:**

A resposta retornada pelo serviço foi:

```json
{
  "strategyId": "COLD_START",
  "status": "ACTIVE",
  "message": "Estratégia atualizada com sucesso"
}
```

### Caso de teste 4 — RF-04: timeout e fallback

**Objetivo:** verificar o comportamento de fallback em uma situação de timeout simulada.

**Comando:**

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/1?simulateTimeout=true"
```

**Resultado esperado:**

- Estratégia `TIMEOUT_FALLBACK_CACHE`.
- `fallbackUsed` igual a `true`.
- Retorno da lista pré-computada de fallback.

**Resultado obtido documentado:**

```text
productId: 1
strategy: TIMEOUT_FALLBACK_CACHE
fallbackUsed: true
```

A lista de fallback foi retornada corretamente.

## Resumo dos testes da AV1

| Caso | Requisito | Resultado documentado |
|---|---|---|
| 1 | RF-01 | Aprovado |
| 2 | RF-02 | Aprovado |
| 3 | RF-03 | Aprovado |
| 4 | RF-04 | Aprovado |

## Observações sobre o mock

Este projeto tem como objetivo representar o contrato de entrada e saída do módulo de recomendação definido na AV1.

Por se tratar de um mock:

- o catálogo utilizado é sintético;
- não existe banco de dados real;
- não são utilizados dados reais de usuários;
- as funções internas podem ser simplificadas ou simuladas;
- o fallback utiliza uma lista pré-computada local;
- a atualização de configuração é simulada;
- o parâmetro `simulateTimeout` existe exclusivamente para possibilitar a demonstração e o teste do comportamento de fallback.

O foco da AV1 é demonstrar que o módulo pode ser executado localmente e que suas interfaces respondem conforme os requisitos funcionais especificados.

## Execução rápida da AV1

Depois de clonar o projeto, os comandos básicos para preparar e executar o serviço são:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
bentoml serve src/service.py
```

Em outro terminal, com o serviço em execução:

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/1"
```

Se uma resposta JSON for retornada, o mock está respondendo à chamada.

