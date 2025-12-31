from mcp.server.fastmcp import FastMCP

# Servis İsmi
mcp = FastMCP("Odev MCP Servisi")

# --- TOOL: Basit Matematik (Ödev Şartı: En az 1 tool) ---
@mcp.tool()
def topla(a: int, b: int) -> int:
    """İki sayıyı toplar."""
    return a + b

# --- BONUS TOOL: Metin Birleştirme ---
@mcp.tool()
def selamla(isim: str) -> str:
    """İsim alıp selam verir."""
    return f"Merhaba {isim}, MCP servisinden selamlar!"

if __name__ == "__main__":
    mcp.run()