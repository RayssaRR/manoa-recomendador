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

O serviço fica disponível localmente em:

```text
http://localhost:3000
```

Mantenha esse terminal aberto enquanto testa os endpoints. Abra um segundo terminal PowerShell, ative o ambiente virtual e entre na pasta do projeto para executar as chamadas HTTP e os comandos de análise.

## Estrutura do projeto após a AV2

A estrutura abaixo apresenta a organização atual do repositório, incluindo os arquivos da AV1 e os componentes acrescentados para atender à AV2.

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

**Arquivos mantidos da AV1:**

- `src/catalogo.py`: mantém o catálogo fictício de produtos utilizado nas recomendações.
- `src/service.py`: implementa o serviço BentoML/FastAPI e os endpoints do módulo de recomendação.

**Arquivos adicionados para a AV2:**

- `src/data_access.py`: centraliza as funções de acesso ao catálogo e registra cada chamada no log.
- `src/resumo.py`: lê o arquivo JSONL e apresenta as estatísticas de utilização.
- `logs/acessos.jsonl`: armazena, em formato JSON Lines, o histórico de chamadas às funções de acesso.

`logs/acessos.jsonl` é criado automaticamente quando uma função de acesso registra sua primeira chamada. `src/__init__.py` identifica o diretório `src` como pacote Python.

## 2. Dicionário de dados

### 2.1. Fonte e versão dos dados

Os dados utilizados são mantidos localmente em `src/catalogo.py`. O catálogo contém 10 registros fictícios de produtos artesanais. Essa versão permite executar e repetir os testes sem depender de banco de dados ou serviço externo.

Não há dados pessoais de compradores, vendedores ou usuários reais.

### 2.2. Campos utilizados

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

### 2.3. Regra de seleção do Cold Start

A estratégia `COLD_START` não depende de histórico de navegação ou compra. Ela seleciona produtos que atendam simultaneamente aos critérios:

- `seloAutoriaCultural == true`;
- `stock > 0`.

Em seguida, o serviço ordena os produtos elegíveis pelo estoque em ordem decrescente e retorna até quatro recomendações.

### 2.4. Caso difícil previsto nos dados

O caso difícil utilizado na validação é a consulta ao identificador `999`, que não existe no catálogo. A função de busca deve retornar ausência de resultado, sem interromper o serviço, e registrar a ocorrência com status `not_found`.

Também foi executado um teste de regra de negócio: o estoque do produto de ID `7` foi temporariamente alterado de `20` para `0`. O produto deixou de aparecer no Cold Start. Após restaurar o estoque para `20`, voltou a aparecer.

### 2.5. Validação da alteração dos dados

Foi realizado um teste para verificar se o Cold Start consulta o catálogo atualizado, em vez de retornar uma lista fixa.

**Procedimento executado:**

1. O produto de ID `7` (`Colar de Miçangas Artesanal`) possuía estoque `20`.
2. O valor de `stock` desse produto foi temporariamente alterado para `0` em `src/catalogo.py`.
3. O serviço foi reiniciado e o endpoint de Cold Start foi chamado.
4. O produto de ID `7` deixou de aparecer, e a função retornou nove produtos elegíveis.
5. O estoque foi restaurado para `20`.
6. O serviço foi reiniciado e o endpoint foi chamado novamente.
7. O produto de ID `7` voltou a aparecer, e a função retornou dez produtos elegíveis antes da seleção das quatro recomendações finais.

**Registros observados no log:**

Durante a alteração:

```json
{
  "function": "get_cold_start_products",
  "caller": "/api/v1/recommendations/home",
  "recordsReturned": 9,
  "recordIds": [1, 2, 3, 4, 5, 6, 8, 9, 10],
  "status": "success"
}
```

Após a restauração:

```json
{
  "function": "get_cold_start_products",
  "caller": "/api/v1/recommendations/home",
  "recordsReturned": 10,
  "recordIds": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "status": "success"
}
```

**Resultado:** o teste confirmou que a função `get_cold_start_products` consulta o catálogo e aplica o critério `stock > 0`. A alteração dos dados modificou o conjunto de produtos retornados e foi registrada no arquivo JSONL.

## 3. Funções de acesso aos dados

