
import json
from collections import Counter
from pathlib import Path

from src.catalogo import catalogo


# Caminho do arquivo de log
LOG_FILE = (
    Path(__file__).resolve().parent.parent
    / "logs"
    / "acessos.jsonl"
)


def gerar_resumo():
    """
    Lê o histórico de acessos e gera estatísticas
    sobre as funções e os produtos consultados.
    """

    chamadas_por_funcao = Counter()
    consultas_por_produto = Counter()

    total_chamadas = 0
    total_erros = 0
    total_nao_encontrados = 0

    if not LOG_FILE.exists():
        print("Arquivo de log não encontrado.")
        return

    with LOG_FILE.open("r", encoding="utf-8") as arquivo:

        for linha in arquivo:

            if not linha.strip():
                continue

            try:
                registro = json.loads(linha)
            except json.JSONDecodeError:
                continue

            total_chamadas += 1

            nome_funcao = registro.get("function", "desconhecida")
            status = registro.get("status", "desconhecido")

            chamadas_por_funcao[nome_funcao] += 1

            if status == "error":
                total_erros += 1

            if status == "not_found" or (
                nome_funcao == "get_product_by_id" and registro.get("recordsReturned") == 0
            ):
                total_nao_encontrados += 1

            # Conta os produtos retornados pelas funções
            for product_id in registro.get("recordIds", []):
                consultas_por_produto[product_id] += 1

    # Todos os produtos cadastrados no catálogo
    todos_os_ids = {
        produto["productId"] for produto in catalogo
    }

    # Produtos que nunca apareceram nos registros
    produtos_nao_consultados = sorted(
        todos_os_ids - set(consultas_por_produto.keys())
    )

    print("\n========== RESUMO DE ACESSOS DO MANOA ==========\n")

    print(f"Total de chamadas: {total_chamadas}")
    print(f"Total de erros: {total_erros}")
    print(f"Consultas sem resultado: {total_nao_encontrados}")

    print("\n--- Chamadas por função ---")

    for funcao, quantidade in sorted(chamadas_por_funcao.items()):
        print(f"{funcao}: {quantidade}")

    print("\n--- Produtos mais consultados ---")

    if consultas_por_produto:
        for product_id, quantidade in consultas_por_produto.most_common():
            print(f"Produto {product_id}: {quantidade} acesso(s)")
    else:
        print("Nenhum produto contabilizado.")

    print("\n--- Produtos nunca consultados ---")

    if produtos_nao_consultados:
        for product_id in produtos_nao_consultados:
            print(f"Produto {product_id}")
    else:
        print("Todos os produtos foram consultados.")

    print("\n===============================================\n")


if __name__ == "__main__":
    gerar_resumo()
