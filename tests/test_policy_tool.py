import unittest

from src.tools import TOOLS
from src.tools.policies import _SECTIONS, consultar_politicas


class PolicyToolTests(unittest.TestCase):
    def test_all_pdf_sections_can_be_retrieved(self):
        for topic, title in _SECTIONS:
            with self.subTest(topic=topic):
                result = consultar_politicas.invoke({"topico": topic})
                self.assertEqual(result["section"], title)
                self.assertTrue(result["text"].startswith(title))
                self.assertTrue(result["pages"])

    def test_arrependimento_returns_only_relevant_section(self):
        result = consultar_politicas.invoke({"topico": "trocas_devolucoes"})
        self.assertEqual(result["pages"], [4])
        self.assertIn("7 (sete) dias corridos", result["text"])
        self.assertNotIn("3. Formas de Pagamento", result["text"])
        self.assertNotIn("5. Política de Frete e Entregas", result["text"])

    def test_freight_section_keeps_both_pages(self):
        result = consultar_politicas.invoke({"topico": "frete_entregas"})
        self.assertEqual(result["pages"], [4, 5])
        self.assertIn("Frete grátis", result["text"])
        self.assertIn("Jadlog", result["text"])

    def test_agent_registers_policy_tool(self):
        self.assertIn("consultar_politicas", [tool.name for tool in TOOLS])


if __name__ == "__main__":
    unittest.main()