O módulo de recomendação acessa o catálogo por meio das funções centralizadas em `src/data_access.py`. As rotas do serviço não devem percorrer o catálogo diretamente para realizar essas consultas.

| Função | Parâmetros | Responsabilidade | Retorno em caso sem resultado |
|---|---|---|---|
| `get_product_by_id(product_id, caller)` | ID do produto e rota chamadora | Busca um produto específico pelo identificador | Retorna `None` se o ID não existir |
| `get_recommendation_candidates(product_id, caller)` | ID do produto e rota chamadora | Recupera os produtos candidatos, excluindo o próprio produto consultado | Retorna uma lista vazia se não houver candidatos |
| `get_cold_start_products(caller)` | Rota chamadora | Recupera produtos com selo de autoria cultural e estoque disponível | Retorna uma lista vazia se não houver produtos elegíveis |

As funções registram suas chamadas por meio de `registrar_acesso()`, também definida em `src/data_access.py`.

### 3.1. Tratamento de resultados e erros

- Uma busca por produto inexistente é registrada como `not_found`, com zero registros retornados.
- Uma chamada executada normalmente é registrada como `success`.
- Uma exceção durante a execução é registrada como `error` e propagada novamente para que não seja ocultada.
- A função de candidatos exclui o produto de origem para evitar recomendá-lo a si mesmo.

### 3.2. Registro dos acessos

Cada chamada a uma função de acesso acrescenta uma linha ao arquivo:

```text
logs/acessos.jsonl
```

O arquivo utiliza o formato JSON Lines: cada linha é um objeto JSON independente. O registro é feito em modo de acréscimo (`a`), portanto as novas chamadas são adicionadas ao final do arquivo, sem sobrescrever o histórico.

Cada registro contém:

| Campo | Conteúdo |
|---|---|
| `timestamp` | Data e hora do acesso, com fuso horário |
| `function` | Nome da função de acesso chamada |
| `caller` | Rota que originou a chamada |
| `parameters` | Parâmetros resumidos, como o ID do produto |
| `recordsReturned` | Quantidade de registros retornados |
| `recordIds` | Identificadores dos produtos retornados |
| `status` | Resultado: `success`, `not_found` ou `error` |

Exemplo de chamada bem-sucedida:

