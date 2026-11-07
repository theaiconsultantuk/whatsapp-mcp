# Using Paul's WhatsApp bridge from albertos-mac-mini (mac48)

## What's already true (checked from mac48 on 18 Oct 2026)
- Paul's Mac: `Pauls-Mac-mini`, Tailscale IP **100.100.17.61**, user `paulcowen`.
- From mac48, `ssh paulcowen@100.100.17.61` works with key auth (`~/.ssh/id_ed25519`), with no password.
- On Paul's Mac, the Go bridge (whatsmeow) is running. It listens on **:8080**, serves `/api/send` and `/api/download`, and has no auth.
- The MCP server lives on Paul's Mac at `/Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-mcp-server/main.py` and runs through `/Users/paulcowen/.local/bin/uv`.
  - **Reads** query SQLite directly: `/Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-bridge/store/messages.db`
  - **Sends** POST to `http://localhost:8080/api/send`

Port 8080 alone is no good from mac48: reads need the SQLite file, which only exists on Paul's Mac. Don't copy or sync messages.db, because the bridge holds a live WAL lock on it.

## Method: run Paul's MCP server over SSH (stdio)
Claude on mac48 starts the MCP server *on Paul's Mac* over SSH. Its stdin/stdout tunnels back through SSH, so both reads and sends happen locally on Paul's Mac. You don't install anything on mac48.

Run this on mac48:
```bash
claude mcp add whatsapp --scope user -- \
  ssh -T -o BatchMode=yes -o ServerAliveInterval=30 paulcowen@100.100.17.61 \
  /Users/paulcowen/.local/bin/uv --directory /Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-mcp-server run main.py
```
Then restart Claude, run `/mcp`, and check that `whatsapp` shows as connected. To smoke-test, call `list_chats` with limit 3.

If the add fails, test the raw pipe:
```bash
ssh -T paulcowen@100.100.17.61 'nc -z localhost 8080 && echo bridge-up; ls -la /Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-bridge/store/messages.db'
```

## Rules the remote Claude must follow
1. **Never send without Paul's explicit "send".** Paul's Mac has a hook that hard-blocks `send_message`, but that hook is NOT on mac48, so here the rule depends on you. Always show the draft and the recipient first, then wait.
2. The recipient must be a plain E.164 number (e.g. `447780691570`) or a full JID. The `Chat: 2119...` IDs printed by `list_messages` are internal LIDs. Passing one returns `success:true` and delivers nothing.
3. `send_message` returns success whether or not the message was delivered. The only real confirmation is Paul checking his phone.
4. File paths are **paths on Paul's Mac**, not on mac48:
   - `send_file` / `send_audio_message`: first `scp file paulcowen@100.100.17.61:~/.claude/scratch/wa-out/`, then pass that remote path.
   - `download_media` returns a path on Paul's Mac. Fetch it with `scp paulcowen@100.100.17.61:<path> .`
5. If a name search finds nothing, that doesn't mean the contact is missing. LID chats are stored under the number, not the name. Resolve them with `ssh paulcowen@100.100.17.61 "sqlite3 /Users/paulcowen/ClaudeProjects/whatsapp-mcp/whatsapp-bridge/store/whatsapp.db \"select lid from whatsmeow_lid_map where pn like '%<number>%'\""`.
6. Captions on images and the URLs behind hyperlinks are not stored (a known bridge gap). Download the media before you conclude that something is missing.

## If it stops working
- Bridge down: `ssh -T paulcowen@100.100.17.61 'lsof -nP -iTCP:8080 -sTCP:LISTEN'` prints nothing. Tell Paul so he can restart it from `whatsapp-bridge/` (`start-bridge-tmux.sh`).
- Don't restart or rebuild the bridge from mac48. Only one instance can hold the session, and a second one fights over the SQLite lock.

(Reference copy on Paul's Mac: /Users/paulcowen/ClaudeProjects/whatsapp-mcp/docs/remote-access-from-mac48.md)
