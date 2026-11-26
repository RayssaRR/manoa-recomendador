
import json
from datetime import datetime
from pathlib import Path

from src.catalogo import catalogo


# Caminho do arquivo de log
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "acessos.jsonl"


def registrar_acesso(
    nome_funcao,
    rota,
    parametros,
    registros,
    record_ids,
    status
):
    """
    Registra cada chamada de uma função de acesso aos dados.
    Cada registro é acrescentado ao final do arquivo JSONL.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    registro = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "function": nome_funcao,
        "caller": rota,
        "parameters": parametros,
        "recordsReturned": registros,
        "recordIds": record_ids,
        "status": status
    }

    with LOG_FILE.open("a", encoding="utf-8") as arquivo:
        arquivo.write(
            json.dumps(registro, ensure_ascii=False) + "\n"
        )


def get_product_by_id(product_id, caller):
    """
    Busca um produto pelo identificador.
    Retorna o produto ou None caso não exista.
    """

    try:
        produto = next(
            (
                item for item in catalogo
                if item["productId"] == product_id
            ),
            None
        )

        registrar_acesso(
            nome_funcao="get_product_by_id",
            rota=caller,
            parametros={"productId": product_id},
            registros=1 if produto else 0,
            record_ids=[produto["productId"]] if produto else [],
            status="success" if produto else "not_found"
        )

        return produto

    except Exception:
        registrar_acesso(
            nome_funcao="get_product_by_id",
            rota=caller,
            parametros={"productId": product_id},
            registros=0,
            record_ids=[],
            status="error"
        )
        raise


def get_recommendation_candidates(product_id, caller):
    """
    Recupera os produtos candidatos à recomendação,
    excluindo o próprio produto informado.
    """

    try:
        produtos = [
            item for item in catalogo
            if item["productId"] != product_id
        ]

        registrar_acesso(
            nome_funcao="get_recommendation_candidates",
            rota=caller,
            parametros={"productId": product_id},
            registros=len(produtos),
            record_ids=[
                produto["productId"] for produto in produtos
            ],
            status="success"
        )

        return produtos

    except Exception:
        registrar_acesso(
            nome_funcao="get_recommendation_candidates",
            rota=caller,
            parametros={"productId": product_id},
            registros=0,
            record_ids=[],
            status="error"
        )
        raise


def get_cold_start_products(caller):
    """
    Recupera produtos com selo de autoria cultural
    e estoque disponível.
    """

    try:
        produtos = [
            item for item in catalogo
            if item["seloAutoriaCultural"] is True
            and item["stock"] > 0
        ]

        registrar_acesso(
            nome_funcao="get_cold_start_products",
            rota=caller,
            parametros={},
            registros=len(produtos),
            record_ids=[
                produto["productId"] for produto in produtos
            ],
            status="success"
        )

        return produtos

    except Exception:
        registrar_acesso(
            nome_funcao="get_cold_start_products",
            rota=caller,
            parametros={},
            registros=0,
            record_ids=[],
            status="error"
        )
        raise
