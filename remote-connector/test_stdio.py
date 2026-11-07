import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
P=StdioServerParameters(command="/Users/paulcowen/.local/bin/uv",args=["--directory","/Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-mcp-server","run","main.py"])
async def go():
    async with stdio_client(P) as (r,w):
        async with ClientSession(r,w) as s:
            await s.initialize()
            res=await s.call_tool("list_chats",{"limit":1,"include_last_message":True})
            print("stdio list_chats isError:",res.isError,len(res.content))
asyncio.run(go())
