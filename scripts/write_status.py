"""Registra no repositório o horário da última execução concluída.

Não significa que uma busca encontrou ofertas. O preço publicado pode ser antigo.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "data" / "history.json"
OUT = ROOT / "status.json"

def main():
    payload = json.loads(HISTORY.read_text(encoding="utf-8")) if HISTORY.exists() else {"quotes": []}
    quotes = payload.get("quotes", [])
    dates = [q.get("date") for q in quotes if q.get("date")]
    status = {
        "last_execution_at": datetime.now(timezone.utc).isoformat(),
        "workflow": "Atualizar preços - manhã e noite",
        "result": "rotina concluída; não implica que todas as lojas tiveram preço disponível",
        "price_source_configured": bool(os.environ.get("SERPAPI_API_KEY", "").strip()),
        "total_price_records": len(quotes),
        "last_quote_at": max(dates) if dates else None,
    }
    OUT.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Última execução concluída registrada (sem divulgar segredos).")

if __name__ == "__main__":
    main()
