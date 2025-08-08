import sys
import json
import argparse
import textwrap
from pathlib import Path
from jsonschema import validate, ValidationError

# Путь к схеме рядом с кодом пакета
BASE = Path(__file__).resolve().parent
SCHEMA_PATH = BASE / "schema" / "aip.schema.json"

def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"Файл не найден: {path}")
    except json.JSONDecodeError as e:
        sys.exit(f"Ошибка JSON в {path}: {e}")

def do_validate(manifest_path: Path) -> None:
    manifest = load_json(manifest_path)
    schema = load_json(SCHEMA_PATH)
    try:
        validate(instance=manifest, schema=schema)
    except ValidationError as e:
        sys.exit(f"❌ Ошибка валидации манифеста:\n{e}\n")
    print("✅ Валидация манифеста: OK")

def do_run(manifest_path: Path) -> None:
    manifest = load_json(manifest_path)
    schema = load_json(SCHEMA_PATH)
    try:
        validate(instance=manifest, schema=schema)
    except ValidationError as e:
        sys.exit(f"❌ Ошибка валидации манифеста:\n{e}\n")
    print("✅ Валидация манифеста: OK\n")

    project = manifest.get("project", {}).get("name", "AIP Scenario")
    print(f"🚀 Сценарий «{project}»\n")

    steps = manifest.get("workflow", {}).get("steps", [])
    if not steps:
        print("⚠️ В манифесте нет шагов workflow.")
        return

    # Демонстрационный прогон без LLM
    agents = {a["id"]: a for a in manifest.get("agents", [])}
    context = ""
    for i, step in enumerate(steps, start=1):
        agent_id = step["agent"]
        agent = agents.get(agent_id)
        if not agent:
            sys.exit(f"Шаг {i}: неизвестный агент id='{agent_id}'")
        task = step["task"]
        print(f"— Шаг {i}: {agent['name']} → {task}")
        demo_answer = f"[demo] Ответ агента {agent['name']} на задачу: {task}"
        print(textwrap.indent(demo_answer, "   "))
        context += f"\n\n### {agent['name']} RESPONSE\n{demo_answer}"

    print("\n🎉 Готово.")

def main():
    parser = argparse.ArgumentParser(prog="aip-runner", description="AIP CLI (minimal)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("validate", help="Проверить манифест")
    pv.add_argument("manifest", help="Путь к AIP JSON")

    pr = sub.add_parser("run", help="Выполнить workflow (демо)")
    pr.add_argument("manifest", help="Путь к AIP JSON")

    args = parser.parse_args()
    manifest_path = Path(getattr(args, "manifest", ""))

    if args.cmd == "validate":
        do_validate(manifest_path)
    elif args.cmd == "run":
        do_run(manifest_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
