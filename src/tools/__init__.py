from src.tools.catalog import buscar_produtos
from src.tools.orders import consultar_pedidos
from src.tools.policies import consultar_politicas

TOOLS = [buscar_produtos, consultar_pedidos, consultar_politicas]

__all__ = ["TOOLS"]
