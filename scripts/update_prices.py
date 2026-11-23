"""Importa feed JSON autorizado sem inventar preços nem referências."""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "products.json"
PRICES = ROOT / "prices.json"
HISTORY = ROOT / "data" / "history.json"

def read_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default

def valid_https(value):
    try:
        p = urlparse(str(value))
        return p.scheme == "https" and bool(p.netloc)
    except Exception:
        return False

def main():
    local_feed = os.environ.get("PRICE_FEED_FILE", "").strip()
    url = os.environ.get("PRICE_FEED_URL", "").strip()
    if local_feed and (ROOT / local_feed).is_file():
        data = read_json(ROOT / local_feed, {})
        print("Importando feed temporário da SerpApi.")
    elif valid_https(url):
        headers = {"Accept": "application/json", "User-Agent": "RadarBlackFriday2026/1.0"}
        token = os.environ.get("PRICE_FEED_TOKEN", "").strip()
        if token:
            headers["Authorization"] = "Bearer " + token
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=25) as response:
            if response.status != 200:
                raise RuntimeError(f"Fonte retornou HTTP {response.status}")
            data = json.load(response)
    else:
        print("Nenhuma fonte configurada com novas cotações; histórico preservado.")
        return
    if not isinstance(data, dict) or not isinstance(data.get("quotes"), list):
        raise ValueError("Feed precisa conter um array quotes")
    ids = {p["id"] for p in read_json(PRODUCTS, {"products": []})["products"]}
    history = read_json(HISTORY, {"quotes": []})
    previous = history.get("quotes", [])
    if not isinstance(previous, list):
        raise ValueError("Histórico inválido")
    known = {(q.get("id"), q.get("date"), q.get("store"), q.get("price")) for q in previous}
    accepted = []
    for q in data["quotes"]:
        if not isinstance(q, dict) or q.get("id") not in ids:
            continue
        try:
            price = float(q["price"])
            date = datetime.fromisoformat(q["date"].replace("Z", "+00:00"))
            if date.tzinfo is None or date > datetime.now(timezone.utc):
                continue
            if price <= 0 or not valid_https(q.get("source_url")) or not str(q.get("store", "")).strip():
                continue
            item = dict(id=q["id"], name=str(q.get("name", "")), date=date.isoformat(), price=price,
                        store=str(q["store"]).strip(), source_url=q["source_url"])
            ref = q.get("reference")
            ref_url = q.get("reference_source_url")
            if q.get("reference_verified") is True and valid_https(ref_url) and ref is not None and float(ref) > 0:
                item.update(reference=float(ref), reference_verified=True, reference_source_url=ref_url)
            key = (item["id"], item["date"], item["store"], item["price"])
            if key not in known:
                accepted.append(item)
                known.add(key)
        except (ValueError, TypeError, KeyError):
            continue
    if not accepted:
        print("Nenhuma nova cotação válida; histórico preservado.")
        return
    all_quotes = previous + accepted
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    HISTORY.write_text(json.dumps({"quotes": all_quotes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PRICES.write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(),
                                  "quotes": all_quotes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(accepted)} novas cotações de preço registrado; total {len(all_quotes)}. Referências de desconto são validadas separadamente.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Erro na coleta: {exc}", file=sys.stderr)
        sys.exit(1)
