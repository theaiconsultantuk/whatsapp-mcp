#!/bin/bash
# Start remote WhatsApp MCP on 127.0.0.1:18765. Flip WA_ALLOW_SEND=1 to enable sends (approval-gated).
cd ~/ClaudeProjects/whatsapp-mcp/whatsapp-mcp-server
exec /opt/homebrew/bin/doppler run -p infra -c prd --only-secrets WHATSAPP_MCP_TOKEN --only-secrets GROKBOT_APPROVAL_WEBHOOK_URL --only-secrets GROKBOT_APPROVAL_SENDER_KEY -- \
  env WA_ALLOW_SEND="${WA_ALLOW_SEND:-1}" ~/.local/bin/uv run --with 'mcp>=1.12,<2' --with uvicorn python ../remote-connector/server.py
