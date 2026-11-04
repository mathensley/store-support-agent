"""Consulta estruturada ao catálogo CSV da loja."""

import json
from decimal import Decimal, ROUND_HALF_UP

from langchain.tools import tool

from src.tools._csv import read_rows
from src.tools._text import tokens


_CENTS = Decimal("0.01")

def _money(value: Decimal) -> str:
    return str(value.quantize(_CENTS, rounding=ROUND_HALF_UP))


@tool
def buscar_produtos(busca: str = "", categoria: str = "", preco_max_brl: float | None = None, somente_disponiveis: bool = False, limite: int = 20) -> dict:
    """
    Consulte produtos, preços, estoque, descrições e especificações dos CSVs.

    Use `busca` para termos de produto, marca, uso ou características (ex.: 'Takamine GD20', 'iniciante', 'cordas de aço').
    Use `categoria` para o tipo de instrumento, como 'violão' ou 'guitarra'. O preço máximo considera promoções marcadas como ativas no arquivo.
    Para opções disponíveis, configure `somente_disponiveis=True`.
    """
    
    if preco_max_brl is not None:
        maximum = Decimal(str(preco_max_brl))
        if not maximum.is_finite() or maximum < 0:
            return {"error": "preco_max_brl deve ser um valor não negativo."}
    else:
        maximum = None
    limite = max(1, min(limite, 20))

    categories = {row["category_id"]: row["name"] for row in read_rows("categories.csv")}
    promotions: dict[str, dict[str, str]] = {}
    for row in read_rows("promotions.csv"):
        if row["is_active"] != "1":
            continue
        current = promotions.get(row["product_id"])
        if current is None or Decimal(row["discount_percent"]) > Decimal(current["discount_percent"]):
            promotions[row["product_id"]] = row

    query_terms = tokens(busca, search_query=True)
    category_terms = tokens(categoria, search_query=True)
    matches = []
    for row in read_rows("products.csv"):
        category_name = categories.get(row["category_id"], "")
        category_words = tokens(category_name)
        if category_terms and not category_terms <= category_words:
            continue

        stock = int(row["stock_quantity"])
        available = row["status"] == "active" and stock > 0
        if somente_disponiveis and not available:
            continue

        base_price = Decimal(row["price_brl"])
        promotion = promotions.get(row["product_id"])
        discount = Decimal(promotion["discount_percent"]) if promotion else Decimal(0)
        final_price = (base_price * (Decimal(100) - discount) / 100).quantize(_CENTS, rounding=ROUND_HALF_UP)
        if maximum is not None and final_price > maximum:
            continue

        specs = json.loads(row["specs"])
        fields = (
            (tokens(row["name"]), 4),
            (category_words, 3),
            (tokens(row["description"]), 2),
            (tokens(" ".join(str(value) for value in specs.values())), 1),
        )
        if query_terms and not all(any(term in words for words, _ in fields) for term in query_terms):
            continue
        score = sum(max((weight for words, weight in fields if term in words), default=0) for term in query_terms)

        product = {
            "product_id": int(row["product_id"]),
            "name": row["name"],
            "category": category_name,
            "description": row["description"],
            "specs": specs,
            "status": row["status"],
            "stock_quantity": stock,
            "available": available,
            "list_price_brl": _money(base_price),
            "price_brl": _money(final_price),
            "promotion": (
                {"description": promotion["description"], "discount_percent": _money(discount)}
                if promotion else None
            )
        }
        matches.append((score, final_price, product))

    matches.sort(key=lambda match: (-match[0], match[1], match[2]["name"]))
    return {
        "total_matches": len(matches),
        "products": [product for _, _, product in matches[:limite]]
    }