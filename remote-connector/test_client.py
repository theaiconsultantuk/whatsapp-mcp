import os, asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
async def go():
    h={"Authorization":"Bearer "+os.environ["WHATSAPP_MCP_TOKEN"]}
    async with streamablehttp_client("http://127.0.0.1:18765/mcp", headers=h) as (r,w,_):
        async with ClientSession(r,w) as s:
            await s.initialize()
            print("tools:", [t.name for t in (await s.list_tools()).tools])
            res = await s.call_tool("list_chats", {"limit":1,"include_last_message":False})
            print("list_chats isError:", res.isError, res.content[0].text[:150] if res.isError else len(res.content))
            res = await s.call_tool("send_message", {"recipient":"000000000000","message":"DRY TEST - must not send"})
            print("send_message isError:", res.isError, (res.content[0].text[:60] if res.content else ""))
asyncio.run(go())
