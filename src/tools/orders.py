from decimal import Decimal
from langchain.tools import tool

from src.tools._csv import read_rows


@tool
def consultar_pedidos(numero_pedido: int) -> dict:
    """
    Consulte um pedido pelo número informado pelo cliente.
    Use quando o cliente perguntar sobre andamento, pagamento, entrega ou rastreio de um pedido. Peça somente o número do pedido.
    """
    
    order = next(
        (
            row for row in read_rows("orders.csv")
            if row["order_id"] == str(numero_pedido)
        ),
        None,
    )
    if order is None:
        return {
            "found": False,
            "total_matches": 0,
            "orders": [],
            "message": "Pedido não encontrado para o número informado.",
        }

    return {
        "found": True,
        "total_matches": 1,
        "orders": [
            {
                "order_id": int(order["order_id"]),
                "order_date": order["order_date"],
                "status": order["status"],
                "total_brl": str(Decimal(order["total_brl"]).quantize(Decimal("0.01"))),
                "payment_method": order["payment_method"],
                "tracking_code": order["tracking_code"] or None,
                "estimated_delivery": order["estimated_delivery"] or None,
                "notes": order["notes"] or None,
            }
        ],
        "source": "CSV de demonstração; o pedido pode ter mudado desde a criação dos arquivos.",
    }