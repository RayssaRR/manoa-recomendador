
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
    sobre as funções executadas e os produtos consultados.
    """

    chamadas_por_funcao = Counter()
    consultas_por_produto = Counter()

    total_chamadas = 0
    total_erros = 0
    total_nao_encontrados = 0

    if not LOG_FILE.exists():
        print("Arquivo de log não encontrado.")
        return

    # IDs válidos existentes no catálogo
    todos_os_ids = {
        produto["productId"] for produto in catalogo
    }

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

            # Conta chamadas realizadas por função
            chamadas_por_funcao[nome_funcao] += 1

            # Conta erros registrados
            if status == "error":
                total_erros += 1

            # Conta consultas sem resultado
            if status == "not_found":
                total_nao_encontrados += 1

            # Conta apenas produtos solicitados individualmente
            # pela função get_product_by_id.
            # Produtos retornados como candidatos ou fallback
            # não são considerados consultas individuais.
            if nome_funcao == "get_product_by_id":

                parametros = registro.get("parameters", {})
                product_id = parametros.get("productId")

                if product_id in todos_os_ids:
                    consultas_por_produto[product_id] += 1

    # Produtos cadastrados que nunca foram consultados
    produtos_nao_consultados = sorted(
        todos_os_ids - set(consultas_por_produto.keys())
    )

    print("\n========== RESUMO DE ACESSOS DO MANOA ==========\n")

    print(f"Total de chamadas: {total_chamadas}")
    print(f"Total de erros: {total_erros}")
    print(f"Consultas sem resultado: {total_nao_encontrados}")

    print("\n--- Chamadas por função ---")

    if chamadas_por_funcao:
        for funcao, quantidade in sorted(chamadas_por_funcao.items()):
            print(f"{funcao}: {quantidade}")
    else:
        print("Nenhuma chamada registrada.")

    print("\n--- Produtos mais consultados ---")

    if consultas_por_produto:
        for product_id, quantidade in consultas_por_produto.most_common():
            print(f"Produto {product_id}: {quantidade} consulta(s)")
    else:
        print("Nenhum produto do catálogo foi consultado.")

    print("\n--- Produtos nunca consultados ---")

    if produtos_nao_consultados:
        for product_id in produtos_nao_consultados:
            print(f"Produto {product_id}")
    else:
        print("Todos os produtos foram consultados.")

    print("\n===============================================\n")


if __name__ == "__main__":
    gerar_resumo()
