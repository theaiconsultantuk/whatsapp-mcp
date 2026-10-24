import os
import subprocess
import threading
import time
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from whatsapp import (
    search_contacts as whatsapp_search_contacts,
    list_messages as whatsapp_list_messages,
    list_chats as whatsapp_list_chats,
    get_chat as whatsapp_get_chat,
    get_direct_chat_by_contact as whatsapp_get_direct_chat_by_contact,
    get_contact_chats as whatsapp_get_contact_chats,
    get_last_interaction as whatsapp_get_last_interaction,
    get_message_context as whatsapp_get_message_context,
    send_message as whatsapp_send_message,
    send_file as whatsapp_send_file,
    send_audio_message as whatsapp_audio_voice_message,
    download_media as whatsapp_download_media
)

# Initialize FastMCP server
mcp = FastMCP("whatsapp")

@mcp.tool()
def search_contacts(query: str) -> List[Dict[str, Any]]:
    """Search WhatsApp contacts by name or phone number.
    
    Args:
        query: Search term to match against contact names or phone numbers
    """
    contacts = whatsapp_search_contacts(query)
    return contacts

@mcp.tool()
def list_messages(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sender_phone_number: Optional[str] = None,
    chat_jid: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_context: bool = True,
    context_before: int = 1,
    context_after: int = 1
) -> List[Dict[str, Any]]:
    """Get WhatsApp messages matching specified criteria with optional context.
    
    Args:
        after: Optional ISO-8601 formatted string to only return messages after this date
        before: Optional ISO-8601 formatted string to only return messages before this date
        sender_phone_number: Optional phone number to filter messages by sender
        chat_jid: Optional chat JID to filter messages by chat
        query: Optional search term to filter messages by content
        limit: Maximum number of messages to return (default 20)
        page: Page number for pagination (default 0)
        include_context: Whether to include messages before and after matches (default True)
        context_before: Number of messages to include before each match (default 1)
        context_after: Number of messages to include after each match (default 1)
    """
    messages = whatsapp_list_messages(
        after=after,
        before=before,
        sender_phone_number=sender_phone_number,
        chat_jid=chat_jid,
        query=query,
        limit=limit,
        page=page,
        include_context=include_context,
        context_before=context_before,
        context_after=context_after
    )
    return messages

@mcp.tool()
def list_chats(
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_last_message: bool = True,
    sort_by: str = "last_active"
) -> List[Dict[str, Any]]:
    """Get WhatsApp chats matching specified criteria.
    
    Args:
        query: Optional search term to filter chats by name or JID
        limit: Maximum number of chats to return (default 20)
        page: Page number for pagination (default 0)
        include_last_message: Whether to include the last message in each chat (default True)
        sort_by: Field to sort results by, either "last_active" or "name" (default "last_active")
    """
    chats = whatsapp_list_chats(
        query=query,
        limit=limit,
        page=page,
        include_last_message=include_last_message,
        sort_by=sort_by
    )
    return chats

@mcp.tool()
def get_chat(chat_jid: str, include_last_message: bool = True) -> Dict[str, Any]:
    """Get WhatsApp chat metadata by JID.
    
    Args:
        chat_jid: The JID of the chat to retrieve
        include_last_message: Whether to include the last message (default True)
    """
    chat = whatsapp_get_chat(chat_jid, include_last_message)
    return chat

@mcp.tool()
def get_direct_chat_by_contact(sender_phone_number: str) -> Dict[str, Any]:
    """Get WhatsApp chat metadata by sender phone number.
    
    Args:
        sender_phone_number: The phone number to search for
    """
    chat = whatsapp_get_direct_chat_by_contact(sender_phone_number)
    return chat

@mcp.tool()
def get_contact_chats(jid: str, limit: int = 20, page: int = 0) -> List[Dict[str, Any]]:
    """Get all WhatsApp chats involving the contact.
    
    Args:
        jid: The contact's JID to search for
        limit: Maximum number of chats to return (default 20)
        page: Page number for pagination (default 0)
    """
    chats = whatsapp_get_contact_chats(jid, limit, page)
    return chats

@mcp.tool()
def get_last_interaction(jid: str) -> str:
    """Get most recent WhatsApp message involving the contact.
    
    Args:
        jid: The JID of the contact to search for
    """
    message = whatsapp_get_last_interaction(jid)
    return message

@mcp.tool()
def get_message_context(
    message_id: str,
    before: int = 5,
    after: int = 5
) -> Dict[str, Any]:
    """Get context around a specific WhatsApp message.
    
    Args:
        message_id: The ID of the message to get context for
        before: Number of messages to include before the target message (default 5)
        after: Number of messages to include after the target message (default 5)
    """
    context = whatsapp_get_message_context(message_id, before, after)
    return context

