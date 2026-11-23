import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from collect_serpapi import candidate, matches

class MatchingTests(unittest.TestCase):
    def test_s26_256(self):
        rule = {"must": ["s26", "ultra"], "exclude": ["capa", "usado"], "storage_gb": 256}
        self.assertTrue(matches("Samsung Galaxy S26 Ultra 256GB Preto", rule))
        self.assertFalse(matches("Samsung Galaxy S26 Ultra 512GB Preto", rule))
        self.assertFalse(matches("Capa Samsung Galaxy S26 Ultra 256GB", rule))

    def test_iphone_17_normal_vs_pro(self):
        rule = {"must": ["iphone", "17"], "exclude": ["pro", "max", "plus", "air"], "storage_gb": 256}
        self.assertTrue(matches("Apple iPhone 17 256 GB", rule))
        self.assertFalse(matches("Apple iPhone 17 Pro 256GB", rule))
        self.assertFalse(matches("Apple iPhone 17 Air 256GB", rule))

    def test_electrolux_vs_filter(self):
        rule = {"must": ["electrolux", "pe12g"], "exclude": ["refil", "filtro"]}
        self.assertTrue(matches("Purificador de Água Electrolux PE12G", rule))
        self.assertFalse(matches("Refil Filtro Electrolux PE12G", rule))

    def test_refuses_foreign_currency(self):
        rule = {"must": ["electrolux", "pe12g"], "exclude": ["refil"]}
        item = {"title": "Electrolux PE12G", "price": "US$ 99.00", "extracted_price": 99,
                "source": "Loja", "product_link": "https://loja.example/purificador"}
        self.assertIsNone(candidate(item, rule))

    def test_accepts_brl_listing(self):
        rule = {"must": ["electrolux", "pe12g"], "exclude": ["refil"]}
        item = {"title": "Electrolux PE12G", "price": "R$ 599,90", "extracted_price": 599.9,
                "source": "Loja", "product_link": "https://loja.example/purificador"}
        self.assertEqual(candidate(item, rule)["price"], 599.9)

if __name__ == "__main__":
    unittest.main()
