# Task: Repoint the WhatsApp MCP server to its new location and restart

## Background / diagnosis (already done — do NOT re-investigate from scratch)
Paul moved the whatsapp-mcp bridge. The move left a **split**:

- ✅ **Bridge (writer)** now runs from the NEW home and is healthy:
  `/Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-bridge`
  - Live DB (39 MB, updating): `/Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-bridge/store/messages.db`
  - Confirmed 4243 chats incl. group `easySPEAKTechnical` = `120363402789529395@g.us`
- ❌ **MCP server (reader)** is STILL running from the OLD, now-empty path:
  `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-mcp-server`
  - Running PIDs at time of diagnosis: 4998, 5028, 5321, 5359, 7185, 7186 (uv + python main.py from the OLD path)

Result: the `mcp__whatsapp__*` tools read a stale/empty DB → `list_chats` returns nothing.

## Goal
Make the MCP server read the NEW messages.db so the WhatsApp tools work again.

## Steps
1. **Find where the MCP server is registered** (whichever applies):
   - `~/.claude.json` / `~/.claude/mcp.json` / project `.mcp.json` — search for `whatsapp` and the old path `/Volumes/Courses/Keto/whatsapp-mcp`.
   - Also check LaunchAgents (see `MCP-LAUNCHAGENTS-DOCUMENTATION.md` in this repo) — `~/Library/LaunchAgents/*whatsapp*`.
2. **Repoint** every reference from
   `/Volumes/Courses/Keto/whatsapp-mcp/whatsapp-mcp-server`  →
   `/Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-mcp-server`
   (the `--directory` arg for `uv`, and any hard-coded DB path inside the server if it isn't relative).
3. **Confirm the new server reads the new DB.** The server should resolve messages.db to
   `/Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-bridge/store/messages.db`.
   If it uses a relative/hard-coded path, fix it to point there.
4. **Kill the old server processes** (the 6 PIDs from the old path — re-check with
   `pgrep -fl "Keto/whatsapp-mcp"`), and restart the MCP server from the new location
   (or `launchctl unload/load` the LaunchAgent).
5. **Verify**: in a Claude session the `mcp__whatsapp__list_chats` should now return chats,
   and searching `easySPEAK` should surface `easySPEAKTechnical`.
   Quick non-MCP sanity check:
   `sqlite3 "/Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-bridge/store/messages.db" "SELECT name FROM chats WHERE name LIKE '%peak%';"`

## Guardrails
- Do NOT touch the bridge (it's healthy). Only the reader/MCP-server side.
- Do NOT delete the old `/Volumes/Courses/Keto/whatsapp-mcp` tree yet — just stop its processes and repoint config. Paul can clean it up later once verified.
- Note: MCP config changes require restarting the Claude client to take effect.

Report back: what you changed, the PIDs killed, and the verification output.
