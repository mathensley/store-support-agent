import unittest
from decimal import Decimal, ROUND_HALF_UP

from src.tools._csv import read_rows
from src.tools.catalog import buscar_produtos
from src.tools.orders import consultar_pedidos


class CatalogToolTests(unittest.TestCase):
    def test_available_guitars_under_budget(self):
        result = buscar_produtos.invoke(
            {"categoria": "violões", "preco_max_brl": 1000, "somente_disponiveis": True}
        )
        self.assertGreater(result["total_matches"], 0)
        self.assertTrue(result["products"])
        self.assertEqual(result["total_matches"], len(result["products"]))
        for product in result["products"]:
            self.assertTrue(product["available"])
            self.assertLessEqual(Decimal(product["price_brl"]), Decimal("1000"))
            self.assertEqual(product["category"], "Violões")

    def test_description_can_find_beginner_product(self):
        result = buscar_produtos.invoke({"busca": "iniciante", "categoria": "violão"})
        ids = {product["product_id"] for product in result["products"]}
        self.assertIn(83, ids)  # Descrição: "perfeito para quem está começando".

    def test_active_promotion_changes_returned_price(self):
        promotion = next(
            row for row in read_rows("promotions.csv") if row["is_active"] == "1"
        )
        product_row = next(
            row for row in read_rows("products.csv")
            if row["product_id"] == promotion["product_id"]
        )
        result = buscar_produtos.invoke({"busca": product_row["name"], "limite": 20})
        product = next(
            item for item in result["products"]
            if item["product_id"] == int(product_row["product_id"])
        )
        expected = (
            Decimal(product_row["price_brl"])
            * (Decimal(100) - Decimal(promotion["discount_percent"]))
            / 100
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.assertEqual(Decimal(product["price_brl"]), expected)
        self.assertIsNotNone(product["promotion"])


class OrderToolTests(unittest.TestCase):
    def test_order_number_returns_requested_fields_without_customer_data(self):
        order = read_rows("orders.csv")[0]
        result = consultar_pedidos.invoke({"numero_pedido": int(order["order_id"])})
        self.assertTrue(result["found"])
        returned = result["orders"][0]
        self.assertEqual(returned["status"], order["status"])
        self.assertEqual(returned["payment_method"], order["payment_method"])
        self.assertEqual(Decimal(returned["total_brl"]), Decimal(order["total_brl"]))
        self.assertEqual(
            set(returned),
            {
                "order_id", "order_date", "status", "total_brl", "payment_method",
                "tracking_code", "estimated_delivery", "notes",
            },
        )
        self.assertNotIn("customer_id", str(result))

        order_with_notes = next(row for row in read_rows("orders.csv") if row["notes"])
        with_notes = consultar_pedidos.invoke(
            {"numero_pedido": int(order_with_notes["order_id"])}
        )
        self.assertEqual(with_notes["orders"][0]["notes"], order_with_notes["notes"])

    def test_unknown_order_number_returns_no_order_data(self):
        result = consultar_pedidos.invoke({"numero_pedido": 999999})
        self.assertFalse(result["found"])
        self.assertEqual(result["orders"], [])


if __name__ == "__main__":
    unittest.main()