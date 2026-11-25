import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from collect_serpapi import matches, candidate

class BlackFridayCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = json.loads((ROOT / "monitoring.json").read_text(encoding="utf-8"))
        catalog = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))
        cls.monitored = {x["id"]: x for x in config["monitored"]}
        cls.products = {x["id"] for x in catalog["products"]}

    def test_all_ten_products_enabled(self):
        self.assertEqual(set(self.monitored), self.products)
        self.assertEqual(len(self.monitored), 10)
        self.assertTrue(all(x["enabled"] for x in self.monitored.values()))

    def test_playstation_disk_version_only(self):
        rule = self.monitored["seed-0"]
        self.assertTrue(matches("Sony PlayStation 5 Slim 1TB com leitor de disco", rule))
        self.assertFalse(matches("PS5 Slim Digital 1TB", rule))
        self.assertFalse(matches("Controle DualSense PlayStation 5 Slim 1TB", rule))

    def test_tablet_fe_cannot_capture_fe_plus(self):
        base, plus = self.monitored["seed-2"], self.monitored["seed-3"]
        self.assertTrue(matches("Samsung Galaxy Tab S10 FE WiFi 128GB", base))
        self.assertFalse(matches("Samsung Galaxy Tab S10 FE+ WiFi 128GB", base))
        self.assertTrue(matches("Samsung Galaxy Tab S10 FE+ WiFi 128GB", plus))
        self.assertFalse(matches("Samsung Galaxy Tab S10 FE WiFi 128GB", plus))
        self.assertFalse(matches("Samsung Galaxy Tab S10 FE Plus 256GB", plus))

    def test_tab_lite_eight_gb_ram_256_storage(self):
        lite = self.monitored["seed-4"]
        self.assertTrue(matches("Samsung Galaxy Tab S10 Lite 256GB 8GB RAM Wi-Fi", lite))
        self.assertFalse(matches("Samsung Galaxy Tab S10 Lite 128GB 6GB RAM Wi-Fi", lite))
        self.assertFalse(matches("Samsung Galaxy Tab S10 FE 256GB 8GB RAM", lite))

    def test_iphone_pro_max_and_base_separate(self):
        pro, base = self.monitored["seed-6"], self.monitored["seed-5"]
        self.assertTrue(matches("Apple iPhone 17 Pro Max 256GB", pro))
        self.assertFalse(matches("Apple iPhone 17 Pro Max 512GB", pro))
        self.assertFalse(matches("Apple iPhone 17 Pro 256GB", pro))
        self.assertFalse(matches("Apple iPhone 17 Pro Max 256GB", base))

    def test_fold_storage(self):
        fold = self.monitored["seed-7"]
        self.assertTrue(matches("Samsung Galaxy Z Fold 8 256GB", fold))
        self.assertFalse(matches("Samsung Galaxy Z Fold 7 256GB", fold))
        self.assertFalse(matches("Samsung Galaxy Z Fold 8 512GB", fold))

    def test_lg_cooling_specific_sku(self):
        lg = self.monitored["seed-9"]
        self.assertTrue(matches("LG Dual Inverter Voice Só Frio S3-Q12JA31L 12000 BTU 220V", lg))
        self.assertFalse(matches("LG Dual Inverter Quente Frio S3-W12JA31D 12000 BTU 220V", lg))

    def test_pe12g_accessory_and_unreasonable_price(self):
        pe = self.monitored["seed-8"]
        self.assertFalse(matches("Refil Filtro para Purificador Electrolux PE12G", pe))
        ad = {"title": "Purificador de água Electrolux PE12G", "price": "R$ 115,00",
              "extracted_price": 115.0, "source": "Loja A", "product_link": "https://example.com/p"}
        self.assertIsNone(candidate(ad, pe))
        ad["extracted_price"] = 557.0
        self.assertEqual(candidate(ad, pe)["price"], 557.0)

if __name__ == "__main__":
    unittest.main()
