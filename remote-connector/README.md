# WhatsApp MCP remote connector (staged, NOT public)
- server.py: imports ../whatsapp-mcp-server/main.py unchanged; streamable HTTP on 127.0.0.1:18765/mcp; Bearer WHATSAPP_MCP_TOKEN (Doppler infra/prd).
- Read tools only by default. Sends: WA_ALLOW_SEND=1 ./run.sh -> send_message/send_file/send_audio_message enabled, each gated by ~/approvals/wa-<id>.request -> needs ~/approvals/wa-<id>.decision = APPROVE (10 min timeout). WA_SEND_APPROVAL=0 removes the gate (not recommended).
- Test: test_client.py (lists tools, calls list_chats, confirms send_message absent).
## Go-live steps (await Paul)
1. cloudflared tunnel login (browser, Paul) ; cloudflared tunnel create whatsapp-mcp
2. cloudflared tunnel route dns whatsapp-mcp wa-mcp.<zone>
3. fill cloudflared-config.yml.draft -> ~/.cloudflared/whatsapp-mcp.yml
4. ./run.sh &  ;  cloudflared tunnel --config ~/.cloudflared/whatsapp-mcp.yml run whatsapp-mcp
5. Grok Bot: add remote MCP URL https://wa-mcp.<zone>/mcp, header Authorization: Bearer <token from Doppler>
(Optional Cloudflare Access service-token in front; Grok Bot would then also need CF-Access-Client-Id/Secret headers.)
## Separate proposal: bridge binds *:8080 with no auth -> change Go listen addr to 127.0.0.1:8080 in whatsapp-bridge/main.go and rebuild. Not done.
