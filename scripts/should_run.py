"""Evita consumir pesquisas duas vezes quando o agendamento de reserva dispara."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "status.json"

def should_run():
    if os.environ.get("RUN_EVENT") == "workflow_dispatch":
        return True, "Execução manual solicitada."
    if not STATUS.exists():
        return True, "Nenhuma execução bem-sucedida anterior."
    try:
        data = json.loads(STATUS.read_text(encoding="utf-8"))
        timestamp = datetime.fromisoformat(data["last_execution_at"].replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - timestamp).total_seconds()
        if 0 <= age < 60 * 60:
            return False, "Já houve execução bem-sucedida na última hora; pulando reserva."
        return True, "Sem execução bem-sucedida na última hora."
    except (OSError, KeyError, ValueError, TypeError, AttributeError):
        return True, "Status anterior ausente/inválido; verificando novamente."

def main():
    run, reason = should_run()
    print(reason)
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as f:
            f.write(f"run={'true' if run else 'false'}\n")

if __name__ == "__main__":
    main()
