import sys
import json
import argparse
import textwrap
from pathlib import Path
from jsonschema import validate, ValidationError

from .i18n import I18n
from .mcp_client import client as mcp_client  # MCP stub client

# Путь к схеме рядом с кодом пакета
BASE = Path(__file__).resolve().parent
SCHEMA_PATH = BASE / "schema" / "aip.schema.json"


def _find_mcp_tool(agent: dict):
    """
    Возвращает описание первого инструмента провайдера MCP у агента,
    либо None, если такого нет.
    Ожидается структура:
      tool = {
        "provider": "mcp",
        "x-mcp": { "server": "...", "tool": "...", "params": {...} }
      }
    """
    for t in agent.get("tools", []) or []:
        if t.get("provider") == "mcp":
            xmcp = t.get("x-mcp", {}) or {}
            return {
                "server": xmcp.get("server"),
                "tool": xmcp.get("tool"),
                "params": xmcp.get("params", {})
            }
    return None


def load_json(path: Path, i18n: I18n) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(i18n.t("file_not_found", path=str(path)))
    except json.JSONDecodeError as e:
        sys.exit(i18n.t("json_error", path=str(path), error=str(e)))


def do_validate(manifest_path: Path, i18n: I18n) -> None:
    manifest = load_json(manifest_path, i18n)
    schema = load_json(SCHEMA_PATH, i18n)
    try:
        validate(instance=manifest, schema=schema)
    except ValidationError as e:
        sys.exit(i18n.t("manifest_validation_failed", error=str(e)))
    print(i18n.t("validation_ok"))


def do_run(manifest_path: Path, i18n: I18n) -> None:
    manifest = load_json(manifest_path, i18n)
    schema = load_json(SCHEMA_PATH, i18n)
    try:
        validate(instance=manifest, schema=schema)
    except ValidationError as e:
        sys.exit(i18n.t("manifest_validation_failed", error=str(e)))
    print(i18n.t("validation_ok"))
    print()

    project = manifest.get("project", {}).get("name", "AIP Scenario")
    print(i18n.t("scenario_start", project=project))
    print()

    steps = manifest.get("workflow", {}).get("steps", [])
    if not steps:
        print(i18n.t("no_steps"))
        return

    # Демонстрационный прогон без LLM
    agents = {a["id"]: a for a in manifest.get("agents", [])}
    context = ""
    for i, step in enumerate(steps, start=1):
        agent_id = step["agent"]
        agent = agents.get(agent_id)
        if not agent:
            sys.exit(i18n.t("unknown_agent", index=i, agent_id=agent_id))

        task = step["task"]
        print(i18n.t("step_header", index=i, agent_name=agent["name"], task=task))

        # Если у агента есть MCP-инструмент — вызовем заглушку и выведем результат
        mcp = _find_mcp_tool(agent)
        if mcp and mcp.get("server") and mcp.get("tool"):
            result = mcp_client.call(mcp["server"], mcp["tool"], mcp.get("params"))
            print(textwrap.indent(result, "   "))
            context += f"\n\n### MCP RESULT ({agent['name']})\n{result}"

        # Демо-ответ агента
        demo_answer = f"[demo] {agent['name']} → {task}"
        print(textwrap.indent(demo_answer, "   "))
        context += f"\n\n### {agent['name']} RESPONSE\n{demo_answer}"

    print()
    print(i18n.t("done"))


def main():
    parser = argparse.ArgumentParser(prog="aip-runner", description="AIP CLI (i18n + MCP stub)")
    # Общий флаг языка
    parser.add_argument("--lang", choices=["en", "ru"], help="UI language (en|ru)")

    sub = parser.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("validate", help="Validate manifest")
    pv.add_argument("manifest", help="Path to AIP JSON")

    pr = sub.add_parser("run", help="Run workflow (demo, no LLM)")
    pr.add_argument("manifest", help="Path to AIP JSON")

    args = parser.parse_args()
    i18n = I18n(args.lang)
    print(i18n.t("using_lang", lang=i18n.lang))

    manifest_path = Path(getattr(args, "manifest", ""))

    if args.cmd == "validate":
        do_validate(manifest_path, i18n)
    elif args.cmd == "run":
        do_run(manifest_path, i18n)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
