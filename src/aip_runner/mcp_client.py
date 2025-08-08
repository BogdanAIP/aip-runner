import json
import os
from typing import Any, Dict, Optional

class MCPClientStub:
    """
    Простая заглушка. В реальной версии тут будет соединение с MCP-сервером
    (stdio/WebSocket) и вызов инструмента. Пока просто формируем строку.
    """
    def call(self, server: str, tool: str, params: Dict[str, Any] | None = None) -> str:
        return f"[mcp-demo] server={server}, tool={tool}, params={params or {}}"

def load_config(cli_json: Optional[str] = None) -> Dict[str, Any]:
    """
    Загружает конфиг MCP-серверов.
    Приоритет:
      1) cli_json (строка JSON из флага --mcp-config)
      2) переменная окружения AIP_MCP_SERVERS (строка JSON)
      3) пустой dict
    Пример значения:
      {"filesystem": {"cmd": "mcp-filesystem --root ./", "transport": "stdio"}}
    """
    text = cli_json or os.getenv("AIP_MCP_SERVERS", "").strip()
    if not text:
        return {}
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}

client = MCPClientStub()
