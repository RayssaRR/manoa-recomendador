
import os
import time

import bentoml
from fastapi import FastAPI, Header, HTTPException

from src.data_access import (
    get_product_by_id,
    get_recommendation_candidates,
    get_cold_start_products,
    get_fallback_products
)

app = FastAPI()


# Configuração do fallback:
# IDs dos produtos e suas respectivas pontuações.
# Os dados dos produtos são recuperados pela camada de acesso.
FALLBACK_PRODUCT_SCORES = {
    3: 1.0,
    9: 0.7,
    2: 0.5,
    4: 0.5
}


@bentoml.service
@bentoml.asgi_app(app)
class ManoaService:

    @app.get("/api/v1/recommendations/product/{productId}")
    def recommend_product(
        self,
        productId: int,
        simulateTimeout: bool = False
    ):

        # Simula uma consulta que ultrapassou o limite de 150 ms
        if simulateTimeout:
            time.sleep(0.16)

            # Recupera os produtos do fallback pela camada de acesso
            produtos_fallback = get_fallback_products(
                list(FALLBACK_PRODUCT_SCORES.keys()),
                "/api/v1/recommendations/product"
            )

            # Monta as recomendações com suas pontuações
            recomendacoes_fallback = [
                {
                    "productId": produto["productId"],
                    "title": produto["title"],
                    "category": produto["category"],
                    "municipality": produto["municipality"],
                    "price": produto["price"],
                    "imageUrl": produto["imageUrl"],
                    "score": FALLBACK_PRODUCT_SCORES[
                        produto["productId"]
                    ]
                }
                for produto in produtos_fallback
            ]

            return {
                "productId": productId,
                "strategy": "TIMEOUT_FALLBACK_CACHE",
                "fallbackUsed": True,
                "recommendations": recomendacoes_fallback
            }

        # Busca o produto principal pela camada de acesso aos dados
        produto_principal = get_product_by_id(
            productId,
            "/api/v1/recommendations/product"
        )

        # Caso o produto não exista, retorna HTTP 404
        if produto_principal is None:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        # Recupera os produtos candidatos pela camada de acesso
        produtos_candidatos = get_recommendation_candidates(
            productId,
            "/api/v1/recommendations/product"
        )

        # Calcula a similaridade de cada produto
        recomendacoes = []

        for produto in produtos_candidatos:

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

            # Adiciona somente produtos com alguma similaridade
            if score > 0:
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

        # Monta a resposta com as 4 melhores recomendações
        resposta = {
            "productId": productId,
            "strategy": "SAME_CATEGORY_AND_ORIGIN",
            "fallbackUsed": False,
            "recommendations": recomendacoes[:4]
        }

        # Informa quando não existem recomendações similares
        if not recomendacoes:
            resposta["message"] = (
                "Não foram encontradas recomendações com atributos em comum."
            )

        return resposta

    @app.get("/api/v1/recommendations/home")
    def recommend_home(self, anonymousSessionId: str):

        # Recupera os produtos pela camada de acesso aos dados
        produtos_disponiveis = get_cold_start_products(
            "/api/v1/recommendations/home"
        )

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

        admin_api_key = os.environ.get("MANOA_ADMIN_API_KEY")

        # Valida a chave administrativa
        if not admin_api_key or x_api_key != admin_api_key:
            raise HTTPException(
                status_code=401,
                detail="Não autorizado"
            )

        # Estratégias aceitas pelo mock
        estrategias_validas = [
            "SAME_CATEGORY_AND_ORIGIN",
            "COLD_START"
        ]

        # Valida a estratégia
        if strategyId not in estrategias_validas:
            raise HTTPException(
                status_code=400,
                detail="strategyId inválido"
            )

        return {
            "strategyId": strategyId,
            "status": "ACTIVE",
            "message": "Estratégia atualizada com sucesso"
        }
