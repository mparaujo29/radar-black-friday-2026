"""Consulta ofertas do Google Shopping via SerpApi (plano gratuito).
Registra somente preço atual observado. Não presume desconto/histórico confiável.
Não executa buscas se não houver chave ou quota disponível.
"""
import json
import math
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "monitoring.json"
CATALOG = ROOT / "products.json"
OUT = ROOT / "data" / ".serpapi-feed.json"
API = "https://serpapi.com/search.json"
ACCOUNT_API = "https://serpapi.com/account.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def fetch(url):
    req = Request(url, headers={"Accept": "application/json", "User-Agent": "RadarBF2026/1.0"})
    with urlopen(req, timeout=35) as response:
        if response.status != 200:
            raise RuntimeError(f"API HTTP {response.status}")
        return json.load(response)

def norm(value):
    value = unicodedata.normalize("NFKD", str(value).lower())
    return "".join(c for c in value if not unicodedata.combining(c))

def matches(title, spec):
    title = norm(title)
    text = re.sub(r"[^a-z0-9]+", " ", title)
    words = set(text.split())
    if any(norm(token) not in words for token in spec.get("must", [])):
        return False
    if any(norm(token) in words for token in spec.get("exclude", [])):
        return False
    storage = spec.get("storage_gb")
    if storage and not re.search(r"(?<![0-9])" + str(storage) + r"\s*(?:gb|g)(?![0-9])", title):
        return False
    return True

def valid_https(url):
    p = urlparse(str(url))
    return p.scheme == "https" and bool(p.netloc)

def candidate(item, spec):
    title = item.get("title", "")
    price_display = str(item.get("price", ""))
    if not matches(title, spec) or not re.search(r"R\s*\$|\bBRL\b", price_display, re.I):
        return None
    if re.search(r"a partir de|por m[eê]s|parcela(s)?|mensal", norm(price_display)):
        return None
    if str(item.get("second_hand_condition", "")).strip():
        return None
    try:
        amount = float(item["extracted_price"])
        if not math.isfinite(amount) or not 30 < amount < 100000:
            return None
    except (ValueError, TypeError, KeyError):
        return None
    source = str(item.get("source", "")).strip()
    link = item.get("link") or item.get("product_link")
    if not source or not valid_https(link):
        return None
    return {"price": round(amount, 2), "store": source[:120], "source_url": link, "title": title}

def main():
    key = os.getenv("SERPAPI_API_KEY", "").strip()
    OUT.unlink(missing_ok=True)
    if not key:
        print("SERPAPI_API_KEY não configurada. Coleta ignorada; nenhum preço inventado.")
        return
    monitored = load(CONFIG).get("monitored", [])
    ids = {x["id"] for x in load(CATALOG).get("products", [])}
    enabled = [x for x in monitored if x.get("enabled", True) and x.get("id") in ids]
    if not enabled:
        print("Nenhum item habilitado em monitoring.json.")
        return
    # Consulta grátis: não consome pesquisas da franquia.
    account = fetch(ACCOUNT_API + "?" + urlencode({"api_key": key}))
    usage = account.get("this_month_usage")
    left = account.get("total_searches_left", account.get("plan_searches_left"))
    if not isinstance(usage, int) or not isinstance(left, int):
        raise RuntimeError("API de conta sem dados suficientes para controle de quota; coleta bloqueada.")
    budget = min(220, int(os.getenv("SERPAPI_MONTHLY_BUDGET", "220")))
    count = min(len(enabled), max(0, budget - usage), max(0, left))
    if count == 0:
        print("Franquia gratuita/reserva mensal esgotada. Nenhuma pesquisa enviada.")
        return
    if count < len(enabled):
        print(f"Quota permite consultar {count} dos {len(enabled)} produtos habilitados.")
    quotes = []
    now = datetime.now(timezone.utc).isoformat()
    for spec in enabled[:count]:
        params = {"engine": "google_shopping", "q": spec["query"], "gl": "br",
                  "hl": "pt", "google_domain": "google.com.br", "api_key": key}
        try:
            data = fetch(API + "?" + urlencode(params))
            if data.get("error"):
                print(f"API sem resultados válidos para {spec['id']}; nenhuma cotação criada.")
                continue
            results = data.get("shopping_results", []) + data.get("inline_shopping_results", [])
            matches_found = [v for x in results if isinstance(x, dict) if (v := candidate(x, spec))]
            if not matches_found:
                print(f"Sem correspondência segura para {spec['id']}.")
                continue
            best = min(matches_found, key=lambda r: r["price"])
            quotes.append({"id": spec["id"], "name": spec["name"], "date": now,
                           "price": best["price"], "store": best["store"],
                           "source_url": best["source_url"]})
            print(f"{spec['id']}: cotação compatível encontrada; preço real será registrado no histórico.")
        except Exception as e:
            print(f"Falha ao consultar {spec['id']}: {type(e).__name__} (não houve registro).", file=sys.stderr)
    if quotes:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps({"quotes": quotes}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{len(quotes)} cotações importáveis; descontos ainda não validados.")
    else:
        print("Nenhuma cotação registrada. Verifique correspondência dos modelos e API.")

if __name__ == "__main__":
    main()
