from typing import Any, Dict

class MCPClientStub:
    """
    Простая заглушка. В реальной версии тут будет соединение с MCP-сервером
    (stdio/WebSocket) и вызов инструмента. Пока просто формируем строку.
    """
    def call(self, server: str, tool: str, params: Dict[str, Any] | None = None) -> str:
        return f"[mcp-demo] server={server}, tool={tool}, params={params or {}}"

client = MCPClientStub()