@mcp.tool()
def send_message(
    recipient: str,
    message: str,
    reply_to: Optional[str] = None
) -> Dict[str, Any]:
    """Send a WhatsApp message to a person or group. For group chats use the JID.

    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        message: The message text to send
        reply_to: Optional message id to quote, turning this into a threaded reply.
                 Use the "id" field of a message returned by list_messages. The id MUST
                 come from the SAME chat you are sending to - message ids are only unique
                 within a chat, and an id from another chat will be rejected rather than
                 silently sent unquoted. Omit for a normal, unquoted message.

    Returns:
        A dictionary containing success status and a status message
    """
    # Validate input
    if not recipient:
        return {
            "success": False,
            "message": "Recipient must be provided"
        }

    # Call the whatsapp_send_message function with the unified recipient parameter
    success, status_message = whatsapp_send_message(recipient, message, reply_to)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def send_file(recipient: str, media_path: str) -> Dict[str, Any]:
    """Send a file such as a picture, raw audio, video or document via WhatsApp to the specified recipient. For group messages use the JID.
    
    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        media_path: The absolute path to the media file to send (image, video, document)
    
    Returns:
        A dictionary containing success status and a status message
    """
    
    # Call the whatsapp_send_file function
    success, status_message = whatsapp_send_file(recipient, media_path)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def send_audio_message(recipient: str, media_path: str) -> Dict[str, Any]:
    """Send any audio file as a WhatsApp audio message to the specified recipient. For group messages use the JID. If it errors due to ffmpeg not being installed, use send_file instead.
    
    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        media_path: The absolute path to the audio file to send (will be converted to Opus .ogg if it's not a .ogg file)
    
    Returns:
        A dictionary containing success status and a status message
    """
    success, status_message = whatsapp_audio_voice_message(recipient, media_path)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def download_media(message_id: str, chat_jid: str) -> Dict[str, Any]:
    """Download media from a WhatsApp message and get the local file path.
    
    Args:
        message_id: The ID of the message containing the media
        chat_jid: The JID of the chat containing the message
    
    Returns:
        A dictionary containing success status, a status message, and the file path if successful
    """
    file_path = whatsapp_download_media(message_id, chat_jid)
    
    if file_path:
        return {
            "success": True,
            "message": "Media downloaded successfully",
            "file_path": file_path
        }
    else:
        return {
            "success": False,
            "message": "Failed to download media"
        }

def _parent_of(pid: int) -> int:
    out = subprocess.run(["ps", "-o", "ppid=", "-p", str(pid)],
                         capture_output=True, text=True).stdout.strip()
    return int(out) if out.isdigit() else 1


def _exit_when_orphaned(interval: float = 20.0) -> None:
    # mcp 1.6.0's stdio server does not exit when the client closes stdin, so every
    # Claude session that ended left this server (and its uv wrapper) running.
    # 935 of them exhausted the Mac's process table on 23 Oct 2026. Exit once the
    # client is gone: our parent is launchd, or our uv wrapper's parent is.
    parent = os.getppid()
    try:
        via_uv = subprocess.run(["ps", "-o", "comm=", "-p", str(parent)], capture_output=True,
                                text=True).stdout.strip().endswith("uv")
    except Exception:
        via_uv = False
    while True:
        time.sleep(interval)
        if os.getppid() == 1:
            os._exit(0)
        try:
            if via_uv and _parent_of(parent) == 1:
                os._exit(0)
        except Exception:
            pass  # fork failed (e.g. EAGAIN); try again next tick


LAUNCH_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "launches.jsonl")
BURST_COUNT, BURST_WINDOW = 20, 600  # launches per seconds that count as a burst


def _record_launch() -> None:
    # Who started this server? 325 orphans came from ~300 launches in one hour on
    # 23 Oct 2026 with no known source. Log each launch's ancestry so a burst can be
    # traced, and raise a desktop alert (at most every 30 min) when one happens.
    import json
    try:
        procs = {}
        out = subprocess.run(["ps", "-A", "-o", "pid=,ppid=,user=,command="],
                             capture_output=True, text=True).stdout
        for line in out.splitlines():
            parts = line.split(None, 3)
            if len(parts) == 4 and parts[0].isdigit():
                procs[int(parts[0])] = (int(parts[1]), parts[2], parts[3][:200])
        chain, pid = [], os.getppid()
        while pid in procs and pid > 1 and len(chain) < 8:
            ppid, user, cmd = procs[pid]
            chain.append({"pid": pid, "user": user, "cmd": cmd})
            pid = ppid
        env = {k: os.environ[k] for k in ("CLAUDE_CODE_ENTRYPOINT", "SSH_CONNECTION", "TMUX",
                                          "TERM_PROGRAM", "PWD") if k in os.environ}
        now = time.time()
        os.makedirs(os.path.dirname(LAUNCH_LOG), exist_ok=True)
        fd = os.open(LAUNCH_LOG, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        with os.fdopen(fd, "a") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "epoch": now,
                                "pid": os.getpid(), "env": env, "ancestry": chain}) + "\n")

        recent = 0
        with open(LAUNCH_LOG) as f:
            for line in f.readlines()[-500:]:
                try:
                    recent += now - json.loads(line)["epoch"] < BURST_WINDOW
                except Exception:
                    pass
        stamp = LAUNCH_LOG + ".alerted"
        if recent >= BURST_COUNT and (not os.path.exists(stamp) or now - os.path.getmtime(stamp) > 1800):
            open(stamp, "w").close()
            subprocess.run(["osascript", "-e",
                            f'display notification "{recent} WhatsApp MCP launches in 10 min - see '
                            f'whatsapp-mcp-server/logs/launches.jsonl" with title "WhatsApp MCP burst"'],
                           capture_output=True)
    except Exception:
        pass  # tracking must never stop the server starting


if __name__ == "__main__":
    _record_launch()
    threading.Thread(target=_exit_when_orphaned, daemon=True).start()
    # Initialize and run the server
    mcp.run(transport='stdio')