```json
{
  "timestamp": "2026-11-26T10:21:29.793527-03:00",
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

Exemplo de consulta sem resultado:

```json
{
  "timestamp": "2026-11-26T10:21:38.958517-03:00",
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

## 4. Gerar o log — três chamadas reproduzíveis

Com o serviço em execução na porta `3000`, abra um segundo terminal PowerShell na raiz do projeto.

Execute as três chamadas abaixo, nesta ordem:

### Chamada 1 — Buscar recomendações para o produto 1

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/1"
```

Essa requisição aciona a busca do produto de origem e a recuperação dos candidatos à recomendação. Por isso, uma única requisição HTTP pode gerar mais de uma linha no log.

### Chamada 2 — Executar Cold Start

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/home?anonymousSessionId=teste-av2"
```

Essa requisição aciona `get_cold_start_products` e retorna até quatro produtos elegíveis.

### Chamada 3 — Consultar um produto inexistente

```powershell
curl.exe "http://localhost:3000/api/v1/recommendations/product/999"
```

Essa chamada exercita o caso difícil. A busca não encontra o produto e deve registrar `not_found`, com `recordsReturned` igual a `0` e `recordIds` vazio.

### 4.1. Conferir os registros gerados

Para visualizar as últimas linhas do arquivo:

```powershell
Get-Content .\logs\acessos.jsonl -Tail 10
```

Para contar as linhas registradas:

```powershell
(Get-Content .\logs\acessos.jsonl).Count
```

As chamadas são reproduzíveis. Ao executá-las novamente, novas linhas serão acrescentadas ao arquivo. O histórico anterior não deve ser apagado durante a validação.

## 5. Gerar e visualizar o resumo

O projeto possui o script `src/resumo.py`, que lê o arquivo JSONL e consolida as informações de acesso.

Na raiz do projeto, execute:

```powershell
python -m src.resumo
```

O resumo apresenta:

- total de chamadas registradas;
- total de erros técnicos (`status == "error"`);
- total de consultas sem resultado (`status == "not_found"` ou busca de produto com `recordsReturned == 0`);
- chamadas agrupadas por função;
- produtos mais presentes nos registros de retorno;
- produtos do catálogo que nunca apareceram em `recordIds`.

O script considera o histórico existente no arquivo. Portanto, os totais aumentam quando novas chamadas são executadas.

### 5.1. Como interpretar a contagem de produtos

A contagem de produtos é baseada nas ocorrências dos identificadores em `recordIds`. Uma função que retorna vários produtos contribui com uma ocorrência para cada identificador retornado.

Assim, a métrica representa a presença dos produtos nos resultados das funções de acesso, e não a quantidade de vezes que pessoas visualizaram ou clicaram nos produtos.

Registros antigos que não possuam o campo `recordIds` continuam sendo lidos; nesses casos, não há identificadores de produtos a contabilizar naquela linha.

## 6. Análise dos resultados — itens A, B e C

A execução mais recente do resumo, realizada em 26/11/2026, apresentou os seguintes resultados:

- **Total de chamadas:** 21.
- **Erros técnicos:** 0.
- **Consultas sem resultado:** 5.
- **Chamadas de `get_cold_start_products`:** 6.
- **Chamadas de `get_product_by_id`:** 10.
- **Chamadas de `get_recommendation_candidates`:** 5.
- **Produtos que nunca apareceram nos registros:** nenhum.

Na mesma execução, os produtos de IDs `1`, `2`, `3`, `4`, `5`, `6`, `8`, `9` e `10` tiveram seis ocorrências em `recordIds` cada. O produto de ID `7` teve cinco ocorrências.

> Os números documentam o histórico de acessos existente no momento da execução. Ao clonar o repositório e executar os testes, os totais poderão ser diferentes, pois dependem das chamadas registradas em `logs/acessos.jsonl`.

### A) Quais dados foram mais utilizados?

Na execução analisada, os produtos de IDs `1`, `2`, `3`, `4`, `5`, `6`, `8`, `9` e `10` foram os mais presentes nos registros, com seis ocorrências cada. O produto de ID `7` apresentou cinco ocorrências.

Entre as funções, `get_product_by_id` teve o maior número de chamadas, com dez, seguida por `get_cold_start_products`, com seis, e `get_recommendation_candidates`, com cinco.

Esses resultados demonstram que a busca por produto foi a função mais acionada durante os testes e que todos os produtos apareceram nos resultados das funções de acesso.

### B) Existem dados que nunca foram consultados? O que isso pode indicar?

Não. Os dez produtos do catálogo apareceram pelo menos uma vez nos registros analisados. Isso indica que, durante os testes realizados, todos os produtos foram contemplados pelos resultados das funções de acesso.

Essa informação não significa que todos tiveram a mesma relevância para a recomendação nem que foram visualizados por usuários, pois a métrica contabiliza a presença dos identificadores nos resultados das funções de acesso.

### C) Ocorreram erros? O que eles indicam?

Não foram registrados erros técnicos (`status: error`). Foram identificadas cinco consultas sem resultado, relacionadas à busca pelo identificador inexistente `999`.

Três dessas consultas já estavam registradas com o status `not_found`. Outras duas eram registros históricos que apresentavam `recordsReturned: 0`, mas estavam classificados anteriormente como `success`.

Para considerar corretamente o histórico, o script `resumo.py` foi ajustado para reconhecer também as buscas de produto com zero registros retornados. Assim, os cinco casos passaram a ser contabilizados como consultas sem resultado.

Isso demonstra que a função `get_product_by_id` trata a ausência de um produto de forma controlada: retorna `None`, registra zero resultados e permite que o serviço responda sem tratar a consulta inexistente como uma falha técnica.

## 7. Declaração de uso de IA generativa

A IA generativa foi utilizada como apoio durante o desenvolvimento e a documentação do trabalho, especialmente para discutir a organização das funções de acesso, o registro dos eventos, a geração do resumo e a revisão do README.

As sugestões foram analisadas e adaptadas ao código e aos requisitos do projeto. As alterações e os testes foram executados pela equipe, que conferiu as respostas dos endpoints e os registros produzidos. A IA foi utilizada como ferramenta de apoio, não como substituta da implementação, validação ou compreensão do funcionamento do sistema.

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

