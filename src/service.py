import time
import bentoml
from fastapi import FastAPI, Header
from src.catalogo import catalogo

app = FastAPI()

# Cache pré-computado para o fallback
fallback_cache = [
    {
        "productId": 3,
        "title": "Bolsa Artesanal de Palha",
        "category": "bolsas",
        "municipality": "Tracunhaém",
        "price": 109.90,
        "imageUrl": "https://example.com/bolsa-artesanal.jpg",
        "score": 1.0
    },
    {
        "productId": 9,
        "title": "Carteira de Palha",
        "category": "bolsas",
        "municipality": "Recife",
        "price": 69.90,
        "imageUrl": "https://example.com/carteira-palha.jpg",
        "score": 0.7
    },
    {
        "productId": 2,
        "title": "Cesto Decorativo de Palha",
        "category": "decoracao",
        "municipality": "Tracunhaém",
        "price": 59.90,
        "imageUrl": "https://example.com/cesto-palha.jpg",
        "score": 0.5
    },
    {
        "productId": 4,
        "title": "Chapéu de Palha Artesanal",
        "category": "acessorios",
        "municipality": "Tracunhaém",
        "price": 49.90,
        "imageUrl": "https://example.com/chapeu-palha.jpg",
        "score": 0.5
    }
]

@bentoml.service
@bentoml.asgi_app(app)
class ManoaService:

    @app.get("/api/v1/recommendations/product/{productId}")
    def recommend_product(self, productId: int, simulateTimeout: bool = False):
                # Simula uma consulta que ultrapassou o limite de 150 ms
        if simulateTimeout:
            time.sleep(0.16)

            return {
                "productId": productId,
                "strategy": "TIMEOUT_FALLBACK_CACHE",
                "fallbackUsed": True,
                "recommendations": fallback_cache
            }

        # Procura o produto solicitado
        produto_principal = next(
            (produto for produto in catalogo
             if produto["productId"] == productId),
            None
        )

        # Caso o produto não exista
        if produto_principal is None:
            return {
                "error": "Produto não encontrado"
            }

        # Calcula a similaridade de cada produto
        recomendacoes = []

        for produto in catalogo:

            # Não recomenda o próprio produto
            if produto["productId"] == productId:
                continue

            score = 0.0

            # Categoria = peso 0.5
            if produto["category"] == produto_principal["category"]:
                score += 0.5

            # Município = peso 0.3
            if produto["municipality"] == produto_principal["municipality"]:
                score += 0.3

            # Técnica = peso 0.2
            if produto["technique"] == produto_principal["technique"]:
                score += 0.2

            recomendacoes.append({
                "productId": produto["productId"],
                "title": produto["title"],
                "category": produto["category"],
                "municipality": produto["municipality"],
                "price": produto["price"],
                "imageUrl": produto["imageUrl"],
                "score": score
            })

        # Ordena do maior score para o menor
        recomendacoes.sort(
            key=lambda produto: produto["score"],
            reverse=True
        )

        # Retorna as 4 melhores recomendações
        return {
            "productId": productId,
            "strategy": "SAME_CATEGORY_AND_ORIGIN",
            "fallbackUsed": False,
            "recommendations": recomendacoes[:4]
        }

    @app.get("/api/v1/recommendations/home")
    def recommend_home(self, anonymousSessionId: str):

        # Seleciona produtos com autoria cultural e estoque disponível
        produtos_disponiveis = [
            produto for produto in catalogo
            if produto["seloAutoriaCultural"] is True
            and produto["stock"] > 0
        ]

        # Ordena pelo maior estoque
        produtos_disponiveis.sort(
            key=lambda produto: produto["stock"],
            reverse=True
        )

        # Retorna exatamente os 4 primeiros
        recomendacoes = produtos_disponiveis[:4]

        return {
            "anonymousSessionId": anonymousSessionId,
            "strategy": "COLD_START",
            "recommendations": recomendacoes
        }
    
    @app.put("/api/v1/recommendations/config")
    def update_config(
        self,
        strategyId: str,
        x_api_key: str = Header(None)
    ):

        # Chave administrativa simulada
        ADMIN_API_KEY = "manoa-admin-123"

        # Valida a chave de administrador
        if x_api_key != ADMIN_API_KEY:
            return {
                "error": "Não autorizado"
            }

        # Estratégias aceitas pelo mock
        estrategias_validas = [
            "SAME_CATEGORY_AND_ORIGIN",
            "COLD_START"
        ]

        # Valida a estratégia
        if strategyId not in estrategias_validas:
            return {
                "error": "strategyId inválido"
            }

        return {
            "strategyId": strategyId,
            "status": "ACTIVE",
            "message": "Estratégia atualizada com sucesso"
        }